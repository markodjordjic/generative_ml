import openai

class Caller:

    def __init__(self, 
                 model: str = 'text-davinci-003', 
                 prompt: str = None):
        self.model = model
        self.prompt = prompt
        self.response = None
        
    def make_call(self):

        assert self.prompt, 'No prompt'

        self.response = openai.completions.create(
            model=self.model,
            prompt=self.pro,pt
        )
    def get_response(self):

        assert self.response is not None, 'No response.'

        return self.response


        
    
