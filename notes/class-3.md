

# Class 3

Lambda Materials:

  + https://learn.lambdaschool.com/ds/module/recZOXl2H7Bbd1LMK/
  + https://github.com/LambdaSchool/DS-Unit-3-Sprint-3-Productization-and-Cloud/tree/master/module3-adding-data-science-to-a-web-application

Other Materials:

  + https://towardsdatascience.com/create-an-api-to-deploy-machine-learning-models-using-flask-and-heroku-67a011800c50

What to do when a model file is too large for GitHub / Heroku? (BONUS):

  + Ask the person who created the model to "reduce dimensionality" so the model file will be smaller, may require prediction accuracy trade-offs
  + Store the model remotely:
    + https://aws.amazon.com/s3/
    + https://console.cloud.google.com/storage/browser/brexitmeter-bucket/weights?authuser=1&project=brexitmeter

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

@admin_routes.route("/admin/reset")
def reset_db():
    print(type(db))
    db.drop_all()
    db.create_all()
    return jsonify({"message": "DB RESET OK"})
```


## Part II

Updating existing routing and views to facilitate the storage of Tweets and Users, and the desired application flow.

## Part III

Integrating with an example predictive model (Iris).

```py
# web_app/routes/stats_routes.py

from flask import Blueprint, request, jsonify, render_template

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression # for example

stats_routes = Blueprint("stats_routes", __name__)

@stats_routes.route("/iris")
def iris():
    X, y = load_iris(return_X_y=True)
    classifier = LogisticRegression(
        random_state=0,
        solver="lbfgs",
        multi_class="multinomial"
    ).fit(X, y)

    result = classifier.predict(X[:2, :])
    return str(result)
```

Training our own model...

> FYI: the purpose of the code below is not to train the best model, but rather to show an example of how to use a model

> FYI: ideally, we'll pre-train our model and save it as a pickled file, and then load it from file in order to make predictions. However given the specific nature of this application and needing a separate model for each combination of two users, we'll do our model training "live"...

```py
# web_app/routes/stats_routes.py

from flask import Blueprint, request, jsonify, render_template

from sklearn.linear_model import LogisticRegression # for example

from web_app.models import User, Tweet
from web_app.basilica_service import basilica_api_client

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

    classifier = LogisticRegression()
    classifier.fit(embeddings, labels)

    print("-----------------")
    print("MAKING A PREDICTION...")
    #result_a = classifier.predict([user_a_tweets[0].embedding])
    #result_b = classifier.predict([user_b_tweets[0].embedding])

    example_embedding = basilica_api_client.embed_sentence(tweet_text)
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

Instead of hard-coding the drop-down menu's options, can you revise this last jinja template to loop through all existing users in the database to populate the options?
