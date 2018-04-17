#############################################################################################
#                           Csillész II Problem Solver Program                              #
#                                                                                           #
#                           > Conversion of Coordinate Systems                              #
#                           > Geographical Distances                                        #
#                           > Sidereal Time/Local Sidereal Time (ST, LST)                   #
#                           > Calculate Twilights' Correct Datetimes                        #
#                                                                                           #
#############################################################################################
# # LEGENDS                                                                                 #
# φ: Latitude                                                                               #
# λ: Longitude                                                                              #
# H: Local Hour Angle in Degrees
# t: Local Hour Angle in Hours                                                                       #
# S: Local Sidereal Time
# A: Azimuth at Horizontal Coords                                                           #
# m: Altitude at Horizontal Coords                                                          #
# δ: Declination at Equatorial Coords
# α: Right Ascension at Equatorial Coords

import math
#import matplotlib.pyplot as plt
#import numpy as np


######## UTILITY FUNCTIONS FOR NORMALIZATION ########

# Normalization with bound [0,NonZeroBound]
def NormalizeZeroBounded(Parameter, NonZeroBound):

    Parameter = Parameter - (int(Parameter / NonZeroBound) * NonZeroBound)

    return(Parameter)

# Normalization between to [-π/2,+π/2]
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

# Normalization between to [-π,+π]
def NormalizeSymmetricallyBoundedPI_2(Parameter):

    if(Parameter <= -360 or Parameter >= 360):
        Parameter = NormalizeZeroBounded(Parameter, 360)

    if(Parameter <= -180 or Parameter >= 180):
        Parameter = 180 - Parameter

    return(Parameter)


######## 1. CONVERSION OF COORDINATE SYSTEMS ########

# 1. Horizontal to Equatorial I
def HorToEquI(Latitude, Altitude, Azimuth, LocalSiderealTime=None):

    # Initial data normalization
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
def HorToEquII(Latitude, Altitude, Azimuth, LocalSiderealTime=None):

    Declination, LocalHourAngle, RightAscension = HorToEquI(Latitude, Altitude, Azimuth, LocalSiderealTime=None)



    return()


# 3. Equatorial I to Horizontal
def EquIToHor(Latitude, RightAscension, Declination, LocalHourAngle, LocalSiderealTime):

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
def EquIToEquII(Latitude, RightAscension, Declination, LocalHourAngle):
    
    LocalSiderealTime = LocalHourAngle + RightAscension

    return(Latitude, RightAscension, Declination, LocalSiderealTime)

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
    EquIToHor(Latitude, RightAscension, Declination, LocalHourAngle, LocalSiderealTime)




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
    
    # Constant : Earth's Radius
    R = 6378e03

    # Step 1
    a = ((math.sin(math.radians(Latitude2 - Latitude1) / 2))**2 +
        (math.cos(math.radians(Latitude1)) * math.cos(math.radians(Latitude2)) * (math.sin(math.radians(Longitude2 - Longitude1) / 2))**2))

    # Step 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # Step 3
    Distance = R * c

    distmsg = ">>> Calculate geographical distance between\n>>> {0}°,{1}° and\n >>>{2}°,{3}°:\n {4} m"
    print(distmsg.format(Latitude1,Longitude1,Latitude2,Longitude2, Distance))

#########################################

######## MAIN ########

def __main__():

    print(">>> Csillész II Problem Solver Program v0.5\n")

    while(True):
        
        print(">> Please choose a mode!\n")
        print("(1) Coordinate System Conversion")
        print("(2) Geographical Distances")
        print("(3) Local Sidereal Time")
        print("(4) Datetimes of Twilights\n")
        print("(Q) Quit Program")
        
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

                    Altitud, Azimuth = HorToEquI(Latitude, Altitude, Azimuth, LocalSiderealTime)

                    # Print Results
                    print("\n> Calculated parameters:")
                    
                    declinmsg = "- Declination (δ): {0}°"
                    print(declinmsg.format(Declination))

                    hourangmsg = "- Local Hour Angle (t): {0} h"
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

                    HorToEquII(Latitude, Altitude, Azimuth, LocalSiderealTime)

                    
                elif(CoordMode == '3'):
                    print(">> Conversion from Equatorial I to Horizontal Coordinate System")
                    print(">> Give Parameters: ")
                    Latitude = float(input("> Latitude (φ): "))
                    RightAscension = float(input("> Right Ascension (α): "))
                    Declination = float(input("> Declination (δ): "))
                    LocalHourAngle = float(input("> Local Hour Angle (t): "))
                    LocalSiderealTime = float(input("> Local Sidereal Time (S): "))

                    EquIToHor(Latitude, RightAscension, Declination, LocalHourAngle, LocalSiderealTime)

                    # Print Results
                    print("> Calculated Parameters:")
                    
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

                    EquIToEquII(Latitude, RightAscension, Declination, LocalHourAngle, LocalSiderealTime)

                    # Print Results
                    print("> Calculated Parameters:")
                    
                    altitmsg = "- Altitude (m): {0}°"
                    azimmsg = "- Azimuth (A):  {0}°"
                    print(altitmsg.format(Altitude))
                    print(azimmsg.format(Azimuth))
                                        

                elif(CoordMode == '5'):
                    print(">> Conversion from Equatorial II to Equatorial I")
                    print(">> Give Parameters: ")
                    RightAscension = float(input("> Right Ascension (α): "))
                    LocalSiderealTime = float(input("> Local Sidereal Time (S): "))

                    EquIIToEquI(RightAscension, LocalSiderealTime)

                elif(CoordMode == '6'):
                    print(">> Conversion from Equatorial II to Horizontal")
                    print(">> Give Parameters: ")
                    Latitude = float(input("> Latitude (φ): "))
                    RightAscension = float(input("> Right Ascension (α): "))
                    Declination = float(input("> Declination (δ): "))
                    LocalHourAngle = float(input("> Local Hour Angle (t): "))
                    LocalSiderealTime = float(input("> Local Sidereal Time (S): "))
                    
                    EquIIToHor(Latitude, RightAscension, Declination, LocalSiderealTime)
                    


                elif(CoordMode == 'Q'):
                    break

                else:
                    print("Invalid option!")
        
        elif(mode == '2'):
            while(True):
                print(">> Geographical Distance Calculator")
                print(">> Give Parameters: ")
                Latitude1 = float(input("> Latitude #1 (φ1): "))
                Longitude1 = float(input("> Longitude #1 (λ1): "))
                Latitude2 = float(input("> Latitude #2 (φ2): "))
                Longitude2 = float(input("> Longitude #2 (λ2): "))

                GeogDistCalc(Latitude1, Latitude2, Longitude1, Longitude2)
                break
            
        elif(mode == '3'):
            while(True):
                print(">> Local Sidereal Time Calculator")
                print(">> Give Parameters: ")

        elif(mode == '4'):
            while(True):
                print(">> Calculate Datetimes of Twilights at Specific Location")
                print(">> Give Parameters")
        else:
            print("Invalid option!")

######## RUN PROGRAM ########
__main__()