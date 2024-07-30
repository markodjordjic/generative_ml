import json
from utilities.general import to_single_line
from operations.operation import OperationManager
from operations.conversing import GenericChatBot


class SentimentAnalysisChatBot(GenericChatBot):

    system_directive = r"""
Your task is to review movie plots. Read the complete plot and determine
how %s. Express your opinion using any whole number between 1, 
which means not at all %s, to 10, which very %s. Do not provide any 
additional explanation in your response. Only provide the characteristic 
and number in the following format. {"%s": your score} 
Here is the movie plot you need to review: %s
"""

    def __init__(self, 
                 personality: str = None,
                 characteristic: str = None,
                 piece_of_text: str = None):
        super().__init__(personality)
        self.personality = personality
        self.characteristic = characteristic
        self.piece_of_text = piece_of_text
        self._initiate_personality()
        self._initiate_system_directive()
        self._score: int = None

    def _initiate_system_directive(self):
        self.history.extend([
            {
                'role': 'system',
                'content': to_single_line(self.system_directive % (
                    self.characteristic,
                    self.characteristic, 
                    self.characteristic,
                    self.characteristic,
                    self.piece_of_text))
            }
        ])

    def generate_score(self) -> None:
        self.chatbot.make_call(messages=self.history)
           

class SentimentAnalysesManager(OperationManager):

    def __init__(self, 
                 texts: list[str],
                 characteristics: list[str], 
                 limit: int = None) -> None:
        super().__init__(texts, limit)
        self.texts = texts
        self.limit = limit
        self.characteristics = characteristics
        self._scores = []

    def generate_sentiments(self):

        assert self.texts is not None, 'Pieces of text are not provided.'
        
        for index, piece_of_text in enumerate(self.texts):
            count = len(self.texts)
            if self.limit is not None:
                count = self.limit
                if self.limit < index+1:
                    break
            print(f"Sentiment analyses for piece of text: {index+1} out of {count}")
            score = []            
            for characteristic in self.characteristics:
                sentiment_analyses = SentimentAnalysisChatBot(
                    personality='scientific and accurate',
                    piece_of_text=piece_of_text,
                    characteristic=characteristic
                )
                sentiment_analyses.generate_score()
                score.extend([
                    json.loads(
                        sentiment_analyses.chatbot.get_response()
                    )[characteristic]
                ]) 
            self._scores.extend([score])

    def get_scores(self):

        return self._scores               
