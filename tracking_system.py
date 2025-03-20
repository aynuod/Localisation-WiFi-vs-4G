from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
from pymongo import MongoClient 
from bson import json_util 
import json
import math
import time

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['location_tracker']
locations_collection = db['locations']

def calculate_speed(point1, point2):
    """Calculate speed between two points in km/h"""
    time1 = datetime.fromisoformat(point1['timestamp'])
    time2 = datetime.fromisoformat(point2['timestamp'])
    time_diff = (time2 - time1).total_seconds() / 3600  # Convert to hours
    
    # Haversine formula for distance
    R = 6371  # Earth's radius in km
    lat1, lon1 = math.radians(point1['latitude']), math.radians(point1['longitude'])
    lat2, lon2 = math.radians(point2['latitude']), math.radians(point2['longitude'])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    distance = R * c  # Distance in km
    
    return distance / time_diff if time_diff > 0 else 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/location", methods=["POST"])
def receive_location():
    try:
        data = request.json
        if not all(k in data for k in ["latitude", "longitude", "connection"]):
            return jsonify({"error": "Missing required fields"}), 400

        # Add timestamp and format data
        location_data = {
            "latitude": float(data["latitude"]),
            "longitude": float(data["longitude"]),
            "connection": data["connection"],
            "timestamp": datetime.now().isoformat(),
            "accuracy": data.get("accuracy", 0)
        }

        # Get previous point for speed calculation
        previous_point = locations_collection.find_one(
            {"connection": data["connection"]},
            sort=[("timestamp", -1)]
        )

        if previous_point:
            location_data["speed"] = calculate_speed(previous_point, location_data)

        # Insert into MongoDB
        locations_collection.insert_one(location_data)

        return jsonify({"message": "Location received!", "data": json.loads(json_util.dumps(location_data))})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/map")
def get_map_data():
    try:
        # Get filter parameters
        connection_type = request.args.get('connection')
        time_filter = request.args.get('timeframe')  # 'hour', 'day', 'all'

        # Build query
        query = {}
        if connection_type:
            query['connection'] = connection_type

        if time_filter:
            time_limit = datetime.now()
            if time_filter == 'hour':
                time_limit = time_limit.replace(hour=time_limit.hour - 1)
            elif time_filter == 'day':
                time_limit = time_limit.replace(day=time_limit.day - 1)
            
            if time_filter != 'all':
                query['timestamp'] = {'$gte': time_limit.isoformat()}

        # Get locations from MongoDB
        locations = list(locations_collection.find(query).sort("timestamp", 1))

        # Calculate statistics
        stats = {
            "4G": {
                "count": locations_collection.count_documents({"connection": "4G"}),
                "avg_accuracy": sum(l.get("accuracy", 0) for l in locations if l["connection"] == "4G") / 
                              max(locations_collection.count_documents({"connection": "4G"}), 1)
            },
            "WiFi": {
                "count": locations_collection.count_documents({"connection": "WiFi"}),
                "avg_accuracy": sum(l.get("accuracy", 0) for l in locations if l["connection"] == "WiFi") / 
                              max(locations_collection.count_documents({"connection": "WiFi"}), 1)
            }
        }

        return jsonify({
            "locations": json.loads(json_util.dumps(locations)),
            "stats": stats
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/clear", methods=["POST"])
def clear_data():
    try:
        locations_collection.delete_many({})
        return jsonify({"message": "All location data cleared"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=8080, debug=True)