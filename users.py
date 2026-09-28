from database import add_user, check_user


def valid_password(password):
    special_characters = "$%*"

    has_letter = any(char.isalpha() for char in password)
    has_number = any(char.isdigit() for char in password)
    has_special = any(
        char in special_characters
        for char in password
    )

    return (
        len(password) >= 5
        and has_letter
        and has_number
        and has_special
    )


def register():
    print("\n=== REGISTER ===")

    username = input("Enter username: ")

    if len(username) < 5:
        print("Username must have at least 5 characters.")
        return

    password = input("Enter password: ")

    if not valid_password(password):
        print("Password must contain:")
        print("- At least 5 characters")
        print("- Letters")
        print("- A number")
        print("- One of $, %, *")
        return

    if add_user(username, password):
        print("Registration successful!")
    else:
        print("Username already exists.")


def login():
    print("\n=== LOGIN ===")

    username = input("Username: ")
    password = input("Password: ")

    user = check_user(username, password)

    if user:
        print("Login successful!")
        return user

    print("Invalid username or password.")
    return None
