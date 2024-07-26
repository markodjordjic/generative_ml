import json
from operations.playlist_generating import PlayListGenerator

if __name__ == '__main__':

    playlist_generator = PlayListGenerator(
        count=5,
        description='Early Punk',
        mode='interactive'
    )
    playlist_generator.generate_list()
    playlist = playlist_generator.get_play_list()
