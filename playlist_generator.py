from operations.playlist_generating import PlayListGenerator
from playlist_making.playlist_maker import PlayListMaker

if __name__ == '__main__':

    PLAYLIST_NAME = 'Surf Rock'

    playlist_generator = PlayListGenerator(
        count=5,
        description=PLAYLIST_NAME,
        mode='singular'
    )
    playlist_generator.generate_list()
    playlist = playlist_generator.get_play_list()

    playlist_maker = PlayListMaker(
        playlist_name = PLAYLIST_NAME,
        playlist=playlist,
    )
    playlist_maker.make_playlist()
