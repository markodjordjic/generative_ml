# %% [markdown]
# # Demonstration of Embeddings for Similarity Measure
# Description of the demo.
# %% [markdown]
# Firstly, let us make the necessary imports.
# %%
import pandas as pd
from operations.operation import EmbeddingManager
from embeddings.embeddings import LatentFeatureAnalysis, SimilarityMeasurement
# %% [markdown]
# # Import the data
# The data consists of movie plots scraped from Wikipedia. In this
# case move plots are movies belonging from the adventure genre,
# starting from 1980s up to the 2020s.
# %%
raw_data = pd.read_csv(
    filepath_or_buffer=r"D:\Projects\025_scenario_writing\other\output\screenplays_adventure_films_1980_2020_prepared.csv"
)
# %% [markdown]
# It is fairly easy to generate embeddings.
# %%
pieces_of_text = [summary for summary in raw_data.loc[:, 'content'].values]
embedding_manager = EmbeddingManager(
    texts=pieces_of_text,
    limit=None
)
embedding_manager.generate_embeddings()
embeddings = embedding_manager.get_embeddings()
# %% [markdown]
# Once that embeddings are available, it is possible to perform some of
# the latent feature analyses. This will (a) preserve the most of the
# variance in the data, while at the same time providing us (b) to
# compute similarity measurement at fraction of the cost, of what
# would be required if we would be using original embeddings.
# Computation over two dimensions is much faster than the computation
# over thousands of dimensions.
# %% 
latent_feature_analyses = LatentFeatureAnalysis(
    data=embeddings,
    method='PCA'
)
latent_feature_analyses.execute_analysis()
# %% [markdown]
# Let us now empirically evaluate the quality of reduction. This can be
# done by selecting a reference movie, and finding the most similar 
# movies by their plots.
# %%
reference_movie = 'The Batman'
mask = raw_data.loc[:, 'film_name'] == reference_movie
reference_index = raw_data.index[mask].to_list()[0]
print(reference_index)
# %% [markdown]
# Now that index of the reference movie is retrieved, it is possible to
# utilize it in the measurement of similarity and identification of the
# most similar movie plots. Count of most similar movie plots is set to
# 10.
# %%
similarity_measurement = SimilarityMeasurement(
    data=latent_feature_analyses.get_reduction(),
    reference_index=reference_index,
    top_k=5,
    method='euclidean'
)
similarity_measurement.compute_distances()
top_k_distances = similarity_measurement.get_top_k()
# %% [markdown]
# Let us discover most similar movies, to our reference movie, according
# embeddings and LFA performed.
# %%
for most_similar in top_k_distances:
    name = raw_data.iloc[most_similar, :]['film_name']
    source = raw_data.iloc[most_similar, :]['source'] 
    print(f"{name}, {source}")
# %% [markdown]
# As it can be seen from the results, embeddings, LFA and similarity
# measurements require further investigation.