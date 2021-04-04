from import_data import books
from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(Form):
    search = StringField("", validators=[DataRequired()])
    submit = SubmitField("Search")

def get_books_by_search(search):
    results = books
    results = results.apply(lambda x: x.str.lower() if(x.dtype == 'object') else x)
    results = results[results["Book-Title"].str.contains(search.lower())]
    results_sorted = results.sort_values(by=["Rating-Count"], ascending=False)[:10]
    isbn_sorted = results_sorted["ISBN"].tolist()
    results = books[books["ISBN"].isin(isbn_sorted)]
    return results