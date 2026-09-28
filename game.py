import random

from database import (
    get_words,
    save_game,
    games_today
)


def play_game(username):

    if games_today(username) >= 3:
        print("You have already played 3 games today.")
        return

    words = get_words()

    if not words:
        print("No words available.")
        return

    secret_word = random.choice(words)

    print("\n=== GUESS THE WORD ===")
    print("Guess the 5-letter word.")
    print("You have 5 attempts.")

    for attempt in range(1, 6):

        guess = input(
            f"Attempt {attempt}/5: "
        ).upper()

        if len(guess) != 5 or not guess.isalpha():
            print("Please enter exactly 5 letters.")
            continue

        if guess == secret_word:
            print("Congratulations! You won!")

            save_game(
                username,
                secret_word,
                True,
                attempt
            )

            return

        result = ""

        for i in range(5):

            if guess[i] == secret_word[i]:
                result += "🟩"

            elif guess[i] in secret_word:
                result += "🟧"

            else:
                result += "⬜"

        print(result)

    print("\nBetter luck next time!")
    print("The word was:", secret_word)

    save_game(
        username,
        secret_word,
        False,
        5
    )
