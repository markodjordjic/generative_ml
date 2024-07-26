from operations.playlist_generating import PlayListGenerator
import spotipy
from dotenv import dotenv_values


if __name__ == '__main__':

    playlist_generator = PlayListGenerator(
        count=5,
        description='Early Punk',
        mode='singular'
    )
    playlist_generator.generate_list()
    playlist = playlist_generator.get_play_list()


