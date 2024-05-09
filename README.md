# IndeeTV
# Django REST API Project

This project is a Django-based RESTful API for managing songs and playlists.

## Features

- Allows users to perform CRUD operations on songs and playlists.
- Provides endpoints for managing songs and playlists.
- Supports pagination for listing songs in playlists.
- Implements functionality to reorder songs within playlists.

## Technologies Used

- Django: Python-based web framework for building the API.
- Django REST Framework: Toolkit for building Web APIs in Django.
- SQLite: Lightweight relational database management system used for data storage.

## Installation


API Endpoints
/api/songs/:
POST: Create a new song.
GET: Retrieve a list of all songs.
/api/songs/<song_id>/:
PUT: Update details of a specific song.
DELETE: Delete a specific song.
/api/playlists/:
POST: Create a new playlist.
GET: Retrieve a list of all playlists.
/api/playlists/<playlist_id>/:
PUT: Update details of a specific playlist.
DELETE: Delete a specific playlist.
/api/playlists/<playlist_id>/songs/:
GET: Retrieve a list of songs in a specific playlist.
/api/playlists/<playlist_id>/songs/<song_id>/:
PUT: Reorder or remove a specific song from a playlist.
DELETE: Remove a specific song from a playlist.
