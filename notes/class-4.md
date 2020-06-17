
# Class 4

> If you haven't already, please sign up for a Heroku account and make sure you have the CLI set up!
>  + https://signup.heroku.com/
>  + https://devcenter.heroku.com/articles/getting-started-with-python#set-up

Lambda Materials:

  + https://learn.lambdaschool.com/ds/module/recpPYQdaOmZdBSYq/
  + https://github.com/LambdaSchool/DS-Unit-3-Sprint-3-Productization-and-Cloud/tree/master/module4-web-application-deployment

Installing production environment dependencies:

```sh
pipenv install gunicorn psycopg2-binary
```

## Part I

Heroku and the Heroku CLI:

  + https://heroku.com/
  + https://devcenter.heroku.com/articles/using-the-cli
  + https://github.com/prof-rossetti/intro-to-python/blob/master/notes/clis/heroku.md (BONUS)
  + ["Delivery and Deployment" Slides](https://docs.google.com/presentation/d/1CPZXF_JO-zi6i6_OU7mGYvDJdqB3LBo7HF4bmyCbjMY/edit#slide=id.g5846519fbe_0_2378) (BONUS)

Logging in to Heroku from the CLI (first time only):

```sh
heroku login
```

Creating a new application server (MUST BE DONE FROM WITHIN THE REPOSITORY'S ROOT DIRECTORY):

```sh
git remote -v
heroku create # optionally provide a name... "heroku create my-app-name"
git remote -v
```

Deploying to production:

```sh
git push heroku master
# or... git push heroku my_branch:master
```

Viewing production app in browser:

```sh
heroku open
```

Checking production server logs:

```sh
heroku logs --tail
```

Logging into production server, running things there:

```sh
heroku run bash
# ... whoami
# ... pwd
# ... python --version
# ... python web_app/services/stocks_service.py
# ... exit
```

Running "detached" commands against the production server:

```sh
heroku run "python web_app/services/stocks_service.py"
```

Using a "Procfile" to specify the "web" process:

```sh
web: gunicorn "web_app:create_app()"
```



## Part II

Heroku PG:

  + https://devcenter.heroku.com/articles/heroku-postgresql#provisioning-heroku-postgres
  + https://devcenter.heroku.com/articles/heroku-postgres-plans#hobby-tier

Flask Migrate:

  + https://stackoverflow.com/questions/17768940/target-database-is-not-up-to-date

Database URL Format: `DATABASE_URL="postgres://USERNAME:PASSWORD@HOST:5432/DB_NAME`

Example Database URLs for local SQLite DB:

```sh
# local .env file...

# mac:
DATABASE_URL="sqlite:////Users/YOURUSERNAME/Desktop/my-web-app-12/web_app/web_app_12.db"

# windows:
DATABASE_URL="sqlite:///C:\\Users\\YOURUSERNAME\\Desktop\\TwitterApp\\web_app\\web_app_200.db"
```

Provisioning production database:

```sh
heroku config
heroku addons:create heroku-postgresql:hobby-dev
#> provisions a new DATABASE_URL
heroku config
```

Migrating the production database:

```sh
# first login to the server, then run the migration commands there:
heroku run bash
# ... FLASK_APP=web_app flask db init
# ... FLASK_APP=web_app flask db migrate
# ... FLASK_APP=web_app flask db upgrade

# that should work, but alternatively you might be able to run these detached commands (if you didn't ignore your migrations dir):
heroku run "FLASK_APP=web_app flask db init"
heroku run "FLASK_APP=web_app flask db stamp head"
heroku run "FLASK_APP=web_app flask db migrate"
heroku run "FLASK_APP=web_app flask db upgrade"
```

## Part III


Configuring production environment variables:

```sh
heroku config
heroku config:set ALPHAVANTAGE_API_KEY="_____"
heroku config:set BASILICA_API_KEY="_____"
heroku config:set TWITTER_API_KEY="_____"
heroku config:set TWITTER_API_SECRET="______"
heroku config:set TWITTER_ACCESS_TOKEN="______"
heroku config:set TWITTER_ACCESS_TOKEN_SECRET="_____"
heroku config
```


