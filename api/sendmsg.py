from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, messaging
import os, json

app = Flask(__name__)

# Load Firebase credentials from environment variable
firebase_cred_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")
if not firebase_cred_json:
    raise ValueError("Missing Firebase credentials")

cred_dict = json.loads(firebase_cred_json)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

@app.route('/sendmsg', methods=['POST'])
def send_message_to_topic():
    data = request.get_json()
    topic = data['topic']
    title = data['title']
    body = data['body']

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        topic=topic,
    )

    response = messaging.send(message)
    return jsonify({"status": "Message sent", "response": response})
