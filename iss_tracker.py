#!/usr/bin/env python3

from flask import Flask, request
import argparse
import requests
import xmltodict
import logging
import socket
import math
from datetime import datetime, timedelta
from typing import List
from geopy.geocoders import Nominatim

app = Flask(__name__)

def sum_squares(inputList: List[dict],keyword1: str,keyword2: str) -> float:
    """
    Sums the contents of a list of dictionaries, where the data is burried under 2 keys

    Args:
        inputList (List): List of dictionaries, which should all have the same keys
        keyword1 (String): Keyword to find in all dictionaries, which in this case should be X_DOT, Y_DOT, or Z_DOT
        keyword2 (String): Keyword to find within the dictionary identified by keyword1, which in this case should be #text

    Returns:
        total (Float): The total sum of all of the individual elements squared individually
    """
    total = 0
    for item in inputList:
        try:
            total += float(item[keyword1][keyword2])**2
        except TypeError:
            logging.warning(f'encountered non-float value {item[keyword1][keyword2]} in sumSquares')
    return total


def find_closest_time_index(inputList: List[dict], keyword:str) -> int:
    """
    Finds the time closest to runtime in a list of times stored in libraries under key keyword

    Args:
        inputList (List): List of dictionaries, which should all contain the key keyword
        keyword (String): Keyword to find in all the dictionaries, which in this case should be EPOCH

    
    Returns:
        min_difference_index (int): The index of the dictionary which contains the time closest to "now"

    """
    current_time = datetime.utcnow()
    time_objects = [datetime.strptime(item[keyword], "%Y-%jT%H:%M:%S.%fZ") for item in inputList]
    time_differences = [abs(current_time - time_obj) for time_obj in time_objects]
    min_difference_index = time_differences.index(min(time_differences))
    return min_difference_index

def latitude(x: float,y: float, z: float) -> float:
    """
    Converts X, Y, and Z coordinates into the appropriate Latitude

    Args:
        x (float): X-Coordinate in Mean of J2000 reference frame (km)
        y (float): Y-Coordinate in Mean of J2000 reference frame (km)
        z (float): Z-Coordinate in Mean of J2000 reference frame (km)

    Returns:
        lat (float): The latitude associated with the 3 input arguments
    """
    lat = math.degrees(math.atan2(z, math.sqrt(x**2 + y**2)))
    return lat;

def altitude(x: float,y: float,z: float) -> float:
    """
    Converts X, Y, and Z coordinates into the appropriate Altitude in kilometers

    Args:
        x (float): X-Coordinate in Mean of J2000 reference frame (km)
        y (float): Y-Coordinate in Mean of J2000 reference frame (km)
        z (float): Z-Coordinate in Mean of J2000 reference frame (km)

    Returns:
        alt (float): The altitude associated with the 3 input arguments
    """
    alt = math.sqrt(x**2 + y**2 + z**2) - 6371.0088
    return alt;

def longitude(x: float, y: float, z: float, time: str) -> float:
    """
    Converts Time + X, Y, and Z coordinates into the appropriate Latitude

    Args:
        x (float): X-Coordinate in Mean of J2000 reference frame (km)
        y (float): Y-Coordinate in Mean of J2000 reference frame (km)
        z (float): Z-Coordinate in Mean of J2000 reference frame (km)
        time (string): time in ISO 8601 format, Mean of J2000
        
    Returns:
        lon (float): The longitude associated with the 4 input arguments
    """
    timeobj=datetime.strptime(time, "%Y-%jT%H:%M:%S.%fZ")
    hrs = timeobj.hour
    mins = timeobj.minute
    lon = math.degrees(math.atan2(y, x)) - ((hrs-12)+(mins/60))*(360/24) + 19
    return lon;

