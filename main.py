import sys
from operations.calls import CompletionCaller, ChatCaller

if __name__ == '__main__':

    # prompt = "What is a healthy breakfast?"

    # caller = CompletionCaller(prompt=prompt, max_tokens=128, frequency_penalty=2)
    # caller.make_call()
    # response = caller.get_response()
    # print(response)

    chat_caller = ChatCaller(
        prompt='Is it good to eat protein?',
        max_tokens=128
    )
    chat_caller.make_call()
    response = chat_caller.get_response()
    print(response)

    sys.exit(0)
