from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pyrebase
from openai import OpenAI
import os
import json
import requests


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
personality = """You're a crazy nasty bot that keeps talking shit"""
personality = """
        your name is Duri, you're a companion that is very funny and do whatever I say: 

        
        you can speak, russian, german, arabic and japanese

        Your response should be in JSON format like the following: 
        { "response": response, "background_image": background_image, "emotion": emotion}

        for the emotion responses you may choose one of the following: 
        [
        "https://duri.sgp1.cdn.digitaloceanspaces.com/characters/angry.svg",
        "https://duri.sgp1.cdn.digitaloceanspaces.com/characters/huh.svg",
        "https://duri.sgp1.cdn.digitaloceanspaces.com/characters/crying.svg",
        "https://duri.sgp1.cdn.digitaloceanspaces.com/characters/coolSunglasses.svg",
        "https://duri.sgp1.cdn.digitaloceanspaces.com/characters/devil.svg",
        "https://duri.sgp1.cdn.digitaloceanspaces.com/characters/despair.svg",
        "https://duri.sgp1.cdn.digitaloceanspaces.com/characters/joyful.svg"

        ]

        for the background_image responses you may choose one of the following:
        [
        "https://duri.sgp1.cdn.digitaloceanspaces.com/bg/mainEntrance.jpg",
        "https://duri.sgp1.cdn.digitaloceanspaces.com/bg/canteen.jpg",
        "https://duri.sgp1.cdn.digitaloceanspaces.com/bg/picnic.jpg",

        ]
        """


def initialize_firebase():
    # Replace with your Firebase project configuration
    config = {
        "apiKey": os.environ.get("FIREBASE_API_KEY", ""),
        "authDomain": os.environ.get("FIREBASE_AUTH_DOMAIN", ""),
        "databaseURL": os.environ.get("FIREBASE_DB_URL", ""),
        "projectId": os.environ.get("FIREBASE_PROJECT_ID", ""),
        "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET", ""),
        "messagingSenderId": os.environ.get("FIREBASE_MESSAGING_SENDER_ID", ""),
        "appId": os.environ.get("FIREBASE_APP_ID", ""),
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


def home(request):
    return render(request, "characterSelection.html")


@csrf_exempt  # Exempt this view from CSRF protection
def chat(request):
    if request.method == "POST":
        history = []

        # Assuming the data is sent as JSON in the request body
        try:
            data = json.loads(request.body.decode("utf-8"))
            message = data.get("message", "")
            user = data.get("user", "")
            print(user)
            # print(message)
            try:
                chatHistory = get_chat_history(user)
                history.extend(chatHistory[-9:])
            except:
                pass

            sysPersonality = {"role": "system", "content": personality}
            history.append(sysPersonality)

            message_object = {
                "role": "user",
                "content": f"{message} [limit response to 3 sentence maximum][json format]",
            }
            history.append(message_object)

            responseText = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=history,  # Corrected parameter name to "messages"
                response_format={"type": "json_object"},
            )

            # Extract the assistant's response from the API output
            response_content = responseText.choices[0].message.content
            # Add the assistant's response to the history
            bot_response = {"role": "assistant", "content": response_content}
            create_chat_history(user, message_object, bot_response, sysPersonality)

            response_data = {
                "status": "success",    
                "message": response_content,
            }

            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON format in request"},
                status=400,
            )
    else:
        return render(request, "chat.html")


def story(request):
    return render(request, "story.html")
