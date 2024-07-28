import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics import DistanceMetric

class LatentFeatureAnalysis:

    def __init__(self, data: np.array = None, method: str = None) -> None:
        self.data = data
        self.method = method
        self.transformer = None
        self._reduction = None

    def _initialize_transformer(self) -> None:
        if self.method == 'PCA':
            self.transformer = PCA(n_components=2)

    def _fit(self) -> None:

        assert self.data is not None, 'No data.'
 
        self.transformer.fit(X=self.data, y=None)

    def _transform(self) -> None:        
        self._reduction = self.transformer.transform(X=self.data)

    def execute_analysis(self) -> None:
        self._initialize_transformer()
        self._fit()
        self._transform()
    
    def get_reduction(self) -> np.array:

        assert self._reduction is not None, 'No reduction.'

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
        self._metric = None
        self._distances = None
        self._relevant_distances = None
        self._k = None

    def _initialize_metric(self) -> None:
        if self.method == 'euclidean':
            self._metric = DistanceMetric().get_metric('euclidean')
        if self.method == 'manhattan':
            self._metric = DistanceMetric().get_metric('manhattan')
        if self.method == 'mahalanobis':
            self._metric = DistanceMetric().get_metric('mahalanobis')

    def _compute_distances(self) -> None:

        assert self._metric is not None, 'Metric not initialized.'
 
        self._distances = self._metric.pairwise(self.data, self.data)

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

        self._initialize_metric()
        self._compute_distances()

    def get_top_k(self) -> list[int]:

        assert self._distances is not None, 'Compute distances first.'

        self._remove_zeros()
        self._select_relevant_distances()
        self._top_k()

        return self._k


    

