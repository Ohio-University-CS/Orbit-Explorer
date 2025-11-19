import unittest
import asyncio
from fastapi.testclient import TestClient
from app.main import app

# services and helpers
from app.services.event import get_events
from app.astro_lib.events import get_body_info
from app.services.user import (
    get_user_saved_locations,
    get_user_preferences,
    get_user_saved_events,
)
from app.schemas.location import GeodeticLocation
from app.services.auth import get_current_user_uuid

# override auth dependency for tests
app.dependency_overrides[get_current_user_uuid] = lambda: "test_user"

client = TestClient(app)


class TestMainApp(unittest.TestCase):
    # tests event search (uses async service `get_events`)
    def test_event_search(self):
        loc = GeodeticLocation(lon=-82.0, lat=39.0, elevation=100.0)
        result = asyncio.run(get_events(loc, 0, 1000, ["eclipse"], []))
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 0)

        result = asyncio.run(get_events(loc, 0, 1000, [], []))
        self.assertIsInstance(result, list)

    # tests getting body information (replaces old `read_body`)
    def test_get_body_info(self):
        result = get_body_info("EARTH")
        self.assertIsInstance(result, dict)
        result = get_body_info("mars")
        self.assertIn("name", result)

        with self.assertRaises(Exception):
            get_body_info("NonexistentBody")

    # tests user service helpers (async functions)
    def test_user_services(self):
        locations = asyncio.run(get_user_saved_locations(0))
        self.assertIsInstance(locations, list)
        for loc in locations:
            self.assertIsInstance(loc, GeodeticLocation)

        prefs = asyncio.run(get_user_preferences(0))
        self.assertIsInstance(prefs, list)

        events = asyncio.run(get_user_saved_events(0))
        self.assertIsInstance(events, list)

    # tests user-related endpoints (auth dependency overridden)
    def test_user_endpoints(self):
        resp = client.get("/users/locations")
        self.assertEqual(resp.status_code, 200)

        resp2 = client.get("/users/saved-events")
        self.assertEqual(resp2.status_code, 200)

        # preferences endpoint returns 404 when empty (per current implementation)
        prefs = client.get("/users/preferences")
        self.assertEqual(prefs.status_code, 404)


if __name__ == "__main__":
    unittest.main()