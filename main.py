import sys
from utilities.calling import Caller
from operations.operations import Summarizer

if __name__ == '__main__':

    prompt = "As an color assistant give me hexadecimal codes of colors according to the example below. Colors should come as a JSON array:\nQ: Colors of autumn? A: ["#E68A00", "#C6514A", "#956B3D"]. \nText: Colors of sunet"
    caller = Caller(
        prompt=prompt
    )
    caller.make_call()
    caller.get_response()

    summarizer = Summarizer(
        instruction="Translate the text below to Romanian:",
        text_document="translation.txt"
    )
    summarizer.make_summary()
    summary = summarizer.get_summary()
    print(summary)
    
    sys.exit(0)
