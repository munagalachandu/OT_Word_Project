import random

words = [
    "APPLE", "HOUSE", "PLANT", "WATER", "MOUSE",
    "CHAIR", "TABLE", "CLOUD", "BREAD", "LIGHT",
    "PHONE", "TRAIN", "WORLD", "GREEN", "SMILE",
    "BEACH", "MUSIC", "BRAVE", "SWEET", "NIGHT"
]

secret_word = random.choice(words)

print("=== GUESS THE WORD ===")
print("Guess the 5-letter word!")
print("You have 5 attempts.\n")

for attempt in range(1, 6):
    guess = input(f"Attempt {attempt}/5 - Enter your guess: ").upper()

    if len(guess) != 5:
        print("Please enter exactly 5 letters.")
        continue

    if guess == secret_word:
        print("Congratulations! You guessed the word!")
        break

    # Show letter feedback
    result = ""

    for i in range(5):
        if guess[i] == secret_word[i]:
            result += "🟩"
        elif guess[i] in secret_word:
            result += "🟧"
        else:
            result += "⬜"

    print(result)

else:
    print("Better luck next time!")
    print("The word was:", secret_word)
