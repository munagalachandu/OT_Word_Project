import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not set in .env")

client = MongoClient(MONGODB_URI)

db = client["guess_the_word"]

users_collection = db["users"]
words_collection = db["words"]
games_collection = db["games"]


def test_connection():
    client.admin.command("ping")
    print("MongoDB connected successfully!")


def add_user(username, password, role="player"):
    if users_collection.find_one({"username": username}):
        return False

    users_collection.insert_one({
        "username": username,
        "password": password,
        "role": role
    })

    return True


def check_user(username, password):
    user = users_collection.find_one({
        "username": username,
        "password": password
    })

    if user:
        return user

    return None


def add_word(word):
    if not words_collection.find_one({"word": word}):
        words_collection.insert_one({
            "word": word
        })


def get_words():
    documents = words_collection.find({}, {"word": 1, "_id": 0})

    return [document["word"] for document in documents]


def save_game(username, secret_word, won, guesses):
    games_collection.insert_one({
        "username": username,
        "secret_word": secret_word,
        "won": won,
        "guesses": guesses,
        "played_at": datetime.now()
    })


def games_today(username):
    start = datetime.now().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    count = games_collection.count_documents({
        "username": username,
        "played_at": {
            "$gte": start
        }
    })

    return count
