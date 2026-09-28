from datetime import datetime, timedelta

from database import games_collection


def daily_report():

    date_text = input(
        "Enter date (YYYY-MM-DD): "
    )

    try:
        date = datetime.strptime(
            date_text,
            "%Y-%m-%d"
        )

    except ValueError:
        print("Invalid date format.")
        return

    next_day = date + timedelta(days=1)

    query = {
        "played_at": {
            "$gte": date,
            "$lt": next_day
        }
    }

    users = games_collection.distinct(
        "username",
        query
    )

    correct = games_collection.count_documents({
        **query,
        "won": True
    })

    print("\n=== DAILY REPORT ===")
    print("Date:", date_text)
    print("Number of users:", len(users))
    print("Correct guesses:", correct)


def user_report():

    username = input(
        "Enter username: "
    )

    games = games_collection.find({
        "username": username
    }).sort("played_at", 1)

    print("\n=== USER REPORT ===")

    found = False

    for game in games:

        found = True

        date = game["played_at"].strftime(
            "%Y-%m-%d"
        )

        print(
            "Date:",
            date,
            "| Guesses:",
            game["guesses"],
            "| Correct:",
            game["won"]
        )

    if not found:
        print("No games found.")
