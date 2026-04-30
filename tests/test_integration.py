import sys, os
sys.path.insert(0, os.path.abspath("src"))
from collector import app, db, Earthquake, save_earthquakes
from analyzer import get_earthquake_summary

def test_collector_database_analyzer_integration():
    mock_features = [
        {
            "id": "integration-earthquake-1",
            "properties": {
                "place": "Integration Testing Location",
                "mag": 5.5,
                "time": 1000000000000
            }
        }
    ]

    with app.app_context():
        db.drop_all()
        db.create_all()
        
        saved_count = save_earthquakes(mock_features)
        summary = get_earthquake_summary()

        assert saved_count == 1
        assert summary["total_earthquakes"] == 1
        assert summary["largest_magnitude"] == 5.5
        assert summary["largest_location"] == "Integration Testing Location"

