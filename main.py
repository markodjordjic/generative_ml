import sys
from operations.operations import Summarizer

if __name__ == '__main__':

    summarizer = Summarizer(
        instruction="Translate the text below to Latin:",
        text_document="translation.txt"
    )
    summarizer.make_summary()
    summary = summarizer.get_summary()
    print(summary)
    
    sys.exit(0)
