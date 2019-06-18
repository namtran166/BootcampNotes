from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from book import Book, BookList

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'brian'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Book, '/books/<int:bookID>')
api.add_resource(BookList, '/books')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug = True)  # important to mention debug=True
