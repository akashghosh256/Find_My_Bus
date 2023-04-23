from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
import os
import csv 

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

serviceAccKey = os.getenv("FIREBASE_KEY")
flaskApp = os.getenv("FLASK_APP")
flaskDebug = os.getenv("FLASK_DEBUG")

# Fetch the service account key JSON file contents
cred = credentials.Certificate('serviceAccountKey.json')

# Initialize the app with a custom auth variable, limiting the server's access
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://findmybus-1bccf-default-rtdb.firebaseio.com/',
    'databaseAuthVariableOverride': {
        'uid': 'my-service-worker'
    }
})

# Get a database reference
# ref = db.reference('restricted-access/data')

# Define the endpoint to insert the data
@app.route('/insertdata')
def insertdata():
    # Load the CSV file
    with open('path/to/file.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        # Create a reference to the 'buses' node in the database
        buses_ref = db.reference('buses')
        # Loop through each row in the CSV file and insert the data into the database
        for row in reader:
            # Use the Bus ID as the key for the child node
            bus_id = row['Bus id']
            # Create a reference to the child node using the bus ID
            bus_ref = buses_ref.child(bus_id)
            # Set the data for the child node
            bus_ref.set({
                'bus_no': row['bus no'],
                'origin': row['origin'],
                'destination': row['destination'],
                'origin_lat': row['origin_lat'],
                'origin_long': row['origin_long'],
                'dest_lat': row['dest_lat'],
                'dest_long': row['dest_long']
            })
        return 'Data inserted successfully!'

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')



