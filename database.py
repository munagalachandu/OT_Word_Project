import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))

db = client["guess_the_word"]

users = db["users"]
words = db["words"]
games = db["games"]


def test_connection():
    client.admin.command("ping")
    print("MongoDB connected!")


def add_user(username, password, role="player"):
    if users.find_one({"username": username}):
        return False

    users.insert_one({
        "username": username,
        "password": password,
        "role": role
    })

    return True


def login_user(username, password):
    return users.find_one({
        "username": username,
        "password": password
    })


def add_word(word):
    if not words.find_one({"word": word}):
        words.insert_one({"word": word})


def get_words():
    return [
        item["word"]
        for item in words.find({}, {"word": 1, "_id": 0})
    ]


def create_game(username, secret_word):
    game = {
        "username": username,
        "secret_word": secret_word,
        "guesses": [],
        "won": False,
        "finished": False,
        "date": datetime.now()
    }

    result = games.insert_one(game)

    return str(result.inserted_id)


def update_game(game_id, guesses, won=False, finished=False):
    from bson import ObjectId

    games.update_one(
        {"_id": ObjectId(game_id)},
        {
            "$set": {
                "guesses": guesses,
                "won": won,
                "finished": finished
            }
        }
    )


def games_today(username):
    start = datetime.now().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    return games.count_documents({
        "username": username,
        "date": {"$gte": start}
    })


def get_daily_report(date_start, date_end):
    user_count = len(
        games.distinct(
            "username",
            {
                "date": {
                    "$gte": date_start,
                    "$lt": date_end
                }
            }
        )
    )

    correct_guesses = games.count_documents({
        "date": {
            "$gte": date_start,
            "$lt": date_end
        },
        "won": True
    })

    return user_count, correct_guesses


def get_user_report(username):
    return games.find(
        {"username": username}
    ).sort("date", 1)
