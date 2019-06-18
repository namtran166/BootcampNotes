from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity

from security import authenticate, identity

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'brian'
api = Api(app)

jwt = JWT(app, authenticate, identity)

bookList = [
    {
        'bookID': 101,
        'name': 'The Book Thief',
        'author': 'Markus Zusak'
    },
    {
        'bookID': 102,
        'name': 'The Four',
        'author': 'Scott Galloway'
    },
    {
        'bookID': 103,
        'name': '1984',
        'author': 'George Orwell'
    }
]

class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type = str,
        required = True,
        help = "What book is this?"
    )
    parser.add_argument('author',
        type = str,
        required = True,
        help = "This book cannot be written by noone"
    )

    # No need for authentication since GET method is safe
    def get(self, bookID):
        return {'book': next(filter(lambda x: x['bookID'] == bookID, bookList), None)}

    @jwt_required()
    def post(self, bookID):
        if next(filter(lambda x: x['bookID'] == bookID, bookList), None) is not None:
            return {'message': "A book with bookID '{}' already exists.".format(bookID)}

        data = Book.parser.parse_args()

        book = {
            'bookID': bookID, 'name': data['name'], 'author': data['author']
        }
        bookList.append(book)
        return book


    @jwt_required()
    def delete(self, bookID):
        global bookList
        bookList = list(filter(lambda x: x['bookID'] != bookID, bookList))
        return {'message': 'Book deleted'}

    @jwt_required()
    def put(self, bookID):
        data = Book.parser.parse_args()
        book = next(filter(lambda x: x['bookID'] == bookID, bookList), None)
        if book is None:
            book = {
                'bookID': bookID,
                'name': data['name'],
                'author': data['author']
            }
            bookList.append(book)
        else:
            book.update(data)
        return book


class BookList(Resource):
    def get(self):
        return {'bookList': bookList}

api.add_resource(Book, '/books/<int:bookID>')
api.add_resource(BookList, '/books')

if __name__ == '__main__':
    app.run(debug = True)  # important to mention debug=True
