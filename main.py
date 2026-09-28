from database import (
    test_connection,
    add_word
)

from users import (
    register,
    login
)

from game import play_game

from admin import (
    daily_report,
    user_report
)

from words import WORDS


def setup_words():

    for word in WORDS:
        add_word(word)


def player_menu(username):

    while True:

        print("\n=== PLAYER MENU ===")
        print("1. Play Game")
        print("2. Logout")

        choice = input("Choose: ")

        if choice == "1":
            play_game(username)

        elif choice == "2":
            break

        else:
            print("Invalid choice.")


def admin_menu():

    while True:

        print("\n=== ADMIN MENU ===")
        print("1. Daily Report")
        print("2. User Report")
        print("3. Logout")

        choice = input("Choose: ")

        if choice == "1":
            daily_report()

        elif choice == "2":
            user_report()

        elif choice == "3":
            break

        else:
            print("Invalid choice.")


def main():

    test_connection()

    setup_words()

    while True:

        print("\n====================")
        print("   GUESS THE WORD")
        print("====================")

        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose: ")

        if choice == "1":
            register()

        elif choice == "2":

            user = login()

            if user:

                username = user["username"]
                role = user["role"]

                if role == "admin":
                    admin_menu()

                else:
                    player_menu(username)

        elif choice == "3":

            print("Thank you for playing!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
