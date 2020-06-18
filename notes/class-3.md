

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

## Part 0 - Admin Routes and Authentication (BONUS)

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

> FYI: you could implement your own API Key authentication to protect these admin routes (see example below), or consider using the [`Flask-BasicAuth` package](https://flask-basicauth.readthedocs.io/en/latest/)

Example API Key Authentication:

```py
# ...

API_KEY = "abc123" # TODO: set as secret env var

# GET /admin/db/reset?api_key=abc123
@admin_routes.route("/admin/db/reset")
def reset_db():
    print("URL PARMS", dict(request.args))

    if "api_key" in dict(request.args) and request.args["api_key"] == API_KEY:
        print(type(db))
        db.drop_all()
        db.create_all()
        return jsonify({"message": "DB RESET OK"})
    else:
        flash("OOPS Permission Denied", "danger")
        return redirect("/users")
```


## Part I - Saving and Loading Pre-trained Models

  + https://docs.python.org/3/library/pickle.html
  
As you are working with your own predictive models (like the iris example below), make sure you know how to [use pickle to save the model to a file](https://github.com/s2t2/titanic-survival-py/blob/3a5827ad5ce57ebaf12b21b31dfd38494b28bff6/app/classifier.py#L165-L169), and also later [reconstitute the model from the file](https://github.com/s2t2/titanic-survival-py/blob/3a5827ad5ce57ebaf12b21b31dfd38494b28bff6/app/classifier.py#L181-L188).

> FYI: the purpose of the code below is not to train the best model, but rather to show an example of how to use a model

```py
# web_app/iris_classifier.py

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

from web_app.iris_classifier import load_model

stats_routes = Blueprint("stats_routes", __name__)

@stats_routes.route("/iris")
def iris():
    model = load_model()
    X, y = load_iris(return_X_y=True) # just to have some data to use when predicting
    result = model.predict(X[:2, :])
    return str(result)
```

What to do when a model file is too large for GitHub / Heroku?

 + A) Ask the person who created the model to "reduce dimensionality" so the model file will be smaller, may require prediction accuracy trade-offs
 + B) Store the model remotely:
    + https://aws.amazon.com/s3/
    + https://console.cloud.google.com/storage/browser/brexitmeter-bucket/weights?authuser=1&project=brexitmeter

## Part II - Training Models On the Fly

Training our own model...

> FYI: the purpose of the code below is not to train the best model, but rather to show an example of how to use a model

> FYI: ideally, we'll pre-train our model and save it as a pickled file, and then load it from file in order to make predictions. However given we'll need a separate model for each combination of two users, and given the training time is negligible, we'll do our model training "live"...

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
   
    #TODO

    print("-----------------")
    print("TRAINING THE MODEL...")
    
    classifier = LogisticRegression()
    # TODO: classifier.fit(___________, ___________)

    print("-----------------")
    print("MAKING A PREDICTION...")

    # TODO
    
    return render_template("results.html",
        screen_name_a=screen_name_a,
        screen_name_b=screen_name_b,
        tweet_text=tweet_text,
        screen_name_most_likely="TODO" 
    )
```

> CHALLENGE: How can you improve the model's predictive accuracy? How many tweets from each user are being used to train the model, and is there parity there?

```html
<!-- web_app/templates/prediction_results.html -->

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
<!-- web_app/templates/prediction_form.html -->


{% extends "layout.html" %}

{% block content %}
    <h2>Prediction Time</h2>

    <p>Use the form below to predict which user is more likely to say a given tweet...</p>

    <form action="/predict" method="POST">

        <!-- TODO: Instead of hard-coding these drop-down menu options, dynamically populate them based on user records from the database -->
        <label>Twitter User A:</label>
        <select name="screen_name_a">
            <option value="elonmusk" selected="true">@elonmusk</option>
            <option value="justinbieber">@justinbieber</option>
            <option value="s2t2">@s2t2</option>
        </select>
        <br>

        <!-- TODO: Instead of hard-coding these drop-down menu options, dynamically populate them based on user records from the database -->
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

> CHALLENGE / TODO: Instead of hard-coding the drop-down menu's options, can you revise this last jinja template to loop through all existing users in the database to populate the options?