def get_location(lat: float, lon: float) -> str:
    """
    Converts latitude and longitude values to a geolocation string using the Nominatim geolocator

    Args:
        lat (float): Latitude of the position in question
        lon (float): Longitude of the position in question

    Returns:
        address_string (String): The geolocation of these coordinates, or "Location not found" if said coordinates are over an area
        such as the ocean
    """
    geolocator = Nominatim(user_agent="iss_tracker.py")
    location = (lat,lon)
    try:
        location_info = geolocator.reverse(location, language='en')
        address_string = location_info.address if location_info else "Location not found"
        return address_string
    except Exception as e:
        logging.critical(f"Error: {e}")
    return None

def location_string(inputDict: dict) -> str:
    """
    Returns a descriptive string of a given epoch

    Args:
        inputDict (Dict): A specific epoch from the NASA provided list

    Returns:
        lcoationString (String): A string containing the latitude, longitude, altitude, and location of the given epoch
    """
    x = float(inputDict['X']['#text'])
    y = float(inputDict['Y']['#text'])
    z = float(inputDict['Z']['#text'])
    lat = latitude(x, y, z)
    alt = altitude(x, y, z)
    lon = longitude(x, y, z, inputDict['EPOCH'])
    location = get_location(lat,lon)
    locationString = f"Latitude: {lat}\nLongitude: {lon}\nAltitude: {alt}\nGeolocation: {location}\n"
    return locationString

@app.route('/comment', methods=['GET'])
def comment():
    response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    code = response.status_code;
    if code==200:
        data = xmltodict.parse(response.text)
    else:
        logging.critical(f'FAILURE TO GET DATA FROM https - error code {code}')
    return data['ndm']['oem']['body']['segment']['data']['COMMENT']

@app.route('/header', methods=['GET'])
def header():
    response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    code = response.status_code;
    if code==200:
        data = xmltodict.parse(response.text)
    else:
        logging.critical(f'FAILURE TO GET DATA FROM https - error code {code}')
    return data['ndm']['oem']['header']

@app.route('/metadata', methods=['GET'])
def metadata():
    response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    code = response.status_code;
    if code==200:
        data = xmltodict.parse(response.text)
    else:
        logging.critical(f'FAILURE TO GET DATA FROM https - error code {code}')
    return data['ndm']['oem']['body']['segment']['metadata']

@app.route('/epochs', methods=['GET'])
def epochs():
    response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    code = response.status_code;
    if code==200:
        data = xmltodict.parse(response.text)
    else:
        logging.critical(f'FAILURE TO GET DATA FROM https - error code {code}')
    dataImportant = data['ndm']['oem']['body']['segment']['data']['stateVector']
    offset = request.args.get('offset', default=1, type=str)
    try:
        offset = int(offset)
    except ValueError:
        return "Invalid offset parameter; must be an integer."
    limit = request.args.get('limit', default=len(dataImportant)-offset,type=str) 
    try:
        limit = int(limit)
    except ValueError:
        return "Invalid limit parameter; must be an integer."
    dataToReturn = dataImportant[offset:offset+limit]
    return dataToReturn;

@app.route('/epochs/<int:epoch>', methods=['GET'])
def specific_epoch(epoch):
    response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    code = response.status_code;
    if code==200:
        data = xmltodict.parse(response.text)
    else:
        logging.critical(f'FAILURE TO GET DATA FROM https - error code {code}')
    try:
        dataImportant = data['ndm']['oem']['body']['segment']['data']['stateVector'][epoch]
    except IndexError:
        logging.critical(f'Error: Index {index} is out of bounds for the list of epochs.')
    dataImportant = data['ndm']['oem']['body']['segment']['data']['stateVector']
    dataToReturn = dataImportant[epoch]
    return dataToReturn;

@app.route('/epochs/<int:epoch>/speed', methods=['GET'])
def specific_epoch_speed(epoch):
    response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    code = response.status_code;
    if code==200:
        data = xmltodict.parse(response.text)
    else:
        logging.critical(f'FAILURE TO GET DATA FROM https - error code {code}')
    try:
        dataImportant = data['ndm']['oem']['body']['segment']['data']['stateVector'][epoch]
    except IndexError:
        logging.critical(f'Error: Index {index} is out of bounds for the list of epochs.')
    xSpeedSquared = float(dataImportant['X_DOT']['#text'])**2
    ySpeedSquared = float(dataImportant['Y_DOT']['#text'])**2
    zSpeedSquared = float(dataImportant['Z_DOT']['#text'])**2
    dataToReturn = str((xSpeedSquared + ySpeedSquared + zSpeedSquared)**0.5)
    StringToReturn = f"Speed at this instance: {dataToReturn}"
    return StringToReturn;

