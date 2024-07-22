from pathlib import Path
from dotenv import dotenv_values
import openai

env_file = Path(r'./.env')
environment = dotenv_values(env_file)

class CompletionCaller:

    openai.api_key = environment['OPEN_API_KEY']
 
    def __init__(self,
                 model: str = 'gpt-3.5-turbo-instruct',
                 max_tokens: int = 32,
                 prompt: str = None,
                 **kwargs):
        self.model = model
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.raw_response = None
        self.post_processed_response = None
        self.kwargs = kwargs
        
    def _extract_response(self):

        assert self.raw_response is not None, 'No response.'

        self.post_processed_response = self.raw_response['choices'][0]['text']
    
    def make_call(self):

        assert self.prompt is not None, 'No prompt.'

        self.raw_response = openai.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            prompt=self.prompt,
            **self.kwargs
        ).to_dict()

    def get_response(self):

        self._extract_response()

        return self.post_processed_response


class ChatCaller:

    openai.api_key = environment['OPEN_API_KEY']

    def __init__(self,
                 model: str = 'gpt-3.5-turbo',
                 max_tokens: int = 32,
                 **kwargs):
        self.model = model
        self.messages = None
        self.max_tokens = max_tokens
        self.raw_response = None
        self.post_processed_response = None
        self.kwargs = kwargs
        
    def _extract_response(self):

        assert self.raw_response is not None, 'No response.'

        self.post_processed_response = \
            self.raw_response['choices'][0]['message']['content']
    
    def make_call(self, messages: str = None):

        self.messages = messages

        assert self.messages is not None, 'No prompt.'
      
        self.raw_response = openai.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=self.messages,
            **self.kwargs
        ).to_dict()

    def get_response(self):

        self._extract_response()

        return self.post_processed_response

