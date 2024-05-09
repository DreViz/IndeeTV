from django.urls import path
from . import views

urlpatterns = [
    # Songs endpoints
    path('api/songs/', views.manage_songs, name='manage_songs'),

    # Playlists endpoints
    path('api/playlists/', views.manage_playlists, name='manage_playlists'),
    path('api/playlists/<int:playlist_id>/', views.manage_playlist, name='manage_playlist'),

    # Endpoint for moving or removing playlist song
    path('api/playlists/<int:playlist_id>/songs/<int:song_id>/', views.manage_playlist_song, name='manage_playlist_song'),

    # Endpoint for listing playlist songs
    path('api/playlists/<int:playlist_id>/songs/', views.list_playlist_songs, name='list_playlist_songs'),
]
