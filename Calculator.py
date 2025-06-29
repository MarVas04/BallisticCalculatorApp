#To get the environmental data and user location the module uses the windy and ipify APIs respectively as well
#as the requests library for sending get() requests to the APIs

import ipinfo
from requests import get
import requests
import json
from datetime import datetime
import math
import numpy

#Initialise variables
mass = 0
calibre = 0
BC = 0
velocity = 0
distance_to_target = 0


#Function to find the epoch time of the user's local time
def local_time():
    #Uses the datetime module to get the user's local time
    user_local_time = datetime.now()
    #Parses datetime converting each value into an integer
    year = int(user_local_time.strftime("%Y"))
    month = int(user_local_time.strftime("%m"))
    day = int(user_local_time.strftime("%d"))
    hour = int(user_local_time.strftime("%H"))
    minute = int(user_local_time.strftime("%M"))
    #Converts datetime to epoch (number of seconds since 01/01/1970)
    local_epoch_time = datetime(year,month,day,hour,minute).timestamp()
    return local_epoch_time


#Function to get environmental data from the internet
def env_data():
    #Program attempts to get the user's IP address
    try:
        #Uses the ipify API to get the public IP of the user
        user_ip = get('https://api.ipify.org').content.decode('utf8')
    #If there was an error in acquiring the user's IP address this code is executed
    except:
        print ("Error in acquiring location")
    #If there was no error in acquiring the user's IP address this code is executed
    else:
        # Uses the ipinfo API to get longitude and latitude of the user's IP address. The API is free to use so the
        # access token is not hidden in this code
        access_token = '392b313830531c'
        handler = ipinfo.getHandler(access_token)
        details = handler.getDetails(user_ip)
        #Gets the user's latitude and longitude (in that order) and then splits the
        #output string into a list
        latlng = details.loc.split(",")
        user_latitude = latlng[0]
        user_longitude = latlng[1]

        #Dictionary containing data in a valid format for the windy API
        request_data_dict = {
            "lat": user_latitude,
            "lon": user_longitude,
            "model": "gfs",
            "parameters": ["wind", "dewpoint", "rh", "pressure", "temp"],
            "levels": ["surface"],
            "key": "qjNo74MtZkSgsiwtqeyfi09B4o6iD407"
        }

        #Sends a POST request (as required in windy documentation) with relevant data encoded as a JSON object
        response = requests.post("https://api.windy.com/api/point-forecast/v2", json = request_data_dict)
        #Converts the return JSON object to a python dictionary for parsing
        return_data_dict = json.loads(response.text)

        #--This section of code is to extract the useful data--

        all_times_array = return_data_dict["ts"]
        times_array = []
        #Takes the first 8 items in the array of epoch times (so 1 full day) and adds them to a new array
        for i in all_times_array[:8]:
            #Converts the values from milliseconds to seconds
            times_array.append(i/1000)
        differences = []
        #Calculates the difference between each item in the new array and the local epoch time
        for k in times_array:
            differences.append(abs((local_time())-(k)))
        #Finds the smallest value in the array of differences
        closest_time = min(differences)
        #Finds the index of the value with the smallest difference
        closest_time_index = differences.index(closest_time)

        # Creates an array of all the relative humidity values then extracts relevant value
        all_RH_array = return_data_dict["rh-surface"]
        relative_humidity = all_RH_array[closest_time_index]

        # Creates an array of all the temperature values then extracts relevant value and converts it to degrees celsius
        all_T_array = return_data_dict["temp-surface"]
        temperature = (all_T_array[closest_time_index]-273.15)

        #----

        #Puts all the relevant data into a dictionary
        environmental_data_dict = {
            "Relative Humidity":relative_humidity,
            "Temperature":temperature
       }
        return environmental_data_dict


#For some reason the mass variable wasn't recognised within the function even though it is defined in the global
# namespace so it is being passed as a parameter instead. The temperature and relative humidity are also provided as
# arguments.
def bullet_drop(mass,temperature,relative_humidity):

    #--Calculate air density--

    # Calculate saturation vapor pressure at specific temperature
    T = temperature
    SVP = 6.1078810*math.pow(10,7.5*(7.5*T/(T + 237.3)))

    #Calculate actual vapour pressure
    RH = relative_humidity
    VP = SVP*RH

    #Calculate pressure of dry air
    PDA = SVP-VP

    #Calculate air density
    T = env_data()["Temperature"]+273.15 #Convert temperature from celsius to kelvin for this calculation
    air_density = -(PDA / (287.058*T))+(VP / (461.495*T))

    #----

    #--Calculate the deceleration due to drag--

    mass = float(mass)/15432 #Convert the mass in grains to mass in kg for the calculation

    #Initialise relevant variables
    #Value of pi
    pi = math.pi
    #Area
    A = (pi*math.pow((float(calibre)/1000),2)*0.25)/10

    #Use the relevant formula to calculate force due to drag and therefore the deceleration
    force_drag = (float(BC)*air_density*A*math.pow(float(velocity),2))/2
    deceleration_from_drag = force_drag/mass

    #-----

    #--Calculate time of flight--

    #Creates an array of coefficients of the quadratic that in terms of t (time) which needs to be solved
    coefficients = [(deceleration_from_drag/2), float(velocity), -(float(distance_to_target))]

    #Solves the quadratic and takes the larger of the 2 solutions of the quadratic (since one is negative but time
    #cannot be negative)
    time_of_flight = max(numpy.roots(coefficients))

    #-----

    #--Calculate the bullet drop--
    #Calculates the vertical bullet drop in metres
    bullet_drop = 0.5*9.81*math.pow(time_of_flight,2)

    return bullet_drop

def MOA_Adjustment(distance_to_target,bullet_drop):
    #Converts distance to target into yards for MOA calculation
    dist_yards = float(distance_to_target)*1.094
    #Converts bullet drop into inches for MOA calculation
    drop_inches = bullet_drop*39.37
    #Calculates the MOA at the distance input
    MOA_at_dist = (dist_yards*1.047) / 100
    #Calculates the adjustment that needs to be made in MOA
    MOA_Adjustment = round((drop_inches/MOA_at_dist),2)
    return float(MOA_Adjustment)

def MILRAD_Adjustment(MOA_Adjustment):
    #Convert MOA adjustment value to Milliradians and return it
    return round(float(MOA_Adjustment)*((1000*math.pi)/(10800)),2)



