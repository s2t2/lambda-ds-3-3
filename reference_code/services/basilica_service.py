import os
from dotenv import load_dotenv
import basilica

load_dotenv()

API_KEY = os.getenv("BASILICA_API_KEY", default="OOPS")

connection = basilica.Connection(API_KEY)

embeddings = connection.embed_sentences(["Hello world!", "How are you?"])

for embed in embeddings:
    print(embed)

# todo: further comparison!
