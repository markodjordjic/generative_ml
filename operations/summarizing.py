from operations.operation import CompletionCaller

class Summarizer:

    def __init__(self, instruction: str, text_document: str) -> None:
        self.instruction = instruction
        self.text_document = text_document
        self.text = None
        self.summary = None
        self.caller = None

    def _get_text(self):
        
        assert self.text_document is not None, 'No text document name.'
        
        with open(self.text_document, 'r') as file:
            self.text = file.read()        

    def _summarize(self):
        prompt = self.instruction + '\n' + self.text
        self.caller = CompletionCaller(prompt=prompt, max_tokens=128)
        self.caller.make_call()
        
    def make_summary(self):
        self._get_text()
        self._summarize()

    def get_summary(self):
        return self.caller.get_response()