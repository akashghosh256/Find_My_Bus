from flask import Flask, render_template, request, url_for, redirect
import firebase_admin
from firebase_admin import credentials, db
# from dotenv import load_dotenv
import os
# import csv 

# load_dotenv()  # Loading environment variables from .env file

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

    # Looping through each bus and adding it to the appropriate route
    for bus_id, bus_data in buses_dict.items():
        origin = bus_data['origin']
        destination = bus_data['destination']
        route_key = f"{origin}-{destination}"
        eachRoute.append(route_key)

    return render_template('home.html', eachRoute = eachRoute)







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






@app.route('/getBusData')
def getBusData():
    buses_ref = db.reference('buses')
    buses_data = buses_ref.get()

    return buses_data




# Route for the search page
@app.route('/search', methods=['POST'])
def search():
    # Retrieving the origin and destination values from the form data
    selectedRoute = request.form['routes']
    # destination = request.form['destination']

    # Generating the URL for the search results page
    search_url = url_for('search_results', selectedRoute = selectedRoute)

    # Redirecting to the search results page
    return redirect(search_url)


# Route for the search results page
@app.route('/search_results')
def search_results():
    # Retrieving the origin and destination values from the URL parameters
    selectedRoute = request.args.get('selectedRoute')
    # destination = request.args.get('destination')

    # Querying the database for buses that match the origin and destination
    routes_ref = db.reference('routes')
    # route_key = f"{origin}-{destination}"
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
            buses_data[bus_id] = {'bus_no': bus_data['bus_no'], 'origin': bus_data['origin'], 'destination': bus_data['destination'], 'route': bus_data['route']}

    # If no buses were found for the route, return an error message
    if len(buses_data) == 0:
        return f"No buses found for route {selectedRoute}"

    # Return the list of buses that match the route
    return render_template('search_results.html', buses=buses_data)





if __name__ == "__main__":
  app.run(host='0.0.0.0', debug = True)