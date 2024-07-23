from utilities.general import to_single_line
from operations.conversing import GenericChatBot


class CodeReviewChatBot(GenericChatBot):

    system_directive_raw = """

        # Directive

        Your task is to review a program written in Python programming 
        language. Conduct the review according to the following rules.

        1. Improve code quality: make suggestions that enhance 
        reusability, readability, performance, and style.

        2. When you have an improvement to suggest, do so according to 
        the following syntax.

            A. One or more pairs of <find:> and <replace:> blocks 
            containing sections of the program you propose to change,
            and changes you propose to make.
            B. Followed by exactly one <message:> block. This is the 
            block where you should explain what changes are you 
            proposing and why.

        An example of a valid response:

        ```
        <find:>
        Code to find
        <replace:>
        Code to replace
        <message:>
        Message to display to the user.
        ``` 

        3. If you are at all uncertain about the code, then ask for 
        clarification. To do so, simply include a <message:> block with 
        no <find:> or <replace:> blocks. The user can clarify and you 
        will have another opportunity to suggest changes in the same 
        format.

        4. You will address a single issue at a time. A single issue 
        might involve many changes, but it should be conceptually a 
        single change.

        5. If you have no change to suggest, then simply include a 
        <message:> followed by your feedback. For example:

        ```
        <message:>
        No proposals for changes.
        ```

        6. Preserve spacing exactly. Your blocks should be indented the 
        same as the code they are replacing. They will be used as the 
        find in a string.replace() call.

        7. If you're suggesting a modification to a specific sequence 
        but that sequence is not unique, then provide more lines of 
        context so as not to clobber other instances of the sequence. 
        In the worst case, your find string can be the entire file's 
        contents.

        8. If there are no further changes to make, then tell the user 
        that. Just like above, simply include a <message:> block with 
        no <find:> or <replace:> blocks.

        9. **DO NOT SUGGEST** any suggestions that we have already 
        rejected/accepted.

        Take a look at the following examples:
"""
    system_directive = to_single_line(text=system_directive_raw)
    system_directive_singe_line = [
        {
            'role': 'system',
            'content': system_directive
        }
    ]

    def _append_examples(self):
        self.history.extend([
            {
                "role": "user",
                "content": """Review the following code:
                    import logger
                    log = logger.get_logger(__name__)

                    def fibonacci(n):
                        log.info("fibonacci(" + n + ") invoked.")
                        if n <= 1:
                            log.info("fibonacci(" + n + ") returning " + n + ".")
                            return n
                        return fibonacci(n - 1) + fibonacci(n - 2)
                    """,
            },
            {
                "role": "assistant",
                "content": """<find:>
                    log.info("fibonacci(" + n + ") invoked.")
                <replace:>
                    log.info(f"fibonacci({n}) invoked.")
                <find:>
                    log.info("fibonacci(" + n + ") returning " + n + ".")
                <replace:>
                    log.info(f"fibonacci({n}) returning {n}")
                <message:>
                The logger supports string interpolation. You can use it to avoid the string concatenation.
                """,
            },
        {"role": "user", "content": "Great."},
        # In this exchange, the user follows up with further modifications they'd like in the alteration.
        {
            "role": "user",
            "content": """Review the following code:
                import logger
                log = logger.get_logger(__name__)

                def fibonacci(n):
                    log.info(f"fibonacci({n}) invoked.")
                    if n <= 1:
                        log.info(F"fibonacci({n}) returning {n}")
                        return n
                    return fibonacci(n - 1) + fibonacci(n - 2)
                """,
        },
        {
            "role": "assistant",
            "content": """<find:>
                if n <= 1:
                    return n
                return fibonacci(n - 1) + fibonacci(n - 2)
            <replace:>
                a, b = 0, 1
                for _ in range(n):
                    a, b = b, a + b
                return a
            <message:>
            Your current implementation uses recursion and runs in O(2^n) time. You can improve that to O(n) by using a loop instead of recursion.
            """,
        },
        {
            "role": "user",
            "content": "The user did not apply the change. Instead, they responded with:\nThis is great, but can you add a docstring regarding your approach, too?",
        },
        {
            "role": "assistant",
            "content": """
                <find:>
                    if n <= 1:
                        return n
                    return fibonacci(n - 1) + fibonacci(n - 2)
                <replace:>
                    # This is a standard implementation of the Fibonacci sequence. It runs in O(n) time and O(1) space.
                    a, b = 0, 1
                    for _ in range(n):
                        a, b = b, a + b
                    return a
                <message:>
                    Your current implementation uses recursion and runs in O(2^n) time. You can improve that to O(n) by using a loop instead of recursion.
            """
        },
        {"role": "user", "content": "Great, thanks!"},
        # In this exchange, you indicate that a user's implementation can be replaced with a built-in library.
        {
            "role": "user",
            "content": """Review the following code:
                def count_words(text):
                    words = text.split()
                    for word in words:
                        if word in word_counts:
                            word_counts[word] += 1
                        else:
                            word_counts[word] = 1
                    return word_counts
                """,
        },
        {
            "role": "assistant",
            "content": """
                <find:>
                    def count_words(text):
                <replace:>
                    from collections import Counter
                    def count_words(text):
                <find:>
                    words = text.split()
                    for word in words:
                        if word in word_counts:
                            word_counts[word] += 1
                        else:
                            word_counts[word] = 1
                    return word_counts
                <replace:>
                    return Counter(text.split())
                <message:>
                The collections.Counter class is a great way to count things. It's a subclass of dict, so you can use it just like a dict.
                """,
        },
        {"role": "user", "content": "Great, thanks!"},
        {
            "role": "user",
            "content": """Review the following code:
                import requests

                def get_api_parameters(title: str):
                    return {
                        "action": "query",
                        "format": "json",
                        "prop": "links",
                        "titles": title,
                        "pllimit": "max",
                    }

                def get_outbound_links(title):
                    url = "https://en.wikipedia.org/w/api.php"
                    response = requests.get(url, params=get_api_parameters(title)).json()
                    pages = response["query"]["pages"]
                    base_url = "https://en.wikipedia.org/wiki/"
                    return [(link["title"], base_url + link["title"].replace(" ", "_")) for page_id in pages for link in pages[page_id].get("links", [])]
                """,
        },
        {
            "role": "assistant",
            "content": """
                <find:>
                    import requests
            <replace:>
                import requests
                from typing import List, Tuple
            <find:>
                def get_api_parameters(title: str):
            <replace:>
                def get_api_parameters(title: str) -> dict:
            <find:>
                def get_outbound_links(title):
            <replace:>
                def get_outbound_links(title) -> List[Tuple[str, str]]:
            <message:>
                I've added some type annotations to your code. They're not required, but they can help you and others understand your code.
            """
        },
            {"role": "user", "content": "Great, thanks!"}
    ])

    def _add_program_text(self):
        self.history.extend([
            {
                'role': 'user',
                'content': f'Review the following program: {self.program_text}'
            }
        ])

    def __init__(self, personality, program_text : str = None):
        super().__init__(personality=personality)
        self.history = self.system_directive_singe_line
        self.program_text = program_text
        self._initiate_personality()
        self._append_examples()
        self._add_program_text()

    def start_review(self):
        while True:
            try:
                self.chatbot.make_call(messages=self.history)
                response = self.chatbot.get_response()
                self.history.extend([{
                    'role': 'assistant',
                    'content': response
                }])
                print(f"{self.personality:}, {response}")
                user_input = input("Enter: ")
                self.history.extend([{
                    'role': 'user',
                    'content': user_input
                }])
            except KeyboardInterrupt:
                print('Service terminated.')
                break



