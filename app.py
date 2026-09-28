from flask import Flask, render_template, request, redirect, session
from datetime import datetime, timedelta
from bson import ObjectId
import random

from database import (
    test_connection,
    add_user,
    login_user,
    add_word,
    get_words,
    create_game,
    update_game,
    games_today,
    get_daily_report,
    get_user_report
)


app = Flask(__name__)
app.secret_key = "change-this-secret-key"


WORDS = [
    "APPLE", "HOUSE", "PLANT", "WATER", "MOUSE",
    "CHAIR", "TABLE", "CLOUD", "BREAD", "LIGHT",
    "PHONE", "TRAIN", "WORLD", "GREEN", "SMILE",
    "BEACH", "MUSIC", "BRAVE", "SWEET", "NIGHT"
]


def setup_words():
    for word in WORDS:
        add_word(word)


@app.route("/")
def home():

    if "username" not in session:
        return redirect("/login")

    if "game_id" not in session:

        if games_today(session["username"]) >= 3:
            return render_template(
                "index.html",
                guesses=[],
                message="You have already played 3 games today."
            )

        word_list = get_words()
        secret_word = random.choice(word_list)

        game_id = create_game(
            session["username"],
            secret_word
        )

        session["game_id"] = game_id
        session["secret_word"] = secret_word
        session["guesses"] = []

    return render_template(
        "index.html",
        guesses=session.get("guesses", [])
    )


@app.route("/guess", methods=["POST"])
def guess():

    if "username" not in session:
        return redirect("/login")

    word = request.form.get("guess", "")

    # Requirement: uppercase only
    if word != word.upper():
        return render_template(
            "index.html",
            guesses=session.get("guesses", []),
            error="Please enter the word in UPPERCASE."
        )

    if len(word) != 5 or not word.isalpha():
        return render_template(
            "index.html",
            guesses=session.get("guesses", []),
            error="Enter exactly 5 letters."
        )

    secret_word = session["secret_word"]

    result = []

    for i in range(5):

        if word[i] == secret_word[i]:
            result.append("green")

        elif word[i] in secret_word:
            result.append("orange")

        else:
            result.append("grey")

    guesses = session.get("guesses", [])

    guesses.append({
        "word": word,
        "result": result
    })

    session["guesses"] = guesses

    # Correct answer
    if word == secret_word:

        update_game(
            session["game_id"],
            guesses,
            won=True,
            finished=True
        )

        return render_template(
            "index.html",
            guesses=guesses,
            message="Congratulations! You won!",
            game_over=True
        )

    # Five guesses used
    if len(guesses) == 5:

        update_game(
            session["game_id"],
            guesses,
            won=False,
            finished=True
        )

        return render_template(
            "index.html",
            guesses=guesses,
            message="Better luck next time!",
            answer=secret_word,
            game_over=True
        )

    # Game continues
    update_game(
        session["game_id"],
        guesses
    )

    return render_template(
        "index.html",
        guesses=guesses
    )


@app.route("/new-game")
def new_game():

    session.pop("game_id", None)
    session.pop("secret_word", None)
    session.pop("guesses", None)

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if len(username) < 5 or len(password) < 5:
            return render_template(
                "register.html",
                error="Username and password must have at least 5 characters."
            )

        if add_user(username, password):
            return redirect("/login")

        return render_template(
            "register.html",
            error="Username already exists."
        )

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = login_user(username, password)

        if user:

            session["username"] = user["username"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect("/admin")

            return redirect("/")

        return render_template(
            "login.html",
            error="Invalid username or password."
        )

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


@app.route("/admin")
def admin():

    if session.get("role") != "admin":
        return "Access denied."

    return render_template("admin.html")


@app.route("/admin/daily", methods=["POST"])
def daily_report():

    if session.get("role") != "admin":
        return "Access denied."

    date_text = request.form["date"]

    date_start = datetime.strptime(
        date_text,
        "%Y-%m-%d"
    )

    date_end = date_start + timedelta(days=1)

    users_count, correct_count = get_daily_report(
        date_start,
        date_end
    )

    return render_template(
        "admin.html",
        daily_date=date_text,
        users_count=users_count,
        correct_count=correct_count
    )


@app.route("/admin/user", methods=["POST"])
def user_report():

    if session.get("role") != "admin":
        return "Access denied."

    username = request.form["username"]

    records = get_user_report(username)

    report = []

    for game in records:

        report.append({
            "date": game["date"].strftime("%Y-%m-%d"),
            "words_tried": len(game["guesses"]),
            "correct": game["won"]
        })

    return render_template(
        "admin.html",
        username=username,
        report=report
    )


if __name__ == "__main__":

    test_connection()
    setup_words()

    app.run(debug=True)
