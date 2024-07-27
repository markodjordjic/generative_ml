import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics import euclidean_distances

class LatentFeatureAnalysis:

    def __init__(self, data: np.array = None) -> None:
        self.data = data
        self.transformer = PCA()
        self.reduction = None

    def _fit(self):

        assert self.data is not None, 'No data.'
 
        self.transformer.fit(X=self.data, y=None)

    def _transform(self):
        
        self.reduction = self.transformer.transform(X=self.data)


class SimilarityMeasurement:

    def __init__(self, data: np.array = None, method: str = 'euclidean') -> None:
        self.data = data
        self.method = method
        self.distances = None

    def _remove_zeros(self):
        zero_mask = self.distances == 0.0
        self.distances[zero_mask] = np.nan

    def _compute_distances(self):
        if self.method == 'euclidean':
            self.distances = euclidean_distances(self.data)

    

