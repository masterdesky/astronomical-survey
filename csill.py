###############################################################################################
####  ______             __  __  __    __                               ______  ______     ####
##   /      \           |  \|  \|  \   \_\                              |      \|      \     ##
##  |  $$$$$$\  _______  \$$| $$| $$  ______    _______  ________        \$$$$$$ \$$$$$$     ##
##  | $$   \$$ /       \|  \| $$| $$ /      \  /       \|        \        | $$    | $$       ##
##  | $$      |  $$$$$$$| $$| $$| $$|  $$$$$$\|  $$$$$$$ \$$$$$$$$        | $$    | $$       ##
##  | $$   __  \$$    \ | $$| $$| $$| $$    $$ \$$    \   /    $$         | $$    | $$       ##
##  | $$__/  \ _\$$$$$$\| $$| $$| $$| $$$$$$$$ _\$$$$$$\ /  $$$$_        _| $$_  _| $$_      ##
##   \$$    $$|       $$| $$| $$| $$ \$$     \|       $$|  $$    \      |   $$ \|   $$ \     ##
##    \$$$$$$  \$$$$$$$  \$$ \$$ \$$  \$$$$$$$ \$$$$$$$  \$$$$$$$$       \$$$$$$ \$$$$$$     ##
##                                            __                                             ##
##                                           / _|                                            ##
##                                          | |_ _ __ ___  _ __ ___                          ##
##                                          |  _| '__/ _ \| '_ ` _ \                         ##
##              _______            __       | | | | | (_) | | | | | |                        ##
##             /       \          /  |      |_| |_|  \___/|_| |_| |_|                        ##
##             $$$$$$$  | ______  $$ |  ______    ______    ______                           ##
##             $$ |__$$ |/      \ $$ | /      \  /      \  /      \                          ##
##             $$    $$/ $$$$$$  |$$ |/$$$$$$  |/$$$$$$  |/$$$$$$  |                         ##
##             $$$$$$$/  /    $$ |$$ |$$    $$ |$$    $$ |$$    $$ |                         ##
##             $$ |     /$$$$$$$ |$$ |$$$$$$$$/ $$$$$$$$/ $$$$$$$$/                          ##
##             $$ |     $$    $$ |$$ |$$       |$$       |$$       |                         ##
##             $$/       $$$$$$$/ $$/  $$$$$$$/  $$$$$$$/  $$$$$$$/                          ##
##                                                                                           ##
##                                                                                           ##
##        > Conversion Between Coordinate Systems                                            ##
##        > Calculate Geographical Distances                                                 ##
##        > Convert Sidereal Time/Local Sidereal Time (ST, LST)                              ##
##        > Calculate Twilights' Correct Datetimes on Specific Locations                     ##
####                                                                                       ####
###############################################################################################
####                                                                                       ####
##        USED LEGENDS AND LABELS:                                                           ##
##                                                                                           ##
##        φ: Latitude                                                                        ##
##        λ: Longitude                                                                       ##
##        H: Local Hour Angle in Degrees                                                     ##
##        t: Local Hour Angle in Hours                                                       ##
##        S: Local Sidereal Time                                                             ##
##        A: Azimuth at Horizontal Coords                                                    ##
##        m: Altitude at Horizontal Coords                                                   ##
##        δ: Declination at Equatorial Coords                                                ##
##        α: Right Ascension at Equatorial Coords                                            ##
####                                                                                       ####
###############################################################################################

# If libraries are not installed, decomment and run
# pip install matplotlib --upgrade
# pip install numpy --upgrade

import math
import matplotlib.pyplot as plt
import numpy as np


######## CONSTANTS FOR CALCULATIONS ########

# Earth's Radius
R = 6378e03

# Lenght of 1 Solar Day = 1.002737909350795 Sidereal Days
# It is Labeled as a dS/dm Quotient
# We Simply Label It as dS
dS = 1.002737909350795

