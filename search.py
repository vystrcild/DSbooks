from import_data import books

def get_books_by_search(search):
    results = books
    results = results.apply(lambda x: x.str.lower() if(x.dtype == 'object') else x)
    results = results[results["Book-Title"].str.contains(search.lower())]
    results_sorted = results.sort_values(by=["Rating-Count"], ascending=False)[:10]
    isbn_sorted = results_sorted["ISBN"].tolist()
    results = books[books["ISBN"].isin(isbn_sorted)]
    return results