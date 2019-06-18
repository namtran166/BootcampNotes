from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.book import BookModel

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
        help = "This book cannot be written by no one!"
    )
    parser.add_argument('store_id',
        type = int,
        required = True,
        help = "Every book needs a store to sell!"
    )

    # No need for authentication since GET method is safe
    def get(self, bookID):
        try:
            book = BookModel.find_by_bookID(bookID)
            if book:
                return book.json(), 200
            return {'message': 'Item not found'}, 404
        except:
            return {'message': 'An error occurred when trying to get this book.'}, 500

    @jwt_required()
    def post(self, bookID):
        if BookModel.find_by_bookID(bookID):
            return {'message': "A book with bookID '{}' already exists.".format(bookID)}, 400

        data = Book.parser.parse_args()
        try:
            book = BookModel(bookID, **data)
            book.save_to_db()
        except:
            return {'message': 'An error occured while trying to post this book.'}, 500
        return book.json(), 201

    @jwt_required()
    def delete(self, bookID):
        book = BookModel.find_by_bookID(bookID)
        if book is None:
            return {'message': "There is no book with bookID '{}'.".format(bookID)}, 400
        else:
            try:
                book.delete_from_db()
                return {'message': 'Book deleted'}, 200
            except:
                return {'message': 'An error occurred when trying to delete this book.'}, 500

    @jwt_required()
    def put(self, bookID):
        data = Book.parser.parse_args()
        book = BookModel.find_by_bookID(bookID)

        try:
            if book:
                book.name = data['name']
                book.author = data['author']
                book.store_id = data['store_id']
            else:
                book = BookModel(bookID, **data)
            book.save_to_db()
        except:
            return {'message': 'An error occured while trying to put this book ID'}, 500
        return book.json(), 200


class BookList(Resource):
    def get(self):
        return {'books': [book.json() for book in BookModel.query.all()]}
