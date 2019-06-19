from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.book import BookModel


class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='What book is this?'
                        )
    parser.add_argument('author',
                        type=str,
                        required=True,
                        help='This book cannot be written by no one!'
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every book needs a store to sell!'
                        )

    # No need for authentication since GET method is safe
    @staticmethod
    def get(book_id):
        try:
            book = BookModel.find_by_book_id(book_id)
            if book:
                return book.json(), 200
            return {'message': 'Book not found!'}, 404
        except:
            return {'message': 'An error occurred when trying to get this book.'}, 500

    @jwt_required()
    def post(self, book_id):
        if BookModel.find_by_book_id(book_id):
            return {'message': "A book with book_id '{}' already exists.".format(book_id)}, 400

        data = Book.parser.parse_args()
        try:
            book = BookModel(book_id, **data)
            book.save_to_db()
        except:
            return {'message': 'An error occured while trying to post this book.'}, 500
        return book.json(), 201

    @jwt_required()
    def delete(self, book_id):
        book = BookModel.find_by_book_id(book_id)
        if book is None:
            return {'message': "There is no book with book_id '{}'.".format(book_id)}, 404
        else:
            try:
                book.delete_from_db()
                return {'message': 'Book deleted'}, 200
            except:
                return {'message': 'An error occurred when trying to delete this book.'}, 500

    @jwt_required()
    def put(self, book_id):
        data = Book.parser.parse_args()
        book = BookModel.find_by_book_id(book_id)

        try:
            if book is None:
                return {'message': 'Book not found.'}, 404
            else:
                book.name = data['name']
                book.author = data['author']
                book.store_id = data['store_id']
                book.save_to_db()
                return book.json(), 200
        except:
            return {'message': 'An error occured while trying to put this book ID'}, 500


class BookList(Resource):
    @staticmethod
    def get():
        return [book.json() for book in BookModel.query.all()], 200
