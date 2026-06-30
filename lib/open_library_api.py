# from flask import Flask
# import requests
# import json
# import jsonify


# class Search:

#     def get_search_results(self, search_term):
#         search_term_formatted = search_term.replace(" ", "+")
#         fields = ["title", "author_name"]
#         fields_formatted = ",".join(fields)
#         limit = 1

#         URL = f"https://openlibrary.org/search.json?title={search_term_formatted}&fields={fields_formatted}&limit={limit}"

#         response = requests.get(URL).json()
#         response_formatted = f"Title: {response['docs'][0]['title']}\nAuthor: {response['docs'][0]['author_name'][0]}"
#         return response_formatted

# search_term = input("Enter a book title: ")
# result = Search().get_search_results(search_term)
# print("Search Result:\n")
# print(result)
# app= Flask(__name__)
# authors = [
#     {"id": 1, "name": "Octavia Butler", "books": [
#         {"id": 1, "title": "Kindred"},
#         {"id": 2, "title": "Parable of the Sower"}
#     ]},
#     {"id": 2, "name": "Toni Morrison", "books": [
#         {"id": 1, "title": "Beloved"},
#         {"id": 2, "title": "Song of Solomon"}
#     ]}
# ]

# @app.route('/authors')
# def get_authors():
#     return jsonify(authors)

# @app.route('/authors/<int:id>')
# def get_author(id):
#     author = next((a for a in authors if a["id"] == id), None)
#     return jsonify(author) if author else ("Author not found", 404)

# @app.route('/authors/<int:id>/books')
# def get_author_books(id):
#     author = next((a for a in authors if a["id"] == id), None)
#     return jsonify(author["books"]) if author else ("Author not found", 404)
# @app.route('/authors/<int:author_id>/books/<int:book_id>')
# def get_author_book(author_id, book_id):
#     author = next((a for a in authors if a["id"] == author_id), None)
#     if not author:
#         return ("Author not found", 404)
#     book = next((b for b in author["books"] if b["id"] == book_id), None)
#     return jsonify(book) if book else ("Book not found", 404)
from flask import Flask, jsonify

app = Flask(__name__)

# Define Book class
class Book:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# Define Author class
class Author:
    def __init__(self, id, name, books):
        self.id = id
        self.name = name
        self.books = books  # list of Book objects

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "books": [book.to_dict() for book in self.books]
        }

# Sample data
authors = [
    Author(1, "Octavia Butler", [
        Book(1, "Kindred"),
        Book(2, "Parable of the Sower")
    ]),
    Author(2, "Toni Morrison", [
        Book(3, "Beloved"),
        Book(4, "Song of Solomon")
    ])
]

# GET /authors
@app.route("/authors")
def get_authors():
    return jsonify([author.to_dict() for author in authors])

# GET /authors/<int:id>
@app.route("/authors/<int:id>")
def get_author(id):
    author = next((a for a in authors if a.id == id), None)
    return jsonify(author.to_dict()) if author else ("Author not found", 404)

# GET /authors/<int:id>/books
@app.route("/authors/<int:id>/books")
def get_books_by_author(id):
    author = next((a for a in authors if a.id == id), None)
    return jsonify([book.to_dict() for book in author.books]) if author else ("Author not found", 404)

# GET /authors/<int:author_id>/books/<int:book_id>
@app.route("/authors/<int:author_id>/books/<int:book_id>")
def get_book_by_author(author_id, book_id):
    author = next((a for a in authors if a.id == author_id), None)
    if not author:
        return ("Author not found", 404)
    book = next((b for b in author.books if b.id == book_id), None)
    return jsonify(book.to_dict()) if book else ("Book not found", 404)


if __name__ == '__main__':
    app.run(debug=True)

