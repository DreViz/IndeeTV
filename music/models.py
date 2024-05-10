from django.db import models

class Song(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    release_year = models.IntegerField()
    position = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.position:
            # Calculate the position based on the number of songs in the playlists
            self.position = self.playlists.count() + 1
            self.save(update_fields=['position'])  

class Playlist(models.Model):
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(Song, related_name='playlists')

    def add_song(self, song):
        """
        Add a song to the playlist.
        """
        self.songs.add(song)
        song.position = self.songs.count() 
        song.save(update_fields=['position'])  