# Predefined Coordinates of Some Notable Cities
Beijing = [39.9042,116.4074]
Budapest = [47.4979,19.0402]
Brussels = [50.8503,4.3517]
Debrecen = [47.5316,21.6273]
Gyor = [47.6875,17.6504]
Jerusalem = [31.7683,35.2137]
Kecskemet = [46.8964,19.6897]
Mako = [46.2219,20.4809]
Miskolc = [48.1035,20.7784]
NewYork = [40.7128,-74.0060]
Pecs = [46.0727,18.2323]
Rio = [-22.9068,-43.1729]
Szeged = [46.2530,20.1414]
Szekesfehervar = [47.1860,18.4221]
Tokyo = [35.6895,139.6917]
Washington = [47.7511,-120.7401]
Zalaegerszeg = [46.8417,16.8416]


######## UTILITY FUNCTIONS ########

# Normalization with Bound [0,NonZeroBound]
def NormalizeZeroBounded(Parameter, NonZeroBound):

    Parameter = Parameter - (int(Parameter / NonZeroBound) * NonZeroBound)

    return(Parameter)

# Normalization Between to [-π/2,+π/2]
def NormalizeSymmetricallyBoundedPI(Parameter):
    
    if(Parameter <= -360 or Parameter >= 360):
        Parameter = NormalizeZeroBounded(Parameter, 360)

    if(Parameter < 0):
        if(Parameter < -90 and Parameter >= -270):
            Parameter = - (Parameter + 180)
        elif(Parameter < -270 and Parameter >= -360):
            Parameter = Parameter + 360

    elif(Parameter > 0):
        if(Parameter > 90 and Parameter <= 270):
            Parameter = - (Parameter - 180)
        elif(Parameter > 270 and Parameter <= 360):
            Parameter = Parameter - 360

    return(Parameter)

# Normalization Between to [-π,+π]
def NormalizeSymmetricallyBoundedPI_2(Parameter):

    if(Parameter <= -360 or Parameter >= 360):
        Parameter = NormalizeZeroBounded(Parameter, 360)

    if(Parameter <= -180 or Parameter >= 180):
        Parameter = 180 - Parameter

    return(Parameter)


# Convert String Input to Variable for Geographic Distance Calculation
def ExtractFromVars(ChoosenCity):

    Latitude = ChoosenCity[0]
    Longitude = ChoosenCity[1]

    return(Latitude, Longitude)


######## 1. CONVERSION OF COORDINATE SYSTEMS ########

# 1. Horizontal to Equatorial I
def HorToEquI(Latitude, Altitude, Azimuth, LocalSiderealTime=None):

    # Initial Data Normalization
    # Latitude: [-π,+π]
    # Altitude: [-π/2,+π/2]
    # Azimuth: [0,2π]
    # Local Sidereal Time: [0,24h]
    Latitude = NormalizeSymmetricallyBoundedPI_2(Latitude)
    Altitude = NormalizeSymmetricallyBoundedPI_2(Altitude)
    Azimuth = NormalizeZeroBounded(Azimuth, 360)
    LocalSiderealTime = NormalizeZeroBounded(LocalSiderealTime, 24)
    
    # Calculate Declination (δ)
    # sin(δ) = sin(m) * sin(φ) + cos(m) * cos(φ) * cos(A)
    Declination =  math.degrees(math.asin(
                   math.sin(math.radians(Altitude)) * math.sin(math.radians(Latitude)) +
                   math.cos(math.radians(Altitude)) * math.cos(math.radians(Latitude)) * math.cos(math.radians(Azimuth))))
    # Normalize result for Declination [-π/2,+π/2]
    Declination = NormalizeSymmetricallyBoundedPI(Declination)

    # Calculate Local Hour Angle in Degrees (H)
    # sin(H) = - sin(A) * cos(m) / cos(δ)
    LocalHourAngleDegrees = math.degrees(math.asin(
                            - math.sin(math.radians(Azimuth)) * math.cos(math.radians(Altitude)) / math.cos(math.radians(Declination))))
    # Normalize result [0,+2π]
    LocalHourAngleDegrees = NormalizeZeroBounded(LocalHourAngleDegrees, 360)
    # Convert to hours from angles (H -> t)
    LocalHourAngle = LocalHourAngleDegrees / 15

    if(LocalSiderealTime != None):
        # Calculate Right Ascension (α)
        # α = S – t
        RightAscension = LocalSiderealTime - LocalHourAngle
    else:
        RightAscension = None

    return(Declination, LocalHourAngle, RightAscension)

