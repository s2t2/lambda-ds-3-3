

# Class 3

Lambda Materials:

  + https://learn.lambdaschool.com/ds/module/recZOXl2H7Bbd1LMK/
  + https://github.com/LambdaSchool/DS-Unit-3-Sprint-3-Productization-and-Cloud/tree/master/module3-adding-data-science-to-a-web-application

Other Materials:

  + https://towardsdatascience.com/create-an-api-to-deploy-machine-learning-models-using-flask-and-heroku-67a011800c50

Installing Package Dependencies:

```sh
pipenv install scikit-learn
```

## Part I

Implementing admin routes to help us reset our database:

```py
# web_app/routes/admin_routes.py

from flask import Blueprint, jsonify, request, render_template, flash, redirect

from web_app.models import db

admin_routes = Blueprint("admin_routes", __name__)

@admin_routes.route("/admin/db/reset")
def reset_db():
    print(type(db))
    db.drop_all()
    db.create_all()
    return jsonify({"message": "DB RESET OK"})

@admin_routes.route("/admin/db/seed")
def seed_db():
    print(type(db))
    # TODO: refactor the existing user and tweet storage logic from our twitter_routes into a re-usable function
    # ... so we can "seed" our database with some example users and tweets
    # ... to ensure that it is ready to make predictions later
    
    # FYI: you might run into Timeout errors, which you'll need to think about how to avoid

    return jsonify({"message": "DB SEEDED OK (TODO)"})
```

