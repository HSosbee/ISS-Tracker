# Easily Deployed ISS Tracker Flask App

## Overview
This code creates a docker container, which then runs a flask app that can be used to get various information from the public International Space Station tracking data. This repository contains a Dockerfile, docker-compose.yaml, and requirements.txt file for building the image, iss_tracker.py which is the bulk of the code, test_iss_tracker.py which is used to test iss_tracker.py, and a diagram of the software/repository. Using this repository you can get an easily deployable code which can be connected to over the internet, and which will only return up to date information at the time of running.

## Instructions
Download this repository, then after logging into docker using "docker login" run the following line:

docker-compose up -d

Now that the code is running, you can call it using the following formats:
1. curl localhost:5000/comment
2. curl localhost:5000/header
3. curl localhost:5000/metadata
4. curl localhost:5000/epochs
5. curl 'localhost:5000/epochs?limit=int&offset=int'
6. curl localhost:5000/epochs/\<epoch>
7. curl localhost:5000/epochs/\<epoch>/speed
8. curl localhost:5000/epochs/\<epoch>/location
9. curl localhost:5000/now

When finished, run the following line to stop the service:

docker-compose down

## Explanations
Note that all returns are Strings

1. Returns just the comment section at the top of the json file
2. Returns the header of the data from the json file
3. Returns the metadata section of the json file
4. Returns entire json file
5. Returns just a segment of the json starting at offset and of length limit
6. Returns the \<epoch>'th epoch from the original file
7. Returns the instantaneous speed of the \<epoch>'th epoch
8. Returns the latitude, longitude, altitude, and geoposition of the \<epoch>'th epoch
9. Returns the latitude, longitude, altitude, and geoposition of the epoch closest to now

## Imports
- argparse
- requests
- xmltodict
- logging
- socket
- datetime
- Flask
- geopy

## Sample Output

(Note that many of these outputs will change depending on the time the code is ran and if the NASA database has been updated)

1.

curl localhost:5000/comment


[
  "Units are in kg and m^2",
  "MASS=471702.00",
  "DRAG_AREA=1487.80",
  "DRAG_COEFF=2.00",
  "SOLAR_RAD_AREA=0.00",
  "SOLAR_RAD_COEFF=0.00",
  "Orbits start at the ascending node epoch",
  "ISS first asc. node: EPOCH = 2024-03-08T12:23:51.689 $ ORBIT = 293 $ LAN(DEG) = 101.66397",
  "ISS last asc. node : EPOCH = 2024-03-23T11:31:42.924 $ ORBIT = 525 $ LAN(DEG) = 25.88236",
  "Begin sequence of events",
  "TRAJECTORY EVENT SUMMARY:",
  null,
  "|       EVENT        |       TIG        | ORB |   DV    |   HA    |   HP    |",
  "|                    |       GMT        |     |   M/S   |   KM    |   KM    |",
  "|                    |                  |     |  (F/S)  |  (NM)   |  (NM)   |",
  "=============================================================================",
  "Crew-7 Undock         071:15:00:00.000             0.0     423.8     410.1",
  "(0.0)   (228.8)   (221.4)",
  null,
  "GMT074 Reboost Preli  074:13:11:00.000             1.6     424.3     409.2",
  "(5.2)   (229.1)   (220.9)",
  null,
  "71S Docking           081:16:39:49.000             0.0     425.0     412.6",
  "(0.0)   (229.5)   (222.8)",
  null,
  "SpX-30 Launch         081:20:54:00.000             0.0     425.0     412.7",
  "(0.0)   (229.5)   (222.8)",
  null,
  "SpX-30 Docking        083:11:00:00.000             0.0     425.2     412.0",
  "(0.0)   (229.6)   (222.5)",
  null,
  "=============================================================================",
  "End sequence of events"
]

2.

curl localhost:5000/header


{
  "CREATION_DATE": "2024-068T18:36:27.254Z",
  "ORIGINATOR": "JSC"
}

3.

curl localhost:5000/metadata


{
  "CENTER_NAME": "EARTH",
  "OBJECT_ID": "1998-067-A",
  "OBJECT_NAME": "ISS",
  "REF_FRAME": "EME2000",
  "START_TIME": "2024-068T12:00:00.000Z",
  "STOP_TIME": "2024-083T12:00:00.000Z",
  "TIME_SYSTEM": "UTC"
}

