import json
from operations.playlist_generating import PlayListGenerator

if __name__ == '__main__':

    playlist_generator = PlayListGenerator(
        count=10,
        description='Summer',
        mode='singular'
    )
    playlist_generator.generate_list()
    history = playlist_generator.get_history()
    playlist = json.loads(history[2]['content'])
    for message in history:
        if message['role'] == 'user':
            if 'accepted' in message['content']:
                playlist = json.loads(message['content'])

    json.loads(history[6]['content'])
