import pandas as pd
import numpy as np

# load ratings
ratings = pd.read_csv('BX-Book-Ratings.csv', encoding='latin-1', sep=';', na_values=0)
ratings = ratings.dropna()

# load books
books = pd.read_csv('BX-Books.csv', encoding='latin-1', sep=';', error_bad_lines=False)

# Merging ratings & books
df = pd.merge(ratings, books, on=["ISBN"])

# Create no. of ratings and average columns
df["Rating-Count"] = df.groupby(['ISBN'])["Book-Rating"].transform(np.sum)
df["Rating-Average"] = df.groupby(['ISBN'])["Book-Rating"].transform(np.mean)

# Create final DF for books & drop duplicates
books = df[["Book-Title", "ISBN", "Rating-Count", "Rating-Average", "Image-URL-S"]]
books.drop_duplicates(inplace=True)