#     message = [
#         {"role": "system", "content": system_directive},
#         # This is a simple example interaction. The user accepts the change.
#         {"role": "user", "content": "Great."},
#         # In this exchange, the user follows up with further modifications they'd like in the alteration.
#         {
#             "role": "user",
#             "content": """Review the following code:
# import logger
# log = logger.get_logger(__name__)

# def fibonacci(n):
#     log.info(f"fibonacci({n}) invoked.")
#     if n <= 1:
#         log.info(F"fibonacci({n}) returning {n}")
#         return n
#     return fibonacci(n - 1) + fibonacci(n - 2)
# """,
#         },
#         {
#             "role": "assistant",
#             "content": """<find:>
#     if n <= 1:
#         return n
#     return fibonacci(n - 1) + fibonacci(n - 2)
# <replace:>
#     a, b = 0, 1
#     for _ in range(n):
#         a, b = b, a + b
#     return a
# <message:>
# Your current implementation uses recursion and runs in O(2^n) time. You can improve that to O(n) by using a loop instead of recursion.
# """,
#         },
#         {
#             "role": "user",
#             "content": "The user did not apply the change. Instead, they responded with:\nThis is great, but can you add a docstring regarding your approach, too?",
#         },
#         {
#             "role": "assistant",
#             "content": """<find:>
#     if n <= 1:
#         return n
#     return fibonacci(n - 1) + fibonacci(n - 2)
# <replace:>
#     # This is a standard implementation of the Fibonacci sequence. It runs in O(n) time and O(1) space.
#     a, b = 0, 1
#     for _ in range(n):
#         a, b = b, a + b
#     return a
# <message:>
# Your current implementation uses recursion and runs in O(2^n) time. You can improve that to O(n) by using a loop instead of recursion.
# """,
#         },
#         {"role": "user", "content": "Great, thanks!"},
#         # In this exchange, you indicate that a user's implementation can be replaced with a built-in library.
#         {
#             "role": "user",
#             "content": """Review the following code:
# def count_words(text):
#     words = text.split()
#     for word in words:
#         if word in word_counts:
#             word_counts[word] += 1
#         else:
#             word_counts[word] = 1
#     return word_counts
# """,
#         },
#         {
#             "role": "assistant",
#             "content": """<find:>
# def count_words(text):
# <replace:>
# from collections import Counter
# def count_words(text):
# <find:>
#     words = text.split()
#     for word in words:
#         if word in word_counts:
#             word_counts[word] += 1
#         else:
#             word_counts[word] = 1
#     return word_counts
# <replace:>
#     return Counter(text.split())
# <message:>
# The collections.Counter class is a great way to count things. It's a subclass of dict, so you can use it just like a dict.
# """,
#         },
#         {"role": "user", "content": "Great, thanks!"},
#         # In this exchange, you make changes at distant separate locations in the code with one semantic change in mind.
#         {
#             "role": "user",
#             "content": """Review the following code:
# import requests

