from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

serviceAccKey = os.getenv("FIREBASE_KEY")
flaskApp = os.getenv("FLASK_APP")
flaskDebug = os.getenv("FLASK_DEBUG")

# Fetch the service account key JSON file contents
cred = credentials.Certificate(serviceAccKey)

# Initialize the app with a custom auth variable, limiting the server's access
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://findmybus-1bccf-default-rtdb.firebaseio.com/',
    'databaseAuthVariableOverride': {
        'uid': 'my-service-worker'
    }
})

# Get a database reference
ref = db.reference('restricted-access/data')

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')



