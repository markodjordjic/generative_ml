import sys
from operations.operations import Summarizer

if __name__ == '__main__':

    summarizer = Summarizer(
        instruction="Extract ingredients from the recipe below:",
        text_document="recipe.txt"
    )
    summarizer.make_summary()
    summary = summarizer.get_summary()
    print(summary)
    
    sys.exit(0)
