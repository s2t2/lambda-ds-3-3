
# Class 4

Lambda Materials:

  + https://learn.lambdaschool.com/ds/module/recpPYQdaOmZdBSYq/
  + https://github.com/LambdaSchool/DS-Unit-3-Sprint-3-Productization-and-Cloud/tree/master/module4-web-application-deployment

Heroku and the Heroku CLI:

  + https://heroku.com/
  + https://devcenter.heroku.com/articles/using-the-cli
  + https://github.com/prof-rossetti/intro-to-python/blob/master/notes/clis/heroku.md (BONUS)

Heroku PG:

  + https://devcenter.heroku.com/articles/heroku-postgresql#provisioning-heroku-postgres
  + https://devcenter.heroku.com/articles/heroku-postgres-plans#hobby-tier

Flask Migrate:

  + https://stackoverflow.com/questions/17768940/target-database-is-not-up-to-date

Database URL Format: `DATABASE_URL="postgres://USERNAME:PASSWORD@HOST:5432/DB_NAME`

Procfile:

```
web: gunicorn "web_app:create_app()"
```

## Commands

Installing production environment dependences:

```sh
pipenv install gunicorn psycopg2-binary
```

Provisioning production database:

```sh
git remote -v
heroku create
git remote -v

heroku config
heroku addons:create heroku-postgresql:hobby-dev
#> provisions a new DATABASE_URL
heroku config
```

Configuring production environment variables:

```sh
heroku config:set BASILICA_API_KEY="_____"
heroku config:set TWITTER_API_KEY="_____"
heroku config:set TWITTER_API_SECRET="______"
heroku config:set TWITTER_ACCESS_TOKEN="______"
heroku config:set TWITTER_ACCESS_TOKEN_SECRET="_____"
heroku config
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
# ... python --version
# ... python web_app/stocks_service.py
# ... exit
```

Running "detached" commands against the production server:

```sh
heroku run "python web_app/stocks_service.py"

heroku run "FLASK_APP=web_app flask db init"
heroku run "FLASK_APP=web_app flask db stamp head"
heroku run "FLASK_APP=web_app flask db migrate"
heroku run "FLASK_APP=web_app flask db upgrade"
```
