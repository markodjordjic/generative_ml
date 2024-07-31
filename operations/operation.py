import io
import matplotlib.image
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import base64
import openai
from utilities.general import environment_reader

environment = environment_reader(env_file='./.env')

class OperationManager:

    def __init__(self,
                 texts: list[str], 
                 limit: int = None) -> None:
        self.texts = texts
        self.limit = limit
        self._operation_outcome = []


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
                 raw_text: str = None, 
                 model: str = 'text-embedding-3-small') -> None:
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
    

class EmbeddingManager:

    def __init__(self,
                 texts: list[str], 
                 limit: int = None) -> None:
        self.texts = texts
        self.limit = limit
        self._embeddings = []

    def generate_embeddings(self):

        assert self.texts is not None, 'Pieces of text are not provided.'

        for index, piece_of_text in enumerate(self.texts):
            if self.limit is not None:
                if self.limit < index+1:
                    break
            print(f"Embedding piece of text: {index+1} out of {len(self.texts)}")
            embedding = Embeddings(raw_text=piece_of_text)
            embedding.generate_embeddings()
            self._embeddings.extend([embedding.get_embeddings()])

    def get_embeddings(self):

        return np.array(self._embeddings)


class ImageCaller:

    openai.api_key = environment['OPEN_API_KEY']

    def __init__(self, prompt: str = None) -> None:
        self.prompt = prompt
        self._image_b64 = None

    def generate_image(self):

        assert self.prompt, 'No prompt provided.'
        output = openai.images.generate(
            prompt=self.prompt,
            size="256x256",
            n=1,
            response_format='b64_json'
        )
        self._image_b64 = output.data[0].b64_json

    def display_image(self):
        image = base64.b64decode(self._image_b64)
        buffer = io.BytesIO(image)
        array = matplotlib.image.imread(buffer, format='JPG')
        plt.imshow(array)
        plt.tick_params(labeltop=True, labelright=True)
        plt.tick_params(axis='both', direction='in')
        plt.tick_params(bottom=True, top=True, left=True, right=True)        
        plt.show()


    # def plot(self):
    #     image = BytesIO()
    #     x = numpy.linspace(0, 10)
    #     y = numpy.sin(x)
    #     pyplot.plot(x, y)
    #     pyplot.savefig(image, format='png')
    #     return base64.encodestring(image.getvalue())