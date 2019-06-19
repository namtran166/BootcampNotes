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
