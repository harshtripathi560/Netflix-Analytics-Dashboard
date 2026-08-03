import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

netflix_df = pd.read_csv("dataset/netflix_titles.csv")

print(netflix_df.head())
#------------------------Inspection----------------------------------
# # rows aur columns check karna
# # print("\nShape of Dataset:")
# # print(netflix_df.shape)

# # print("\nColumn Names:")
# # print(netflix_df.columns)

# # print("\nDataset Information:")
# # print(netflix_df.info())

# # print("\nMissing Values:")
# # print(netflix_df.isnull().sum())

# duplicate_count = netflix_df.duplicated().sum()
# print("Duplicate Records: ", duplicate_count)


#------------------PREPROCESSING---------------------------------

netflix_df["director"] = netflix_df["director"].fillna("Not Available")

netflix_df["cast"] = netflix_df["cast"].fillna("Not Available")

netflix_df["country"] = netflix_df["country"].fillna("Unknown")

# rating column me mode fill karna
most_common_rating = netflix_df["rating"].mode()[0]
netflix_df["rating"] = netflix_df["rating"].fillna(most_common_rating)

# date_added aur duration me missing values wali rows remove karna
netflix_df = netflix_df.dropna(subset=["date_added", "duration"])

print("\nMissing VAlues Atfer Cleaning")
print(netflix_df.isnull().sum())

# cleaned dataset save karna
netflix_df.to_csv(
    "dataset/netflix_cleaned.csv",
    index=False
)
print("\nCleaned dataset saved successfully!")



#----------------------Date Conversion + Feature Engineering--------------

#date_added ko datetime me convert krra hu

netflix_df["date_added"] = pd.to_datetime(netflix_df["date_added"].str.strip(), errors = "coerce" )

#new cols
netflix_df["added_year"] = netflix_df["date_added"].dt.year
netflix_df["added_month"] = netflix_df["date_added"].dt.month
netflix_df["added_month_name"] = netflix_df["date_added"].dt.month_name()

#checkin al l colums
print("\nData Feature Preview: ")
print( netflix_df[["date_added", "added_year", "added_month", "added_month_name"]].head() )

netflix_df.to_csv("dataset/netflix_titles.csv" , index=False)

print("Updated Cleaned data saved!")



#------------------------------ANALYSIS------------------------------------

content_count = netflix_df["type"].value_counts()

print("\nContent Distribution: ")
print(content_count)

content_percentage = round((content_count / len(netflix_df)) * 100, 2)

print("\nContent Percentage: ")
print(content_percentage)



#-----------------------------Visualiation---------------------------------

# content distribution chart----------

content_count.plot(kind="bar")
plt.title("Movies VS TV Shows on Netflix")
plt.xlabel("Content Type")
plt.ylabel("Count")

plt.tight_layout()

plt.savefig("static/charts/content_distribution.png")
plt.show()


#year wise content additions-----------

yearly_content = (netflix_df["added_year"].value_counts().sort_index())
print("\nYear Wise Content Additions: ")
print(yearly_content)

#
fig = px.line(
    x=yearly_content.index,
    y=yearly_content.values,
    markers=True,
    title="Content Added Over Years"
)

fig.update_layout(
    xaxis_title="year",
    yaxis_title="Number of Titles"
)
fig.show()

highest_year = yearly_content.idxmax()
highest_count = yearly_content.max()
print(
    f"\nHighest content addition year: {highest_year}"
)
print(
    f"Titles added: {highest_count}"
)


# COUNTRY WISE CONTENT COUNT-----------

country_count = (
    netflix_df["country"]
    .str.split(",")
    .explode()
    .str.strip()
    .value_counts()
)
top_10_countries = country_count.head(10)
print("\n Top 10 Countries: ")
print(top_10_countries)
#chart---
fig = px.bar(
    top_10_countries,
    title="Top 10 countries by Netflix Content"
)
fig.write_html("static/charts/top_countries.html")
fig.show()

# RATING WISE CONTENT COUNT -----------

rating_count = netflix_df["rating"].value_counts()

print("\nRating Wise Content Count:")
print(rating_count)

#Top 10 Countries (Without Unknown)-----
country_count_without_unknown = country_count.drop(
    "Unknown",
    errors="ignore"
)

top_10_countries_clean = (
    country_count_without_unknown.head(10)
)

print("\nTop 10 Countries (Without Unknown):")
print(top_10_countries_clean)


# genre analysis------------------------

genre_count = (
    netflix_df["listed_in"]
    .str.split(",")
    .explode()
    .str.strip()
    .value_counts()
)

top_10_genres = genre_count.head(10)

print("\nTop 10 Genres:")
print(top_10_genres)


# rating analysis---------------------------------------------

rating_count = netflix_df["rating"].value_counts()
print("\nRating Distribution:")
print(rating_count)



# release year analysis----------------------------------------------

release_year_count = (
    netflix_df["release_year"]
    .value_counts()
    .sort_index()
)
print("\nRelease Year Trend:")
print(release_year_count.tail(20))

fig = px.line(
    x=release_year_count.index,
    y=release_year_count.values,
    markers=True,
    title="Netflix Content by Release Year"
)

fig.update_layout(
    xaxis_title="Release Year",
    yaxis_title="Number of Titles"
)

fig.show()