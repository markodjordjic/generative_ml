from utilities.general import environment_reader
import openai


environment = environment_reader(env_file='./.env')


class CompletionCaller:

    openai.api_key = environment['OPEN_API_KEY']
 
    def __init__(self,
                 model: str = 'gpt-3.5-turbo',
                 max_tokens: int = 1024,
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

        try:
      
            self.raw_response = openai.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=self.messages,
                **self.kwargs
            ).to_dict()

            self._extract_response()
        
        except openai.BadRequestError as e:
            pass

    def get_response(self):

        return self.post_processed_response


class Embeddings:

    def __init__(self, 
                 raw_text: str, 
                 model: str = 'text-embedding-ada-002') -> None:
        self.raw_text = raw_text
        self.model = model
        self.raw_embeddings = None

    def generate_embeddings(self):

        assert self.raw_text is not None, 'No raw text provided.'

        self.raw_embeddings = openai.embeddings.create(
            input=self.raw_text,
            model=self.model
        )

    def get_embeddings(self):
        
        return self.raw_embeddings.data[0].embedding
