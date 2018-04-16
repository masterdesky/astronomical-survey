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
# H: Local Hour Angle                                                                       #
# t: Local Sidereal Time
# A: Azimuth at Horizontal Coords                                                           #
# a: Altitude at Horizontal Coords                                                          #
# δ: Declination at Equatorial I
# α: Right Ascension at Equatorial I

import sys
import math
import matplotlib.pyplot as plt
import numpy as np


######## UTILITY FUNCTIONS ########

# Normalization with bound [0,NonZeroBound]
def ZeroBoundedNormalization(Parameter, NonZeroBound):

    Parameter = Parameter - (int(Parameter / NonZeroBound) * NonZeroBound)

    return(Parameter)

# Normalization between to [-π/2,+π/2]
def NormalizeDeclinations(Declination):
    
    if(Declination <= -360 or Declination >= 360):
        Declination = ZeroBoundedNormalization(Declination, 360)

    if(Declination < 0):
        if(Declination < -90 and Declination >= -270):
            Declination = - (Declination + 180)
        elif(Declination < -270 and Declination >= -360):
            Declination = Declination + 360

    elif(Declination > 0):
        if(Declination > 90 and Declination <= 270):
            Declination = - (Declination - 180)
        elif(Declination > 270 and Declination <= 360):
            Declination = Declination - 360

    return(Declination)


######## CONVERSIONS ########

# Horizontal to Equatorial I
def HorToEquI(Latitude, Altitude, Azimuth, LocalSiderealTime=None):

    # Initial data normalization
    # Latitude: [-π,+π]
    # Altitude: []
    # Azimuth: []
    # Local Sidereal Time: [0,24h]

    # Calculate Declination (δ)
    # sin(δ) = sin(a) * sin(φ) + cos(a) * cos(φ) * cos(A)
    Declination =  math.degrees(math.asin(
                    math.sin(math.radians(Altitude)) * math.sin(math.radians(Latitude)) +
                    math.cos(math.radians(Altitude)) * math.cos(math.radians(Latitude)) * math.cos(math.radians(Azimuth))))
    # Normalize result for Declination [-π/2,+π/2]
    Declination = NormalizeDeclinations(Declination)

    # Calculate Local Hour Angle (H)
    # sin(H) = - sin(A) * cos(a) / cos(δ)
    LocalHourAngleDegrees = math.degrees(math.asin(
                            - math.sin(math.radians(Azimuth)) * math.cos(math.radians(Altitude)) / math.cos(math.radians(Declination))))
    # Normalize result [0,+2π]
    LocalHourAngleDegrees = ZeroBoundedNormalization(LocalHourAngleDegrees, 360)
    # Convert to hours from angles
    LocalHourAngle = LocalHourAngleDegrees / 15

    if(LocalSiderealTime != None):
        # Calculate Right Ascension (α)
        # α = t – H
        RightAscension = LocalSiderealTime - LocalHourAngle

    print(">>> Conversion from Horizontal to Equatorial I Coordinate System\n")
    print("> Calculated parameters:")
    
    declinmsg = "- Declination (δ): {0}°"
    print(declinmsg.format(Declination))
    
    if(LocalSiderealTime != None):
        RAmsg = "- Right Ascension (α):  {0} h"
        print(RAmsg.format(RightAscension))

# Equatorial I to Horizontal
def EquIToHor(Latitude, RightAscension, Declination, LocalSiderealTime):

    # Initial data normalization
    # Latitude: [-π,+π]
    # Right Ascension: [0h,24h]
    # Declination: [-π/2,+π/2]
    Latitude = None
    RightAscension = ZeroBoundedNormalization(RightAscension, 24)
    Declination = NormalizeDeclinations(Declination)
    

    # Calculate Local Hour Angle (H)
    # H = t - α
    LocalHourAngle = LocalSiderealTime - RightAscension
    # Convert to angles from hours
    LocalHourAngleDegrees = LocalHourAngle * 15

    # Calculate Altitude (a)
    # sin(a) = sin(δ) * sin(φ) + cos(δ) * cos(φ) * cos(H)
    Altitude = math.degrees(math.asin(
               math.sin(math.radians(Declination)) * math.cos(math.radians(Latitude)) + 
               math.cos(math.radians(Declination)) * math.cos(math.radians(Latitude)) * math.cos(math.radians(LocalHourAngleDegrees))))

    # Calculate Azimuth (A)
    # sin(A) = - sin(H) * cos(δ) / cos(a)
    Azimuth = math.degrees(math.asin(
              - math.sin(math.radians(LocalHourAngleDegrees)) * math.cos(math.radians(Declination)) / math.cos(math.radians(Altitude))))

    print(">>> Conversion from Equatorial I to Horizontal Coordinate System\n")
    print("> Calculated parameters:")
    
    altitmsg = "- Altitude (a): {0}°"
    azimmsg = "- Azimuth (A):  {0}°"
    print(altitmsg.format(Altitude))
    print(azimmsg.format(Azimuth))


######## MAIN ########

def main():

    print('''
        >>> Csillész II Problem Solver Program v1.0\n
    ''')

    print('''
        > Please choose a mode!\n
        
        1. Coordinate System Conversion
        2. Geographical Distances
        3. Local Sidereal Time
        4. Different Twilight Datetimes\n
    ''')
    while(True):
        mode = input('''
            > Choose a number and press enter...: 
        ''')

        if(mode == 1):
            while(True):
                CoordMode = input('''
                    > Please choose which coordinate system conversion you'd like to make!\n
                    
                    1. Horizontal to Equatorial I
                    2. Equatorial I to Horizontal
                ''')
                if(CoordMode == 1):
                    print(">> Parameters: ")
                    Latitude = input("> Latitude (φ): ")
                    Altitude = input("> Altitude (a): ")
                    Azimuth = input("> Azimuth (A): ")
                    LocalSiderealTime = input("> Local Sidereal Time (t): ")
                    HorToEquI(Latitude, Altitude, Azimuth, LocalSiderealTime)
                    break

                elif(CoordMode == 2):
                    print(">> Parameters: ")
                    Latitude = input("> Latitude (φ): ")
                    RightAscension = input("> Right Ascension (α): ")
                    Declination = input("> Declination (δ): ")
                    LocalSiderealTime = input("> Local Sidereal Time (t): ")
                    EquIToHor(Latitude, RightAscension, Declination, LocalSiderealTime)
                    break

                else:
                    print("Invalid option!")
            break
        
        elif(mode == 2):
            while(True):
                break