@app.route('/epochs/<int:epoch>/location', methods=['GET'])
def specific_location(epoch):
    response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    code = response.status_code;
    if code==200:
        data = xmltodict.parse(response.text)
    else:
        logging.critical(f'FAILURE TO GET DATA FROM https - error code {code}')
    try:
        dataImportant = data['ndm']['oem']['body']['segment']['data']['stateVector'][epoch]
    except IndexError:
        logging.critical(f'Error: Index {index} is out of bounds for the list of epochs.')
    locationString = location_string(dataImportant)
    return locationString


@app.route('/now', methods=['GET'])
def get_current():
    response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    code = response.status_code;
    if code==200:
        data = xmltodict.parse(response.text)
    else:
        logging.critical(f'FAILURE TO GET DATA FROM https - error code {code}')
    dataImportant = data['ndm']['oem']['body']['segment']['data']['stateVector']
    closestData = dataImportant[find_closest_time_index(dataImportant,'EPOCH')]
    """ The following commented out section is an outdated functionality for this method
    xSpeed = float(closestData['X_DOT']['#text'])
    ySpeed = float(closestData['Y_DOT']['#text'])
    zSpeed = float(closestData['Z_DOT']['#text'])
    dataToReturn = str((xSpeed**2 + ySpeed**2 + zSpeed**2)**0.5)
    StringToReturn = f"Speed at this instance: {dataToReturn}\nX Velocity: {xSpeed}\nY Velocity: {ySpeed}\nZ Velocity: {zSpeed}"
    return StringToReturn;
    """
    locationString = location_string(closestData)
    return locationString


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--loglevel', type=str, required = False, default = 'ERROR',
                        help = 'set log level to DEBUG, INFO, WARNING, ERROR, or CRITICAL')
    args=parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    

    response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    code = response.status_code;
    if code==200:
        data = xmltodict.parse(response.text)
    else:
        logging.critical(f'FAILURE TO GET DATA FROM https - error code {code}')
    ##print(float(data['ndm']['oem']['body']['segment']['data']['stateVector'][0]['X']['#text']))
    dataImportant = data['ndm']['oem']['body']['segment']['data']['stateVector']

    xSquares = sum_squares(dataImportant, 'X_DOT', '#text')
    ySquares = sum_squares(dataImportant, 'Y_DOT', '#text')
    zSquares = sum_squares(dataImportant, 'Z_DOT', '#text')
    averageSpeed = ((xSquares + ySquares + zSquares)/len(dataImportant))**0.5

    closestData = dataImportant[find_closest_time_index(dataImportant,'EPOCH')]
    timeSpan = abs(datetime.strptime(dataImportant[0]['EPOCH'], "%Y-%jT%H:%M:%S.%fZ")-
                    datetime.strptime(dataImportant[len(dataImportant)-1]['EPOCH'], "%Y-%jT%H:%M:%S.%fZ"))

    ##Printing the output
    print(f'This data covers a span of {timeSpan}\n')
    print(f'\nMost current data: \n\tTime: {closestData["EPOCH"]}\n')
    print(f'\tX-Coordinate (km): {closestData["X"]["#text"]}\n\tY-Coordinate (km): {closestData["Y"]["#text"]}\n\tZ-Coordinate (km): {closestData["Z"]["#text"]}\n')
    print(f'\tX-Velocity (km/s): {closestData["X_DOT"]["#text"]}\n\tY-Velocity (km/s): {closestData["Y_DOT"]["#text"]}\n\tZ-Velocity (km/s): {closestData["Z_DOT"]["#text"]}')
    print(f'\nAverage Speed (km/s): {averageSpeed}')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
