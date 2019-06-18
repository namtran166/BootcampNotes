A project created based on the REST APIs with Flask and Python course taught by Jose Salvatierra

# Preparation

## Set up virtual environment and required Python package
For this small project, we need to install virtual environment and some Python libraries, including Flask, Flask-JWT, Flask-RESTful, and Flask-SQLAlchemy. I am using Python 3.7.3, but other versions of Python are also supported.
```
$ pip3.7 install virtualenv
$ virtualenv -p python3 /path_to_your_virtualenv       # create your own path to virtualenv
$ source your_virtualenv_path/bin/activate             # activate your virtualenv
$ pip3.7 install Flask                                 # install Flask
$ pip3.7 install Flask-JWT                             # install Flask-JWT
$ pip3.7 install Flask-RESTful                         # install Flask-RESTful
$ pip3.7 install Flask-SQLAlchemy.                     # install Flask-SQLAlchemy
$ pip3.7 freeze                                        # double check the requirements
$ deactivate                                           # exit the current virtualenv
```

## Start the server
```
$ source your_virtualenv_path/bin/activate             # activate your virtualenv
$ cd folder_name/chap6
$ python app.py
```
Then we can open the server at http://127.0.0.1:5000/

# API Docs

## /register
User authentication is required when using "unsafe" requests, which including POST, DELETE, and PUT, since these methods modify our database. This endpoint is used to register a new user.
```
Header:
    Content-Type: application/json
    
Body:
{
    "username": <string:username>
    "password": <string:password>
}
```
When an user is created successfully, a 201 Created response will be sent back, alongside with this message:
```
{
    "message": "User created successfully."
}
```
When an user with this username already exists in our database, a 400 Bad Request response will be sent back, alongside with this message:
```
{
    "message": "A user with that username already exists"
}
```
When there is some unexpected error within our internal server, a 500 Internal Server Error response will be returned, and you should upload the bug for us to fix!
```
{
    "message": "An error occurred when trying to create this user."
}
```
In case you forgot to put an username, a 400 Bad Request response will be sent back alongside with this message:
```
{
    "message": {
        "username": "Username cannot be blank."
    }
}
```
The same thing happens when you forget to put a password, a 400 Bad Request response will be returned with this message:
```
{
    "message": {
        "password": "Password cannot be blank."
    }
}
```

## /auth
Once you create an user in our server, you can retrieve the access token anytime you want! This endpoint will return an access token whenever a registered user information is provided.
```
Header:
    Content-Type: application/json
   
Body:   
{
    "username": <string:username>
    "password": <string:password>
}
```
When a registered user with correct password requests successfully, a 200 OK response will be sent back, alongside with the access token:
```
{
    "access_token": <string:access_token>
}
```
When the client enters an unregistered user, or an registered user with incorrect password, or missing either password or username, a 401 Unauthorized response will be sent back, alongside with this message:
```
{
    "description": "Invalid credentials",
    "error": "Bad Request",
    "status_code": 401
}
```

## GET /books
What is even a bookstore without our favorite books? With this endpoint we can easily access to all books we currently have in our database! Just a quick reminder, don't forget to put some books in the database first!
```
No request body needed!
```
Whatever the request is, there is always a 200 OK response with our books (none or many):
```
{
    "books": [
        {
            "bookID": <int:bookID>,
            "name": <string:name>,
            "author": <string:author>,
            "store_id": <int:store_id>
        },
        ...
    ]
}
```

## GET /books/bookID
With this endpoint we can easily access to a particular book we currently have in our database! Just a quick reminder, don't forget to put the bookID!
```
No request body needed!
```
In case you find your book, congratulations! There is always a 200 OK response with your book as well:
```
{
    "bookID": <int:bookID>,
    "name": <string:name>,
    "author": <string:author>,
    "store_id": <int:store_id>
}
```
Too bad we cannot find your book! However, we find a 404 Not Found response for you:
```
{
    "message": "Item not found"
}
```
When there is some unexpected error within our internal server, a 500 Internal Server Error response will be returned, and you should upload the bug for us to fix!
```
{
    "message": "An error occurred when trying to get this book."
}
```

