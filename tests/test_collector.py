from unittest.mock import MagicMock, patch
import sys, os
sys.path.insert(0, os.path.abspath("src"))
from collector import app, db, Earthquake, save_earthquakes, fetch_earthquakes

#mock test
def test_fetch_earthquakes_with_mock():
    mock_response = {
        "features": [
            {
                "id": "mock-id",
                "properties": {
                    "place": "Mock Place",
                    "mag": 3.2,
                    "time": 1000000000000
                }
            }
        ]
    }

    with patch("collector.requests.get") as mock_get:
        mock_get.return_value.json = MagicMock(return_value=mock_response)

        result = fetch_earthquakes()

        assert len(result) == 1
        assert result[0]["id"] == "mock-id"

#unit test
def test_save_earthquakes_with_mock_data():
    mock_features = [
        {
            "id": "test-earthquake-1",
            "properties": {
                "place": "Test Location",
                "mag": 4.5,
                "time": 1000000000000
            }
        }
    ]

    with app.app_context():
        db.drop_all()
        db.create_all()

        saved_count = save_earthquakes(mock_features)

        earthquake = db.session.get(Earthquake, "test-earthquake-1")

        assert saved_count == 1
        assert earthquake is not None
        assert earthquake.place == "Test Location"
        assert earthquake.magnitude == 4.5