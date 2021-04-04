from flask import Flask, render_template, request
from search import SearchForm, get_books_by_search
from import_data import books
from get_recs import get_books_by_correlations

app = Flask(__name__)


@app.route('/', methods=["GET","POST"])
def index():
    form = SearchForm()
    return render_template("index.html", form=form)

@app.route('/result', methods=["GET","POST"])
def search_result():
    form = SearchForm(request.form)
    results = get_books_by_search(form.search.data)
    results_len = len(results.index)
    return render_template("result.html", form=form, results=results, results_len=results_len)

@app.route('/detail/<isbn>', methods=["GET","POST"])
def get_detail(isbn):
    form = SearchForm()
    book = books[books["ISBN"]==isbn]
    recommended_books = get_books_by_correlations(isbn)
    results_len = len(recommended_books.index)
    return render_template("detail.html", book=book, recs=recommended_books, form=form, results_len=results_len)

if __name__ == '__main__':
    app.run(debug=True)
