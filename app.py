from flask import Flask, render_template, jsonify, request
import requests
from config import serviceInstanceID, integrationID
from helperroute import *
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',  watson_integration_id=integrationID,
                           watson_service_instance_id=serviceInstanceID)
@app.route('/check')
def routequery():
    return render_template('routequery.html')

@app.route('/get_coordinates', methods=['GET'])
def get_coordinates():
    address = request.args.get('address')
    # Call geocoding API here and return response
    response = requests.get(f'https://geocode.maps.co/search?q={address}&format=json')
    data = response.json()
    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return jsonify({'latitude': lat, 'longitude': lon})
    return jsonify({'error': 'Address not found'}), 404

@app.route('/get_intersections', methods=['POST'])
def get_intersections():
    data = request.get_json()
    start_address = data.get('start_address')
    end_address = data.get('end_address')

    start_coords = address_to_coords(start_address)
    end_coords = address_to_coords(end_address)

    if not start_coords or not end_coords:
        return jsonify({"error": "Invalid addresses or unable to fetch coordinates."}), 400
    route_coords = get_route(start_coords, end_coords)
    if route_coords is None:
        return jsonify({"error": "Error fetching route."}), 500

    intersections = check_route_for_intersections(route_coords)  
    intersection_addresses = []
    for intersection in intersections:
        lat, lon = intersection['Latitude'], intersection['Longitude']
        address = coords_to_address(lat, lon)
        intersection_addresses.append(address)
    return jsonify(intersection_addresses)

if __name__ == '__main__':
    app.run(debug=True)
