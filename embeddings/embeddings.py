import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics import euclidean_distances

class LatentFeatureAnalysis:

    def __init__(self, data: np.array = None, method: str = None) -> None:
        self.data = data
        self.method = method
        self.transformer = None
        self._reduction = None

    def _initialize_transformer(self):
        if self.method == 'PCA':
            self.transformer = PCA(n_components=2)

    def _fit(self):
        assert self.data is not None, 'No data.'
 
        self.transformer.fit(X=self.data, y=None)

    def _transform(self):        
        self._reduction = self.transformer.transform(X=self.data)

    def execute_analysis(self):
        self._initialize_transformer()
        self._fit()
        self._transform()
    
    def get_reduction(self):

        return self._reduction


class SimilarityMeasurement:

    def __init__(self, 
                 data: np.array = None, 
                 method: str = 'euclidean',
                 reference_index: int = 0,
                 top_k: int = 5) -> None:
        self.data = data
        self.method = method
        self.reference_index = reference_index
        self.top_k = top_k
        self._distances = None
        self._relevant_distances = None
        self._k = None

    def _compute_distances(self) -> None:
        if self.method == 'euclidean':
            self._distances = euclidean_distances(self.data)

    def _remove_zeros(self) -> None:

        assert self._distances is not None, 'Distance not computed.'

        mask = self._distances == 0.0
        self._distances[mask] = np.nan

    def _select_relevant_distances(self):
        self._relevant_distances = self._distances[self.reference_index, :]

    def _top_k(self):
        k = []
        for _ in range(0, self.top_k):
            top_k_distances = np.nanargmin(self._relevant_distances)
            k.extend([top_k_distances])
            self._relevant_distances[top_k_distances] = np.nan  # Exclude.

        self._k = k

    def compute_distances(self) -> None:

        self._compute_distances()

    def get_top_k(self) -> list[int]:

        assert self._distances is not None, 'Compute distances first.'

        self._remove_zeros()
        self._select_relevant_distances()
        self._top_k()

        return self._k


    

