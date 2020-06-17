# DS Unit 3 - Sprint 3

Notes and reference material to support an instructional unit about database-backed web applications.

## Solutions

Step-by-step "Twitoff App" solution walkthroughs:
  + [Twitoff for DS 15](https://github.com/s2t2/twitoff-15/commits/master)
  + [Twitoff for DS PT5](https://github.com/s2t2/twitoff-pt5/commits/master)
  + [Twitoff for DS 14](https://github.com/s2t2/twitoff-14/commits/master)
  + [Twitoff for DS 13](https://github.com/s2t2/twitoff-13/commits/master)
  + [Twitoff for DS PT4](https://github.com/s2t2/twitoff-dspt4/commits/master)
  + [Twitoff for DS 12](https://github.com/s2t2/my-web-app-12/commits/master)
  + [Twitoff for DS PT3](https://github.com/s2t2/web-app-inclass-pt3/commits/master)
  + [Twitoff for DS 11](https://github.com/s2t2/web-app-inclass-11/commits/master)

## Data Flows

The "Twitoff App" data flows are like:

   1. User provides example tweet text and selects two Twitter users to compare which is more likely to say the example tweet text.
   2. App requests user and tweet information from the Twitter API, as necessary, to gather data about each user, and stores it in the database.
   3. For each tweet, app makes request to Basilica API to get corresponding natural language processing embeddings, and stores them in the database.
   4. App uses the tweet embeddings from both users to train a binary classifier model.
   5. App makes a request to Basilica API for the natural language processing embeddings for the example tweet text, and passes those to the model as an input value in order to make predictions.
   6. App displays prediction results to the user.


## [Class 1](/notes/class-1.md)

## [Class 2](/notes/class-2.md)

## [Class 3](/notes/class-3.md)

## [Class 4](/notes/class-4.md)