# 2. Horizontal to Equatorial II
def HorToEquII(Latitude, Altitude, Azimuth, LocalSiderealTime):

    # First Convert Horizontal to Equatorial I Coordinates
    Declination, LocalHourAngle, RightAscension = HorToEquI(Latitude, Altitude, Azimuth, LocalSiderealTime)

    # Convert Equatorial I to Equatorial II
    LocalSiderealTime = LocalHourAngle + RightAscension

    return(Declination, LocalSiderealTime)


# 3. Equatorial I to Horizontal
def EquIToHor(Latitude, RightAscension, Declination, LocalSiderealTime, LocalHourAngle):

    # Initial data normalization
    # Latitude: [-π,+π]
    # Right Ascension: [0h,24h]
    # Declination: [-π/2,+π/2]
    Latitude = NormalizeSymmetricallyBoundedPI_2(Latitude)
    RightAscension = NormalizeZeroBounded(RightAscension, 24)
    Declination = NormalizeSymmetricallyBoundedPI(Declination)  

    if(LocalHourAngle == None):
        # Calculate Local Hour Angle in Hours (t)
        # t = S - α
        LocalHourAngle = LocalSiderealTime - RightAscension
    # Convert to angles from hours (t -> H)
    LocalHourAngleDegrees = LocalHourAngle * 15

    # Calculate Altitude (m)
    # sin(m) = sin(δ) * sin(φ) + cos(δ) * cos(φ) * cos(H)
    Altitude = math.degrees(math.asin(
               math.sin(math.radians(Declination)) * math.cos(math.radians(Latitude)) + 
               math.cos(math.radians(Declination)) * math.cos(math.radians(Latitude)) * math.cos(math.radians(LocalHourAngleDegrees))))

    # Calculate Azimuth (A)
    # sin(A) = - sin(H) * cos(δ) / cos(m)
    Azimuth = math.degrees(math.asin(
              - math.sin(math.radians(LocalHourAngleDegrees)) * math.cos(math.radians(Declination)) / math.cos(math.radians(Altitude))))

    return(Altitude, Azimuth)

# 4. Equatorial I to Equatorial II
def EquIToEquII(RightAscension, LocalHourAngle):
    
    LocalSiderealTime = LocalHourAngle + RightAscension

    return(LocalSiderealTime)

# 5. Equatorial II to Equatorial I
def EquIIToEquI(RightAscension, LocalSiderealTime):

    # Calculate Right Ascension or Local Sidereal Time
    if(RightAscension != None and LocalSiderealTime == None):
        LocalHourAngle = LocalSiderealTime - RightAscension

    elif(RightAscension == None and LocalSiderealTime != None):
        RightAscension = LocalSiderealTime - LocalHourAngle

    return(RightAscension, LocalHourAngle)

# 6. Equatorial II to Horizontal
def EquIIToHor(Latitude, RightAscension, Declination, LocalSiderealTime):

    RightAscension, LocalHourAngle = EquIIToEquI(RightAscension, LocalSiderealTime)
    Altitude, Azimuth = EquIToHor(Latitude, RightAscension, Declination, LocalHourAngle, LocalSiderealTime)

    return(Altitude, Azimuth)


######## 2. GEOGRAPHICAL DISTANCE ########

# Calculate distances between coordinates
def GeogDistCalc(Latitude1, Latitude2, Longitude1, Longitude2):
    
    # Initial data normalization
    # Latitude: [-π,+π]
    # Longitude: [0,+2π]
    Latitude1 = NormalizeSymmetricallyBoundedPI(Latitude1)
    Latitude2 = NormalizeSymmetricallyBoundedPI(Latitude2)
    Longitude1 = NormalizeZeroBounded(Longitude1, 360)
    Longitude2 = NormalizeZeroBounded(Longitude2, 360)

    # Haversine formula:
    # Step 1.: hav_1 = (sin((φ2 - φ1) / 2))^2 + cos(φ1) ⋅ cos(φ2) ⋅ (sin((λ2 - λ1) / 2))^2
    # Step 2.: hav_2 = 2 * atan2(sqrt(hav_1),sqrt(1 − hav_1))
    # Step 3.: d = R * hav_2

    # Step 1
    hav_1 = ((math.sin(math.radians(Latitude2 - Latitude1) / 2))**2 +
        (math.cos(math.radians(Latitude1)) * math.cos(math.radians(Latitude2)) * (math.sin(math.radians(Longitude2 - Longitude1) / 2))**2))

    # Step 2
    hav_2 = 2 * math.atan2(math.sqrt(hav_1), math.sqrt(1-hav_1))

    # Step 3
    Distance = R * hav_2

    return(Distance)


