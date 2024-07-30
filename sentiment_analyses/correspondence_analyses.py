from pathlib import Path
import io
import numpy as np
import imageio
import matplotlib.pyplot as plt


class CorrespondenceAnalysis:

    def __init__(self, x: np.array = None):
        self.x = x
        self._row_coordinates = None
        self._column_coordinates = None
    
    def compute_coordinates(self):
        P = self.x / self.x.sum()
        r = P.sum(axis=1)
        c = P.sum(axis=0).T
        # Compute diagonal matrices.
        D_r_rsq = np.diag(1. / np.sqrt(r.A1))
        D_c_rsq = np.diag(1. / np.sqrt(c.A1))
        # Compute residuals.
        S = D_r_rsq * (P - r * c.T) * D_c_rsq
        # SVD
        U, D_a, V = np.linalg.svd(S, full_matrices=False)
        D_a = np.asmatrix(np.diag(D_a))
        V = V.T
        # Compute principal coordinates.
        self._row_coordinates = D_r_rsq * U * D_a
        self._column_coordinates = D_c_rsq * V * D_a
            
    def get_coordinates(self):

        return self._row_coordinates, self._column_coordinates
    
class VideoMaker:

    def __init__(self,
                 names: list[str],
                 columns: np.array,
                 rows: np.array,
                 characteristics: list[str],
                 path: Path = None) -> None:
        self.names = names
        self.columns = columns
        self.rows = rows
        self.characteristics = characteristics
        self._frames = []
        self.path = path

    def generate_frames(self):
        plt.ioff()
        #subset_data['film_name'].to_list()
        for row_index, film_name in enumerate(self.names):
            # Set font size.
            plt.rcParams["font.size"] = 6
            # Set figure size.
            figure = plt.figure(figsize=[26.6667*.33, 15*.33])
            plt.scatter(self.columns[:, 0].A1, self.columns[:, 1].A1)
            for column_index, characteristic in enumerate(self.characteristics):
                plt.text(
                    x=self.columns[column_index, 0],
                    y=self.columns[column_index, 1],
                    s=characteristic
                )       
            plt.scatter(
                x=self.rows[row_index, 0],
                y=self.rows[row_index, 1],
                marker='*'
            )
            plt.text(
                x=self.rows[row_index, 0],
                y=self.rows[row_index, 1],
                s=film_name
            )
            buffer = io.BytesIO()
            plt.savefig(buffer, format='raw')
            image_as_array = np.reshape(
                    np.frombuffer(buffer.getvalue(), dtype=np.uint8),
                    newshape=(
                        int(figure.bbox.bounds[3]),
                        int(figure.bbox.bounds[2]), 
                        -1
                    )
                )
            # Close the figure.
            self._frames.extend([image_as_array])
            plt.close()

    def write_video(self):
        imageio.mimwrite(
            self.path,
            self._frames,
            format='MP4',
            fps=0.5,
            output_params=['-intra'],
            quality=10
        )