from utilities.calls import ChatCaller

class ChatBot:
    
    history = []
    chatbot = ChatCaller()

    def __init__(self):
        pass

    def start(self):
        while True:
            try:
                user_input = input("Enter: ")
                self.history.extend([{
                    'role': 'user',
                    'content': user_input
                }])
                self.chatbot.make_call(messages=self.history)
                response = self.chatbot.get_response()
                print(response)
                self.history.extend([{
                    'role': 'assistant',
                    'content': response
                }])

            except KeyboardInterrupt:
                print('Service terminated.')
                break

