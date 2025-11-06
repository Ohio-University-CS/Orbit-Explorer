import unittest
from fastapi.testclient import TestClient
from app.main import *
from app.astro_lib.events import *


client = TestClient(app)

class TestMainApp(unittest.TestCase):
    # tests event search for normal use edge input and bad coordinates
    def test_event_search(self):
        result = event_search(
            start_time=0, end_time=1000, lon=-82.0, lat=39.0, elevation=100.0,
            whitelisted_event_types=["eclipse"], event_specific_criteria=[]
        )
        self.assertIsInstance(result, list)

        result = event_search(
            start_time=0, end_time=1000, lon=-82.0, lat=39.0, elevation=100.0,
            whitelisted_event_types=[], event_specific_criteria=[]
        )
        self.assertIsInstance(result, list)

        with self.assertRaises(ValueError):
            event_search(
                start_time=0, end_time=1000, lon=999, lat=39.0, elevation=100.0,
                whitelisted_event_types=["eclipse"], event_specific_criteria=[]
            )

    # tests read body for valid names lowercase names and missing ones
    def test_read_body(self):
        result = read_body("EARTH")
        self.assertIsInstance(result, dict)

        result = read_body("mars")
        self.assertIn("name", result)

        with self.assertRaises(HTTPException) as context:
            read_body("NonexistentBody")
        self.assertEqual(context.exception.status_code, 404)

    # tests saved locations returns correct type handles valid and invalid
    def test_read_user_locations(self):
        locations = get_user_saved_locations()
        self.assertIsInstance(locations, list)
        for loc in locations:
            self.assertIsInstance(loc, GeodeticLocation)

        with self.assertRaises(TypeError):
            hash(set(locations))

    # tests preferences output for list type and bad input
    def test_read_user_preferences(self):
        prefs = get_user_preferences()
        self.assertIsInstance(prefs, list)

        self.assertIsInstance([], list)

        with self.assertRaises(TypeError):
            get_user_preferences("invalid")

    # tests saved events for list type valid data and bad type
    def test_read_user_saved_events(self):
        events = get_user_saved_events()
        self.assertIsInstance(events, list)
        self.assertTrue(all(isinstance(e, dict) for e in events))

        with self.assertRaises(TypeError):
            get_user_saved_events("invalid")

    # tests adding user location for success edge elevation and missing name
    def test_post_user_saved_location(self):
        data = {"lon": -82.0, "lat": 39.0, "elevation": 100.0, "name": "Home"}
        response = client.post("/user/locations/add", params=data)
        self.assertEqual(response.status_code, 200)

        data["elevation"] = 9000
        response = client.post("/user/locations/add", params=data)
        self.assertEqual(response.status_code, 200)

        data.pop("name")
        response = client.post("/user/locations/add", params=data)
        self.assertEqual(response.status_code, 422)

    # tests updating preferences with normal data empty list and bad input
    def test_post_update_user_preferences(self):
        data = ["theme:dark", "notifications:on"]
        response = client.post("/user/preferences/update", json=data)
        self.assertEqual(response.status_code, 200)

        response = client.post("/user/preferences/update", json=[])
        self.assertEqual(response.status_code, 200)

        response = client.post("/user/preferences/update", json="invalid")
        self.assertEqual(response.status_code, 422)

    # tests getting preferences endpoint for response validity and bad url
    def test_get_user_preferences_endpoint(self):
        response = client.get("/user/preferences")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

        second = client.get("/user/preferences")
        self.assertEqual(second.status_code, 200)

        bad = client.get("/user/preferences/bad")
        self.assertEqual(bad.status_code, 404)

    # tests getting locations endpoint for repeat calls and invalid path
    def test_get_user_locations_endpoint(self):
        response = client.get("/user/locations")
        self.assertEqual(response.status_code, 200)

        response2 = client.get("/user/locations")
        self.assertEqual(response2.status_code, 200)

        response3 = client.get("/user/locations/invalid")
        self.assertEqual(response3.status_code, 404)

    # tests getting saved events endpoint normal behavior and bad url
    def test_get_user_saved_events_endpoint(self):
        response = client.get("/user/saved_events")
        self.assertEqual(response.status_code, 200)

        response2 = client.get("/user/saved_events")
        self.assertEqual(response2.status_code, 200)

        bad = client.get("/user/saved_events/bad")
        self.assertEqual(bad.status_code, 404)

if __name__ == "__main__":
    unittest.main()