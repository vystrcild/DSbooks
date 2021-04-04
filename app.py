from flask import Flask, render_template, request
from search import SearchForm, get_books_by_search

app = Flask(__name__)


@app.route('/', methods=["GET","POST"])
def index():
    form = SearchForm()
    return render_template("index.html", form=form)

@app.route('/result', methods=["GET","POST"])
def search_result():
    form = SearchForm(request.form)
    results = get_books_by_search(form.search.data)
    return render_template("result.html", form=form, results=results)

if __name__ == '__main__':
    app.run(debug=True)