# Calculate distances between choosen cities
def GeogDistCityCalc(Latitude1, Latitude2, Longitude1, Longitude2):
    
    # Initial data normalization
    # Latitude: [-π,+π]
    # Longitude: [0,+2π]
    Latitude1 = NormalizeSymmetricallyBoundedPI(Latitude1)
    Latitude2 = NormalizeSymmetricallyBoundedPI(Latitude2)
    Longitude1 = NormalizeZeroBounded(Longitude1, 360)
    Longitude2 = NormalizeZeroBounded(Longitude2, 360)

    # Haversine formula:
    # Step 1.: hav_1 = (sin((φ2 - φ1) / 2))^2 + cos(φ1) ⋅ cos(φ2) ⋅ (sin((λ2 - λ1) / 2))^2
    # Step 2.: hav_2 = 2 * atan2(sqrt(hav_1),sqrt(1 − hav_1))
    # Step 3.: d = R * hav_2

    # Step 1
    hav_1 = ((math.sin(math.radians(Latitude2 - Latitude1) / 2))**2 +
        (math.cos(math.radians(Latitude1)) * math.cos(math.radians(Latitude2)) * (math.sin(math.radians(Longitude2 - Longitude1) / 2))**2))

    # Step 2
    hav_2 = 2 * math.atan2(math.sqrt(hav_1), math.sqrt(1-hav_1))

    # Step 3
    Distance = R * hav_2

    return(Distance)


######## 3. GEOGRAPHICAL DISTANCE ########

#########################################

######## MAIN ########


print(">>> Csillész II Problem Solver Program v0.8\n")

