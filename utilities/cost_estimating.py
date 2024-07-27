import tiktoken


class CostEstimator:

    def __init__(self, 
                 model_name: str = None, 
                 text: str = None,
                 price_per_one_m_tokens: float = None) -> None:
        self.model_name = model_name
        self.encoding = None
        self.text = text
        self._encoded_text = None
        self.price_per_one_m_tokens = price_per_one_m_tokens
        self._cost_estimate = None

    def _get_encoding_for_model(self) -> None:

        assert self.model_name is not None, 'Model name is not provided.'

        self.encoding = \
            tiktoken.encoding_for_model(model_name=self.model_name)
        
    def _encode_text(self) -> None:

        assert self.encoding is not None, 'No encoding provided'

        self._encoded_text = self.encoding.encode(self.text)

    def _make_estimate(self) -> None:

        self._cost_estimate = \
            len(self._encoded_text) * (self.price_per_one_m_tokens/1000000)

    def make_estimation(self):

        self._get_encoding_for_model()

        self._encode_text()
        self._make_estimate()

    
    def get_cost_estimate(self):

        return self._cost_estimate