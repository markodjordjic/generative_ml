import sys
from miscallaneous.api_call import Caller


if __name__ == '__main__':

    prompt = 'Generate a list of top 10 movies of all time'

    caller = Caller(prompt=prompt, max_tokens=64)
    caller.make_call()
    response = caller.get_response()
    print(response)

    sys.exit(0)
