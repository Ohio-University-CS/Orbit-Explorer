#File name: assignment09_functionstest.py
#Name: McKenzie Searcy
#Date: 11-05-2025 
#Class: CS3560

# this file tests the 10 functions in assignment09_functions.py
import unittest
from assignment09_function import (
    check_username,
    check_password,
    check_email,
    check_login,
    check_planet_name,
    check_latitude,
    check_longitude,
    user_location,
    is_habitable,
    avg_planet_temp,
)


class TestAssignment09(unittest.TestCase):
    def test_check_username(self):
        self.assertEqual(check_username("mckenzie"), "mckenzie")
        self.assertEqual(check_username("abc"), "abc")
        with self.assertRaises(ValueError):
            check_username("")

    def test_check_password(self):
        self.assertEqual(check_password("secret1"), "secret1")
        self.assertEqual(check_password("123456"), "123456")
        with self.assertRaises(ValueError):
            check_password("")

    def test_check_email(self):
        self.assertEqual(check_email("user@example.com"), "user@example.com")
        self.assertEqual(check_email("a@b.co"), "a@b.co")
        with self.assertRaises(ValueError):
            check_email("not-an-email")

    def test_check_login(self):
        result = check_login("dorian", "password1")
        self.assertTrue(result["logged_in"])
        result = check_login("a", "1")
        self.assertTrue(result["logged_in"])
        with self.assertRaises(ValueError):
            check_login("dorian", "")

    def test_check_planet_name(self):
        self.assertEqual(check_planet_name("Mars"), "mars")
        self.assertEqual(check_planet_name("earth"), "earth")
        with self.assertRaises(ValueError):
            check_planet_name("pluto")

    def test_check_latitude(self):
        self.assertEqual(check_latitude(40), 40)
        self.assertEqual(check_latitude(-90), -90)
        with self.assertRaises(ValueError):
            check_latitude(120)

    def test_check_longitude(self):
        self.assertEqual(check_longitude(-82), -82)
        self.assertEqual(check_longitude(180), 180)
        with self.assertRaises(ValueError):
            check_longitude(200)

    def test_user_location(self):
        loc = user_location(40, -82)
        self.assertEqual(loc["lat"], 40)
        self.assertEqual(loc["lon"], -82)
        loc = user_location(-90, 180)
        self.assertEqual(loc["lat"], -90)
        self.assertEqual(loc["lon"], 180)
        with self.assertRaises(ValueError):
            user_location(40, 500)

    def test_is_habitable(self):
        self.assertTrue(is_habitable("earth"))
        self.assertTrue(is_habitable("Earth"))
        with self.assertRaises(ValueError):
            is_habitable("pluto")

    def test_avg_planet_temp(self):
        self.assertEqual(avg_planet_temp("earth"), 15)
        self.assertEqual(avg_planet_temp("Mercury"), 167)
        with self.assertRaises(ValueError):
            avg_planet_temp("pluto")


if __name__ == "__main__":
    unittest.main()
