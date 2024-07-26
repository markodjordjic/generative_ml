from utilities.general import to_single_line
from operations.conversing import GenericChatBot


class PlayListGenerator(GenericChatBot):

    system_directive_text = """You are a playlist generating assistant.
        You should generate a list of songs and their artists according 
        to a text prompt.
        Provide the playlist as a JSON document, according to the following 
        format: {"song": <song_title>, "artist": <artist_name>}
        User will accept or reject your proposal.
        Pay attention to the responses of user and adjust your proposals
        according to the responses provided by the user. 
        Always return a JSON array, where each element follows this 
        format: {"song": <song_title>, "artist": <artist_name>}
    """

    def __init__(self, 
                 personality: str = 'Helpful',
                 count: int = 1,
                 description: str = 'Disco Funk',
                 mode: str = 'singular'):
        super().__init__(personality=personality)
        self.mode = mode
        self.count = count
        self.description = description
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
            "content": f"Generate a playlist of {self.count} songs based" + 
                f"on this prompt: {self.description}"
        }
        self.history.extend([prompt])

    def _singular(self):
        self.chatbot.make_call(messages=self.history)
        response = self.chatbot.get_response()
        self.history.extend([{
            'role': 'assistant',
            'content': response
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
                user_input = input("Accept (Y) reject (N) or ask further questions: ")
                if user_input.upper() == 'Y':
                    user_response = {
                        'role': 'user',
                        'content': f'This proposal is accepted: {response}'
                    }
                elif user_input.upper() == 'N':
                    additional_input = input('Provide suggestion what can be corrected: ')
                    user_response = {
                        'role': 'user',
                        'content': f'This proposal is rejected: {response}. Try to adjust it acording to {additional_input}.'
                    }
                else:
                    user_response = {
                        'role': 'user',
                        'content': user_input
                    }
                self.history.extend([user_response])

            except KeyboardInterrupt:
                print('Service terminated.')
                break

    def generate_list(self):

        if self.mode == 'singular':
            self._singular()

        if self.mode == 'interactive':
            self._interactive()