4.

curl localhost:5000/epochs


[
  {
    "EPOCH": "2024-067T11:58:00.000Z",
    "X": {
      "#text": "-4283.9472609613204",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "0.14844509525019001",
      "@units": "km/s"
    },
    "Y": {
      "#text": "824.44392134937004",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "-7.5467160106393596",
      "@units": "km/s"
    },
    "Z": {
      "#text": "5202.40213205689",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "1.3210479505166799",
      "@units": "km/s"
    }
  },
  {
    "EPOCH": "2024-067T12:00:00.000Z",
    "X": {
      "#text": "-4227.0773764199703",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "0.79790725822602004",
      "@units": "km/s"
    },
    "Y": {
      "#text": "-85.931573193827504",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "-7.6030772047199298",
      "@units": "km/s"
    },
    "Z": {
      "#text": "5312.8123730253401",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "0.51635285711225998",
      "@units": "km/s"
    }
   }
   ...
]

5.

curl 'localhost:5000/epochs?limit=3&offset=2'


[
  {
    "EPOCH": "2024-052T12:08:00.000Z",
    "X": {
      "#text": "1553.2933215427799",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "-7.41636649187486",
      "@units": "km/s"
    },
    "Y": {
      "#text": "4010.7468991515598",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "1.63519793497544",
      "@units": "km/s"
    },
    "Z": {
      "#text": "-5263.9972699270802",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "-0.94189768208915003",
      "@units": "km/s"
    }
  },
  {
    "EPOCH": "2024-052T12:12:00.000Z",
    "X": {
      "#text": "-261.34862045626102",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "-7.6136961101315599",
      "@units": "km/s"
    },
    "Y": {
      "#text": "4253.1746722929802",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "0.37275476244953998",
      "@units": "km/s"
    },
    "Z": {
      "#text": "-5296.1069673632701",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "0.67594566756106",
      "@units": "km/s"
    }
  },
  {
    "EPOCH": "2024-052T12:16:00.000Z",
    "X": {
      "#text": "-2057.0449194561202",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "-7.2593818542478497",
      "@units": "km/s"
    },
    "Y": {
      "#text": "4187.4720402411203",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "-0.91708256596170001",
      "@units": "km/s"
    },
    "Z": {
      "#text": "-4943.4402468286598",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "2.2451860609513501",
      "@units": "km/s"
    }
  }
]

6. 

(Note that this output should be the same as the first epoch in the previous call)

curl localhost:5000/epochs/2

{
  "EPOCH": "2024-052T12:08:00.000Z",
  "X": {
    "#text": "1553.2933215427799",
    "@units": "km"
  },
  "X_DOT": {
    "#text": "-7.41636649187486",
    "@units": "km/s"
  },
  "Y": {
    "#text": "4010.7468991515598",
    "@units": "km"
  },
  "Y_DOT": {
    "#text": "1.63519793497544",
    "@units": "km/s"
  },
  "Z": {
    "#text": "-5263.9972699270802",
    "@units": "km"
  },
  "Z_DOT": {
    "#text": "-0.94189768208915003",
    "@units": "km/s"
  }
}

7.

curl localhost:5000/epochs/20/speed

Speed at this instance: 7.6530359018080825

8. 

curl localhost:5000/epochs/20/location

(note that if the Geolocation: Location not found line occurs that likely means that the ISS is over the ocean, or a similar region that does not have an address)


Latitude: -28.74208476891908
Longitude: -61.56298146402443
Altitude: 430.6627799207736
Geolocation: Municipio de Villa Minetti, Departamento 9 de Julio, Santa Fe, Argentina

9.

curl localhost:5000/now

(format will  be identical to the 8th method, just different values)

## Information on the ISS Tracking Data from their website

After the header, ISS state vectors in the Mean of J2000 (J2K) reference frame are listed at four-minute intervals spanning a total length of 15 days. During reboosts (translation maneuvers), the state vectors are reported in two-second intervals. Each state vector lists the time in UTC; position X, Y, and Z in km; and velocity X, Y, and Z in km/s.

## Citations
- ISS Tracking Data can be found at https://spotthestation.nasa.gov/trajectory_data.cfm
- reading requests into xml file assisted by chatGPT
- datetime and geopy usage assisted by chatGPT
