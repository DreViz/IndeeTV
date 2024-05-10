from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Song, Playlist
from .serializers import SongSerializer, PlaylistSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

@api_view(['POST', 'GET'])
def manage_songs(request):
    if request.method == 'POST':
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        songs = Song.objects.all().order_by('id')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_songs = paginator.paginate_queryset(songs, request)
        serializer = SongSerializer(paginated_songs, many=True)
        
        response_data = {
            "count": songs.count(),
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": serializer.data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def manage_playlists(request):
    if request.method == 'POST':
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        playlists = Playlist.objects.all().order_by('id')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_playlists = paginator.paginate_queryset(playlists, request)
        serializer = PlaylistSerializer(paginated_playlists, many=True)
        
        response_data = {
            "count": playlists.count(),
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": serializer.data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['PUT', 'DELETE'])
def manage_playlist(request, playlist_id):
    try:
        playlist = Playlist.objects.get(pk=playlist_id)
    except Playlist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
       
        if 'name' in request.data:
            playlist.name = request.data['name']
            playlist.save()
            serializer = PlaylistSerializer(playlist)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Name field is required."}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        playlist.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def list_playlist_songs(request, playlist_id):
    try:
        playlist = Playlist.objects.get(pk=playlist_id)
    except Playlist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    songs = playlist.songs.all().order_by('position')
    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_songs = paginator.paginate_queryset(songs, request)

    
    for i, song in enumerate(paginated_songs, start=1):
        song.position = i
        song.save()

    serializer = SongSerializer(paginated_songs, many=True)

    response_data = {
        'count': songs.count(),
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link(),
        'results': serializer.data
    }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['PUT', 'DELETE'])
def manage_playlist_song(request, playlist_id, song_id):
    try:
        playlist = Playlist.objects.get(pk=playlist_id)
        song = Song.objects.get(pk=song_id)
    except (Playlist.DoesNotExist, Song.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        new_position = request.data.get('position')
        if new_position is not None:
            try:
                new_position = int(new_position)
                if new_position < 1:
                    raise ValueError
            except ValueError:
                return Response({"position": ["Invalid position. Position must be a positive integer."]}, status=status.HTTP_400_BAD_REQUEST)

            if new_position == song.position:
                return Response({"position": ["The song is already at the requested position."]}, status=status.HTTP_400_BAD_REQUEST)

            old_position = song.position

            # Determine the direction of movement (up or down)
            if new_position < old_position:
                songs_to_move = playlist.songs.filter(position__gte=new_position, position__lt=old_position).exclude(pk=song_id)
                increment = 1
            else:
                songs_to_move = playlist.songs.filter(position__lte=new_position, position__gt=old_position).exclude(pk=song_id)
                increment = -1

            # Update positions of other songs within the range
            for s in songs_to_move:
                s.position += increment
                s.save()

            # Update position of the current song
            song.position = new_position
            song.save()

            return Response({"position": new_position}, status=status.HTTP_200_OK)
        else:
            return Response({"position": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Check if the song exists in the playlist
        if song not in playlist.songs.all():
            return Response({"detail": "The specified song is not in the playlist."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove the song from the playlist and update positions of other songs
        position_to_remove = song.position
        songs_to_move_up = playlist.songs.filter(position__gt=position_to_remove)

        # Update positions of songs after the one being removed
        for s in songs_to_move_up:
            s.position -= 1
            s.save()

        # Remove the song from the playlist
        playlist.songs.remove(song)

        return Response(status=status.HTTP_200_OK)
