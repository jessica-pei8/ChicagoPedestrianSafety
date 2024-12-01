import requests
import math
import json 
import openrouteservice
from config import ORSapi_key, GEOCODEapikey

def address_to_coords(address):
    base_url = "https://geocode.maps.co/search"
    params = {
        'q': address, 
        'api_key': GEOCODEapikey, 
        'format': 'json'  
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return (float(lat), float(lon))
        else:
            print("Address not found.")
            return None
    else:
        print("Error with the API request. Status code:", response.status_code)
        return None

def coords_to_address(lat,lon):
    base_url = "https://geocode.maps.co/reverse"   
    
    params = {
        'lat': lat,   
        'lon': lon,   
        'api_key': GEOCODEapikey,   
        'format': 'json'  
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['display_name']
    else:
        print("Error with the API request. Status code:", response.status_code)
        return None

    
def get_route(start_coords, end_coords):
    client = openrouteservice.Client(key=ORSapi_key)
    start_lat, start_lon = start_coords
    end_lat, end_lon = end_coords

    try:
        route = client.directions(
            coordinates=[(start_lon, start_lat), (end_lon, end_lat)],  # Start and end coordinates
            profile='foot-walking',  # Walking profile
            format='geojson' 
        )
        route_coordinates = route['features'][0]['geometry']['coordinates']
        return route_coordinates
    except Exception as e:
        print(f"Error occurred while fetching route: {e}")
        return None

def load_intersections(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)
    
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c * 1000  

def check_route_for_intersections(route_coords, threshold=10):
    passed_intersections = []
    top_intersections = load_intersections('saved_jsons/centroids.json')
    for intersection in top_intersections:
        for point in route_coords:
            distance = haversine(intersection['Latitude'], intersection['Longitude'], point[1], point[0])
            print(distance)
            if distance <= threshold:
                passed_intersections.append(intersection)
                break
    
    return passed_intersections


# # Example user inputs (start and end coordinates)
# start_coords =   address_to_coords('225 S Canal St, Chicago, IL 60606') 
# end_coords =  address_to_coords(' 800 W Fulton Market, Chicago, IL 60607')

# # Get the route coordinates
# route_coordinates = get_route(start_coords, end_coords)
# # Check if the route passes through any intersections
# if route_coordinates:
#     intersections_near_route = check_route_for_intersections(route_coordinates)
#     print(f"Intersections near the route: {intersections_near_route}")

