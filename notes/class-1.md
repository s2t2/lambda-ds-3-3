
# Class 1

Topics / Agenda:

  1. HTTP, Client-server architecture; Web Application Routing
  2. Web Application Views and View Templates
  3. Adding a database w/ Flask SQL Alchemy

Lambda Materials:

  + https://learn.lambdaschool.com/ds/module/recKGvwkPaEsfnwDL/
  + https://github.com/LambdaSchool/DS-Unit-3-Sprint-3-Productization-and-Cloud/tree/master/module1-web-application-development-with-flask

Create a new repo on GitHub, then get it setup locally:

```sh
git clone YOUR_REMOTE_ADDRESS
cd your-repo-name
pipenv --python 3.7
```

Installing package dependencies:

```sh
pipenv install Flask Flask-SQLAlchemy Flask-Migrate
```

## Part I

HTTP Slides:
  + https://docs.google.com/presentation/d/1K83U0VjYob6dgdRodbidWBtFxK4Q_9h8zojzmto2wJY/edit#slide=id.g5846519fbe_0_1904

Flask Basics:

  + https://github.com/pallets/flask
  + https://palletsprojects.com/p/flask/
  + https://flask.palletsprojects.com/en/1.1.x/quickstart/
  + https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
  + https://flask.palletsprojects.com/en/1.1.x/blueprints/
  + https://flask.palletsprojects.com/en/1.1.x/tutorial/static/

