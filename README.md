# Homework05 - ISS Tracker Flask App

## Overview
This code creates a docker container, which then runs a flask app that can be used to get various information from the public International Space Station tracking data. This repository contains a Dockerfile for building the image, iss_tracker.py which is the bulk of the code, test_iss_tracker.py which is used to test iss_tracker.py, and a diagram of the software/repository. Using this repository you can get an easily deployable code which can be connected to over the internet, and which will only return up to date information at the time of running.

## Instructions
Download this repository, then after logging into docker using "docker login" run the following lines:

docker build -t username/iss-tracker-flask:1.0 .

docker run --name "iss-tracker-app" -d -p 5000:5000 username/iss-tracker-flask:1.0

Now that the code is running, you can call it using the following formats:
1. curl localhost:5000/epochs
2. curl 'localhost:5000/epochs?limit=int&offset=int'
3. curl localhost:5000/epochs/\<epoch>
4. curl localhost:5000/epochs/\<epoch>/speed
5. curl localhost:5000/now

## Explanations
Note that all returns are Strings

1. Returns entire json file
2. Returns just a segment of the json starting at offset and of length limit
3. Returns the \<epoch>'th epoch from the original file
4. Returns the instantaneous speed of the \<epoch>'th epoch
5. Returns the state vectors and instantaneous speed of the epoch closest to now

## Imports
- argparse
- requests
- xmltodict
- logging
- socket
- datetime
- Flask

## Sample Output

(Note that all of these outputs will change depending on the time the code is ran and if the NASA database has been updated)

1.  curl localhost:5000/epochs


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

2.  curl 'localhost:5000/epochs?limit=3&offset=2'


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

3. 

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

4.

curl localhost:5000/epochs/2/speed

Speed at this instance: 7.652681586991391

5.

curl localhost:5000/now

Speed at this instance: 7.656077768147414
X Velocity: -1.09017972522795
Y Velocity: 5.74223356545237
Z Velocity: -4.94507721258376

## Information on the ISS Tracking Data from their website

After the header, ISS state vectors in the Mean of J2000 (J2K) reference frame are listed at four-minute intervals spanning a total length of 15 days. During reboosts (translation maneuvers), the state vectors are reported in two-second intervals. Each state vector lists the time in UTC; position X, Y, and Z in km; and velocity X, Y, and Z in km/s.

## Citations
- ISS Tracking Data can be found at https://spotthestation.nasa.gov/trajectory_data.cfm
- reading requests into xml file assisted by chatGPT
- README formating from chatGPT
- find_closest_time_index from chatGPT
