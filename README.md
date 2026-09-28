# OT_Word_Project

# Guess the Word Game

 A simple **5-letter word guessing game** built using Python, Flask, HTML/CSS, and MongoDB.

 ## Features

 - User registration and login
- Player and Admin users
- Random 5-letter word from MongoDB
- Maximum 5 guesses per game
- Green = correct letter and position
- Orange = correct letter, wrong position
- Grey = letter not in the word
- Previous guesses remain visible
- Maximum 3 games per user per day
- Game results saved in MongoDB
- Admin daily and user reports

 ## Technologies

 - Python
- Flask
- HTML/CSS
- MongoDB Atlas
- PyMongo

 ## How to Run

 Install the required packages:

```
pip install -r requirements.txt
```

 Create a `.env` file:

```
MONGODB_URI=your_mongodb_connection_string
```

 Then run:

```
python app.py
```

 Open the Flask URL shown in the terminal.

 ## Project Structure

```
OT_Word_Project/
│
├── app.py
├── database.py
├── users.py
├── game.py
├── admin.py
├── words.py
├── requirements.txt
├── .env
│
└── templates/
    ├── index.html
    ├── login.html
    ├── register.html
    └── admin.html
```

 ## Game Flow

```
Register/Login
      ↓
   Start Game
      ↓
 Random Word
      ↓
 Enter 5-letter Guess
      ↓
 Green / Orange / Grey
      ↓
  Correct? ── No ──→ Guess Again
      │
     Yes
      ↓
 Congratulations
      ↓
     Game Ends
```
