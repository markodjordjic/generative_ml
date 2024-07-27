import json
from utilities.general import to_single_line
from operations.conversing import GenericChatBot


class PlayListGenerator(GenericChatBot):

    system_directive_text = """You are a playlist generating assistant.
        You should generate a list of songs and their artists according 
        to a text prompt.
        Provide the playlist as a JSON document, according to the 
        following format: {"song": <song_title>, "artist": <artist_name>}
        User will accept or reject your proposal.
        Pay attention to the responses of user and adjust your proposals
        according to the responses provided by the user. 
        Always return a JSON array, where each element follows this 
        format: {"song": <song_title>, "artist": <artist_name>}.
        Do not add any additional text to your response except the
        JSON array.
    """

    def __init__(self, 
                 personality: str = 'Helpful',
                 count: int = 1,
                 description: str = 'Disco Funk',
                 mode: str = 'singular'):
        super().__init__(personality=personality)
        self.history = []  # Resetting the history.
        self.mode = mode
        self.count = count
        self.description = description
        self._initiate_personality()
        self._add_system_directive()
        self._add_prompt()

    def _add_system_directive(self):
        system_directive = {
            "role": "system",
            "content": to_single_line(self.system_directive_text),
        }
        self.history.extend([system_directive])

    def _add_prompt(self):
        prompt = {
            "role": "user",
            "content": f"Generate a playlist of {self.count} songs based " + 
                f"on this prompt: {self.description}"
        }
        self.history.extend([prompt])

    def _singular(self):
        self.chatbot.make_call(messages=self.history)
        response = self.chatbot.get_response()
        self.history.extend([{
            'role': 'assistant',
            'content': f'This is final playlist {response}'
        }])
    
    def _interactive(self):
        while True:
            try:
                self.chatbot.make_call(messages=self.history)
                response = self.chatbot.get_response()
                self.history.extend([{
                    'role': 'assistant',
                    'content': response
                }])
                print(f"{self.personality:}, {response}")
                user_input = input("Accept (Y), reject (N), or finish (F): ")
                if user_input.upper() == 'Y':
                    additional_input = input(
                        '>> Provide further suggestions: '
                    )
                    user_response = {
                        'role': 'user',
                        'content': f'This proposal is accepted: {response}. Also: make following changes: {additional_input}.'
                    }
                    self.history.extend([user_response])

                if user_input.upper() == 'N':
                    additional_input = input(
                        '>> Provide suggestion what can be corrected? '
                    )
                    user_response = {
                        'role': 'user',
                        'content': f'This proposal is rejected: {response}. Adjust your next proposal according to: {additional_input}.'
                    }
                    self.history.extend([user_response])

                if user_input.upper() == 'F':
                    user_response = {
                        'role': 'user',
                        'content': f'This is final playlist {response}'
                    }
                    self.history.extend([user_response])
                    break

            except KeyboardInterrupt:
                print('Service terminated.')
                break

    def generate_list(self):
        if self.mode == 'singular':
            self._singular()

        if self.mode == 'interactive':
            self._interactive()

    def get_play_list(self):
        playlist = []


        if self.mode == 'singular':
            search_key = 'assistant'
        if self.mode == 'interactive':
            search_key = 'user'

        for message in self.history:
            if message['role'] == search_key:
                if 'final' in message['content']:
                    content = message['content']
                    clean = content.replace(
                        'This is final playlist ', ""
                    )
                    playlist = json.loads(clean)

        assert len(playlist) > 0, 'Error when parsing content.'

        return playlist
