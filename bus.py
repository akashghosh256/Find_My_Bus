from flask import Flask, render_template, request, url_for, redirect
import firebase_admin 
from firebase_admin import credentials, db
#from dotenv import load_dotenv
import os
#import csv 

#load_dotenv()  # Loading environment variables from .env file

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
@app.route('/updatedata')
def updatedata():
    # Loading the CSV file
    with open("C:\\Users\\HP\\Downloads\\BUS_ROUTES - Sheet1.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        # Creating a reference to the 'buses' node in the database
        buses_ref = db.reference('buses')
        # Looping through each row in the CSV file and updating the route field of the corresponding child node
        for row in reader:
            # Using the Bus ID as the key for the child node
            bus_id = row['bus_id']
            # Creating a reference to the child node using the bus ID
            bus_ref = buses_ref.child(bus_id)
            # Updating and adding the 'bus_fare' field to the child node
            bus_ref.update({'bus_fare': row['bus_fare']})
        return 'Data updated successfully!'
    
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
            # Using the arrival value as the key for the child node
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
   #Creating a reference to the database
    buses_ref = db.reference('buses')
    # Retrieve the data from the buses node
    buses_data = buses_ref.get()
    #Filtering out the null values
    buses_data = [bus for bus in buses_data if bus is not None]
    
    #Storing the buses_data in a dictionary
    buses_dict = {bus['bus_id']: bus for bus in buses_data}

    #Creating an empty list to store the route values
    eachRoute = []
    uniqueRoutes = list(set(eachRoute))

    # Looping through each bus and adding it to the appropriate route
    for bus_id, bus_data in buses_dict.items():
        origin = bus_data['origin']
        destination = bus_data['destination']
        route_key = f"{origin}-{destination}"
        eachRoute.append(route_key)

    return render_template('home.html', eachRoute = uniqueRoutes)

# Route for the search page
@app.route('/search', methods=['POST'])
def search():
    # Retrieving the origin and destination values from the form data
    selectedRoute = request.form['routes']

    # Generating the URL for the search results page
    search_url = url_for('search_results', selectedRoute = selectedRoute)

    # Redirecting to the search results page
    return redirect(search_url)


# Route for the search results page
@app.route('/search_results')
def search_results():
    # Retrieving the route values from the URL parameters
    selectedRoute = request.args.get('selectedRoute')

    # Querying the database for buses that match the route
    routes_ref = db.reference('routes')
    route_data = routes_ref.child(selectedRoute).get()

    # If the route doesn't exist, returning an error message
    if route_data is None:
        return f"No buses found for route {selectedRoute}"

    # Retrieving the data for each bus in the route
    buses_ref = db.reference('buses')
    buses_data = {}
    for bus_id in route_data:
        bus_data = buses_ref.child(bus_id).get()
        if bus_data is not None:
            buses_data[bus_id] = {'bus_no': bus_data['bus_no'], 'origin': bus_data['origin'], 'destination': bus_data['destination'], 'route': bus_data['route'], 'bus_fare': bus_data['bus_fare']}

    # If no buses were found for the route, return an error message
    if len(buses_data) == 0:
        return f"No buses found for route {selectedRoute}"

    # Return the list of buses that match the route
    return render_template('search_results.html', buses=buses_data)

@app.route("/about")
def about():
  return render_template('about.html')

@app.route("/help")
def help():
  return render_template('help.html')

@app.route("/track")
def track():
  return render_template('track.html')

@app.route("/mylocation")
def mylocation():
  return render_template('mylocation.html')

@app.route("/pointlocation")
def pointlocation():
  return render_template('pointlocation.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug = True)
