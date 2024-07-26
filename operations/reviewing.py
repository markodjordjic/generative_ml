from copy import deepcopy
import re
from operations.conversing import GenericChatBot


class ProposalManager:

    accepted_proposals = []
    
    def __init__(self, 
                 file_name: str = None, 
                 original_file: str = None) -> None:
        self.file_name = file_name
        self.original_file = original_file
        self.reviewed_file = deepcopy(self.original_file)

    @staticmethod
    def _identify_positions(accepted_proposal):
        find_position = re.search('<find:>', accepted_proposal)
        replace_position = re.search('<replace:>', accepted_proposal)
        message_position = re.search('<message:>', accepted_proposal)

        return find_position, replace_position, message_position

    @staticmethod
    def _get_strings(accepted_proposal,
                     find_position, 
                     replace_position, 
                     message_position):

        string_to_find = \
            accepted_proposal[find_position.end():replace_position.start()]
        string_to_replace = \
            accepted_proposal[replace_position.end():message_position.start()]
        
        with open('proposal.txt', 'w') as file:
            file.writelines(accepted_proposal)
        
        return string_to_find, string_to_replace

    def _extract_strings(self, accepted_proposal: str):
        find_position, replace_position, message_position = \
            self._identify_positions(accepted_proposal=accepted_proposal)
        
        string_to_find, string_to_replace = self._get_strings(
            accepted_proposal=accepted_proposal,
            find_position=find_position,
            replace_position=replace_position,
            message_position=message_position
        )
        
        return string_to_find, string_to_replace
    
    def _apply_change(self, accepted_proposal: str = None) -> None:
        # Count the number of issues.
        find_blocks = []
        replace_blocks = []
        for item in re.finditer('<find:>', accepted_proposal):
            find_blocks.append(item.span())
        for item in re.finditer('<replace:>', accepted_proposal):
            replace_blocks.append(item.span())

        assert len(find_blocks) == len(replace_blocks), 'Unequal number of find/replace blocks'

        for index, find_replace in enumerate(zip(find_blocks, replace_blocks)):
            if len(find_blocks) > 1:
                find_start = find_replace[0][1]
                find_end = find_replace[1][0]
                replace_start = find_replace[1][1]
                replace_end = find_blocks[index+1][0]
            if len(find_blocks) == 1:
                find_start = find_replace[0][1]
                find_end = find_replace[1][0]
                replace_start = find_replace[1][1]
                replace_end = len(accepted_proposal)

        string_to_find = accepted_proposal[find_start:find_end]
        string_to_replace = accepted_proposal[replace_start:replace_end]

        self.reviewed_file = self.reviewed_file.replace(
            string_to_find, string_to_replace
        )
    
    def apply_changes(self) -> None:
        for accepted_proposal in self.accepted_proposals:
            self._apply_change(accepted_proposal=accepted_proposal)

    def write_file(self) -> None:
        with open(self.file_name, 'w') as file:
            file.writelines(
                self.reviewed_file
            )
            
class CodeReviewChatBot(GenericChatBot):
    
    with open('directive.txt', 'r') as file:
        system_directive = file.read()

    proposal_manager = None

    def __init__(self, 
                 personality: str = 'helpful', 
                 program_text : str = None, 
                 output_file_name: str = None):
        super().__init__(personality=personality)
        self.program_text = program_text
        self.output_file_name = output_file_name
        self._initialise_proposal_manager()
        self._initiate_personality()
        self._initiate_history()
        #self._add_examples()
        self._add_program_text()

    def _initialise_proposal_manager(self):
        self.proposal_manager = ProposalManager(
            file_name=self.output_file_name,
            original_file=self.program_text
        )
 
    def _initiate_history(self):
        self.history = [{
            'role': 'system',
            'content': self.system_directive,
        }]

    def _add_examples(self):
        messages = [
                # This is a simple example interaction. The user accepts the change.
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
        """
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
        """
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
        """
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
        """
                },
                {
                    "role": "user",
                    "content": "The user did not apply the change. Instead, they responded with:\nThis is great, but can you add a docstring regarding your approach, too?",
                },
                {
                    "role": "assistant",
                    "content": """<find:>
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
"""
                },
                {
                    "role": "assistant",
                    "content": """<find:>
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
        """
                },
                {"role": "user", "content": "Great, thanks!"},
                # In this exchange, you make changes at distant separate locations in the code with one semantic change in mind.
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
        """
                },
                {
                    "role": "assistant",
                    "content": """<find:>
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
        ]

        self.history.extend(messages)

    def _add_program_text(self):
        self.history.extend([
            {
                'role': 'user',
                'content': f'Review the following program: {self.proposal_manager.reviewed_file}'
            }
        ])

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
                user_input = input("Accept (Y) reject (N) or ask further questions: ")
                if user_input.upper() == 'Y':
                    user_response = {
                        'role': 'user',
                        'content': f'This proposal is accepted: {response}'
                    }
                    self.proposal_manager.accepted_proposals.extend([response])
                elif user_input.upper() == 'N':
                    user_response = {
                        'role': 'user',
                        'content': f'This proposal is ignored: {response}'
                    }
                else:
                    user_response = {
                        'role': 'user',
                        'content': user_input
                    }
                self.history.extend([user_response])
          
            except KeyboardInterrupt:
                print('Service terminated.')
                self.proposal_manager.apply_changes()
                self.proposal_manager.write_file()
                
                break