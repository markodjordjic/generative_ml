from pathlib import Path
import json
from utilities.general import to_single_line
from operations.operation import ChatCaller

class GenericChatBot:

    chatbot = ChatCaller(max_tokens=4096, temperature=0)

    def __init__(self, personality: 'str' = None):
        self.history = []  # Reset.
        self.personality = personality

    def _initiate_personality(self):

        if self.personality is not None:
            raw_system_content = f"""
                You are an assistant. Your personality is: {self.personality} 
            """

            system_content = to_single_line(raw_system_content)
            self.history.extend([{
                'role': 'assistant',
                'content': system_content
            }])

    def get_history(self):

        return self.history

    def write_history(self, path: str = None) -> None:
        """Write the chat history to disk

        Parameters
        ----------
        path : str, optional
            Path towards the JSON file, by default None

        """

        assert path is not None, 'No path provided.'

        history_json = Path(path)

        with open(history_json, 'w') as file:
            json.dump(self.history, file, indent=4)


class ConversationalChatBot(GenericChatBot):

    def __init__(self, personality: str = None):
        super().__init__(personality=personality)
        self._initiate_personality()
    
    def _start_conversation(self):
        while True:
            try:
                user_input = input("Enter: ")
                self.history.extend([{
                    'role': 'user',
                    'content': user_input
                }])
                self.chatbot.make_call(messages=self.history)
                response = self.chatbot.get_response()
                print(f"{self.personality:}, {response}")
                self.history.extend([{
                    'role': 'assistant',
                    'content': response
                }])

            except KeyboardInterrupt:
                print('Service terminated.')
                break

    def start(self):
        self._initiate_personality()
        self._start_conversation()
