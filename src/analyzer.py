#data analyzer

from collector import app, db, Earthquake
from message_queue import consume_event

def get_earthquake_summary():
    earthquakes = Earthquake.query.all()
    if not earthquakes:
        return {
            "total_earthquakes": 0,
            "average_magnitude": 0,
            "largest_magnitude": 0,
            "largest_location": "Data isn't available"
        }
    
    total = len(earthquakes)
    average_magnitude = sum(eq.magnitude for eq in earthquakes) / total
    largest = max(earthquakes, key = lambda eq: eq.magnitude)

    return {
        "total_earthquakes": total,
        "average_magnitude": round(average_magnitude, 2),
        "largest_magnitude": round(largest.magnitude, 2),
        "largest_location": largest.place
    }

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        event = consume_event()
        if event:
            print("New data detected, running analysis...")
            summary = get_earthquake_summary()
            print(summary)
        else:
            print("No new events.")