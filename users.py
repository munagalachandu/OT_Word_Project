users = {}


def register():
    print("\n=== REGISTER ===")

    username = input("Enter username: ")

    if len(username) < 5:
        print("Username must have at least 5 characters.")
        return

    if username in users:
        print("Username already exists.")
        return

    password = input("Enter password: ")

    if len(password) < 5:
        print("Password must have at least 5 characters.")
        return

    users[username] = password
    print("Registration successful!")


def login():
    print("\n=== LOGIN ===")

    username = input("Username: ")
    password = input("Password: ")

    if username in users and users[username] == password:
        print("Login successful!")
        return username

    print("Invalid username or password.")
    return None
