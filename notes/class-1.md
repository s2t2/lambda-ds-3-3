
# Class 1

Topics / Agenda:

  1. HTTP, Client-server architecture; Web Application Routing
  2. Web Application Views and View Templates
  3. Adding a database w/ Flask SQL Alchemy

Lambda Materials:

  + https://learn.lambdaschool.com/ds/module/recKGvwkPaEsfnwDL/
  + https://github.com/LambdaSchool/DS-Unit-3-Sprint-3-Productization-and-Cloud/tree/master/module1-web-application-development-with-flask

## Part I

HTTP Slides:
  + https://docs.google.com/presentation/d/1K83U0VjYob6dgdRodbidWBtFxK4Q_9h8zojzmto2wJY/edit#slide=id.g5846519fbe_0_1904

Flask:

  + https://github.com/pallets/flask
  + https://palletsprojects.com/p/flask/
  + https://flask.palletsprojects.com/en/1.1.x/quickstart/
  + https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
  + https://flask.palletsprojects.com/en/1.1.x/blueprints/

"Twitoff" Flask App Examples:

  + [For DS 11](https://github.com/s2t2/web-app-inclass-11)
  + [For DS PT3](https://github.com/s2t2/web-app-inclass-pt3)

Other Flask App Examples (FYI / BONUS):

  + https://github.com/prof-rossetti/web-app-starter-flask
  + https://github.com/prof-rossetti/web-app-starter-flask-sheets (uses a google sheets datastore)
  + https://github.com/prof-rossetti/salad-system-alchemy (MySQL version, a little old)

Testing a Flask App (FYI / BONUS):

  + https://flask.palletsprojects.com/en/1.1.x/testing/
  + https://github.com/prof-rossetti/products-api-flask/blob/master/tests/products_api/app_test.py

## Part II

Flask View Templates:
  + https://flask.palletsprojects.com/en/1.1.x/tutorial/templates/
  + https://jinja.palletsprojects.com/en/2.11.x/templates/

Twitter Bootstrap (BONUS):
  + https://getbootstrap.com/docs/4.4/getting-started/introduction/

Using Twitter Bootstrap to improve the look and feel of your HTML view templates, and inheriting HTML contents from a common base layout, and other template examples (BONUS):
  + https://github.com/prof-rossetti/web-app-starter-flask-sheets/blob/master/web_app/templates/layout.html
  + https://github.com/prof-rossetti/web-app-starter-flask-sheets/blob/master/web_app/templates/index.html
  + https://github.com/prof-rossetti/web-app-starter-flask-sheets/blob/master/web_app/templates/products/index.html

Example of flash and redirect (BONUS):
  + https://github.com/prof-rossetti/web-app-starter-flask-sheets/blob/master/web_app/routes/products_api.py#L31-L32

## Part III

Flask-SQLAlchemy:
  + https://github.com/pallets/flask-sqlalchemy/
  + https://flask-sqlalchemy.palletsprojects.com/en/2.x/
  + https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#models
  + https://docs.sqlalchemy.org/en/13/core/type_basics.html
  + https://docs.sqlalchemy.org/en/13/orm/join_conditions.html?highlight=foreign%20key

```py

```

Flask-Migrate:
  + https://flask-migrate.readthedocs.io/en/latest/
  + https://github.com/miguelgrinberg/Flask-Migrate

```sh
FLASK_APP=web_app flask db init
FLASK_APP=web_app flask db migrate
FLASK_APP=web_app flask db upgrade
```
