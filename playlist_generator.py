
from operations.playlist_generating import PlayListGenerator
from playlist_making.playlist_maker import PlayListMaker

if __name__ == '__main__':

    PLAYLIST_NAME = 'Surf Rock'

    playlist_generator = PlayListGenerator(
        count=8,
        description=PLAYLIST_NAME,
        mode='interactive'
    )
    playlist_generator.generate_list()
    playlist_generator.write_history(path='playlist_generator_history.json')
    playlist = playlist_generator.get_play_list()

    playlist_maker = PlayListMaker(
        playlist_name = PLAYLIST_NAME,
        playlist=playlist,
    )
    playlist_maker.make_playlist()
