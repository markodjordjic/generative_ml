import pandas as pd
from operations.calling import Embeddings

if __name__ == '__main__':

    data = pd.read_csv(
        filepath_or_buffer='"D:\Projects\025_scenario_writing\other\output\screenplays_adventure_films_1980_2020_prepared.csv"'
    )


    embedding = Embeddings(
        raw_text=None
    )
    embedding.generate_embeddings()