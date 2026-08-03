import pandas as pd
import plotly.express as px


netflix_df = pd.read_csv(
    "dataset/netflix_cleaned.csv"
)


def get_dashboard_data():

    total_titles = len(netflix_df)

    movies_count = (
        netflix_df["type"] == "Movie"
    ).sum()

    tv_shows_count = (
        netflix_df["type"] == "TV Show"
    ).sum()

    top_country = (
        netflix_df[
            netflix_df["country"] != "Unknown"
        ]["country"]
        .value_counts()
        .idxmax()
    )

    most_common_genre = (
        netflix_df["listed_in"]
        .str.split(", ")
        .explode()
        .value_counts()
        .idxmax()
    )

    movie_percentage = round(
        (movies_count / total_titles) * 100,
        2
    )

    tv_percentage = round(
        (tv_shows_count / total_titles) * 100,
        2
    )

    return {
        "total_titles": total_titles,
        "movies_count": movies_count,
        "tv_shows_count": tv_shows_count,
        "top_country": top_country,
        "most_common_genre": most_common_genre,
        "movie_percentage": movie_percentage,
        "tv_percentage": tv_percentage
    }

def get_kpi_data():

    return get_dashboard_data()