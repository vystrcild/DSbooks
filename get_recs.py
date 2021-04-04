from import_data import ratings
import pandas as pd

isbn_input = "043935806X"

def get_readers(isbn):
    """
    Get list of User-IDs who read input book
    :param isbn: string
    :return: list
    """
    readers = ratings["User-ID"][ratings["ISBN"] == isbn]
    readers = readers.tolist()
    return readers

def get_ratings_by_readers(isbn):
    """
    Get all book ratings by specific User-IDs
    :param isbn: string
    :return: DataFrame
    """
    readers = get_readers(isbn)
    ratings_by_readers = ratings[ratings["User-ID"].isin(readers)]

    # Filter books with ratings > 8
    number_of_rating_per_book = ratings_by_readers.groupby(['ISBN']).agg('count').reset_index()
    books_to_compare = number_of_rating_per_book['ISBN'][number_of_rating_per_book['User-ID'] >= 8]
    books_to_compare = books_to_compare.tolist()

    ratings_by_readers = ratings_by_readers[ratings_by_readers["ISBN"].isin(books_to_compare)]

    return ratings_by_readers

def get_pivot_table(isbn):
    """
    Prepare pivot table for correlation
    :param isbn: string
    :return: DataFrame
    """
    ratings_by_readers = get_ratings_by_readers(isbn)
    ratings_pivot = ratings_by_readers.pivot(index="User-ID", columns="ISBN", values="Book-Rating")
    return ratings_pivot

def get_correlations(isbn):
    """
    Get list of ISBNs with highest correlations
    :param isbn: string
    :return: list
    """
    ratings_pivot = get_pivot_table(isbn)
    clean_pivot = ratings_pivot.copy(deep=False)
    clean_pivot.drop([isbn], axis=1, inplace=True)

    # empty lists
    book_titles = []
    correlations = []
    result_list = []

    for book_title in list(clean_pivot.columns.values):
        book_titles.append(book_title)
        correlations.append(ratings_pivot[isbn].corr(clean_pivot[book_title]))

    # final dataframe of all correlation of each book
    corr_fellowship = pd.DataFrame(list(zip(book_titles, correlations)), columns=['ISBN', 'corr'])
    result_list.append(corr_fellowship.sort_values('corr', ascending=False).head(10))
    return result_list