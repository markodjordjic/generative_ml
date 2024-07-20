import sys
from miscallaneous.api_call import Caller


if __name__ == '__main__':

    prompt = 'How is the weather today in Belgrade?'

    caller = Caller(prompt=prompt)
    caller.make_call()
    response = caller.get_response()

    sys.exit(0)
