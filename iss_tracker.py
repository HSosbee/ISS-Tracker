#!/usr/bin/env python3

from flask import Flask, request
import argparse
import requests
import xmltodict
import logging
import socket
from datetime import datetime, timedelta
from typing import List

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
    dataImportant = data['ndm']['oem']['body']['segment']['data']['stateVector'][epoch]
    xSpeedSquared = float(dataImportant['X_DOT']['#text'])**2
    ySpeedSquared = float(dataImportant['Y_DOT']['#text'])**2
    zSpeedSquared = float(dataImportant['Z_DOT']['#text'])**2
    dataToReturn = str((xSpeedSquared + ySpeedSquared + zSpeedSquared)**0.5)
    StringToReturn = f"Speed at this instance: {dataToReturn}"
    return StringToReturn;

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
    xSpeed = float(closestData['X_DOT']['#text'])
    ySpeed = float(closestData['Y_DOT']['#text'])
    zSpeed = float(closestData['Z_DOT']['#text'])
    dataToReturn = str((xSpeed**2 + ySpeed**2 + zSpeed**2)**0.5)
    StringToReturn = f"Speed at this instance: {dataToReturn}\nX Velocity: {xSpeed}\nY Velocity: {ySpeed}\nZ Velocity: {zSpeed}"
    return StringToReturn;
    


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
