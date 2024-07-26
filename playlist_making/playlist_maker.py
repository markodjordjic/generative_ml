import spotipy
from dotenv import dotenv_values

environment = dotenv_values(dotenv_path='./.env')


class PlayListMaker:

    spotify_client_id = environment['SPOTIFY_CLIENT_ID']
    spotify_client_secret = environment['SPOTIFY_CLIENT_SECRET']

    def __init__(self, 
                 playlist: list[str] = None, 
                 playlist_name: str = None) -> None:
        self.playlist = playlist
        self.playlist_name = playlist_name
        self.current_user = None
        self.authentication_manager = None
        self.spotify_authentication = None

    def _authenticate(self):
        self.authentication_manager = spotipy.SpotifyOAuth(
            client_id=self.spotify_client_id,
            client_secret=self.spotify_client_secret,
            redirect_uri='http://localhost:9999',
            scope="playlist-modify-private"
        )
        self.spotify_authentication = spotipy.Spotify(
            auth_manager=self.authentication_manager
        )

    def _get_current_user(self):

        self.current_user = self.spotify_authentication.current_user()

    def _get_track(self, q):
        search_results = self.spotify_authentication.search(
            q=q, type="track", limit=10
        )
        track = search_results["tracks"]["items"][0]["id"]

        return track

    def _get_tracks(self):
        tracks = []
        for item in self.playlist:
            q = f"{item['song']}, {item['artist']}"
            track = self._get_track(q=q)
            tracks.extend([track])

        return tracks
    
    def make_playlist(self):
        tracks = self._get_tracks()
        created_playlist = self.spotify_authentication.user_playlist_create(
            self.current_user['id'],
            public=False,
            name=self.playlist_name
        )
        self.spotify_authentication.user_playlist_add_tracks(
            self.current_user['id'], created_playlist['id'], tracks=tracks
        )
