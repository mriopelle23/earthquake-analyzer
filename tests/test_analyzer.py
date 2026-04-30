import sys, os
sys.path.insert(0, os.path.abspath("src"))
from collector import app, db, Earthquake
from analyzer import get_earthquake_summary
from datetime import datetime

def test_analyzer_summary():
    with app.app_context():
        db.drop_all()
        db.create_all()

        eq1 = Earthquake(
            id = "a1",
            place = "First Location",
            magnitude = 2.0,
            time = datetime(2025, 5, 26)
        )

        eq2 = Earthquake(
            id = "a2",
            place = "Second Location",
            magnitude = 4.0,
            time = datetime(2025, 5, 27)
        )

        db.session.add(eq1)
        db.session.add(eq2)
        db.session.commit()

        summary = get_earthquake_summary()

        assert summary["total_earthquakes"] == 2
        assert summary["average_magnitude"] == 3.0
        assert summary["largest_magnitude"] == 4.0
        assert summary["largest_location"] == "Second Location"