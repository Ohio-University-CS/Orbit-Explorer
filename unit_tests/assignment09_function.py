#File name: assignment09_function.py
#Name: McKenzie Searcy
#Date: 11-05-2025 
#Class: CS3560

#10 functions

#1
def check_username(username): 
    if not username:
        raise ValueError("Username is required.")
    if len(username) < 3:
        raise ValueError("Username must be 3 characters at minimum.")
    return username    
#ensures username is entered and is 3 characters or greater 

#2
def check_password(password):
    if not password:
        raise ValueError("Password is required.")
    if len(password) < 6:
        raise ValueError("Password must be 6 characters at minimum.")
    return password
#ensures password is entered and is 6 characters or greater

#3
def check_email(email):
    if not email:
        raise ValueError("Email is required.")
    if "." not in email or "@" not in email:
        raise ValueError("The email you entered has incorrect formatting.")
    return email
#ensures email is entered and contains a "." or "@"

#4
def check_login(username, password):
    if not username or not password:
        raise ValueError("Username and password are required.")
    return {"username": username, "logged_in": True}
#ensures a username and password is entered to make logged_in True 

#5
def check_planet_name(name):
    if not name:
        raise ValueError("Planet name is required.")
    allowed = ["mercury", "venus", "earth", "mars", "jupiter",
               "saturn", "uranus", "neptune"]
    formatted_name = name.lower()
    if formatted_name not in allowed:
        raise ValueError("Planet is not recognized.")
    return formatted_name
#only mercury, venus, earth, mars, jupiter, saturn, uranus, or neptune can be entered 
#if none of those are then it isn't recognized 

#6
def check_latitude(lat):
    if lat is None:
        raise ValueError("Latitude is required.")
    if lat < -90 or lat > 90:
        raise ValueError("A Latitude between -90 and 90 is required.")
    return lat
#latitude has to be between -90 and 90, if none is entered there will also be an error

#7
def check_longitude(lon):
    if lon is None:
        raise ValueError("Longitude is required.")
    if lon < -180 or lon > 180:
        raise ValueError("A Longitude between -180 and 180 is required.")
    return lon
#longitude has to be between -180 and 180, if none is entered there will also be an error 

#8
def user_location(lat, lon):
    checked_lat = check_latitude(lat)
    checked_lon = check_longitude(lon)
    return {"lat": checked_lat, "lon": checked_lon}
#returns latitude and longitude 

#9
def is_habitable(planet_name):
    if not planet_name:
        raise ValueError("Planet name is required.")
    name = planet_name.lower()
    known = ["mercury", "venus", "earth", "mars", "jupiter",
             "saturn", "uranus", "neptune"]
    if name not in known:
        raise ValueError("Planet is not recognized.")
    return name == "earth"  # only earth is habitable
#only earth will be returned bc its the only habitable planet 'that we know of' 

#10
def avg_planet_temp(planet_name):  # in celsius
    if not planet_name:
        raise ValueError("Planet name is required.")
    name = planet_name.lower()
    temps = {
        "mercury": 167,
        "venus": 464,
        "earth": 15,
        "mars": -65,
        "jupiter": -110,
        "saturn": -140,
        "uranus": -195,
        "neptune": -200,
    }
    if name not in temps:
        raise ValueError("Planet is not recognized.")
    return temps[name]
#googled these values
#tells you what the average temperature of the planet is

#run instructions
#python3 assignment09_functionstest.py