# def get_api_parameters(title: str):
#     return {
#         "action": "query",
#         "format": "json",
#         "prop": "links",
#         "titles": title,
#         "pllimit": "max",
#     }

# def get_outbound_links(title):
#     url = "https://en.wikipedia.org/w/api.php"
#     response = requests.get(url, params=get_api_parameters(title)).json()
#     pages = response["query"]["pages"]
#     base_url = "https://en.wikipedia.org/wiki/"
#     return [(link["title"], base_url + link["title"].replace(" ", "_")) for page_id in pages for link in pages[page_id].get("links", [])]
# """,
#         },
#         {
#             "role": "assistant",
#             "content": """<find:>
# import requests
# <replace:>
# import requests
# from typing import List, Tuple
# <find:>
# def get_api_parameters(title: str):
# <replace:>
# def get_api_parameters(title: str) -> dict:
# <find:>
# def get_outbound_links(title):
# <replace:>
# def get_outbound_links(title) -> List[Tuple[str, str]]:
# <message:>
# I've added some type annotations to your code. They're not required, but they can help you and others understand your code.
# """,
#         },
#         {"role": "user", "content": "Great, thanks!"},
#         # Now, finally, we pass our actual code.
#         {"role": "user", "content": f"Review the following code:\n{code}"},
#     ]

#     def __init__(self, personality: str = None):
#         super().__init__(personality=personality)

    

