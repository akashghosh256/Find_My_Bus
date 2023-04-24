from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
import os
import csv 

load_dotenv()  # Loading environment variables from .env file

app = Flask(__name__)

flaskApp = os.getenv("FLASK_APP")
flaskDebug = os.getenv("FLASK_DEBUG")

# Fetching the service account key JSON file contents
cred = credentials.Certificate('serviceAccountKey.json')

# Initializing the app with a custom auth variable, limiting the server's access
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://findmybus-1bccf-default-rtdb.firebaseio.com/',
    'databaseAuthVariableOverride': {
        'uid': 'my-service-worker'
    }
})


# Defining the endpoint to insert the data
@app.route('/insertdata')
def insertdata():
    # Loading the CSV file
    with open("C:\\Users\\HP\\Downloads\\BUS_ROUTES - Sheet1.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        # Creating a reference to the 'buses' node in the database
        buses_ref = db.reference('buses')
        # Skipping the first row/header
        next(reader)
        # Looping through each row in the CSV file and insert the data into the database
        for row in reader:
            # Using the Bus ID as the key for the child node
            bus_id = row['bus_id']
            # Creating a reference to the child node using the bus ID
            bus_ref = buses_ref.child(bus_id)
            # Creating a dictionary to insert the child node
            bus_data = {
                'bus_id': row['bus_id'],
                'bus_no': row['bus_no'],
                'origin': row['origin'],
                'destination': row['destination'],
                'origin_lat': row['origin_lati'],
                'origin_long': row['origin_longi'],
                'dest_lat': row['dest_lati'],
                'dest_long': row['dest_longi'],
                'route' : row['route']
            }
            # Setting the data for the child node
            bus_ref.set(bus_data)
        return 'Data inserted successfully!'
    
# Defining the endpoint to update the data
# @app.route('/updatedata')
# def updatedata():
#     # Loading the CSV file
#     with open("C:\\Users\\HP\\Downloads\\BUS_ROUTES - Sheet1.csv") as csvfile:
#         reader = csv.DictReader(csvfile)
#         # Creating a reference to the 'buses' node in the database
#         buses_ref = db.reference('buses')
#         # Looping through each row in the CSV file and updating the route field of the corresponding child node
#         for row in reader:
#             # Using the Bus ID as the key for the child node
#             bus_id = row['bus_id']
#             # Creating a reference to the child node using the bus ID
#             bus_ref = buses_ref.child(bus_id)
#             # Updating the 'route' field of the child node
#             bus_ref.update({'bus_id': row['bus_id']})
#         return 'Data updated successfully!'
    
@app.route('/departure')
def departure():
    #Loading the csv file
    with open("C:\\Users\\HP\\Downloads\\BUS_DEPART - Sheet1.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        # Creating a reference to the 'departure' node in the database
        departure_ref = db.reference('departure')
        #Looping through each row in the csv file and inserting the data in the database
        for row in reader:
            # Using the departure value as the key for the child node
            departure_value = row['departure']
            #Creating a reference to the child node
            new_departure_ref = departure_ref.child(departure_value)
        
            # Setting the data for the child node
            new_departure_ref.set(True)

        return 'Departures added successfully!'

@app.route('/arrival')
def arrival():
    #Loading the csv file
    with open("C:\\Users\\HP\\Downloads\\BUS_ARRIVE - Sheet1.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        # Creating a reference to the 'arrival' node in the database
        arrival_ref = db.reference('arrival')
        #Looping through each row in the csv file and inserting the data in the database
        for row in reader:
            # Using the departure value as the key for the child node
            arrival_value = row['arrival']
            #Creating a reference to the child node
            new_arrival_ref = arrival_ref.child(arrival_value)
        
            # Setting the data for the child node
            new_arrival_ref.set(True)

        return 'Arrivals added successfully!'

@app.route('/creating_routes')
def creating_routes():

   #Creating a reference to the database
    buses_ref = db.reference('buses')
    routes_ref = db.reference('routes')

    # Retrieve the data from the buses node
    buses_data = buses_ref.get()
    #Filtering out the null values
    buses_data = [bus for bus in buses_data if bus is not None]
    #print(type(buses_data))
    
    #Storing the buses_data in a dictionary
    buses_dict = {bus['bus_id']: bus for bus in buses_data}

    # Initializing an empty dictionary to store the routes
    routes_dict = {}

    # Looping through each bus and adding it to the appropriate route
    for bus_id, bus_data in buses_dict.items():
        origin = bus_data['origin']
        destination = bus_data['destination']
        route_key = f"{origin}-{destination}"
        if route_key in routes_dict:
            routes_dict[route_key].append(bus_id)
        else:
            routes_dict[route_key] = [bus_id]

    # Writing the routes to the routes node
    routes_ref.set(routes_dict)
    return "Routes added successfully!"

@app.route("/getOriDest")
def getOriDest():
    # Creating a reference to the buses node in the database
    buses_ref = db.reference('buses')

    # Retrieving the data from the buses node
    buses_data = buses_ref.get()
    #Filtering out the null values
    buses_data = [bus for bus in buses_data if bus is not None]

    #Storing the buses_data in a dictionary
    buses_dict = {bus['bus_id']: bus for bus in buses_data}

    # Initializing empty sets for storing unique origin and destination values
    unique_origins = set()
    unique_destinations = set()

    # Looping through each bus and adding its origin and destination to the respective sets
    for bus_id, bus_data in buses_dict.items():
        unique_origins.add(bus_data['origin'])
        unique_destinations.add(bus_data['destination'])

    # Counting the number of unique origin and destination values
    num_origins = len(unique_origins)
    num_destinations = len(unique_destinations)

    # Returning the unique origin and destination sets as a response to the client
    return f"Unique origins: {unique_origins}, Unique destinations: {unique_destinations}" + f"Unique Origin Count: {num_origins}, Unique destinations count: {num_destinations}"



@app.route('/getArrivalData')
def getArrivalData():
    arrival_ref = db.reference('arrival')
    arrival_data = arrival_ref.get()

    return arrival_data

@app.route('/getBusData')
def getBusData():
    buses_ref = db.reference('buses')
    buses_data = buses_ref.get()

    return buses_data


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')



