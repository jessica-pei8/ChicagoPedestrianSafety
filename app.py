from flask import Flask, render_template, jsonify, request
import requests
from config import serviceInstanceID, integrationID
from helperroute import *
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',  watson_integration_id=integrationID,
                           watson_service_instance_id=serviceInstanceID)

# API endpoint to process frontend requests
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

if __name__ == '__main__':
    app.run(debug=True)
