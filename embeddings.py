import pandas as pd
from operations.calling import Embeddings
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np


if __name__ == '__main__':

    data = pd.read_csv(
        filepath_or_buffer=r"D:\Projects\025_scenario_writing\other\output\screenplays_adventure_films_1980_2020_prepared.csv"
    )


    film_summary_embeddings = []
    for film_name, film_summary in zip(data.loc[:, 'film_name'], data.loc[:, 'content']):
        print(f'Making embedding for {film_name}')
        embedding = Embeddings(raw_text=film_summary)
        embedding.generate_embeddings()
        film_summary_embeddings.extend(
            [embedding.get_embeddings()]
        )

    len(film_summary_embeddings)
    film_summary_tabe = pd.DataFrame.from_records(film_summary_embeddings)

    latent_feature_analysis = PCA()
    latent_feature_analysis.fit(film_summary_tabe)
    dimensionality_rediction = latent_feature_analysis.fit_transform(X=film_summary_tabe)
    plt.scatter(dimensionality_rediction[:, 0], dimensionality_rediction[:, 1])
    plt.show()

    distances = euclidean_distances(dimensionality_rediction)
    zero_mask = distances == 0.0
    distances[zero_mask] = np.nan    
    mask = data.loc[:, 'film_name'] == 'The Batman'
    index = data.index[mask].to_list()[0]
    distances_per_film = distances[index, :]
    top_k = 5
    k = []
    for top_k_index in range(0, top_k):
        top_k_distances = np.nanargmin(distances_per_film).tolist()
        k.extend([top_k_distances])
        distances_per_film[top_k_distances] = np.nan
    
    for most_similar in k:
        print(data.iloc[most_similar]['film_name'])

