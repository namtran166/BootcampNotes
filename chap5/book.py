import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

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
        help = "This book cannot be written by no one"
    )

    @classmethod
    def find_by_bookID(cls, bookID):
        connection = sqlite3.connect('data.db')

        cursor = connection.cursor()
        select_query = "SELECT * FROM bookList WHERE bookID = ?"
        result = cursor.execute(select_query, (bookID,))
        row = result.fetchone()

        connection.close()

        if row:
            return {'book': {'bookID': row[0], 'name': row[1], 'author': row[2]}}

    @classmethod
    def insert_book(cls, book):
        connection = sqlite3.connect('data.db')

        cursor = connection.cursor()
        insert_query = "INSERT INTO bookList VALUES (?, ?, ?)"
        cursor.execute(insert_query, (book['bookID'], book['name'], book['author']))

        connection.commit()
        connection.close()

    @classmethod
    def update_book(cls, book):
        connection = sqlite3.connect('data.db')

        cursor = connection.cursor()
        update_query = "UPDATE bookList SET name = ?, author = ? WHERE bookID = ?"
        cursor.execute(update_query, (book['name'], book['author'], book['bookID']))

        connection.commit()
        connection.close()

    # No need for authentication since GET method is safe
    def get(self, bookID):
        item = self.find_by_bookID(bookID)
        if item:
            return item, 200
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, bookID):
        if self.find_by_bookID(bookID):
            return {'message': "A book with bookID '{}' already exists.".format(bookID)}, 400

        data = Book.parser.parse_args()
        try:
            book = {'bookID': bookID, 'name': data['name'], 'author': data['author']}
            self.insert_book(book)
        except:
            return {'message': 'an error occured while trying to post this book ID'}, 500
        return book, 201

    @jwt_required()
    def delete(self, bookID):
        if self.find_by_bookID(bookID) is None:
            return {'message': "There is no book with bookID '{}'.".format(bookID)}, 400

        connection = sqlite3.connect('data.db')

        cursor = connection.cursor()
        delete_query = "DELETE FROM bookList WHERE bookID = ?"
        cursor.execute(delete_query, (bookID,))

        connection.commit()
        connection.close()
        return {'message': 'Book deleted'}, 200

    @jwt_required()
    def put(self, bookID):
        data = Book.parser.parse_args()
        book = {'bookID': bookID, 'name': data['name'], 'author': data['author']}

        if self.find_by_bookID(bookID):
            try:
                self.insert_book(book)
            except:
                return {'message': 'an error occured while trying to insert this book ID'}, 500
        else:
            try:
                self.update_book(book)
            except:
                return {'message': 'an error occured while trying to update this book ID'}, 500
        return book


class BookList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')

        cursor = connection.cursor()
        select_all_query = "SELECT * FROM bookList"
        all_row = cursor.execute(select_all_query)
        items = [{'bookID': row[0], 'name': row[1], 'author': row[2]} for row in all_row]

        connection.close()
        return {'items': items}