while(True):
    
    print(">> MAIN MENU <<")
    print("(1) Coordinate System Conversion")
    print("(2) Geographical Distances")
    print("(3) Local Sidereal Time")
    print("(4) Datetimes of Twilights")
    print("(Q) Quit Program\n")
    
    # Choose mode by user input
    mode = input("> Choose a mode and press enter...:")
    
    print('\n')
    
    if(mode == '1'):
        while(True):
            print(">> Coordinate System Conversion")
            print(">> Please choose which coordinate system conversion you'd like to make!")
            print("(1) Horizontal to Equatorial I")
            print("(2) Horizontal to Equatorial II")
            print("(3) Equatorial I to Horizontal")
            print("(4) Equatorial I to Equatorial II")
            print("(5) Equatorial II to Equatorial I")
            print("(6) Equatorial II to Horizontal")
            print("(Q) Quit to Main Menu")
            CoordMode = input("> Choose a number and press enter...:")

            if(CoordMode == '1'):
                print(">> Conversion from Horizontal to Equatorial I Coordinate System")
                print(">> Give Parameters: ")
                Latitude = float(input("> Latitude (φ): "))
                Altitude = float(input("> Altitude (m): "))
                Azimuth = float(input("> Azimuth (A): "))
                LocalSiderealTime = float(input("> Local Sidereal Time (S): "))

                Declination, LocalHourAngle, RightAscension = HorToEquI(Latitude, Altitude, Azimuth, LocalSiderealTime)

                # Print Results
                print("\n> Calculated parameters:")
                
                declinmsg = "- Declination (δ): {0}°"
                hourangmsg = "- Local Hour Angle (t): {0} h"
                print(declinmsg.format(Declination))
                print(hourangmsg.format(LocalHourAngle))
                
                if(LocalSiderealTime != None):
                    RAmsg = "- Right Ascension (α):  {0} h"
                    print(RAmsg.format(RightAscension))

                print('\n')

            elif(CoordMode == '2'):
                print(">> Conversion from Horizontal to Equatorial II Coordinate System")
                print(">> Give Parameters: ")
                Latitude = float(input("> Latitude (φ): "))
                Altitude = float(input("> Altitude (m): "))
                Azimuth = float(input("> Azimuth (A): "))
                LocalSiderealTime = float(input("> Local Sidereal Time (S): "))

                Declination, LocalSiderealTime = HorToEquII(Latitude, Altitude, Azimuth, LocalSiderealTime)

                # Print Results
                print("\n> Calculated Parameters:")
                
                declinmsg = "- Declination (δ): {0}°"
                sidermsg = "- Local Sidereal Time (S):  {0}°"
                print(declinmsg.format(Declination))
                print(sidermsg.format(LocalSiderealTime))
                print('\n')
                
            elif(CoordMode == '3'):
                print(">> Conversion from Equatorial I to Horizontal Coordinate System")
                print(">> Give Parameters: ")
                Latitude = float(input("> Latitude (φ): "))
                RightAscension = float(input("> Right Ascension (α): "))
                Declination = float(input("> Declination (δ): "))
                LocalSiderealTime = float(input("> Local Sidereal Time (S): "))
                LocalHourAngle = float(input("> Local Hour Angle (t): "))

                Altitude, Azimuth = EquIToHor(Latitude, RightAscension, Declination, LocalSiderealTime, LocalHourAngle)

                # Print Results
                print("\n> Calculated Parameters:")
                
                altitmsg = "- Altitude (m): {0}°"
                azimmsg = "- Azimuth (A):  {0}°"
                print(altitmsg.format(Altitude))
                print(azimmsg.format(Azimuth))
                print('\n')

            elif(CoordMode == '4'):
                print(">> Conversion from Equatorial I to Equatorial II Coordinate System")
                print(">> Give Parameters: ")
                Latitude = float(input("> Latitude (φ): "))
                RightAscension = float(input("> Right Ascension (α): "))
                Declination = float(input("> Declination (δ): "))
                LocalHourAngle = float(input("> Local Hour Angle in Hours (t): "))
                LocalSiderealTime = float(input("> Local Sidereal Time (S): "))

                LocalSiderealTime = EquIToEquII(RightAscension, LocalHourAngle)

                # Print Results
                print("\n> Calculated Parameters:")
                
                latmsg = "- Latitude (φ): {0}°"
                declinmsg = "- Declination (δ): {0}°"
                sidermsg = "- Local Sidereal Time (S):  {0}°"
                print(latmsg.format(Latitude))
                print(declinmsg.format(Declination))
                print(sidermsg.format(LocalSiderealTime))
                print('\n')
                                    

            elif(CoordMode == '5'):
                print(">> Conversion from Equatorial II to Equatorial I")
                print(">> Give Parameters: ")
                RightAscension = float(input("> Right Ascension (α): "))
                LocalSiderealTime = float(input("> Local Sidereal Time (S): "))

                EquIIToEquI(RightAscension, LocalSiderealTime)

                # Print Results
                print("\n> Calculated parameters:")
                
                declinmsg = "- Declination (δ): {0}°"
                hourangmsg = "- Local Hour Angle (t): {0} h"
                print(declinmsg.format(Declination))
                print(hourangmsg.format(LocalHourAngle))
                
                if(LocalSiderealTime != None):
                    RAmsg = "- Right Ascension (α):  {0} h"
                    print(RAmsg.format(RightAscension))
                
                print('\n')

            elif(CoordMode == '6'):
                print(">> Conversion from Equatorial II to Horizontal")
                print(">> Give Parameters: ")
                Latitude = float(input("> Latitude (φ): "))
                RightAscension = float(input("> Right Ascension (α): "))
                Declination = float(input("> Declination (δ): "))
                LocalHourAngle = float(input("> Local Hour Angle (t): "))
                LocalSiderealTime = float(input("> Local Sidereal Time (S): "))
                
                Altitude, Azimuth = EquIIToHor(Latitude, RightAscension, Declination, LocalSiderealTime)
                
                # Print Results
                print("> Calculated Parameters:")
                
                altitmsg = "- Altitude (m): {0}°"
                azimmsg = "- Azimuth (A):  {0}°"
                print(altitmsg.format(Altitude))
                print(azimmsg.format(Azimuth))
                print('\n')

            elif(CoordMode == 'Q' or CoordMode == 'q'):
                break

            else:
                print("Invalid option! Try again!\n")
    
    elif(mode == '2'):
        while(True):
            print(">> Geographical Distance Calculator\n")
            print(">> Please choose a mode you'd like to use!")
            print("(1) Positional Coordinates from User Input")
            print("(2) Positional Coordinates of Predefined Cities")
            print("(Q) Quit to Main Menu")
            DistMode = input("> Choose a mode and press enter...:")

            print()
            if(DistMode == '1'):
                print(">> Calculate Distance from give Coordinates\n")
                print(">> Give Parameters: ")
                Latitude1 = float(input("> Latitude #1 (φ1): "))
                Longitude1 = float(input("> Longitude #1 (λ1): "))
                Latitude2 = float(input("> Latitude #2 (φ2): "))
                Longitude2 = float(input("> Longitude #2 (λ2): "))

                Distance = GeogDistCalc(Latitude1, Latitude2, Longitude1, Longitude2)

                distmsg = "\n>>> The Geographical Distance Between\n>>> {0}°,{1}°\n>>> and\n>>> {2}°,{3}°\n>>> is\n>>> {4} m\n"
                print(distmsg.format(Latitude1,Longitude1,Latitude2,Longitude2, Distance))
            
            elif(DistMode == '2'):
                print(">> Calculate Distance of Choosen Predefined Cities\n")
                print(">> Write the Name on the Input of Two Choosen Cities!")
                City1 = input("City #1: ")
                City2 = input("City #2: ")

                # Convert Input String to Usable Variable
                # Only Predefined Variable Names Could Be Used
                # Which are Listed from Line 30 (Lists with City Names)
                VarsCity1 = vars()[(City1)]
                VarsCity2 = vars()[(City2)]

                Latitude1, Longitude1 = ExtractFromVars(VarsCity1)
                Latitude2, Longitude2 = ExtractFromVars(VarsCity2)

                Distance = GeogDistCityCalc(Latitude1, Latitude2, Longitude1, Longitude2)

                distmsg = "\n>>> The Geographical Distance Between\n>>> {0} and {1} is\n>>> {2} m\n"
                print(distmsg.format(City1, City2, Distance))
            
            elif(DistMode == 'Q' or DistMode == 'q'):
                break

            else:
                print("Invalid option! Try again!")
        
    elif(mode == '3'):
        while(True):
            print(">> Local Sidereal Time Calculator")
            print(">> Please choose a mode you'd like to use!")
            print("(1) Positional Coordinates from User Input")
            print("(2) Positional Coordinates of Predefined Cities")
            print("(Q) Quit to Main Menu")
            DistMode = input("> Choose a mode and press enter...:")

            print()
            if(DistMode == '1'):
                print(">> Calculate Distance from give Coordinates\n")
                print(">> Give Parameters: ")
                Latitude = float(input("> Latitude (φ): "))
                Longitude = float(input("> Longitud (λ): "))

                UnitedDateTime, LocalSiderealTime = SiderealFromInput(Latitude, Longitude, UnitedTime)

                sidmsg = "\n>>> The Local Sidereal Time\n>>> at {0} UT, at location\n>>> {1}°,{2}° is\n>>> {3}"
                print(distmsg.format(UnitedDateTime, Latitude, Longitude, LocalSiderealTime))
            
            elif(DistMode == '2'):
                print(">> Calculate from the Coordinates of a Predefined City\n")
                print(">> Write the Name on the Input of the Choosen City!")
                City = input("City's name: ")

                # Convert Input String to Usable Variable
                # Only Predefined Variable Names Could Be Used
                # Which are Listed from Line 30 (Lists with City Names)
                VarsCity = vars()[(City)]

                Latitude1, Longitude1 = ExtractFromVars(VarsCity1)
                Latitude2, Longitude2 = ExtractFromVars(VarsCity2)

                Distance = GeogDistCityCalc(Latitude1, Latitude2, Longitude1, Longitude2)

                distmsg = "\n>>> The Geographical Distance Between\n>>> {0} and {1} is\n>>> {2} m\n"
                print(distmsg.format(City1, City2, Distance))

            elif(DistMode == 'Q' or DistMode == 'q'):
                break

            else:
                print("Invalid option! Try again!")

    elif(mode == '4'):
        while(True):
            print(">> Calculate Datetimes of Twilights at Specific Location")
            print(">> Give Parameters")

    elif(mode == 'Q' or mode == 'q'):
        print("All Rights Reserved to Balage Paliere Co.!")
        exit()
        
    else:
        print("Invalid option! Try again!")