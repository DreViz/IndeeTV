#Playlist_API
Description
This project is a RESTful API for managing songs and playlists. It allows users to perform CRUD operations on songs and playlists, as well as manage songs within playlists.

##Features
Manage Songs: Create, retrieve, update, and delete songs.
Manage Playlists: Create, retrieve, update, and delete playlists.
Manage Playlist Songs: Add, remove, and reorder songs within playlists.
Pagination: Paginate through lists of songs and playlists.
Technologies Used
Django: Python web framework
Django REST Framework: Toolkit for building Web APIs
SQLite: Database management system
Python: Programming language
##Setup Instructions
Clone the repository:
git clone <repository-url>

Navigate to the project directory:
cd <project-directory>

Install dependencies:
pip install -r requirements.txt

Run migrations to create database tables:
python manage.py migrate

Start the development server:
python manage.py runserver

Access the API in your web browser or using tools like cURL or Postman:
1.API endpoint for managing songs: http://localhost:8000/api/songs/
2.API endpoint for managing playlists: http://localhost:8000/api/playlists/

#API Documentation
Sure, here's the updated API documentation based on the provided code:

### Songs Endpoints

#### Manage Songs

- **POST** `/api/songs/`: Create a new song
- **GET** `/api/songs/`: Retrieve list of songs

### Playlists Endpoints

#### Manage Playlists

- **POST** `/api/playlists/`: Create a new playlist
- **GET** `/api/playlists/`: Retrieve paginated list of playlists
- **GET** `/api/playlists/<playlist_id>/`: Retrieve details of a specific playlist
- **PUT** `/api/playlists/<playlist_id>/`: Update details of a specific playlist
- **DELETE** `/api/playlists/<playlist_id>/`: Delete a specific playlist

#### Manage Playlist Songs

- **POST** `/api/playlists/<playlist_id>/songs/`: Add a song to a playlist
- **DELETE** `/api/playlists/<playlist_id>/songs/<song_id>/`: Remove a song from a playlist
- **PUT** `/api/playlists/<playlist_id>/songs/<song_id>/`: Reorder a song within a playlist

#### List Playlist Songs

- **GET** `/api/playlists/<playlist_id>/songs/`: Retrieve paginated list of songs in a playlist

### Pagination

For endpoints that return lists of items (songs and playlists), pagination is applied with a default page size of 10. Pagination information is included in the response headers as well as in the response body:

- **Response Headers**:
  - `Link`: Provides links to the next and previous pages of results.

- **Response Body**:
  ```json
  {
    "count": <int>,               // Total count of items
    "next": "<str> | null",       // Link to the next page of results
    "previous": "<str> | null",   // Link to the previous page of results
    "results": [                  // List of items (maximum of 10 entries)
      {
        "id": <int>,               // Unique identifier of the item
        "name": "<str>",           // Name of the item
        "artist": "<str>",         // Artist of the song (if applicable)
        "release_year": <int>,     // Release year of the song (if applicable)
        "position": <int>          // Position of the song within the playlist (if applicable)
      },
      // Additional items...
    ]
  }
  ```

### Error Handling

- 404 Not Found: Returned when a requested resource does not exist.
- 400 Bad Request: Returned when there is an issue with the request payload or parameters.

Feel free to customize the documentation further based on your project's specific requirements and endpoints.