> FYI: you could implement your own API Key authentication to protect these admin routes, or consider using the [`Flask-BasicAuth` package](https://flask-basicauth.readthedocs.io/en/latest/)

Updating existing routing and views to facilitate the storage of Tweets and Users, and the desired application flow.

```py
# web_app/routes/twitter_routes.py

# ...

@twitter_routes.route("/users")
@twitter_routes.route("/users.json")
def list_users():
    db_users = User.query.all()
    users_response = parse_records(db_users)
    return jsonify(users_response)

@twitter_routes.route("/users/<screen_name>")
def get_user(screen_name=None):
    print(screen_name)

    # ...

    return render_template("user.html", user=db_user, tweets=statuses) # tweets=db_tweets

```

```html
<!-- web_app/templates/user.html -->

{% extends "layout.html" %}

{% block content %}
    <h2>Twitter User: {{ user.screen_name }} </h2>

    <p>Name: {{ user.name }}</p>
    <p>Location: {{ user.location }}</p>
    <p>Followers: {{ user.followers_count }}</p>

    {% if tweets %}
        <ul>
        {% for status in tweets %}
            <li>{{ status.full_text }}</li>
        {% endfor %}
        </ul>

    {% else %}
        <p>No tweets found.</p>
    {% endif %}

{% endblock %}
```

> CHALLENGE: Can you display the tweets in a twitter bootstrap table, instead of a list?

## Part II

As you are working with your own predictive models (like the iris example below), make sure you know how to [use pickle to save the model to a file](https://github.com/s2t2/titanic-survival-py/blob/3a5827ad5ce57ebaf12b21b31dfd38494b28bff6/app/classifier.py#L165-L169), and also later [reconstitute the model from the file](https://github.com/s2t2/titanic-survival-py/blob/3a5827ad5ce57ebaf12b21b31dfd38494b28bff6/app/classifier.py#L181-L188).

> FYI: the purpose of the code below is not to train the best model, but rather to show an example of how to use a model

```py
# web_app/classifier.py

import os
import pickle

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression # for example

MODEL_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "models", "latest_model.pkl")

def train_and_save_model():
    print("TRAINING THE MODEL...")
    X, y = load_iris(return_X_y=True)
    #print(type(X), X.shape) #> <class 'numpy.ndarray'> (150, 4)
    #print(type(y), y.shape) #> <class 'numpy.ndarray'> (150,)
    classifier = LogisticRegression() # for example
    classifier.fit(X, y)

    print("SAVING THE MODEL...")
    with open(MODEL_FILEPATH, "wb") as model_file:
        pickle.dump(classifier, model_file)

    return classifier

def load_model():
    print("LOADING THE MODEL...")
    with open(MODEL_FILEPATH, "rb") as model_file:
        saved_model = pickle.load(model_file)
    return saved_model

if __name__ == "__main__":

    train_and_save_model()

    clf = load_model()
    print("CLASSIFIER:", clf)

    X, y = load_iris(return_X_y=True) # just to have some data to use when predicting
    inputs = X[:2, :]
    print(type(inputs), inputs)

    result = clf.predict(inputs)
    print("RESULT:", result)
```

Integrating the model into our app (just an example):

```py
# web_app/routes/stats_routes.py

from flask import Blueprint, request, jsonify, render_template
from sklearn.datasets import load_iris # just to have some data to use when predicting

from web_app.classifier import load_model

stats_routes = Blueprint("stats_routes", __name__)

@stats_routes.route("/iris")
def iris():
    model = load_model()
    X, y = load_iris(return_X_y=True) # just to have some data to use when predicting
    result = model.predict(X[:2, :])
    return str(result)
```

What to do when a model file is too large for GitHub / Heroku? (BONUS):

 + Ask the person who created the model to "reduce dimensionality" so the model file will be smaller, may require prediction accuracy trade-offs
 + Store the model remotely:
    + https://aws.amazon.com/s3/
    + https://console.cloud.google.com/storage/browser/brexitmeter-bucket/weights?authuser=1&project=brexitmeter

## Part III

Training our own model...

> FYI: the purpose of the code below is not to train the best model, but rather to show an example of how to use a model

> FYI: ideally, we'll pre-train our model and save it as a pickled file, and then load it from file in order to make predictions. However given the specific nature of this application and needing a separate model for each combination of two users, we'll do our model training "live"...

```py
# web_app/routes/stats_routes.py

from flask import Blueprint, request, jsonify, render_template

from sklearn.linear_model import LogisticRegression # for example

from web_app.models import User, Tweet
from web_app.services.basilica_service import basilica_api_client

stats_routes = Blueprint("stats_routes", __name__)

@stats_routes.route("/predict", methods=["POST"])
def predict():
    print("PREDICT ROUTE...")
    print("FORM DATA:", dict(request.form))
    #> {'screen_name_a': 'elonmusk', 'screen_name_b': 's2t2', 'tweet_text': 'Example tweet text here'}
    screen_name_a = request.form["screen_name_a"]
    screen_name_b = request.form["screen_name_b"]
    tweet_text = request.form["tweet_text"]

    print("-----------------")
    print("FETCHING TWEETS FROM THE DATABASE...")
    # todo: wrap in a try block in case the user's don't exist in the database
    user_a = User.query.filter(User.screen_name == screen_name_a).one()
    user_b = User.query.filter(User.screen_name == screen_name_b).one()
    user_a_tweets = user_a.tweets
    user_b_tweets = user_b.tweets
    #user_a_embeddings = [tweet.embedding for tweet in user_a_tweets]
    #user_b_embeddings = [tweet.embedding for tweet in user_b_tweets]
    print("USER A", user_a.screen_name, len(user_a.tweets))
    print("USER B", user_b.screen_name, len(user_b.tweets))

    print("-----------------")
    print("TRAINING THE MODEL...")
    embeddings = []
    labels = []
    for tweet in user_a_tweets:
        labels.append(user_a.screen_name)
        embeddings.append(tweet.embedding)

    for tweet in user_b_tweets:
        labels.append(user_b.screen_name)
        embeddings.append(tweet.embedding)

    classifier = LogisticRegression() # for example
    classifier.fit(embeddings, labels)

    print("-----------------")
    print("MAKING A PREDICTION...")
    #result_a = classifier.predict([user_a_tweets[0].embedding])
    #result_b = classifier.predict([user_b_tweets[0].embedding])

    basilica_api = basilica_api_client()
    example_embedding = basilica_api.embed_sentence(tweet_text)
    result = classifier.predict([example_embedding])
    #breakpoint()

    #return jsonify({"message": "RESULTS", "most_likely": result[0]})
    return render_template("results.html",
        screen_name_a=screen_name_a,
        screen_name_b=screen_name_b,
        tweet_text=tweet_text,
        screen_name_most_likely= result[0]
    )
```

> CHALLENGE: How can you improve the model's predictive accuracy? How many tweets from each user are being used to train the model, and is there parity there?

```html
<!-- web_app/templates/results.html -->

{% extends "layout.html" %}

{% block content %}
    <h2>Results!</h2>

    <p>Between '@{{ screen_name_a }}' and '@{{ screen_name_b }}',
        the user who is most likely to say '{{ tweet_text }}'
        is '@{{ screen_name_most_likely }}'
    </p>
{% endblock %}
```

```html
<!-- web_app/templates/results.html -->


{% extends "layout.html" %}

{% block content %}
    <h2>Prediction Time</h2>

    <p>Use the form below to predict which user is more likely to say a given tweet...</p>

    <form action="/predict" method="POST">

        <label>Twitter User A:</label>
        <select name="screen_name_a">
            <option value="elonmusk" selected="true">@elonmusk</option>
            <option value="justinbieber">@justinbieber</option>
            <option value="s2t2">@s2t2</option>
        </select>
        <br>

        <label>Twitter User B:</label>
        <select name="screen_name_b">
            <option value="elonmusk">@elonmusk</option>
            <option value="justinbieber" selected="true">@justinbieber</option>
            <option value="s2t2">@s2t2</option>
          </select>
        <br>

        <label>Tweet Text:</label>
        <input type="text" name="tweet_text" placeholder="Tesla Model S production facility is great" value="Tesla Model S production facility is great">
        <br>

        <button>Submit</button>
    </form>
{% endblock %}
```

> CHALLENGE: Instead of hard-coding the drop-down menu's options, can you revise this last jinja template to loop through all existing users in the database to populate the options?