Flask App Examples:

  + [Twitoff App Solutions](https://github.com/s2t2/lambda-ds-3-3/blob/master/README.md#solutions)
  + https://github.com/prof-rossetti/web-app-starter-flask (BONUS / FYI)
  + https://github.com/prof-rossetti/web-app-starter-flask-sheets (BONUS / FYI, uses a google sheets datastore)
  + https://github.com/prof-rossetti/salad-system-alchemy (BONUS / FYI, MySQL version, a little old)

Testing a Flask App (FYI / BONUS):

  + https://flask.palletsprojects.com/en/1.1.x/testing/
  + https://github.com/prof-rossetti/products-api-flask/blob/master/tests/products_api/app_test.py

Defining a basic Flask App:

```py
# hello.py

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    x = 2 + 2
    return f"Hello World! {x}"

@app.route("/about")
def about():
    return "About me"
```

Running a Flask App:

```sh
# Mac:
FLASK_APP=hello.py flask run

# Windows:
export FLASK_APP=hello.py # one-time thing, to set the env var
flask run
```

> NOTE: if you're on Windows and `export` doesn't work for you, try `set` instead.

> NOTE: right now our app is located in the "hello.py" file, which is why we use `FLASK_APP=hello.py` but we will soon be changing this when our app grows larger...

Init file in "web_app" directory:

```py
# web_app/__init__.py

from flask import Flask

from web_app.routes.home_routes import home_routes
from web_app.routes.book_routes import book_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_routes)
    app.register_blueprint(book_routes)
    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
```

Home routes:

```py
# web_app/routes/home_routes.py

from flask import Blueprint

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def index():
    x = 2 + 2
    return f"Hello World! {x}"

@home_routes.route("/about")
def about():
    return "About me"
```

Running the Flask App, after new "web_app" organizational structure in place:

```sh
# Mac:
FLASK_APP=web_app flask run

# Windows:
set FLASK_APP=web_app # one-time thing, to set the env var
flask run
```


## Part II

> FYI: As a basic requirement for this part of class, we'll just return some plain HTML pages. Only if you have time and interest should you also concern yourself with the shared layouts and the Twitter Bootstrap styling. We might have some time to review them in-class during class 4, otherwise all the info and starter code you need is below. 

HTML:
  + https://www.w3schools.com/html/html_basic.asp
  + https://www.w3schools.com/html/html_forms.asp
  
Flask View Templates:
  + https://flask.palletsprojects.com/en/1.1.x/tutorial/templates/
  + https://jinja.palletsprojects.com/en/2.11.x/templates/
  + https://jinja.palletsprojects.com/en/2.11.x/tricks/

Twitter Bootstrap (BONUS):
  + https://getbootstrap.com/
  + https://getbootstrap.com/docs/4.4/getting-started/introduction/
  + https://getbootstrap.com/docs/4.0/components/navbar/
  + https://getbootstrap.com/docs/3.4/examples/navbar-fixed-top/
  + https://getbootstrap.com/docs/4.0/components/navbar/#color-schemes
  + https://stackoverflow.com/questions/19733447/bootstrap-navbar-with-left-center-or-right-aligned-items

Using Twitter Bootstrap to improve the look and feel of your HTML view templates, and inheriting HTML contents from a common base layout, and other template examples (BONUS):
  + https://github.com/prof-rossetti/web-app-starter-flask-sheets/blob/master/web_app/templates/layout.html
  + https://github.com/prof-rossetti/web-app-starter-flask-sheets/blob/master/web_app/templates/index.html
  + https://github.com/prof-rossetti/web-app-starter-flask-sheets/blob/master/web_app/templates/products/index.html

Example of flash and redirect (BONUS):
  + https://github.com/prof-rossetti/web-app-starter-flask-sheets/blob/master/web_app/routes/products_api.py#L31-L32


Book routes:

```py
# web_app/routes/book_routes.py

from flask import Blueprint, jsonify, request, render_template #, flash, redirect

book_routes = Blueprint("book_routes", __name__)

@book_routes.route("/books.json")
def list_books():
    books = [
        {"id": 1, "title": "Book 1"},
        {"id": 2, "title": "Book 2"},
        {"id": 3, "title": "Book 3"},
    ]
    return jsonify(books)

@book_routes.route("/books")
def list_books_for_humans():
    books = [
        {"id": 1, "title": "Book 1"},
        {"id": 2, "title": "Book 2"},
        {"id": 3, "title": "Book 3"},
    ]
    return render_template("books.html", message="Here's some books", books=books)

@book_routes.route("/books/new")
def new_book():
    return render_template("new_book.html")

@book_routes.route("/books/create", methods=["POST"])
def create_book():
    print("FORM DATA:", dict(request.form))
    # todo: store in database
    return jsonify({
        "message": "BOOK CREATED OK (TODO)",
        "book": dict(request.form)
    })
    #flash(f"Book '{new_book.title}' created successfully!", "success")
    #return redirect(f"/books")

```

Books Page:

```html
<!-- web_app/templates/books.html -->

{% extends "layout.html" %}

{% block title %}
    <title>Books Page</title>
{% endblock %}

{% block content %}

    <h2>Welcome to the Books Page</h2>

    <p>{{ message }}</p>

    {% if books %}
        <ul>
        {% for book in books %}
            <li>{{ book["title"] }}</li>
        {% endfor %}
        </ul>

    {% else %}
        <p>Books not found.</p>
    {% endif %}

{% endblock %}
```

New Book Form:

```html
<!-- web_app/templates/new_book.html -->

{% extends "layout.html" %}

{% block content %}

    <h1>New Book Page</h1>

    <p>Please fill out the form and submit to create a new book!</p>

    <form action="/books/create" method="POST">

        <label>Title:</label>
        <input type="text" name="title" placeholder="Book XYZ" value="Book XYZ">

        <label>Author:</label>
        <select name="author_name">
          <option value="A1">Author 1</option>
          <option value="A2">Author 2</option>
          <option value="A3">Author 3</option>
        </select>

        <button>Submit</button>
    </form>
{% endblock %}
```

Shared layout, basic:

```html
<!-- web_app/templates/layout.html -->

<!doctype html>
<html>
  <head>
    {% block title %}
      <title>My Starter Web App | Helps students learn how to use the Flask Python package.</title>
    {% endblock %}
  </head>

  <body>

    <!-- SITE NAVIGATION -->
    <div class="container">
      <div id="nav">
        {% block nav %}
          <h1><a href="/">My Web App</a></h1>
          <ul>
            <li><a href="/books">Books Page</a></li>
            <li><a href="/books/new">New Book Form</a></li>
          </ul>
        {% endblock %}
      </div>
      <hr>

      <!-- PAGE CONTENTS -->
      <div id="content">
        {% block content %}
        {% endblock %}
      </div>

      <!-- FOOTER -->
      <div id="footer">
        <hr>
        &copy; Copyright 2020 [YOUR NAME HERE!] |
        <a href="https://github.com/YOUR_NAME/YOUR_REPO">source</a>
      </div>
    </div>

  </body>
</html>
```

... Or optionally reference this [Twitter Bootstrap Layout](/reference_code/templates/bootstrap_layout.html).

... Or this slightly more complex [Twitter Bootstrap Navbar Layout](/reference_code/templates/bootstrap_nav_layout.html), in which case you'll also need to add `{% set active_page = "books" %}` to the "books.html" and `{% set active_page = "new_book" %}` to the "new_book.html".

## Part III

Flask-SQLAlchemy:
  + https://github.com/pallets/flask-sqlalchemy/
  + https://flask-sqlalchemy.palletsprojects.com/en/2.x/
  + https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#models
  + https://docs.sqlalchemy.org/en/13/core/type_basics.html
  + https://docs.sqlalchemy.org/en/13/orm/join_conditions.html?highlight=foreign%20key

Flask-Migrate:
  + https://flask-migrate.readthedocs.io/en/latest/
  + https://github.com/miguelgrinberg/Flask-Migrate


Defining database model class(es):

```py
# web_app/models.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

migrate = Migrate()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    author_id = db.Column(db.String(128))

    def __repr__(self):
        return f"<Book {self.id} {self.title}>"
    
def parse_records(database_records):
    """
    A helper method for converting a list of database record objects into a list of dictionaries, so they can be returned as JSON

    Param: database_records (a list of db.Model instances)

    Example: parse_records(User.query.all())

    Returns: a list of dictionaries, each corresponding to a record, like...
        [
            {"id": 1, "title": "Book 1"},
            {"id": 2, "title": "Book 2"},
            {"id": 3, "title": "Book 3"},
        ]
    """
    parsed_records = []
    for record in database_records:
        print(record)
        parsed_record = record.__dict__
        del parsed_record["_sa_instance_state"]
        parsed_records.append(parsed_record)
    return parsed_records
```

> WHY BOOKS? The `Book` class is just an example class so we can learn how to store and retrieve records. The assignment mentions making `User` class and/or a `Tweet class`. You can feel free to use whatever class you want for now. Next class we'll fetch user and tweet data from the Twitter API, at which point we'll be better positioned to know what attributes exist, which will inform how we define the `User` and `Tweet` classes.

Updating app construction:

```py
# web_app/__init__.py

from flask import Flask

from web_app.models import db, migrate
from web_app.routes.home_routes import home_routes
from web_app.routes.book_routes import book_routes

DATABASE_URI = "sqlite:///web_app_99.db" # using relative filepath
#DATABASE_URI = "sqlite:////Users/Username/Desktop/your-repo-name/web_app_99.db" # using absolute filepath on Mac (recommended)
#DATABASE_URI = "sqlite:///C:\\Users\\Username\\Desktop\\your-repo-name\\web_app_99.db" # using absolute filepath on Windows (recommended) h/t: https://stackoverflow.com/a/19262231/670433

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_routes)
    app.register_blueprint(book_routes)

    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)

```

Creating and migrating the database:

```sh
# Windows users can omit the "FLASK_APP=web_app" part...

FLASK_APP=web_app flask db init #> generates app/migrations dir

# run both when changing the schema:
FLASK_APP=web_app flask db migrate #> creates the db (with "alembic_version" table)
FLASK_APP=web_app flask db upgrade #> creates the specified tables
```

Updating routes to integrate with database:

```sh
# SELECT * FROM books
book_records = Book.query.all()
print(book_records)

# INSERT INTO books ...
new_book = Book(title=request.form["title"], author_id=request.form["author_name"])
db.session.add(new_book)
db.session.commit()
```
