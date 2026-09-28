import random
from users import register, login

words = [
    "APPLE", "HOUSE", "PLANT", "WATER", "MOUSE",
    "CHAIR", "TABLE", "CLOUD", "BREAD", "LIGHT",
    "PHONE", "TRAIN", "WORLD", "GREEN", "SMILE",
    "BEACH", "MUSIC", "BRAVE", "SWEET", "NIGHT"
]


def play_game(username):
    secret_word = random.choice(words)

    print("\n=== GUESS THE WORD ===")
    print("Player:", username)
    print("You have 5 attempts.")

    for attempt in range(1, 6):
        guess = input(f"\nAttempt {attempt}/5: ").upper()

        if len(guess) != 5 or not guess.isalpha():
            print("Enter exactly 5 letters.")
            continue

        if guess == secret_word:
            print("Congratulations! You won!")
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


while True:
    print("\n1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        register()

    elif choice == "2":
        username = login()

        if username:
            play_game(username)

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")
