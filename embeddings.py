import pandas as pd
from operations.calling import Embeddings

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