## POST /books/bookID
With this endpoint we can easily upload our favorite book we currently have in our database! Just a quick reminder, don't forget to put the bookID!
```
Header:
    Content-Type: application/json
    Authorization: JWT <string:jwt_token>

Body:
{
    "bookID": <int:bookID>,
    "name": <string:name>,
    "author": <string:author>,
    "store_id": <int:store_id>
}
```
In case we can upload your book, congratulations! We return a 201 Created response with your book as well:
```
{
    "bookID": <int:bookID>,
    "name": <string:name>,
    "author": <string:author>,
    "store_id": <int:store_id>
}
```
Too bad we cannot upload your book since someone already registered for this bookID! A 400 Bad Request response will be return with this message:
```
{
    "message": "A book with bookID <int:bookID> already exists."
}
```
Did you forgot to authorize yourself? You bet. Since our books are precious, we cannot allow anyone to go and just upload some random books! A 401 Unauthorized reminder for you!
```
{
    "description": "Request does not contain an access token",
    "error": "Authorization Required",
    "status_code": 401
}
```
Did you log in a long time ago? You should log in again since our protected system invalidate unused access token after some time! A 401 Unauthorized reminder for you!
```
{
    "description": "Signature has expired",
    "error": "Authorization Required",
    "status_code": 401
}
```
When there is some unexpected error within our internal server, a 500 Internal Server Error response will be returned, and you should upload the bug for us to fix!
```
{
    "message": "An error occurred when trying to post this book."
}
```

## DELETE /books/bookID
With this endpoint we can easily remove our unwanted book we currently have in our database! Just a quick reminder, don't forget to put the bookID!
```
Header:
    Authorization: JWT <string:jwt_token>
```
In case we can remove the book you hated, congratulations! We return a 200 OK response with this message:
```
{
    "message": "Book deleted"
}
```
Too bad we cannot find the book you hated, maybe it was removed a long time ago! A 404 Not Found response will be return with this message:
```
{
    "message": "There is no book with bookID <int:bookID>"
}
```
Did you forgot to authorize yourself? You bet. Since our books are precious, we cannot allow anyone to go and just delete some random books! A 401 Unauthorized reminder for you!
```
{
    "description": "Request does not contain an access token",
    "error": "Authorization Required",
    "status_code": 401
}
```
Did you log in a long time ago? You should log in again since our protected system invalidate unused access token after some time! A 401 Unauthorized reminder for you!
```
{
    "description": "Signature has expired",
    "error": "Authorization Required",
    "status_code": 401
}
```
When there is some unexpected error within our internal server, a 500 Internal Server Error response will be returned, and you should upload the bug for us to fix!
```
{
    "message": "An error occurred when trying to delete this book."
}
```

## PUT /books/bookID
Unsure you put this book to our database or not? Well, you can simply use this PUT method, it will create a new book or update an existing one based on the bookID you provided.
```
Header:
    Content-Type: application/json
    Authorization: JWT <string:jwt_token>

Body:
{
    "bookID": <int:bookID>,
    "name": <string:name>,
    "author": <string:author>,
    "store_id": <int:store_id>
}
```
In case there is no book in our database with this ID, we just created a new one for you! We return a 201 Created response with this book you just created:
```
{
    "bookID": <int:bookID>,
    "name": <string:name>,
    "author": <string:author>,
    "store_id": <int:store_id>
}
```
Yay we found your book in our database! We return a 200 OK response with the updated book:
```
{
    "bookID": <int:bookID>,
    "name": <string:name>,
    "author": <string:author>,
    "store_id": <int:store_id>
}
```
Did you forgot to authorize yourself? You bet. Since our books are precious, we cannot allow anyone to go and just update some random books! A 401 Unauthorized reminder for you!
```
{
    "description": "Request does not contain an access token",
    "error": "Authorization Required",
    "status_code": 401
}
```
Did you log in a long time ago? You should log in again since our protected system invalidate unused access token after some time! A 401 Unauthorized reminder for you!
```
{
    "description": "Signature has expired",
    "error": "Authorization Required",
    "status_code": 401
}
```
When there is some unexpected error within our internal server, a 500 Internal Server Error response will be returned, and you should upload the bug for us to fix!
```
{
    "message": "An error occurred when trying to put this book."
}
