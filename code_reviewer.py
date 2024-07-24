from operations.reviewing import CodeReviewChatBot
from tenacity import (
    retry, 
    retry_if_exception_type, 
    stop_after_attempt, 
    wait_random_exponential
)


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
    review = code_reviewer.get_history()

    # start_point = generate_base_messages(
    #     content,
    #     ignore_list=ignore_list,
    #     accept_list=accept_list
    # )

    # while True:
    #     code_review = code_review(start_point, content)

    #     if len(code_review.suggested_changes.changes) == 0:
    #         print('No changes were required.')
        
    #     else:
    #         proposed_change = code_review.suggested_changes.changes
    #         explanations = code_review.suggested_changes.messages
