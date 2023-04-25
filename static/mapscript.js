// Create a new Leaflet map with a center and zoom level
var map_init = L.map('map', {
    center: [9.0820, 8.6753],
    zoom: 1
});

// Add an OpenStreetMap tile layer to the map
var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    // attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    attribution: 'Map data &copy; OpenStreetMap contributors'
}).addTo(map_init);

// Add a geocoder control to the map
L.Control.geocoder().addTo(map_init);

// Check if geolocation is supported by the browser, and if so, get the user's location every 5 seconds
// if (!navigator.geolocation) {
//     console.log("Your browser doesn't support geolocation feature!")
// } else {
//     setInterval(() => {
//         navigator.geolocation.getCurrentPosition(getPosition)
//     }, 5000);
//     map_init.zoom = 4

// };



// Check if geolocation is supported
if (navigator.geolocation) {
    // Ask the user for permission to access their location
    navigator.geolocation.getCurrentPosition(
      function(position) {
        // If permission is granted, do something with the location data
        setInterval(() => {
            navigator.geolocation.getCurrentPosition(getPosition)
        }, 5000);
        map_init.zoom = 4
    
      },
      function(error) {
        // If permission is denied, show an error message
        alert("Error getting location: " + error.message);
      }
    );
  } else {
    // If geolocation is not supported, show an error message
    alert("Geolocation is not supported by this browser.");
  }
  

















// Declare variables to hold the marker, circle, latitude, longitude, and accuracy of the user's position
var marker, circle, lat, long, accuracy , go, fixed;


// A function to handle the user's position returned by the geolocation API
function getPosition(position) {
    // Update the latitude, longitude, and accuracy variables
    lat = position.coords.latitude
    long = position.coords.longitude
    accuracy = position.coords.accuracy

    go = L.marker([lat, long])

    // Remove the previous marker and circle from the map, if they exist
    if (marker) {
        map_init.removeLayer(marker)
    }

    if (circle) {
        map_init.removeLayer(circle)
    }

    // Create a new marker and circle at the user's location
    marker = L.marker([lat, long])
    circle = L.circle([lat, long], { radius: accuracy })
     // Add the marker and circle to a feature group and add the group to the map, then fit the map to the bounds of the feature group
     var featureGroup = L.featureGroup([marker, circle]).addTo(map_init).bindPopup('You are here<br/>').openPopup();
     map_init.fitBounds(featureGroup.getBounds())
     console.log("Your coordinate is ok: Lat: " + lat + " Long: " + long + " Accuracy: " + accuracy)



     var redIcon = L.icon({
        iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });
    
     fixed = L.marker([22.5736296,88.3251045])
     fixed.setIcon(redIcon)
    L.featureGroup([fixed]).addTo(map_init).bindPopup('Point A<br/>').openPopup();




// Define two points as LatLng objects
var point1 = L.latLng(22.5736296,88.3251045); // San Francisco
var point2 = L.latLng(lat, long); // Los Angeles

// Calculate the distance between the two points in meters
var distance = (point1.distanceTo(point2))/1000;
document.getElementById('length').innerHTML = distance.toFixed(2) + " km from your location" + "<br> Average time: " + (distance.toFixed(2)/24.5).toFixed(2) + " hrs";

console.log("it is -----"+distance); // Output: 535161.6335689421 meters





}
