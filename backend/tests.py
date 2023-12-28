import pyrebase
def initialize_firebase():
    # Replace with your Firebase project configuration
    config = {
        "apiKey": "AIzaSyBLv1DiRB6egmpaoIKfjODXZF5fYheQKIM",
        "authDomain": "realtimedatabasetest-f226a.firebaseapp.com",
        "databaseURL": "https://realtimedatabasetest-f226a-default-rtdb.asia-southeast1.firebasedatabase.app",
        "projectId": "realtimedatabasetest-f226a",
        "storageBucket": "realtimedatabasetest-f226a.appspot.com",
        "messagingSenderId": "348704796176",
        "appId": "1:348704796176:web:b19a37e276fd097a2ce495",
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    return db


firebaseDB = initialize_firebase()


def create_chat_history(user, user_msg, bot_response, personality):
    # Initialize Firebase
    db = firebaseDB

    # Check if the 'Chathistory' table exists, if not, create it
    if not db.child("Chathistory").shallow().get().val():
        db.child("Chathistory").set({})

    # Check if the user exists in the 'Chathistory' table
    user_records = db.child("Chathistory").child(user).get().val()

    if user_records:
        # User exists, append a new record
        user_records.append(personality)
        user_records.append(user_msg)
        user_records.append(bot_response)
        db.child("Chathistory").child(user).set(user_records)
    else:
        # User doesn't exist, create a new record
        db.child("Chathistory").child(user).set(
            [
                 personality,
                 user_msg,
                 bot_response
            ]
        )


def get_chat_history(user):
    # Initialize Firebase
    db = firebaseDB

    # Check if the 'Chathistory' table exists
    if not db.child("Chathistory").shallow().get().val():
        return []

    # Get the user's chat history
    user_records = db.child("Chathistory").child(user).get().val()

    if user_records:
        return user_records
    else:
        return []



# Example Usage:
# create_chat_history("", "Hello", "Hi there!", "crazy bot")

user_history = get_chat_history("Shami")
[print(i) for i in user_history]
