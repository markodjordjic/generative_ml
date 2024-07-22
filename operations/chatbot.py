from utilities.general import to_single_line
from operations.calls import ChatCaller

class GenericChatBot:

    history = []
    chatbot = ChatCaller()

    def __init__(self, personality: 'str' = None):
        self.personality = personality

    def _initiate_personality(self):
        raw_system_content = '''
            You are a chatbot.
            Your personality is: 
        ''' % (self.personality)

        system_content = to_single_line(raw_system_content)

        if self.personality:
            self.history.extend([{
                'role': 'system',
                'content': system_content
            }])

class ConversationalChatBot(GenericChatBot):

    def __init__(self, personality: str = None):
        super().__init__(personality=personality)
    
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
