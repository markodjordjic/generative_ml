from operations.reviewing import CodeReviewChatBot


if __name__ == '__main__':

    python_file = 'cocktail_sort.py'

    with open(python_file, 'r') as file:
        content = file.read()

    code_reviewer = CodeReviewChatBot(
        personality='helpful',
        program_text=content,
        output_file_name='cocktail_sort_review.py'
    )
    code_reviewer.start_review()
