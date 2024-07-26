import spotipy
from dotenv import dotenv_values

environment = dotenv_values(dotenv_path='.env')

authentication_manager = spotipy.SpotifyOAuth(
    client_id=environment['SPOTIFY_CLIENT_ID'],
    client_secret=environment['SPOTIFY_CLIENT_SECRET'],
    redirect_uri='http://localhost:9999'
)
spotify_authentication = spotipy.Spotify(
    auth_manager=authentication_manager
)

current_user = spotify_authentication.current_user()
print(current_user)