# %% [markdown]
# # Sentiment Analysis with General Pre-trained Transformers (GPT)
# In this demo it will be possible to observe the capability of GPTs to
# perform sentiment analyses of the pieces of text. In this case
# movie plots have been selected for this purpose. Eleven dimensions
# have been selected to perform sentiment analyses.
# Firstly, lets make the necessary imports
# %%
from pathlib import Path
import pandas as pd
import numpy as np
from IPython.display import Video
from operations.sentiment_analyses import SentimentAnalysesManager
from sentiment_analyses.correspondence_analyses import \
    CorrespondenceAnalysis, VideoMaker
# %% [markdown]
# # Data Import
# Now, let us read the data.
# %%
raw_data = pd.read_csv(
    filepath_or_buffer=r"D:\Projects\025_scenario_writing\other\output\screenplays_adventure_films_1980_2020_prepared.csv"
)
# Since the original data-set is too large it is necessary to make a
# subset first.
# %%
selection = [index%10==0 for index in range(0, len(raw_data))]
subset_data = raw_data.loc[selection, :]
pieces_of_text = [summary for summary in subset_data.loc[:, 'content'].values]
# %% [markdown]
# # Analysis Setup
# Here are the characteristics accross which sentiment analyses will be
# performed.
# %%
characteristics = [
    'violent',
    'calm',
    'funny',
    'serious', 
    'warm',
    'cold',
    'tense',
    'relaxed',
    'romantic',
    'futuristic',
    'archaic'
]
# %% [markdown]
# # Analysis Execution
# Let us perform the analyses.
# %%
sentiment_analyses = SentimentAnalysesManager(
    texts=pieces_of_text,
    characteristics=characteristics
)
sentiment_analyses.generate_sentiments()
scores = sentiment_analyses.get_scores()
# %% [markdown]
# Scores need to be placed into `pd.DataFrame` object for further 
# processing.
# %%
film_scores = pd.DataFrame(scores)
film_scores.index = subset_data.index
# %% [markdown]
# # Visualization
# Field of categorical data analysis, lends us the use of a special case
# of latent feature analyses that can be applied to categorical data.
# It will allow us to extract coordinates of the sentiments, as well as
# movie plots, when projected into dimensions which capture the most
# variance
# %%
ca = CorrespondenceAnalysis(x=np.matrix(film_scores.values))
ca.compute_coordinates()
rows, columns = ca.get_coordinates()
# %% [markdown]
# Since analysis spans across multiple characteristics and movie plots
# it is necessary to add a dimension of time to the visualization and
# observe it as a sequence of images, one by one, rather than all of
# them together.
# %%
video_maker = VideoMaker(
    names=subset_data['film_name'].to_list(),
    columns=columns,
    rows=rows,
    characteristics=characteristics,
    path=Path('ca_movie_plots.mp4')
)
video_maker.generate_frames()
video_maker.write_video()
# %% [markdown]
# Let us take a look at the analysis.
# %%
Video("ca_movie_plots.mp4")
# %% [markdown]
# As we can see movie plots have been correctly associated with varying
# degrees of different characteristics by GPT.

