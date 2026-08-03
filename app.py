import numpy as np
import plotly.express as px
from flask import Flask, render_template
import pandas as pd

from dashboard_data import (
    get_dashboard_data,
    get_kpi_data
)

app = Flask(__name__)

# dataset load
netflix_df = pd.read_csv("dataset/netflix_cleaned.csv")


@app.route("/")
def home():

    dashboard_data = get_dashboard_data()

    kpi_data = get_kpi_data()

    total_titles = len(netflix_df)

    movies_count = (
        netflix_df["type"] == "Movie"
    ).sum()

    tv_shows_count = (
        netflix_df["type"] == "TV Show"
    ).sum()

    top_country = (
        netflix_df[netflix_df["country"] != "Unknown"]
        ["country"]
        .value_counts()
        .idxmax()
    )

    content_distribution = (
         netflix_df["type"]
        .value_counts()
    )

    fig = px.pie(
         values=content_distribution.values,
        names=content_distribution.index,
        title="Movies vs TV Shows"
    )

    fig.update_layout(
    template="plotly_dark",
    height=450
    )

    chart_html = fig.to_html(
         full_html=False
    )
#------------------------------------------------------------------------
    genre_data = (
        netflix_df["listed_in"]
        .str.split(", ")
        .explode()
        .value_counts()
        .head(10)
    )

    genre_fig = px.bar(
        x=genre_data.values,
        y=genre_data.index,

        orientation="h",

        title="Top 10 Genres on Netflix"
    )

    genre_fig.update_layout(
    template="plotly_dark",
    height=450
    )

    genre_chart_html = genre_fig.to_html(
        full_html=False
    )
##--------------------------------------------------------------
    country_data = (
    netflix_df[netflix_df["country"] != "Unknown"]
    ["country"]
    .value_counts()
    .head(10)
    )

    country_fig = px.bar(
        x=country_data.index,
        y=country_data.values,

        title="Top 10 Countries by Content"
    )

    country_fig.update_layout(
    template="plotly_dark",
    height=450
    )

    country_chart_html = country_fig.to_html(
        full_html=False
    )
#---------------------------------------------------------
    rating_data = (
    netflix_df["rating"]
    .value_counts()
)

    rating_fig = px.bar(
        x=rating_data.index,
        y=rating_data.values,

        title="Rating Distribution"
    )

    rating_fig.update_layout(
    template="plotly_dark",
    height=450
    )

    rating_chart_html = rating_fig.to_html(
        full_html=False
    )
#-----------------------------------------------------------
    release_year_data = (
    netflix_df["release_year"]
    .value_counts()
    .sort_index()
)

    release_fig = px.line(
        x=release_year_data.index,
        y=release_year_data.values,

        title="Release Year Trend"
    )

    release_fig.update_layout(
    template="plotly_dark",
    height=500
    )

    release_chart_html = release_fig.to_html(
        full_html=False
    )
 #-------------------------------------------------------------------   
    most_common_genre = (
    netflix_df["listed_in"]
    .str.split(", ")
    .explode()
    .value_counts()
    .idxmax()
    )
    peak_year = (
    netflix_df["release_year"]
    .value_counts()
    .idxmax()
    )

    peak_year_count = (
        netflix_df["release_year"]
        .value_counts()
        .max()
    )

    most_common_rating = (
        netflix_df["rating"]
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

    countries_count = (
        netflix_df[netflix_df["country"] != "Unknown"]
        ["country"]
        .nunique()
    )

    genres_count = (
        netflix_df["listed_in"]
        .str.split(", ")
        .explode()
        .nunique()
    )

    min_year = netflix_df["release_year"].min()

    max_year = netflix_df["release_year"].max()


#------------------------------------------------------
    return render_template(
        "index.html",

        total_titles=total_titles,

        movies_count=movies_count,

        tv_shows_count=tv_shows_count,

        top_country=top_country,

        chart_html=chart_html,

        genre_chart_html=genre_chart_html,

        country_chart_html=country_chart_html,

        rating_chart_html=rating_chart_html,

        release_chart_html=release_chart_html,

        most_common_genre=most_common_genre,

        movie_percentage=movie_percentage,

        tv_percentage=tv_percentage,

        countries_count=countries_count,

        genres_count=genres_count,

        min_year=min_year,

        max_year=max_year,

        peak_year=peak_year,

        peak_year_count=peak_year_count,

        most_common_rating=most_common_rating

    )

if __name__ == "__main__":
    app.run(debug=True)