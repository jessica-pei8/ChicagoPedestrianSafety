from flask import Flask, render_template, jsonify, request, send_from_directory
import requests
from helperroute import *
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/check')
def routequery():
    return render_template('routequery.html')
@app.route('/visualizations')
def visualizations():
    return render_template('visualizations.html')
@app.route('/top300')
def top():  
    return render_template('topintersections.html')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('assets', filename)

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
    intersection_details = [
        {
            "Latitude": intersection['Latitude'],
            "Longitude": intersection['Longitude'],
            'Count': intersection['Cluster_Count'], 
            "Address": coords_to_address(intersection['Latitude'], intersection['Longitude'])
        }
        for intersection in intersections
    ]

    return jsonify({"route": route_coords, "intersections": intersection_details})

@app.route('/get_dangerous_intersections', methods=['GET'])
def get_dangerous_intersections():
    return jsonify(get_centroids())

if __name__ == '__main__':
    app.run(debug=True)
