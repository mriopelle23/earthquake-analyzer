#data collection

import os
import requests
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from message_queue import publish_event

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///earthquakes.sqlite3"

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok = True)

#Data persistence
DB_PATH = os.path.join(INSTANCE_DIR, "earthquake.sqlite3")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Earthquake(db.Model):
    id = db.Column(db.String, primary_key=True)
    place = db.Column(db.String, nullable=False)
    magnitude = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

#REST API Endpoint
def fetch_earthquakes():
    response = requests.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson")
    return response.json()["features"]

def save_earthquakes(features):
    saved_count = 0
    for feature in features:
        earthquake_id = feature["id"]
        properties = feature["properties"]

        if (db.session.get(Earthquake, earthquake_id)):
            continue
        
        earthquake = Earthquake(
            id = earthquake_id,
            place = properties["place"] or "Unknown",
            magnitude = properties["mag"] or 0.0,
            time = datetime.fromtimestamp(properties["time"] / 1000)
        )

        db.session.add(earthquake)
        saved_count += 1
    
    db.session.commit()
    publish_event("new_earthquake_data")
    return saved_count

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        earthquakes = fetch_earthquakes()
        count = save_earthquakes(earthquakes)
        print(f"Saved {count} new earthquakes.")

        