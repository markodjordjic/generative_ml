import io
import matplotlib.image
import matplotlib.pyplot as plt
import matplotlib.gridspec as grid
import numpy as np
import base64
import openai
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import warnings
from PIL import Image
from utilities.general import environment_reader
import textwrap
from utilities.general import to_single_line

environment = environment_reader(env_file='./.env')

class OperationManager:

    def __init__(self,
                 texts: list[str], 
                 limit: int = None) -> None:
        self.texts = texts
        self.limit = limit
        self._operation_outcome = []


class CompletionCaller:

    openai.api_key = environment['OPENAI_API_KEY']
 
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

    openai.api_key = environment['OPENAI_API_KEY']

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


class GenericImageCaller:

    openai_api_key = environment['OPENAI_API_KEY']
    stabilityai_api_key = environment['STABILITYAI_API_KEY']

    def __init__(self, prompt: str = None) -> None:
        self.prompt = prompt
        self._image_b64 = None
        self._image_array = None

    def _image_to_array(self):
        image = base64.b64decode(self._image_b64)
        image = base64.b64decode(self._image_b64)
        buffer = io.BytesIO(image)
        self._image_array = matplotlib.image.imread(buffer, format='JPG')
 
class ImageCaller(GenericImageCaller):

    def __init__(self, prompt: str = None) -> None:
        super().__init__(prompt)

    def generate_image(self):

        assert self.prompt, 'No prompt provided.'

        output = openai.images.generate(
            prompt=self.prompt,
            size="256x256",
            n=1,
            response_format='b64_json'
        )

        self._image_b64 = output.data[0].b64_json
        self._image_to_array()


class StabilityAiImage(GenericImageCaller):

    def __init__(self, prompt: str = None, description = None) -> None:
        super().__init__(prompt)
        self.api = None
        self.image = None
        self._raw_image = None
        self.description = description

    def _initialize_api(self):
        self.api = client.StabilityInference(
            key=self.stabilityai_api_key, # API Key reference.
            verbose=False, # Print debug messages.
            engine="stable-diffusion-xl-1024-v1-0", # Set the engine to use for generation.
            # Check out the following link for a list of available engines: https://platform.stability.ai/docs/features/api-parameters#engine
        )
    
    def generate_image(self, image = None):
        self._initialize_api()

        if image == None:
            answers = self.api.generate(
                prompt=self.prompt,
                seed=4253978046,
                steps=50,
                cfg_scale=8.0, 
                width=256, 
                height=256,
                samples=1, 
                sampler=generation.SAMPLER_K_DPMPP_2M
            )
        if image != None:
            answers = self.api.generate(
                prompt=self.prompt,
                init_image=image,
                seed=4253978046,
                steps=50,
                cfg_scale=8.0, 
                width=256, 
                height=256,
                samples=1, 
                sampler=generation.SAMPLER_K_DPMPP_2M
            )

        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    self._raw_image = Image.open(io.BytesIO(artifact.binary))
                    self._image_b64 = artifact.binary

    def display_image(self):
        img = Image.open(io.BytesIO(self._image_b64))
        plt.rcParams["font.size"] = 8
        # Set figure size.
        figure = plt.figure()
        plotting_grid = grid.GridSpec(nrows=4, ncols=1)
        axis_1 = figure.add_subplot(plotting_grid[0:3, 0])
        axis_1.imshow(img)
        axis_1.tick_params(labeltop=True, labelright=True)
        axis_1.tick_params(axis='both', direction='in')
        axis_1.tick_params(bottom=True, top=True, left=True, right=True) 
        axis_2 = figure.add_subplot(plotting_grid[3, 0])
        text_kwargs = dict(ha='center', va='center', fontsize=8)
        short_text = textwrap.wrap(text=to_single_line(self.description), width=48)
        short_text_for_plotting = '\n'.join(short_text)
        axis_2.text(x=.5, y=.5, s=short_text_for_plotting, wrap=True, **text_kwargs)  
        axis_2.set_xticklabels([])
        axis_2.set_yticklabels([])
        figure.subplots_adjust(left=.25, right=.75)   
        plt.show()


        


