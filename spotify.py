import spotipy
from dotenv import dotenv_values

environment = dotenv_values(dotenv_path='.env')

authentication_manager = spotipy.SpotifyOAuth(
    client_id=environment['SPOTIFY_CLIENT_ID'],
    client_secret=environment['SPOTIFY_CLIENT_SECRET'],
    redirect_uri='http://localhost:9999',
    scope="playlist-modify-private"
)
spotify_authentication = spotipy.Spotify(
    auth_manager=authentication_manager
)

current_user = spotify_authentication.current_user()
print(current_user)

search_results = spotify_authentication.search(q="Wasting Love", type="track", limit=10)
tracks = [search_results["tracks"]["items"][0]["id"]]

created_playlist = spotify_authentication.user_playlist_create(
    current_user['id'],
    public=False,
    name="Testing Playlist"
)
spotify_authentication.user_playlists(current_user['id'])
spotify_authentication.user_playlist_add_tracks(current_user['id'], created_playlist['id'], tracks=tracks)