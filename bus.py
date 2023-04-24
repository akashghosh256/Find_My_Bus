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
    with open("C:\\Users\\HP\\Downloads\\BUS_ROUTES- Sheet1.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        # Create a reference to the 'buses' node in the database
        buses_ref = db.reference('buses')
        # Loop through each row in the CSV file and insert the data into the database
        for row in reader:
            # Use the Bus ID as the key for the child node
            bus_id = row['bus_id']
            # Create a reference to the child node using the bus ID
            bus_ref = buses_ref.child(bus_id)
            # Set the data for the child node
            bus_ref.set({
                'bus_no': row['bus_no'],
                'origin': row['origin'],
                'destination': row['destination'],
                'origin_lat': row['origin_lati'],
                'origin_long': row['origin_longi'],
                'dest_lat': row['dest_lati'],
                'dest_long': row['dest_longi'],
                'route' : row['route']
            })
        return 'Data inserted successfully!'
    
# Define the endpoint to update the data
@app.route('/updatedata')
def updatedata():
    # Load the CSV file
    with open("C:\\Users\\HP\\Downloads\\BUS_ROUTES- Sheet1.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        # Create a reference to the 'buses' node in the database
        buses_ref = db.reference('buses')
        # Loop through each row in the CSV file and update the route field of the corresponding child node
        for row in reader:
            # Use the Bus ID as the key for the child node
            bus_id = row['bus_id']
            # Create a reference to the child node using the bus ID
            bus_ref = buses_ref.child(bus_id)
            # Update the 'route' field of the child node
            bus_ref.update({'route': row['route']})
        return 'Data updated successfully!'
    
@app.route('/departure')
def departure():
    #Loading the csv file
    with open("C:\\Users\\HP\\Downloads\\BUS_DEPART - Sheet1.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        # Create a reference to the 'departure' node in the database
        departure_ref = db.reference('departure')
        #Looping through each row in the csv file and inserting the data in the database
        for row in reader:
            # Use the departure value as the key for the child node
            departure_value = row['departure']
            #Creating a reference to the child node
            new_departure_ref = departure_ref.child(departure_value)
        
            # Set the data for the child node
            new_departure_ref.set(True)

        return 'Departures added successfully!'

@app.route('/arrival')
def arrival():
    #Loading the csv file
    with open("C:\\Users\\HP\\Downloads\\BUS_ARRIVE - Sheet1.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        # Create a reference to the 'arrival' node in the database
        arrival_ref = db.reference('arrival')
        #Looping through each row in the csv file and inserting the data in the database
        for row in reader:
            # Use the departure value as the key for the child node
            arrival_value = row['arrival']
            #Creating a reference to the child node
            new_arrival_ref = arrival_ref.child(arrival_value)
        
            # Set the data for the child node
            new_arrival_ref.set(True)

        return 'Arrivals added successfully!'

@app.route('/creating_routes')
def creating_routes():

   #Creating a reference to the database
    buses_ref = db.reference('buses')
    routes_ref = db.reference('routes')

    # Retrieve the data from the buses node
    buses_data = buses_ref.get()

    # Initialize an empty dictionary to store the routes
    routes_dict = {}

    # Loop through each bus and add it to the appropriate route
    for bus_id, bus_data in buses_data.items():
        origin = bus_data['origin']
        destination = bus_data['destination']
    
        route_key = f"{origin}-{destination}"
        if route_key in routes_dict:
            routes_dict[route_key].append(bus_id)
        else:
            routes_dict[route_key] = [bus_id]

    # Write the routes to the routes node
    routes_ref.set(routes_dict)
    return "Routes added successfully!"




@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')



