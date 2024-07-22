import sys
from operations.chatbot import ChatBot

if __name__ == '__main__':

    # prompt = "What is a healthy breakfast?"

    # caller = CompletionCaller(prompt=prompt, max_tokens=128, frequency_penalty=2)
    # caller.make_call()
    # response = caller.get_response()  
    # print(response)

    # chat_caller = ChatCaller(
    #     messages=[
    #         {
    #             'role': 'user',
    #             'content': 'What is the fastest animal on Earth?'
    #         }
    #     ],
    #     max_tokens=128
    # )
    # chat_caller.make_call()
    # response = chat_caller.get_response()
    # print(response)

    chatbot = ChatBot()
    chatbot.start()

    sys.exit(0)
