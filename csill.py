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
##        > Convert Sidereal Time/Local Mean Sidereal Time (S, LMST)                         ##
##        > Calculate Datetimes of Sunrises and Sunsets                                      ##
##        > Calculate Twilights' Correct Datetimes at Specific Locations                     ##
##        > Solve Csillész II End-Semester Homework with One Click                           ##
##       Future:                                                                             ##
##        > Draw Sun Analemma for a Choosen Year                                             ##
##        > Draw Sun's Path on Earth during a Choosen Year                                   ##
##        > Better Optimalization and Greater Precision                                      ##
####                                                                                       ####
###############################################################################################
####                                                                                       ####
##        USED LEGENDS AND LABELS:                                                           ##
##                                                                                           ##
##        φ: Latitude                                                                        ##
##        λ: Longitude                                                                       ##
##        H: Local Hour Angle in Degrees                                                     ##
##        t/LHA: Local Hour Angle in Hours                                                   ##
##        S/LMST: Local Mean Sidereal Time                                                   ##
##        S_0/GMST: Greenwich Mean Sidereal Time                                             ##
##        A: Azimuth at Horizontal Coords                                                    ##
##        m: Altitude at Horizontal Coords                                                   ##
##        δ: Declination at Equatorial Coords                                                ##
##        α/RA: Right Ascension at Equatorial Coords                                         ##
##        ε: Obliquity of the equator of the planet compared to the orbit of the planet      ##
##        Π: Perihelion of the planet, relative to the ecliptic and vernal equinox           ##
####                                                                                       ####
###############################################################################################

# If libraries are not installed, decomment and run
# pip install matplotlib --upgrade
# pip install numpy --upgrade

import math
# import matplotlib.pyplot as plt
# import numpy as np

# Current Version of the Csillész II Problem Solver
ActualVersion = 'v1.17'



################################################################
########                                                ########
########         CONSTANTS FOR CALCULATIONS             ########
########                                                ########
################################################################

# Earth's Radius
R = 6378e03

# Lenght of 1 Solar Day = 1.002737909350795 Sidereal Days
# It's Usually Labeled as dS/dm
# We Simply Label It as dS
dS = 1.002737909350795

# Predefined Coordinates of Some Notable Cities
# Format:
# "LocationName": [N Latitude (φ), E Longitude(λ)]
# Latitude: + if N, - if S
# Longitude: + if E, - if W
LocationDict = {
    "Amsterdam": [52.3702, 4.8952],
    "Athen": [37.9838, 23.7275],
    "Baja": [46.1803, 19.0111],
    "Beijing": [39.9042, 116.4074],
    "Berlin": [52.5200, 13.4050],
    "Budapest": [47.4979, 19.0402],
    "Budakeszi": [47.5136, 18.9278],
    "Budaors": [47.4621, 18.9530],
    "Brussels": [50.8503, 4.3517],
    "Debrecen": [47.5316, 21.6273],
    "Dunaujvaros": [46.9619, 18.9355],
    "Gyor": [47.6875, 17.6504],
    "Jerusalem": [31.7683, 35.2137],
    "Kecskemet": [46.8964, 19.6897],
    "London": [51.5074, -0.1278],
    "Mako": [46.2219, 20.4809],
    "Miskolc": [48.1035, 20.7784],
    "Nagykanizsa": [46.4590, 16.9897],
    "NewYork": [40.7128, -74.0060],
    "Paris": [48.8566, 2.3522],
    "Piszkesteto": [47.91806, 19.8942],
    "Pecs": [46.0727, 18.2323],
    "Rio": [-22.9068, -43.1729],
    "Rome": [41.9028, 12.4964],
    "Szeged": [46.2530, 20.1414],
    "Szeghalom": [47.0239, 21.1667],
    "Szekesfehervar": [47.1860, 18.4221],
    "Szombathely": [47.2307, 16.6218],
    "Tokyo": [35.6895, 139.6917],
    "Washington": [47.7511, -120.7401],
    "Zalaegerszeg": [46.8417, 16.8416]
}

# Predefined Equatorial I Coordinates of Some Notable Stellar Objects
# Format:
# "StarName": [Right Ascension (RA), Declination (δ)]
StellarDict = {
    "Achernar": [1.62857, -57.23675],
    "Aldebaran": [4.59868, 16.50930],
    "Algol": [3.13614, 40.95565],
    "AlphaAndromedae": [0.13979, 29.09043],
    "AlphaCentauri": [14.66014, -60.83399],
    "AlphaPersei": [3.40538, 49.86118],
    "Alphard": [9.45979, -8.65860],
    "Altair": [19.84639, 8.86832],
    "Antares": [16.49013, -26.43200],
    "Arcturus": [14.26103, 19.18222],
    "BetaCeti": [0.72649, -17.986605],
    "BetaUrsaeMajoris": [11.03069, 56.38243],
    "BetaUrsaeMinoris": [14.84509, 74.15550],
    "Betelgeuse": [5.91953, 7.407064],
    "Canopus": [6.39920, -52.69566],
    "Capella": [5.278155, 45.99799],
    "Deneb": [20.69053, 45.28028],
    "Fomalhaut": [22.960845, -29.62223],
    "GammaDraconis": [17.94344, 51.4889],
    "GammaVelorum": [8.15888, -47.33658],
    "M31": [0.712305,],
    "Polaris": [2.53030, 89.26411],
    "Pollux": [7.75526, 28.02620],
    "ProximaCentauri": [14.49526, -62.67949],
    "Rigel": [5.24230, -8.20164],
    "Sirius": [6.75248, -16.716116],
    "Vega": [18.61565, 38.78369],
    "VYCanisMajoris": [7.38287, -25.767565]
}

# Months' length int days, without leap day
MonthLengthList = [31,28,31,30,31,30,31,31,30,31,30,31]

# Months' length int days, with leap day
MonthLengthListLeapYear = [31,28,31,30,31,30,31,31,30,31,30,31]

# Constants for Planetary Orbits
# Format:
# "PlanetNameX": [X_0, X_1, X_2 ...] or [X_1, X_3, ..., X_E] etc.
# "PlanetNameOrbit": [Π, ε]
OrbitDict = {
    "Mercury": [],
    "Venus": [],
    "EarthJ": [0.0009, 0.0053, -0.0068, 1.0000000],
    "EarthC": [1.9148, 0.0200, 0.0003, 0.00000, 0.00000, 0.00000, 0.00000],
    "EarthM": [357.5291, 0.98560028],
    "EarthA": [-2.4657, 0.0529, -0.0014, 0.0003],
    "EarthD": [22.7908, 0.5991, 0.0492, 0.0003],
    "EarthH": [22.137, 0.599, 0.016],
    "EarthOrbit": [102.9373, 23.4393],
    "Mars": [],
    "Jupyter": [],
    "Saturn": [],
    "Neptunus": [],
    "Uranus": [],
    "Pluto": []
}


################################################################
########                                                ########
########               UTILITY FUNCTIONS                ########
########                                                ########
################################################################

# Normalization with Bound [0,NonZeroBound]
def NormalizeZeroBounded(Parameter, NonZeroBound):

    if(Parameter >= 0):
        Parameter = Parameter - (int(Parameter / NonZeroBound)) * NonZeroBound

    else:
        Parameter = Parameter + (abs(int(Parameter / NonZeroBound)) + 1) * NonZeroBound

    return(Parameter)

# Normalization Between to [-π,+π[
def NormalizeSymmetricallyBoundedPI(Parameter):

    if(Parameter <= -360 or Parameter >= 360):
        Parameter = NormalizeZeroBounded(Parameter, 360)

    if(Parameter <= -180 and Parameter >= -270):
        Parameter = 360 + Parameter
    
    elif(Parameter >= 180 and Parameter <= 270):
        Parameter = 180 - Parameter
    
    elif(Parameter > 270):
        Parameter = 360 - Parameter

    elif(Parameter < -270):
        Parameter = 360 + Parameter

    return(Parameter)

# Normalization Between to [-π/2,+π/2]
def NormalizeSymmetricallyBoundedPI_2(Parameter):
    
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

def NormalizeTimeParameters(Time, Year, Month, Day):

    Hours = int(Time)
    Minutes = int((Time - Hours) * 60)
    if(Minutes >= 60):
        NormalizeZeroBounded(Minutes, 60)
        Hours += 1
    if(Hours >= 24):
        NormalizeZeroBounded(Hours, 24)
        Day += 1
    if(Year%4 == 0 and (Year%100 != 0 or Year%400 == 0)):
        if(Day > MonthLengthListLeapYear[Month - 1]):
            Month =+ 1
    else:
        if(Day > MonthLengthList[Month - 1]):
            Month += 1
    if(Month > 12):
        Month = 1
        Year =+ 1

    Seconds = int((((Time - Hours) * 60) - Minutes) * 60)
    if(Seconds >= 60):
        Seconds = NormalizeZeroBounded(Seconds, 60)
        Minutes += 1
    if(Minutes >= 60):
        NormalizeZeroBounded(Minutes, 60)
        Hours += 1
    if(Hours >= 24):
        NormalizeZeroBounded(Hours, 24)
        Day += 1
    if(Year%4 == 0 and (Year%100 != 0 or Year%400 == 0)):
        if(Day > MonthLengthListLeapYear[Month - 1]):
            Month =+ 1
    else:
        if(Day > MonthLengthList[Month - 1]):
            Month += 1
    if(Month > 12):
        Month = 1
        Year =+ 1

    return(Time, Hours, Minutes, Seconds, Year, Month, Day)

# Normalization and Conversion of Local Time to United Time
def LTtoUT(LocalHours, LocalMinutes, LocalSeconds, DateYear, DateMonth, DateDay):
    
    # Calculate United Time
    LocalTime = LocalHours + LocalMinutes/60 + LocalSeconds/3600
    # Normalize LT
    LocalTime = NormalizeZeroBounded(LocalTime, 24)

    # Summer/Winter Saving time
    # Summer: March 26/31 - October 8/14 LT+1
    # Winter: October 8/14 - March 26/31 LT+0
    if((DateMonth > 3 and DateMonth < 10) or ((DateMonth == 3 and DateDay >=25) or (DateMonth == 10 and (DateDay >= 8 and DateDay <=14)))):
        UnitedTime = LocalTime - (int(Longitude/15) + 1)

    else:
        UnitedTime = LocalTime - int(Longitude/15)

    if(UnitedTime < 0):
        UnitedHours = int(NormalizeZeroBounded(UnitedTime, 24))
        UnitedDateDay = DateDay - 1
        if(UnitedDateDay <= 0):
            UnitedDateMonth = DateMonth - 1
            if(UnitedDateMonth == 0):
                UnitedDateMonth = 12
                UnitedDateYear = DateYear - 1
            # Leap year handling
            if(DateYear%4 == 0 and (DateYear%100 != 0 or DateYear%400 == 0)):
                UnitedDateDay = MonthLengthListLeapYear[UnitedDateMonth - 1]

            else:
                UnitedDateDay = MonthLengthList[UnitedDateMonth - 1]

    elif(UnitedTime >= 24):
        UnitedHours = int(NormalizeZeroBounded(UnitedTime, 24))
        UnitedDateDay = DateDay + 1
        if(DateYear%4 == 0 and (DateYear%100 != 0 or DateYear%400 == 0)):
            if(UnitedDateDay > MonthLengthListLeapYear[DateMonth - 1]):
                UnitedDateMonth = DateMonth + 1
            else:
                UnitedDateMonth = DateMonth

        else:
            if(UnitedDateDay > MonthLengthList[DateMonth - 1]):
                UnitedDateMonth = DateMonth + 1
            else:
                UnitedDateMonth = DateMonth

        if(UnitedDateMonth > 12):
            UnitedDateMonth = 1
            UnitedDateYear = DateYear + 1
        else:
            UnitedDateYear = DateYear

    else:
        UnitedDateYear = DateYear
        UnitedDateMonth = DateMonth
        UnitedDateDay = DateDay
        
        UnitedTime, UnitedHours, UnitedMinutes, UnitedSeconds, UnitedDateYear, UnitedDateMonth, UnitedDateDay = NormalizeTimeParameters(UnitedTime, UnitedDateYear, UnitedDateMonth, UnitedDateDay)


    return(UnitedTime, UnitedHours, UnitedMinutes, UnitedSeconds, UnitedDateYear, UnitedDateMonth, UnitedDateDay)

def UTtoLT(Latitude, UnitedHours, UnitedMinutes, UnitedSeconds, UnitedDateYear, UnitedDateMonth, UnitedDateDay):

    # Calculate United Time
    UnitedTime = UnitedHours + UnitedMinutes/60 + UnitedSeconds/3600
    # Normalize LT
    UnitedTime = NormalizeZeroBounded(UnitedTime, 24)

    # Summer/Winter Saving time
    # Summer: March 26/31 - October 8/14 LT+1
    # Winter: October 8/14 - March 26/31 LT+0
    if((UnitedDateMonth > 3 and UnitedDateMonth < 10) or ((UnitedDateMonth == 3 and UnitedDateDay >=25) or (UnitedDateMonth == 10 and (UnitedDateDay >= 8 and UnitedDateDay <=14)))):
        LocalTime = UnitedTime + (int(Longitude/15) + 1)

    else:
        LocalTime = UnitedTime + int(Longitude/15)

    if(LocalTime < 0):
        LocalHours = int(NormalizeZeroBounded(LocalTime, 24))
        LocalDateDay = UnitedDateDay - 1
        if(LocalDateDay <= 0):
            LocalDateMonth = UnitedDateMonth - 1
            if(LocalDateMonth == 0):
                LocalDateMonth = 12
                LocalDateYear = UnitedDateYear - 1
            # Leap year handling
            if(UnitedDateYear%4 == 0 and (UnitedDateYear%100 != 0 or UnitedDateYear%400 == 0)):
                LocalDateDay = MonthLengthListLeapYear[LocalDateMonth - 1]

            else:
                LocalDateDay = MonthLengthList[LocalDateMonth - 1]

    elif(LocalTime >= 24):
        LocalHours = int(NormalizeZeroBounded(LocalTime, 24))
        LocalDateDay = UnitedDateDay + 1
        if(UnitedDateYear%4 == 0 and (UnitedDateYear%100 != 0 or UnitedDateYear%400 == 0)):
            if(UnitedDateDay > MonthLengthListLeapYear[UnitedDateMonth - 1]):
                LocalDateMonth = UnitedDateMonth + 1
            else:
                LocalDateMonth = UnitedDateMonth

        else:
            if(LocalDateDay >= MonthLengthList[UnitedDateMonth - 1]):
                LocalDateMonth = UnitedDateMonth + 1
            else:
                LocalDateMonth = UnitedDateMonth

        if(LocalDateMonth > 12):
            LocalDateMonth = 1
            LocalDateYear = UnitedDateYear + 1

        else:
            LocalDateYear = UnitedDateYear

    else:
        LocalDateYear = UnitedDateYear
        LocalDateMonth = UnitedDateMonth
        LocalDateDay = UnitedDateDay

    LocalTime, LocalHours, LocalMinutes, LocalSeconds, LocalDateYear, LocalDateMonth, LocalDateDay = NormalizeTimeParameters(LocalTime, LocalDateYear, LocalDateMonth, LocalDateDay)

    # Correction for Julian Date
    #LocalHours += 12
    #LocalHours = NormalizeZeroBounded(LocalHours, 24)

    # Apply Correction for Local Time
    LocalTime = LocalHours + LocalMinutes/60 + LocalSeconds/3600

    return(LocalTime, LocalHours, LocalMinutes, LocalSeconds, LocalDateYear, LocalDateMonth, LocalDateDay)

# Calculate Greenwich Mean Sidereal Time (GMST = S_0) at UT 00:00 on Given Date
def CalculateGMST(Longitude, UnitedHoursForGMST, UnitedMinutesForGMST, UnitedSecondsForGMST, UnitedDateYear, UnitedDateMonth, UnitedDateDay):

    # JulianDays = UT days since J2000.0, including parts of a day
    # Could be + or - or 0
    #Dwhole = int(int(1461 * int(UnitedDateYear + 4800 + (UnitedDateMonth - 14) / 12)) / 4) + int((367 * (UnitedDateMonth - 2 - 12 * int((UnitedDateMonth - 14) / 12))) / 12) - int((3 * int((UnitedDateYear + 4900 + (UnitedDateMonth - 14)/12) / 100)) / 4) + UnitedDateDay - 32075
    #Dwhole = 367 * UnitedDateYear - int(int(7 * (UnitedDateYear + 5001 + (UnitedDateMonth - 9) / 7)) / 4) + int((275 * UnitedDateMonth) / 9) + UnitedDateDay + 1729777
    Dwhole = 367 * UnitedDateYear - int(7 * (UnitedDateYear + int((UnitedDateMonth + 9) / 12)) / 4) + int(275 * UnitedDateMonth / 9) + UnitedDateDay - 730531.5
    # Dfrac: Fraction of the day
    # If UT = 00:00:00, then Dfrac = 0
    Dfrac = (UnitedHoursForGMST + UnitedMinutesForGMST/60 + UnitedSecondsForGMST/3600)/24
    JulianDays = Dwhole + Dfrac

    # Number of Julian centuries since J2000.0
    JulianCenturies = JulianDays / 36525

    # Calculate GMST in Degrees
    GMSTDegrees = 280.46061837 + 360.98564736629 * JulianDays + 0.000388 * JulianCenturies**2

    # Normalize between to [0,+2π[
    GMSTDegrees = NormalizeZeroBounded(GMSTDegrees, 360)

    # Convert GMST to Hours
    GMST = GMSTDegrees / 15

    return(GMST)

################################################################
########                                                ########
########      1. CONVERSION OF COORDINATE SYSTEMS       ########
########                                                ########
################################################################

# 1. Horizontal to Equatorial I
def HorToEquI(Latitude, Altitude, Azimuth, LocalSiderealTime=None):

    # Initial Data Normalization
    # Latitude: [-π,+π]
    # Altitude: [-π/2,+π/2]
    # Azimuth: [0,+2π[
    # Local Mean Sidereal Time: [0,24h[
    Latitude = NormalizeSymmetricallyBoundedPI(Latitude)
    Altitude = NormalizeSymmetricallyBoundedPI_2(Altitude)
    Azimuth = NormalizeZeroBounded(Azimuth, 360)
    if (LocalSiderealTime != None):
        LocalSiderealTime = NormalizeZeroBounded(LocalSiderealTime, 24)

    # Calculate Declination (δ)
    # sin(δ) = sin(m) * sin(φ) + cos(m) * cos(φ) * cos(A)
    Declination =  math.degrees(math.asin(
                   math.sin(math.radians(Altitude)) * math.sin(math.radians(Latitude)) +
                   math.cos(math.radians(Altitude)) * math.cos(math.radians(Latitude)) * math.cos(math.radians(Azimuth))
                   ))
    # Normalize result for Declination [-π/2,+π/2]
    Declination = NormalizeSymmetricallyBoundedPI_2(Declination)

    # Calculate Local Hour Angle in Degrees (H)
    # sin(H) = - sin(A) * cos(m) / cos(δ)
    LocalHourAngleDegrees = math.degrees(math.asin(
                            - math.sin(math.radians(Azimuth)) * math.cos(math.radians(Altitude)) / math.cos(math.radians(Declination))
                            ))
    # Normalize result [0,+2π[
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
    # Normalize LMST
    # LMST: [0,24h[
    LocalSiderealTime = NormalizeZeroBounded(LocalSiderealTime, 24)

    return(Declination, RightAscension, LocalSiderealTime)


# 3. Equatorial I to Horizontal
def EquIToHor(Latitude, RightAscension, Declination, Altitude, Azimuth, LocalSiderealTime, LocalHourAngle):

    # Initial Data Normalization
    # Latitude: [-π,+π]
    # Right Ascension: [0h,24h[
    # Declination: [-π/2,+π/2]
    Latitude = NormalizeSymmetricallyBoundedPI(Latitude)
    if(RightAscension != None):
        RightAscension = NormalizeZeroBounded(RightAscension, 24)
    if(Declination != None):
        Declination = NormalizeSymmetricallyBoundedPI_2(Declination)


    if(LocalSiderealTime != None):
        # Calculate Local Hour Angle in Hours (t)
        # t = S - α
        LocalHourAngle = LocalSiderealTime - RightAscension
        # Normalize LHA
        # LHA: [0h,24h[
        LocalHourAngle = NormalizeZeroBounded(LocalHourAngle, 24)

    if(LocalHourAngle != None and Azimuth == None):
        # Convert to angles from hours (t -> H)
        LocalHourAngleDegrees = LocalHourAngle * 15

        # Calculate Altitude (m)
        # sin(m) = sin(δ) * sin(φ) + cos(δ) * cos(φ) * cos(H)
        Altitude = math.degrees(math.asin(
                math.sin(math.radians(Declination)) * math.cos(math.radians(Latitude)) +
                math.cos(math.radians(Declination)) * math.cos(math.radians(Latitude)) * math.cos(math.radians(LocalHourAngleDegrees))
                ))
        # Normalize Altitude
        # Altitude: # Declination: [-π/2,+π/2]
        Altitude = NormalizeSymmetricallyBoundedPI_2(Altitude)

        # Calculate Azimuth (A)
        # sin(A) = - sin(H) * cos(δ) / cos(m)
        # Azimuth at given H Local Hour Angle
        Azimuth = math.degrees(math.asin(
                - math.sin(math.radians(LocalHourAngleDegrees)) * math.cos(math.radians(Declination)) / math.cos(math.radians(Altitude))
                ))
        # Normalize Azimuth
        # Azimuth: [0,+2π[
        Azimuth = NormalizeZeroBounded(Azimuth, 360)

        return(Altitude, Azimuth)

    elif(Altitude != None):
        # Starting Equations: 
        # sin(m) = sin(δ) * sin(φ) + cos(δ) * cos(φ) * cos(H)
        # We can calculate eg. setting/rising with the available data (m = 0°), or other things...
        # First let's calculate LHA:
        # cos(H) = (sin(m) - sin(δ) * sin(φ)) / cos(δ) * cos(φ)
        LocalHourAngleDegrees1 = math.degrees(math.acos(
                                (math.sin(math.radians(Altitude)) - math.sin(math.radians(Declination)) * math.sin(math.radians(Latitude))) /
                                (math.cos(math.radians(Declination)) * math.cos(math.radians(Latitude)))
                                ))

        # acos(x) has two correct output on this interval
        LocalHourAngleDegrees2 = - LocalHourAngleDegrees1

        # Calculate Azimuth (A)
        # sin(A) = - sin(H) * cos(δ) / cos(m)

        # Setting Azimuth
        Azimuth1 = math.degrees(math.asin(
                - math.sin(math.radians(LocalHourAngleDegrees1)) * math.cos(math.radians(Declination)) / math.cos(math.radians(Altitude))
                ))

        # Rising Azimuth
        Azimuth2 = math.degrees(math.asin(
                - math.sin(math.radians(LocalHourAngleDegrees2)) * math.cos(math.radians(Declination)) / math.cos(math.radians(Altitude))
                ))
        # Normalize Azimuth
        # Azimuth: [0,+2π[
        Azimuth1 = NormalizeZeroBounded(Azimuth1, 360)
        Azimuth2 = NormalizeZeroBounded(Azimuth2, 360)

        # Calculate time between them
        # sin(H) = - sin(A) * cos(m) / cos(δ)
        H1 = math.degrees(math.asin(
            - math.sin(math.radians(Azimuth1)) * math.cos(math.radians(Altitude)) / math.cos(math.radians(Declination)) ))

        H2 = math.degrees(math.asin(
            - math.sin(math.radians(Azimuth2)) * math.cos(math.radians(Altitude)) / math.cos(math.radians(Declination)) ))

        H1 = NormalizeZeroBounded(H1, 360)
        H2 = NormalizeZeroBounded(H2, 360)

        if(H2 >= H1):
            H_dil = H2 - H1
        else:
            H_dil = H1 - H2

        return(Altitude, Azimuth1, Azimuth2, H_dil)

# 4. Equatorial I to Equatorial II
def EquIToEquII(RightAscension, LocalHourAngle):
    
    LocalSiderealTime = LocalHourAngle + RightAscension
    # Normalize LMST
    # LMST: [0,24h[
    LocalSiderealTime = NormalizeZeroBounded(LocalSiderealTime, 24)

    return(LocalSiderealTime)

# 5. Equatorial II to Equatorial I
def EquIIToEquI(LocalSiderealTime, RightAscension, LocalHourAngle):

    # Calculate Right Ascension or Local Mean Sidereal Time
    if(RightAscension != None and LocalHourAngle == None):
        LocalHourAngle = LocalSiderealTime - RightAscension
        # Normalize LHA
        # LHA: [0,24h[
        LocalHourAngle = NormalizeZeroBounded(LocalHourAngle, 24)

    elif(RightAscension == None and LocalHourAngle != None):
        RightAscension = LocalSiderealTime - LocalHourAngle
        # Normalize Right Ascension
        # Right Ascension: [0,24h[
        RightAscension = NormalizeZeroBounded(RightAscension, 24)

    else:
        pass

    return(LocalHourAngle, RightAscension)

# 6. Equatorial II to Horizontal
def EquIIToHor(Latitude, RightAscension, Declination, Altitude, Azimuth, LocalSiderealTime, LocalHourAngle):

    # Initial Data Normalization
    # Latitude: [-π,+π]
    # Local Mean Sidereal Time: [0h,24h[
    # Local Hour Angle: [0h,24h[
    # Right Ascension: [0h,24h[
    # Declination: [-π/2,+π/2]
    Latitude = NormalizeSymmetricallyBoundedPI(Latitude)
    LocalSiderealTime = NormalizeZeroBounded(LocalSiderealTime, 24)
    
    if(RightAscension == None and LocalHourAngle != None):
        LocalHourAngle = NormalizeZeroBounded(LocalHourAngle, 24)

    elif(RightAscension != None and LocalHourAngle == None):
        RightAscension = NormalizeZeroBounded(RightAscension, 24)
    
    Declination = NormalizeSymmetricallyBoundedPI_2(Declination)

    # Convert Equatorial II to Equatorial I
    LocalHourAngle, RightAscension = EquIIToEquI(LocalSiderealTime, RightAscension, LocalHourAngle)

    # Normalization of Output Data
    LocalHourAngle = NormalizeZeroBounded(LocalHourAngle, 24)
    RightAscension = NormalizeZeroBounded(RightAscension, 24)

    # Convert Equatorial I to Horizontal
    Altitude, Azimuth = EquIToHor(Latitude, RightAscension, Declination, Altitude, Azimuth, LocalSiderealTime, LocalHourAngle)

    # Normalization of Output Data
    # Altitude: [-π/2,+π/2]
    # Azimuth: [0,+2π[
    Altitude = NormalizeSymmetricallyBoundedPI_2(Altitude)
    Azimuth = NormalizeZeroBounded(Azimuth, 360)

    return(Altitude, Azimuth)


################################################
########                                ########
########    2. GEOGRAPHICAL DISTANCE    ########
########                                ########
################################################
# Calculate distances between coordinates
def GeogDistCalc(Latitude1, Latitude2, Longitude1, Longitude2):
    
    # Initial Data Normalization
    # Latitude: [-π,+π]
    # Longitude: [0,+2π[
    Latitude1 = NormalizeSymmetricallyBoundedPI(Latitude1)
    Latitude2 = NormalizeSymmetricallyBoundedPI(Latitude2)
    Longitude1 = NormalizeZeroBounded(Longitude1, 360)
    Longitude2 = NormalizeZeroBounded(Longitude2, 360)

    # Haversine formula:
    # Step 1.: hav_1 = (sin((φ2 - φ1) / 2))^2 + cos(φ1) ⋅ cos(φ2) ⋅ (sin((λ2 - λ1) / 2))^2
    # Step 2.: hav_2 = 2 * atan2(sqrt(hav_1),sqrt(1 - hav_1))
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
def GeogDistLocationCalc(Latitude1, Latitude2, Longitude1, Longitude2):

    # Initial Data Normalization
    # Latitude: [-π,+π]
    # Longitude: [0,+2π[
    Latitude1 = NormalizeSymmetricallyBoundedPI(Latitude1)
    Latitude2 = NormalizeSymmetricallyBoundedPI(Latitude2)
    Longitude1 = NormalizeZeroBounded(Longitude1, 360)
    Longitude2 = NormalizeZeroBounded(Longitude2, 360)

    # Haversine formula:
    # Step 1.: hav_1 = (sin((φ2 - φ1) / 2))^2 + cos(φ1) ⋅ cos(φ2) ⋅ (sin((λ2 - λ1) / 2))^2
    # Step 2.: hav_2 = 2 * atan2(sqrt(hav_1),sqrt(1 - hav_1))
    # Step 3.: d = R * hav_2

    # Step 1
    hav_1 = ((math.sin(math.radians(Latitude2 - Latitude1) / 2))**2 +
        (math.cos(math.radians(Latitude1)) * math.cos(math.radians(Latitude2)) * (math.sin(math.radians(Longitude2 - Longitude1) / 2))**2))

    # Step 2
    hav_2 = 2 * math.atan2(math.sqrt(hav_1), math.sqrt(1-hav_1))

    # Step 3
    Distance = R * hav_2

    return(Distance)


################################################################
########                                                ########
######## 3. CALCULATE LOCAL MEAN SIDEREAL TIME (LMST)   ########
########                                                ########
################################################################

# Calculate LMST from Predefined Coordinates
def LocalSiderealTimeCalc(Longitude, LocalHours, LocalMinutes, LocalSeconds, DateYear, DateMonth, DateDay):

    # Initial Data Normalization
    # Longitude: [0,+2π[
    Longitude = NormalizeZeroBounded(Longitude, 360)

    UnitedTime, UnitedHours, UnitedMinutes, UnitedSeconds, UnitedDateYear, UnitedDateMonth, UnitedDateDay = LTtoUT(LocalHours, LocalMinutes, LocalSeconds, DateYear, DateMonth, DateDay)

    # Calculate Greenwich Mean Sidereal Time (GMST)
    # Now UT = 00:00:00
    UnitedHoursForGMST = 0
    UnitedMinutesForGMST = 0
    UnitedSecondsForGMST = 0
    S_0 = CalculateGMST(Longitude, UnitedHoursForGMST, UnitedMinutesForGMST, UnitedSecondsForGMST, UnitedDateYear, UnitedDateMonth, UnitedDateDay)

    # Greenwich Zero Time for Supervision
    GreenwichSiderealTime, GreenwichHours, GreenwichMinutes, GreenwichSeconds, SiderealDateYear, SiderealDateMonth, SiderealDateDay = NormalizeTimeParameters(S_0, DateYear, DateMonth, DateDay)

    # Calculate LMST
    LMST = S_0 + Longitude/15 + dS * UnitedTime
    
    # Norm LMST
    LMSTNorm = NormalizeZeroBounded(LMST, 24)

    LocalSiderealTime, LocalSiderealHours, LocalSiderealMinutes, LocalSiderealSeconds, LocalDateYear, LocalDateMonth, LocalDateDay = NormalizeTimeParameters(LMSTNorm, DateYear, DateMonth, DateDay)

    return(LocalSiderealHours, LocalSiderealMinutes, LocalSiderealSeconds, UnitedHours, UnitedMinutes, UnitedSeconds, GreenwichHours, GreenwichMinutes, GreenwichSeconds)


################################################################
########                                                ########
########  4. CALCULATE DATETIMES OF SUNSETS AND RISES   ########
########                                                ########
################################################################

def CalculateJulianDate(LocalDateYear, LocalDateMonth, LocalDateDay, UnitedHours, UnitedMinutes, UnitedSeconds):

    # JulianDays = UT days since J2000.0, including parts of a day
    # Could be + or - or 0
    #Dwhole = int(int(1461 * int(LocalDateYear + 4800 + (LocalDateMonth - 14) / 12)) / 4) + int((367 * (LocalDateMonth - 2 - 12 * int((LocalDateMonth - 14) / 12))) / 12) - int((3 * int((LocalDateYear + 4900 + (LocalDateMonth - 14)/12) / 100)) / 4) + LocalDateDay - 32075
    #Dwhole = 367 * LocalDateYear - int(int(7 * (LocalDateYear + 5001 + (LocalDateMonth - 9) / 7)) / 4) + int((275 * LocalDateMonth) / 9) + LocalDateDay + 1729777
    Dwhole = 367 * LocalDateYear - int(7 * (LocalDateYear + int((LocalDateMonth + 9) / 12)) / 4) + int(275 * LocalDateMonth / 9) + LocalDateDay - 730531.5
    #Dwhole = round(Dwhole, 0)
    # Dfrac: Fraction of the day
    Dfrac = (UnitedHours + UnitedMinutes/60 + UnitedSeconds/3600)/24
    # Julian days
    JulianDays = Dwhole + Dfrac

    return(JulianDays)

def SunsCoordinatesCalc(Planet, Latitude, Longitude, AltitudeOfSun, JulianDays):

    # 1. Mean Solar Noon
    # JAnomaly is an approximation of Mean Solar Time at WLongitude expressed as a Julian day with the day fraction
    # WLongitude is the longitude west (west is positive, east is negative) of the observer on the Earth
    WLongitude = - Longitude
    JAnomaly = (JulianDays - OrbitDict[Planet + "J"][0]) / OrbitDict[Planet + "J"][3] - WLongitude/360

    # 2. Solar Mean Anomaly
    # MeanAnomaly (M) is the Solar Mean Anomaly used in a few of next equations
    # MeanAnomaly = (M_0 + M_1 * (JulianDays-J2000)) and Norm to 360
    MeanAnomaly = (OrbitDict[Planet + "M"][0] + OrbitDict[Planet + "M"][1] * JulianDays)
    # Normalize Result
    MeanAnomaly = NormalizeZeroBounded(MeanAnomaly, 360)

    # 3. Equation of the Center
    # EquationOfCenter (C) is the Equation of the center value needed to calculate Lambda (see next equation)
    # EquationOfCenter = C_1 * sin(M) + C_2 * sin(2M) + C_3 * sin(3M) + C_4 * sin(4M) + C_5 * sin(5M) + C_6 * sin(6M)
    EquationOfCenter = (OrbitDict[Planet + "C"][0] * math.sin(math.radians(MeanAnomaly)) + OrbitDict[Planet + "C"][1] * math.sin(math.radians(2 * MeanAnomaly)) + 
                       OrbitDict[Planet + "C"][2] * math.sin(math.radians(3 * MeanAnomaly)) + OrbitDict[Planet + "C"][3] * math.sin(math.radians(4 * MeanAnomaly)) + 
                       OrbitDict[Planet + "C"][4] * math.sin(math.radians(5 * MeanAnomaly)) + OrbitDict[Planet + "C"][5] * math.sin(math.radians(6 * MeanAnomaly)))

    # 4. Ecliptic Longitude
    # MeanEclLongitudeSun (L_sun) in the Mean Ecliptic Longitude
    # EclLongitudeSun (λ) is the Ecliptic Longitude
    # 102.9372 is a value for the argument of perihelion
    MeanEclLongitudeSun = MeanAnomaly + 180 + 102.9372
    EclLongitudeSun = EquationOfCenter + MeanEclLongitudeSun
    MeanEclLongitudeSun = NormalizeZeroBounded(MeanEclLongitudeSun, 360)
    EclLongitudeSun = NormalizeZeroBounded(EclLongitudeSun, 360)

    # 5. Right Ascension of Sun (α)
    # EarthA_2, EarthA_4 and EarthA_6 (measured in degrees) are coefficients in the series expansion of the Sun's Right Ascension
    # They varie for different planets in the Solar System
    # RightAscensionSun = EclLongitudeSun + S ≈ EclLongitudeSun + EarthA_2 * sin(2 * EclLongitudeSun) + EarthA_4 * sin(4 * EclLongitudeSun) + EarthA_6 * sin(6 * EclLongitudeSun)
    RightAscensionSun = (EclLongitudeSun + OrbitDict[Planet + "A"][0] * math.sin(math.radians(2 * EclLongitudeSun)) + OrbitDict[Planet + "A"][1] * 
                        math.sin(math.radians(4 * EclLongitudeSun)) + OrbitDict[Planet + "A"][2] * math.sin(math.radians(6 * EclLongitudeSun)))

    # 6./a Declination of the Sun (δ) (Wikipedia)
    # DeclinationSun (δSun) is the Declination of the Sun
    # 23.44° is Earth's maximum Axial Tilt toward's the Sun
    #DeclinationSun = math.degrees(math.asin(
    #       math.sin(math.radians(EclLongitudeSun)) * math.sin(math.radians(23.44)) ))
    # Normalize Declination
    #DeclinationSun = NormalizeSymmetricallyBoundedPI_2(DeclinationSun)

    # 6./b Declination of the Sun (δ) (Astronomy Answers)
    # EarthD_1, EarthD_3 and EarthD_5 (measured in degrees) are coefficients in the series expansion of the Sun's Declination.
    # They varie for different planets in the Solar System.
    # DeclinationSun = EarthD_1 * sin(EclLongitudeSun) + EarthD_3 * (sin(EclLongitudeSun))^3 + EarthD_5 * (sin(EclLongitudeSun))^5
    DeclinationSun = (OrbitDict[Planet + "D"][0] * math.sin(math.radians(EclLongitudeSun)) + OrbitDict[Planet + "D"][1] * 
                     (math.sin(math.radians(EclLongitudeSun)))**3 + OrbitDict[Planet + "D"][2] * (math.sin(math.radians(EclLongitudeSun)))**5)

    # 7./a Local Hour Angle of Sun (H)
    # H+ ≈ 90° + H_1 * sin(EclLongitudeSun) * tan(φ) + H_3 * sin(EclLongitudeSun)^3 * tan(φ) * (3 + tan(φ)^2) + H_5 * sin(EclLongitudeSun)^5 * tan(φ) * (15 + 10*tan(φ)^2 + 3 * tan(φ)^4))
    LocalHourAngleSun_Pos = (90 + OrbitDict[Planet + "H"][0] * math.sin(math.radians(EclLongitudeSun)) * math.tan(math.radians(Latitude)) + OrbitDict[Planet + "H"][1] * 
                            math.sin(math.radians((EclLongitudeSun))**3 * math.tan(math.radians(Latitude)) * (3 + math.tan(math.radians(Latitude))**2) + OrbitDict[Planet + "H"][2] * 
                            math.sin(math.radians(EclLongitudeSun))**5 * math.tan(math.radians(Latitude)) * (15 + 10 * math.tan(math.radians(Latitude))**2 + 3 * math.tan(math.radians(Latitude))**4)))

    # 7./b Local Hour Angle of Sun (H)
    # cos(H) = (sin(m_0) - sin(φ) * sin(δ)) / (cos(φ) * cos(δ))
    # LocalHourAngleSun (t_0) is the Local Hour Angle from the Observer's Zenith
    # Latitude (φ) is the North Latitude of the Observer (north is positive, south is negative) on the Earth
    # m_0 = -0.83 is a compensation of Altitude (m) in degrees, for the Sun's distorted shape, and the atmospherical refraction
    LocalHourAngleSun_Orig = math.degrees(math.acos(
                           ((math.sin(math.radians(AltitudeOfSun - 0.83)) - math.sin(math.radians(Latitude)) * math.sin(math.radians(DeclinationSun))) /
                           (math.cos(math.radians(Latitude)) * math.cos(math.radians(DeclinationSun)))) ))
    
    # Normalize result for Hour Angles
    LocalHourAngleSun_Pos = NormalizeZeroBounded(LocalHourAngleSun_Pos, 360)
    LocalHourAngleSun_Orig = NormalizeZeroBounded(LocalHourAngleSun_Orig, 360)

    # 8. Solar Transit
    # Jtransit is the Julian date for the Local True Solar Transit (or Solar Noon)
    # JulianDate = JulianDays + 2451545
    # 2451545.5 is midnight or the beginning of the equivalent Julian year reference
    # Jtransit = J_x + 0.0053 * sin(MeanANomaly) - 0.0068 * sin(2 * L_sun)
    # "0.0053 * sin(MeanAnomaly) - 0.0069 * sin(2 * EclLongitudeSun)"  is a simplified version of the equation of time
    J_x = (JulianDays + 2451545) + OrbitDict[Planet + "J"][3] * (JulianDays - JAnomaly)
    Jtransit = J_x + OrbitDict[Planet + "J"][1] * math.sin(math.radians(MeanAnomaly)) + OrbitDict[Planet + "J"][2] * math.sin(math.radians(2 * MeanEclLongitudeSun))

    return(LocalHourAngleSun_Pos, LocalHourAngleSun_Orig, RightAscensionSun, DeclinationSun, Jtransit)

def CalculateCorrectionsForJ(Planet, Latitude, Longitude, AltitudeOfSun, JAlt_0):

    # Calculate Corrections for LHA of Sun
    LocalHourAngleSun_PosCorr, LocalHourAngleSun_OrigCorr, RightAscensionSunCorr, DeclinationSunCorr, JtransitCorr = SunsCoordinatesCalc(Planet, Latitude, Longitude, AltitudeOfSun, JAlt_0)

    return(LocalHourAngleSun_PosCorr, LocalHourAngleSun_OrigCorr, RightAscensionSunCorr, DeclinationSunCorr, JtransitCorr)

def CalculateRiseAndSetTime(Planet, Latitude, Longitude, AltitudeOfSun, LocalDateYear, LocalDateMonth, LocalDateDay):

    # Calculate Actual Julian Date
    # Now UT = 0
    UnitedHours = 0
    UnitedMinutes = 0
    UnitedSeconds = 0
    JulianDays = CalculateJulianDate(LocalDateYear, LocalDateMonth, LocalDateDay, UnitedHours, UnitedMinutes, UnitedSeconds)

    # Calulate Sun's coordinates on sky
    LocalHourAngleSun_Pos, LocalHourAngleSun_Orig, RightAscensionSun, DeclinationSun, Jtransit = SunsCoordinatesCalc(Planet, Latitude, Longitude, AltitudeOfSun, JulianDays)
    
    '''print("LocalHourAngleSun_Pos: ", LocalHourAngleSun_Pos)
    print("LocalHourAngleSun_Orig: ", LocalHourAngleSun_Orig)'''

    # Calulate Rising and Setting Datetimes of the Sun
    # JRise is the actual Julian date of sunrise
    # JSet is the actual Julian date of sunset
    JRise = Jtransit - LocalHourAngleSun_Orig / 360
    JSet = Jtransit + LocalHourAngleSun_Orig / 360

    LocalHourAngleSun_PosCorrRise, LocalHourAngleSun_OrigCorrRise, RightAscensionSunCorrRise, DeclinationSunCorrRise, JtransitCorrRise =  CalculateCorrectionsForJ(Planet, Latitude, Longitude, AltitudeOfSun, JRise)
    LocalHourAngleSun_PosCorrSet, LocalHourAngleSun_OrigCorrSet, RightAscensionSunCorrSet, DeclinationSunCorrSet, JtransitCorrSet = CalculateCorrectionsForJ(Planet, Latitude, Longitude, AltitudeOfSun, JSet)
        
    '''print("LocalHourAngleSun_PosCorrRise: ", LocalHourAngleSun_PosCorrRise)
    print("LocalHourAngleSun_OrigCorrRise: ", LocalHourAngleSun_OrigCorrRise)
    print("LocalHourAngleSun_PosCorrSet: ", LocalHourAngleSun_PosCorrSet)
    print("LocalHourAngleSun_OrigCorrSet: ", LocalHourAngleSun_OrigCorrSet)'''
    
    # Apply Corrections
    #JRise -= (LocalHourAngleSun_Orig + LocalHourAngleSun_OrigCorrRise) / 360
    #JSet -= (LocalHourAngleSun_Orig - LocalHourAngleSun_OrigCorrSet) / 360

    return(JRise, JSet)


# Calculate Sunrise and Sunset's Datetime
def SunSetAndRiseDateTime(Planet, Latitude, Longitude, AltitudeOfSun, LocalDateYear, LocalDateMonth, LocalDateDay):

    JRise, JSet = CalculateRiseAndSetTime(Planet, Latitude, Longitude, AltitudeOfSun, LocalDateYear, LocalDateMonth, LocalDateDay)

    # SUNRISE
    #SunRiseUTYearsDecimal = (JRise - 2451545.5) / 365
    SunRiseUTDateYear = LocalDateYear

    #SunRiseUTDateMonthDecimal = (SunRiseUTDateYearDecimal - SunRiseUTDateYear + 2000) * 12 + 1
    SunRiseUTDateMonth = LocalDateMonth
    # Leap year handling
    #if(SunRiseUTDateYear%4 == 0 and (SunRiseUTDateYear%100 != 0 or SunRiseUTDateYear%400 == 0)):
    #    SunRiseUTDateDayDecimal = (SunRiseUTDateMonthDecimal - SunRiseUTDateMonth) * MonthLengthListLeapYear[SunRiseUTDateMonth - 1] - 1
    #    SunRiseUTDateDay = int(SunRiseUTDateDayDecimal)
    #else:
    #    SunRiseUTDateDayDecimal = (SunRiseUTDateMonthDecimal - SunRiseUTDateMonth) * MonthLengthList[SunRiseUTDateMonth - 1] - 1
    #    SunRiseUTDateDay = int(SunRiseUTDateDayDecimal)
    SunRiseUTDateDay = LocalDateDay

    UTFracDayRise = JRise - int(JRise)

    UTFracDayRise *= 24

    SunRiseUT, SunRiseUTHours, SunRiseUTMinutes, SunRiseUTSeconds, SunRiseUTDateYear, SunRiseUTDateMonth, SunRiseUTDateDay = NormalizeTimeParameters(UTFracDayRise, SunRiseUTDateYear, SunRiseUTDateMonth, SunRiseUTDateDay)


    # SUNSET
    #SunSetUTDateYearDecimal = (JSet - 2451545) / 365.2422
    SunSetUTDateYear = LocalDateYear

    #SunSetUTDateMonthDecimal = (SunSetUTDateYearDecimal - SunSetUTDateYear + 2000) * 12 + 1
    SunSetUTDateMonth = LocalDateMonth
    
    # Leap year handling for Days
    #if(SunSetUTDateYear%4 == 0 and (SunSetUTDateYear%100 != 0 or SunSetUTDateYear%400 == 0)):
    #   SunSetUTDateDayDecimal = (SunSetUTDateMonthDecimal - SunSetUTDateMonth) * MonthLengthListLeapYear[SunSetUTDateMonth - 1] - 1
    #    SunSetUTDateDay = int(SunSetUTDateDayDecimal)
    #else:
    #    SunSetUTDateDayDecimal = (SunSetUTDateMonthDecimal - SunSetUTDateMonth) * MonthLengthList[SunSetUTDateMonth - 1] - 1
    #    SunSetUTDateDay = int(SunSetUTDateDayDecimal)

    SunSetUTDateDay = LocalDateDay

    UTFracDaySet = JSet - int(JSet)

    UTFracDaySet *= 24

    SunSetUT, SunSetUTHours, SunSetUTMinutes, SunSetUTSeconds, SunSetUTDateYear, SunSetUTDateMonth, SunSetUTDateDay = NormalizeTimeParameters(UTFracDaySet, SunSetUTDateYear, SunSetUTDateMonth, SunSetUTDateDay)

    # Convert results to Local Time
    LocalTimeRise, LocalHoursRise, LocalMinutesRise, LocalSecondsRise, LocalDateYearRise, LocalDateMonthRise, LocalDateDayRise = UTtoLT(Latitude, SunRiseUTHours, SunRiseUTMinutes, SunRiseUTSeconds, SunRiseUTDateYear, SunRiseUTDateMonth, SunRiseUTDateDay)
    LocalTimeSet, LocalHoursSet, LocalMinutesSet, LocalSecondsSet, LocalDateYearSet, LocalDateMonthSet, LocalDateDaySet = UTtoLT(Latitude, SunSetUTHours, SunSetUTMinutes, SunSetUTSeconds, SunSetUTDateYear, SunSetUTDateMonth, SunSetUTDateDay)

    return(LocalTimeSet, LocalHoursSet, LocalMinutesSet, LocalSecondsSet, LocalDateYearSet, LocalDateMonthSet, LocalDateDaySet, LocalTimeRise, LocalHoursRise, LocalMinutesRise, LocalSecondsRise, LocalDateYearRise, LocalDateMonthRise, LocalDateDayRise)

################################################################
########                                                ########
########      5. CALCULATE DATETIMES OF TWILIGHTS       ########
########                                                ########
################################################################

def TwilightCalc(Planet, Latitude, Longitude, LocalDateYear, LocalDateMonth, LocalDateDay):

    # Definition of differenc Twilights
    # Begin/End of Civil Twilight:          m = -6°
    # Begin/End of Nautical Twilight:       m = -12°
    # Begin/End of Astronomical Twilight:   m = -18°
    AltitudeDaylight = 0
    AltitudeCivil = -6
    AltitudeNaval = -12
    AltitudeAstro = -18

    #Daylight
    (LocalTimeSetDaylight, LocalHoursSetDaylight, LocalMinutesSetDaylight, LocalSecondsSetDaylight, LocalDateYearSetDaylight, LocalDateMonthSetDaylight, LocalDateDaySetDaylight, 
    LocalTimeRiseDaylight, LocalHoursRiseDaylight, LocalMinutesRiseDaylight, LocalSecondsRiseDaylight, LocalDateYearRiseDaylight, LocalDateMonthRiseDaylight, LocalDateDayRiseDaylight) = SunSetAndRiseDateTime(Planet, Latitude, Longitude, AltitudeDaylight, LocalDateYear, LocalDateMonth, LocalDateDay)

    # Civil Twilight
    (LocalTimeSetCivil, LocalHoursSetCivil, LocalMinutesSetCivil, LocalSecondsSetCivil, LocalDateYearSetCivil, LocalDateMonthSetCivil, LocalDateDaySetCivil, 
    LocalTimeRiseCivil, LocalHoursRiseCivil, LocalMinutesRiseCivil, LocalSecondsRiseCivil, LocalDateYearRiseCivil, LocalDateMonthRiseCivil, LocalDateDayRiseCivil) = SunSetAndRiseDateTime(Planet, Latitude, Longitude, AltitudeCivil, LocalDateYear, LocalDateMonth, LocalDateDay)

    # Nautical Twilight
    (LocalTimeSetNaval, LocalHoursSetNaval, LocalMinutesSetNaval, LocalSecondsSetNaval, LocalDateYearSetNaval, LocalDateMonthSetNaval, LocalDateDaySetNaval, 
    LocalTimeRiseNaval, LocalHoursRiseNaval, LocalMinutesRiseNaval, LocalSecondsRiseNaval, LocalDateYearRiseNaval, LocalDateMonthRiseNaval, LocalDateDayRiseNaval) = SunSetAndRiseDateTime(Planet, Latitude, Longitude, AltitudeNaval, LocalDateYear, LocalDateMonth, LocalDateDay)

    # Astronomical Twilight
    (LocalTimeSetAstro, LocalHoursSetAstro, LocalMinutesSetAstro, LocalSecondsSetAstro, LocalDateYearSetAstro, LocalDateMonthSetAstro, LocalDateDaySetAstro, 
    LocalTimeRiseAstro, LocalHoursRiseAstro, LocalMinutesRiseAstro, LocalSecondsRiseAstro, LocalDateYearRiseAstro, LocalDateMonthRiseAstro, LocalDateDayRiseAstro) = SunSetAndRiseDateTime(Planet, Latitude, Longitude, AltitudeAstro, LocalDateYear, LocalDateMonth, LocalDateDay)

    # Step +1 day
    LocalDateNextDay = LocalDateDay + 1

    if(LocalDateYear%4 == 0 and (LocalDateYear%100 != 0 or LocalDateYear%400 == 0)):
        if(LocalDateNextDay > MonthLengthListLeapYear[LocalDateMonth - 1]):
            LocalDateNextDay = 1
            LocalDateNextMonth = LocalDateMonth + 1
        else:
            LocalDateNextDay = LocalDateDay + 1
            LocalDateNextMonth = LocalDateMonth
    
    else:
        if(LocalDateNextDay > MonthLengthList[LocalDateMonth - 1]):
            LocalDateNextDay = 1
            LocalDateNextMonth = LocalDateMonth + 1
        else:
            LocalDateNextDay = LocalDateDay + 1
            LocalDateNextMonth = LocalDateMonth

    if(LocalDateNextMonth > 12):
        LocalDateNextMonth = 1
        LocalDateNextYear = LocalDateYear + 1

    else:
        LocalDateNextYear = LocalDateYear

    # Astronomical Twilight Next Day
    (LocalTimeSetAstro2, LocalHoursSetAstro2, LocalMinutesSetAstro2, LocalSecondsSetAstro2, LocalDateYearSetAstro2, LocalDateMonthSetAstro2, LocalDateDaySetAstro2, 
    LocalTimeRiseAstro2, LocalHoursRiseAstro2, LocalMinutesRiseAstro2, LocalSecondsRiseAstro2, LocalDateYearRiseAstro2, LocalDateMonthRiseAstro2, LocalDateDayRiseAstro2) = SunSetAndRiseDateTime(Planet, Latitude, Longitude, AltitudeAstro, LocalDateNextYear, LocalDateNextMonth, LocalDateNextDay)


    # Noon and Midnight
    LocalTimeNoon = LocalTimeRiseDaylight + (LocalTimeSetDaylight - LocalTimeRiseDaylight) / 2
    LocalTimeMidnight = LocalTimeSetAstro + (((24 - LocalTimeSetAstro) + LocalTimeRiseAstro2) / 2)

    # Calc Midnight Date
    if(LocalTimeMidnight > 24):
        LocalDateDayMidnight = LocalDateDayRiseAstro2

        if(LocalDateYear%4 == 0 and (LocalDateYear%100 != 0 or LocalDateYear%400 == 0)):
            if(LocalDateDayMidnight > MonthLengthListLeapYear[LocalDateMonthSetAstro - 1]):
                LocalDateDayMidnight = 1
                LocalDateMonthMidnight = LocalDateMonthSetAstro + 1
            else:
                LocalDateDayMidnight = LocalDateDaySetAstro + 1
                LocalDateMonthMidnight = LocalDateMonthSetAstro

        else:
            if(LocalDateDayMidnight > MonthLengthList[LocalDateMonthSetAstro - 1]):
                LocalDateDayMidnight = 1
                LocalDateMonthMidnight = LocalDateMonthSetAstro + 1
            else:
                LocalDateDayMidnight = LocalDateDaySetAstro + 1
                LocalDateMonthMidnight = LocalDateMonthSetAstro
        
        if(LocalDateMonthMidnight > 12):
            LocalDateMonthMidnight = 1
            LocalDateYearMidnight = LocalDateYearSetAstro + 1

        else:
            LocalDateYearMidnight = LocalDateYearSetAstro

    else:
        LocalDateDayMidnight = LocalDateDaySetAstro
        LocalDateMonthMidnight = LocalDateMonthSetAstro
        LocalDateYearMidnight = LocalDateYearSetAstro

    # Calc Noon Date
    LocalDateDayNoon = LocalDateDayRiseAstro
    LocalDateMonthNoon = LocalDateMonthRiseAstro
    LocalDateYearNoon = LocalDateYearRiseAstro

    # Normalize results
    LocalTimeNoon = NormalizeZeroBounded(LocalTimeNoon, 24)
    LocalTimeMidnight = NormalizeZeroBounded(LocalTimeMidnight, 24)

    # LT of Noon and Midnight
    LocalTimeNoon, LocalHoursNoon, LocalMinutesNoon, LocalSecondsNoon, LocalDateYearNoon, LocalDateMonthNoon, LocalDateDayNoon = NormalizeTimeParameters(LocalTimeNoon, LocalDateYearNoon, LocalDateMonthNoon, LocalDateDayNoon)
    LocalTimeMidnight, LocalHoursMidnight, LocalMinutesMidnight, LocalSecondsMidnight, LocalDateYearMidnight, LocalDateMonthMidnight, LocalDateDayMidnight = NormalizeTimeParameters(LocalTimeMidnight, LocalDateYearMidnight, LocalDateMonthMidnight, LocalDateDayMidnight)

    return(LocalHoursNoon, LocalMinutesNoon, LocalSecondsNoon, LocalDateYearNoon, LocalDateMonthNoon, LocalDateDayNoon,
            LocalHoursMidnight, LocalMinutesMidnight, LocalSecondsMidnight, LocalDateYearMidnight, LocalDateMonthMidnight, LocalDateDayMidnight,
            LocalHoursRiseDaylight, LocalMinutesRiseDaylight, LocalSecondsRiseDaylight, LocalDateYearRiseDaylight, LocalDateMonthRiseDaylight, LocalDateDayRiseDaylight,
            LocalHoursSetDaylight, LocalMinutesSetDaylight, LocalSecondsSetDaylight, LocalDateYearSetDaylight, LocalDateMonthSetDaylight, LocalDateDaySetDaylight,
            LocalHoursRiseCivil, LocalMinutesRiseCivil, LocalSecondsRiseCivil, LocalDateYearRiseCivil, LocalDateMonthRiseCivil, LocalDateDayRiseCivil,
            LocalHoursSetCivil, LocalMinutesSetCivil, LocalSecondsSetCivil, LocalDateYearSetCivil, LocalDateMonthSetCivil, LocalDateDaySetCivil,
            LocalHoursRiseNaval, LocalMinutesRiseNaval, LocalSecondsRiseNaval, LocalDateYearRiseNaval, LocalDateMonthRiseNaval, LocalDateDayRiseNaval,
            LocalHoursSetNaval, LocalMinutesSetNaval, LocalSecondsSetNaval, LocalDateYearSetNaval, LocalDateMonthSetNaval, LocalDateDaySetNaval,
            LocalHoursRiseAstro, LocalMinutesRiseAstro, LocalSecondsRiseAstro, LocalDateYearSetAstro, LocalDateMonthSetAstro, LocalDateDaySetAstro,
            LocalHoursSetAstro, LocalMinutesSetAstro, LocalSecondsSetAstro, LocalDateYearRiseAstro, LocalDateMonthRiseAstro, LocalDateDayRiseAstro)


################################################################
########                                                ########
########   6. DRAW THE SUN'S ANNUAL PATH ON A SUNDIAL   ########
########                                                ########
################################################################

def SundialPrecalculations(Planet, Latitude, Longitude, LocalDateYear, LocalDateMonth, LocalDateDay):

    # We would like to calculate rising and setting time
    AltitudeOfSun = 0

    # Daylight start and end LT
    (LocalTimeSetDaylight, LocalHoursSetDaylight, LocalMinutesSetDaylight, LocalSecondsSetDaylight, LocalDateYearSetDaylight, LocalDateMonthSetDaylight, LocalDateDaySetDaylight, 
    LocalTimeRiseDaylight, LocalHoursRiseDaylight, LocalMinutesRiseDaylight, LocalSecondsRiseDaylight, LocalDateYearRiseDaylight, LocalDateMonthRiseDaylight, LocalDateDayRiseDaylight) = SunSetAndRiseDateTime(Planet, Latitude, Longitude, AltitudeOfSun, LocalDateYear, LocalDateMonth, LocalDateDay)
    
    # Calculate the Coordinates of the Sun's Apparent Position
    # Now UT = 0
    UnitedHours = 0
    UnitedMinutes = 0
    UnitedSeconds = 0
    JulianDays = CalculateJulianDate(LocalDateYear, LocalDateMonth, LocalDateDay, UnitedHours, UnitedMinutes, UnitedSeconds)
    LocalHourAngleSun_Pos, LocalHourAngleSun_Orig, RightAscensionSun, DeclinationSun, Jtransit = SunsCoordinatesCalc(Planet, Latitude, Longitude, AltitudeOfSun, JulianDays)

    # Calculate Local Mean Sidereal Time for both Rising and Setting time
    LocalSiderealHoursRise, LocalSiderealMinutesRise, LocalSiderealSecondsRise, UnitedHoursRise, UnitedMinutesRise, UnitedSecondsRise, GreenwichHoursRise, GreenwichMinutesRise, GreenwichSecondsRise = LocalSiderealTimeCalc(Longitude, LocalHoursRiseDaylight, LocalMinutesRiseDaylight, LocalSecondsRiseDaylight, LocalDateYearRiseDaylight, LocalDateMonthRiseDaylight, LocalDateDayRiseDaylight)
    LocalSiderealHoursSet, LocalSiderealMinutesSet, LocalSiderealSecondsSet, UnitedHoursSet, UnitedMinutesSet, UnitedSecondsSet, GreenwichHoursSet, GreenwichMinutesSet, GreenwichSecondsSet = LocalSiderealTimeCalc(Longitude, LocalHoursSetDaylight, LocalMinutesSetDaylight, LocalSecondsSetDaylight, LocalDateYearSetDaylight, LocalDateMonthSetDaylight, LocalDateDaySetDaylight)

    # Convert them to Decimal
    LocalSiderealTimeRise = LocalSiderealHoursRise + LocalSiderealMinutesRise/60 + LocalSiderealSecondsRise/3600
    LocalSiderealTimeSet = LocalSiderealHoursSet + LocalSiderealMinutesSet/60 + LocalSiderealSecondsSet/3600

    # Calculate Hour Angle of Rising and Setting Sun
    LocalHourAngleRise = LocalSiderealTimeRise - RightAscensionSun
    LocalHourAngleSet = LocalSiderealTimeSet - RightAscensionSun

    # Normalize Results
    LocalHourAngleRise = NormalizeZeroBounded(LocalHourAngleRise, 24)
    LocalHourAngleSet = NormalizeZeroBounded(LocalHourAngleSet, 24)

    return(LocalHourAngleRise, LocalHourAngleSet, DeclinationSun)

def SundialParametersCalc(Latitude, LocalHourAngle, DeclinationSun):

    # Convert LHA from Hours to Degrees
    LocalHourAngleDegrees = LocalHourAngle * 15

    # Calculate Altitude (m)
    # sin(m) = sin(δ) * sin(φ) + cos(δ) * cos(φ) * cos(H)
    Altitude = math.degrees(math.asin(
            math.sin(math.radians(DeclinationSun)) * math.cos(math.radians(Latitude)) +
            math.cos(math.radians(DeclinationSun)) * math.cos(math.radians(Latitude)) * math.cos(math.radians(LocalHourAngleDegrees))
            ))
    # Normalize Altitude
    # Altitude: # Declination: [-π/2,+π/2]
    Altitude = NormalizeSymmetricallyBoundedPI_2(Altitude)

    # Calculate Azimuth (A)
    # sin(A) = - sin(H) * cos(δ) / cos(m)

    # Azimuth at given H Local Hour Angle
    Azimuth = math.degrees(math.asin(
            - math.sin(math.radians(LocalHourAngleDegrees)) * math.cos(math.radians(DeclinationSun)) / math.cos(math.radians(Altitude))
            ))
    # Normalize Azimuth
    # Azimuth: [0,+2π[
    Azimuth = NormalizeZeroBounded(Azimuth, 360)

    return(Altitude, Azimuth)


###############################################################################################
####                ...     ..      ..                                                     ####
##                x*8888x.:*8888: -"888:                 @88>                                ##
##               X   48888X `8888H  8888                 %8P                                 ##
##              X8x.  8888X  8888X  !888>                       x@88k u@88c.                 ##
##              X8888 X8888  88888   "*8%-    us888u.   .@88u  ^"8888""8888"                 ##
##              '*888!X8888> X8888  xH8>   .@88 "8888" ''888E`   8888  888R                  ##
##                `?8 `8888  X888X X888>   9888  9888    888E    8888  888R                  ##
##                -^  '888"  X888  8888>   9888  9888    888E    8888  888R                  ##
##                 dx '88~x. !88~  8888>   9888  9888    888E    8888  888R                  ##
##               .8888Xf.888x:!    X888X.: 9888  9888    888&   "*88*" 8888"                 ##
##              :""888":~"888"     `888*"  "888*""888"   R888"    ""   'Y"                   ##
##                  "~'    "~        ""                   ""                                 ##
####                                                                                       ####
###############################################################################################
###  ####                                                                             ####  ###
  ####  ###                                                                         ###  ####
        ##                                                                           ##
  #   ###                                                                             ###   #
   ####                                                                                 ####

# Print version info
STARTMSG = "\n#### Csillész II Problem Solver Program {0} ####\n####    Developed by Balage Paliére and Co.   ####\n\n"
print(STARTMSG.format(ActualVersion))

while(True):

    print(">> MAIN MENU <<")
    print("(1) Coordinate System Conversion")
    print("(2) Geographical Distances")
    print("(3) Local Mean Sidereal Time")
    print("(4) Datetimes of Sunsets and Sunrises")
    print("(5) Datetimes of Twilights")
    print("(6) Plot Sun's Path on Sundial")
    print("(H) Solve End-Semester Homework")
    print("(Q) Quit Program\n")

    # Choose mode by user input
    mode = input("> Choose a mode and press enter...: ")
    print('\n\n')

    #    _____                    _    _____              _____                 
    #   / ____|                  | |  / ____|            / ____|                
    #  | |     ___   ___  _ __ __| | | (___  _   _ ___  | |     ___  _ ____   __
    #  | |    / _ \ / _ \| '__/ _` |  \___ \| | | / __| | |    / _ \| '_ \ \ / /
    #  | |___| (_) | (_) | | | (_| |  ____) | |_| \__ \ | |___| (_) | | | \ V / 
    #   \_____\___/ \___/|_|  \__,_| |_____/ \__, |___/  \_____\___/|_| |_|\_/  
    #                                         __/ |                             
    #                                        |___/                              
    # COORDINATE SYSTEM CONVERSION
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
            print("(Q) Quit to Main Menu\n")
            CoordMode = input("> Choose a number and press enter...:")

            print('\n')

            #  __  
            # /  | 
            # `| | 
            #  | | 
            # _| |__
            # \___(_)
            # 1. Horizontal to Equatorial I Coordinate System
            if(CoordMode == '1'):
                print(">> Conversion from Horizontal to Equatorial I Coordinate System")
                print(">> Give Parameters!")
                
                print(">> Would you like to give Geographical Coordinates by yourself,\n>> or would like just to choose a predefined Location's Coordinates?")
                print("Write \'1\' for User defined Coordinates, and write \'2\' for Predefined Locations' Coordinates!")

                HorToEquIILocationChoose = input(">> (1) User Defined, (2) Predefined: ")
                
                while(True):
                    if(HorToEquIILocationChoose == '1'):
                        print(">> HINT: You can write Latitude as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                        LatitudeHours = float(input("> Latitude (φ) Hours: ") or "0")
                        LatitudeMinutes = float(input("> Latitude (φ) Minutes: ") or "0")
                        LatitudeSeconds = float(input("> Latitude (φ) Seconds: ") or "0")
                        Latitude = LatitudeHours + LatitudeMinutes/60 + LatitudeSeconds/3600
                        break
                    
                    elif(HorToEquIILocationChoose == '2'):
                        while(True):
                            Location = input("> Location's name (type \'H\' for Help): ")

                            if(Location == "Help" or Location == "help" or Location == "H" or Location == "h"):
                                print("Predefined Locations you can choose from:")
                                for keys in LocationDict.items():
                                    print(keys)
                            
                            else:
                                try:
                                    Latitude = LocationDict[Location][0]

                                except KeyError:
                                    print(">>>> ERROR: The Location, named \"" + Location + "\" is not in the Database!")
                                    print(">>>> Type \"Help\" to list Available Cities in Database!")
                                    
                                else:
                                    break

                        break
                            
                    else:
                        print(">>>> ERROR: Invalid option! Try Again!")

                Altitude = float(input("> Altitude (m): "))
                Azimuth = float(input("> Azimuth (A): "))

                print("Is Local Mean Sidereal Time given?")
                while(True):
                    HorToEquIChoose = input("Write \'Y\' or \'N\' (Yes or No)")
                    if(HorToEquIChoose == 'Y' or HorToEquIChoose == 'y' or HorToEquIChoose == 'Yes' or HorToEquIChoose == 'yes' or HorToEquIChoose == 'YEs' or HorToEquIChoose == 'yEs' or HorToEquIChoose == 'yeS' or HorToEquIChoose == 'YeS' or HorToEquIChoose == 'yES'):
                        print(">> HINT: You can write LMST as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                        LocalSiderealTimeHours = float(input("> Local Mean Sidereal Time (S) Hours: ") or "0")
                        LocalSiderealTimeMinutes = float(input("> Local Mean Sidereal Time (S) Minutes: ") or "0")
                        LocalSiderealTimeSeconds = float(input("> Local Mean Sidereal Time (S) Seconds: ") or "0")
                        LocalSiderealTime = LocalSiderealTimeHours + LocalSiderealTimeMinutes/60 + LocalSiderealTimeSeconds/3600
                        break

                    elif(HorToEquIChoose == 'N' or HorToEquIChoose == 'n' or HorToEquIChoose == 'No' or HorToEquIChoose == 'no' or HorToEquIChoose == 'nO'):
                        LocalSiderealTime = None
                        break

                    else:
                        print(">>>> ERROR: Invalid option! Try Again!")

                # Used Formulas:
                # sin(δ) = sin(m) * sin(φ) + cos(m) * cos(φ) * cos(A)
                # sin(H) = - sin(A) * cos(m) / cos(δ)
                # α = S – t
                Declination, LocalHourAngle, RightAscension = HorToEquI(Latitude, Altitude, Azimuth, LocalSiderealTime)

                DeclinationHours = int(Declination)
                DeclinationMinutes = int((Declination - DeclinationHours) * 60)
                DeclinationSeconds = int((((Declination - DeclinationHours) * 60) - DeclinationMinutes) * 60)

                LocalHourAngleHours = int(LocalHourAngle)
                LocalHourAngleMinutes = int((LocalHourAngle - LocalHourAngleHours) * 60)
                LocalHourAngleSeconds = int((((LocalHourAngle - LocalHourAngleHours) * 60) - LocalHourAngleMinutes) * 60)

                # Print Results
                print("\n> Calculated parameters in Equatorial I Coord. Sys.:")
                
                declinmsg = "- Declination (δ): {0}° {1}\' {2}\""
                hourangmsg = "- Local Hour Angle (t): {0}h {1}m {2}s"
                print(declinmsg.format(DeclinationHours, DeclinationMinutes, DeclinationSeconds))
                print(hourangmsg.format(LocalHourAngleHours, LocalHourAngleMinutes, LocalHourAngleSeconds))
                
                if(LocalSiderealTime != None):
                    
                    RightAscensionHours = int(RightAscension)
                    RightAscensionMinutes = int((RightAscension - RightAscensionHours) * 60)
                    RightAscensionSeconds = int((((RightAscension - RightAscensionHours) * 60) - RightAscensionMinutes) * 60)

                    RAmsg = "- Right Ascension (α): {0}h {1}m {2}s"
                    print(RAmsg.format(RightAscensionHours, RightAscensionMinutes, RightAscensionSeconds))

                print('\n')

            #  _____   
            # / __  \  
            # `' / /'  
            #   / /    
            # ./ /____ 
            # \_____(_)
            # 2. Horizontal to Equatorial II Coordinate System
            elif(CoordMode == '2'):
                print(">> Conversion from Horizontal to Equatorial II Coordinate System")
                print(">> Give Parameters!")
                
                print(">> Would you like to give Geographical Coordinates by yourself,\n>> or would like just to choose a predefined Location's Coordinates?")
                print(">> Write \'1\' for User defined Coordinates, and write \'2\' for Predefined Locations' Coordinates!")

                HorToEquIILocationChoose = input(">> (1) User Defined, (2) Predefined: ")
                
                while(True):
                    if(HorToEquIILocationChoose == '1'):
                        print(">> HINT: You can write Latitude as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                        LatitudeHours = float(input("> Latitude (φ) Hours: ") or "0")
                        LatitudeMinutes = float(input("> Latitude (φ) Minutes: ") or "0")
                        LatitudeSeconds = float(input("> Latitude (φ) Seconds: ") or "0")
                        Latitude = LatitudeHours + LatitudeMinutes/60 + LatitudeSeconds/3600
                        break
                    
                    elif(HorToEquIILocationChoose == '2'):
                        while(True):
                            Location = input("> Location's name (type \'H\' for Help): ")

                            if(Location == "Help" or Location == "help" or Location == "H" or Location == "h"):
                                print(">> Predefined Locations you can choose from:")
                                for keys in LocationDict.items():
                                    print(keys)
                            
                            else:
                                try:
                                    Latitude = LocationDict[Location][0]

                                except KeyError:
                                    print(">>>> ERROR: The Location, named \"" + Location + "\" is not in the Database!")
                                    print(">>>> Type \"Help\" to list Available Cities in Database!")
                                    
                                else:
                                    break

                        break
                            
                    else:
                        print(">>>> ERROR: Invalid option! Try Again!")

                Altitude = float(input("> Altitude (m): "))
                Azimuth = float(input("> Azimuth (A): "))
                
                print(">> HINT: You can write LMST as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                LocalSiderealTimeHours = float(input("> Local Mean Sidereal Time (S) Hours: ") or "0")
                LocalSiderealTimeMinutes = float(input("> Local Mean Sidereal Time (S) Minutes: ") or "0")
                LocalSiderealTimeSeconds = float(input("> Local Mean Sidereal Time (S) Seconds: ") or "0")
                LocalSiderealTime = LocalSiderealTimeHours + LocalSiderealTimeMinutes/60 + LocalSiderealTimeSeconds/3600

                Declination, RightAscension, LocalSiderealTime = HorToEquII(Latitude, Altitude, Azimuth, LocalSiderealTime)

                DeclinationHours = int(Declination)
                DeclinationMinutes = int((Declination - DeclinationHours) * 60)
                DeclinationSeconds = int((((Declination - DeclinationHours) * 60) - DeclinationMinutes) * 60)

                RightAscensionHours = int(RightAscension)
                RightAscensionMinutes = int((RightAscension - RightAscensionHours) * 60)
                RightAscensionSeconds = int((((RightAscension - RightAscensionHours) * 60) - RightAscensionMinutes) * 60)

                LocalSiderealTimeHours = int(LocalSiderealTime)
                LocalSiderealTimeMinutes = int((LocalSiderealTime - LocalSiderealTimeHours) * 60)
                LocalSiderealTimeSeconds = int((((LocalSiderealTime - LocalSiderealTimeHours) * 60) - LocalSiderealTimeMinutes) * 60)


                # Print Results
                print("\n> Calculated Parameters in Equatorial II Coord. Sys.:")

                declinmsg = "- Declination (δ): {0}° {1}\' {2}\""
                RAmsg = "- Right Ascension (α): {0}h {1}m {2}s"
                sidermsg = "- Local Mean Sidereal Time (S): {0}:{1}:{2}\n"
                print(declinmsg.format(DeclinationHours, DeclinationMinutes, DeclinationSeconds))
                print(RAmsg.format(RightAscensionHours, RightAscensionMinutes, RightAscensionSeconds))
                print(sidermsg.format(LocalSiderealTimeHours, LocalSiderealTimeMinutes, LocalSiderealTimeSeconds))
                print('\n')

            #  _____  
            # |____ | 
            #     / / 
            #     \ \ 
            # .___/ / 
            # \____(_)
            # 3. Equatorial I to Horizontal Coordinate System
            elif(CoordMode == '3'):
                print(">> Conversion from Equatorial I to Horizontal Coordinate System")
                print(">> Give Parameters!\n")
                
                print(">>> LOCATION")
                print(">> Would you like to give Geographical Coordinates by yourself,\n>> Or would like just to choose a predefined Location's Coordinates?")
                print(">> Write \'1\' for User defined Coordinates, and\n>> Write \'2\' for Predefined Locations' Coordinates!")

                EquIToHorLocationChoose1 = input(">> (1) User Defined, (2) Predefined: ")
                
                while(True):
                    if(EquIToHorLocationChoose1 == '1'):
                        print(">> HINT: You can write Latitude as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                        LatitudeHours = float(input("> Latitude (φ) Hours: ") or "0")
                        LatitudeMinutes = float(input("> Latitude (φ) Minutes: ") or "0")
                        LatitudeSeconds = float(input("> Latitude (φ) Seconds: ") or "0")
                        Latitude = LatitudeHours + LatitudeMinutes/60 + LatitudeSeconds/3600
                        break
                    
                    elif(HorToEquIILocationChoose == '2'):
                        while(True):
                            Location = input("> Location's name (type \'H\' for Help): ")

                            if(Location == "Help" or Location == "help" or Location == "H" or Location == "h"):
                                print(">> Predefined Locations you can choose from:")
                                for keys in LocationDict.items():
                                    print(keys)
                            
                            else:
                                try:
                                    Latitude = LocationDict[Location][0]

                                except KeyError:
                                    print(">>>> ERROR: The Location, named \"" + Location + "\" is not in the Database!")
                                    print(">>>> Type \"Help\" to list Available Cities in Database!")
                                    
                                else:
                                    break

                        break
                            
                    else:
                        print(">>>> ERROR: Invalid option! Try Again!")

                print("\n>>> STELLAR OBJECT")
                print(">> Would you like to give the stellar object's Coordinates by yourself,\n>> Or would like just to choose a predefined object's Coordinates?")
                print(">> Write \'1\' for User defined Coordinates, and\n>> Write \'2\' for a Predefined Stellar Object's Coordinates!")

                EquIToHorStellarChoose = input(">> (1) User Defined, (2) Predefined: ")
                
                while(True):
                    if(EquIToHorStellarChoose == '1'):
                        print(">> Which Parameter Is given?")
                        RAorDecEquIToHorChoose = input(">> Only Right Ascension (write \'A\'), Only Declination (write \'D\'), Or Both of them (write \'B\')?: ")

                        if(RAorDecEquIToHorChoose == 'D' or RAorDecEquIToHorChoose == 'd'):
                            RightAscension = None
                            DeclinationHours = float(input("> Declination (δ) Hours: ") or "0")
                            DeclinationMinutes = float(input("> Declination (δ) Minutes: ") or "0")
                            DeclinationSeconds = float(input("> Declination (δ) Seconds: ") or "0")
                            Declination = DeclinationHours + DeclinationMinutes/60 + DeclinationSeconds/3600
                            break

                        elif(RAorDecEquIToHorChoose == 'B' or RAorDecEquIToHorChoose == 'b'):
                            print(">> HINT: You can write RA as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                            RightAscensionHours = float(input("> Right Ascension (α) Hours: ") or "0")
                            RightAscensionMinutes = float(input("> Right Ascension (α) Minutes: ") or "0")
                            RightAscensionSeconds = float(input("> Right Ascension (α) Seconds: ") or "0")
                            RightAscension = RightAscensionHours + RightAscensionMinutes/60 + RightAscensionSeconds/3600
                            DeclinationHours = float(input("> Declination (δ) Hours: ") or "0")
                            DeclinationMinutes = float(input("> Declination (δ) Minutes: ") or "0")
                            DeclinationSeconds = float(input("> Declination (δ) Seconds: ") or "0")
                            Declination = DeclinationHours + DeclinationMinutes/60 + DeclinationSeconds/3600
                            break

                        else:
                            print(">>>> ERROR: Invalid option! Try Again! Write \'D\' or \'B\'!")
                    
                    elif(EquIToHorStellarChoose == '2'):
                        while(True):
                            StellarObject = input("> Stellar object's name (type \'H\' for Help): ")

                            if(StellarObject == "Help" or StellarObject == "help" or StellarObject == "H" or StellarObject == "h"):
                                print(">> Predefined Objects you can choose from:")
                                for keys in StellarDict.items():
                                    print(keys)
                            
                            else:
                                try:
                                    TestVariable = StellarDict[StellarObject][0]
                                    del TestVariable

                                except KeyError:
                                    print(">>>> ERROR: The Stellar Object, named \"" + StellarObject + "\" is not in the Database!")
                                    print(">>>> Type \"Help\" to list Available Stellar Objects in Database!")

                                else:
                                    print(">> Which Parameter Is given?")
                                    print(">> Declination is essential for calculation Horizontal Coordinates!\n>> Right Ascension only, isn't enough for calculating these parameters!")
                                    RAorDecEquIToHorChoose = input(">> Only Declination (write \'D\'), Or both of Right Ascension and Declination (write \'B\')?: ")

                                    if(RAorDecEquIToHorChoose == 'D' or RAorDecEquIToHorChoose == 'd'):
                                        RightAscension = None
                                        Declination = StellarDict[StellarObject][1]
                                        break

                                    elif(RAorDecEquIToHorChoose == 'B' or RAorDecEquIToHorChoose == 'b'):
                                        RightAscension = StellarDict[StellarObject][0]
                                        Declination = StellarDict[StellarObject][1]
                                        break

                                    else:
                                        print(">>>> ERROR: Invalid option! Try Again! Write \'D\' or \'B\'!")

                        break

                    else:
                        print(">>>> ERROR: Invalid option! Try Again!")

                if(RightAscension != None and Declination != None):

                    print(">> Is Local Mean Sidereal Time given?")
                    while(True):
                        EquIToHorChoose1 = input(">> Write \'Y\' or \'N\' (Yes or No): ")

                        if(EquIToHorChoose1 == 'Y' or EquIToHorChoose1 == 'y' or EquIToHorChoose1 == 'Yes' or EquIToHorChoose1 == 'yes' or EquIToHorChoose1 == 'YEs' or EquIToHorChoose1 == 'yEs' or EquIToHorChoose1 == 'yeS' or EquIToHorChoose1 == 'YeS' or EquIToHorChoose1 == 'yES'):
                            print(">> HINT: You can write LMST as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                            LocalSiderealTimeHours = float(input("> Local Mean Sidereal Time (S) Hours: ") or "0")
                            LocalSiderealTimeMinutes = float(input("> Local Mean Sidereal Time (S) Minutes: ") or "0")
                            LocalSiderealTimeSeconds = float(input("> Local Mean Sidereal Time (S) Seconds: ") or "0")
                            LocalSiderealTime = LocalSiderealTimeHours + LocalSiderealTimeMinutes/60 + LocalSiderealTimeSeconds/3600
                            break

                        elif(EquIToHorChoose1 == 'N' or EquIToHorChoose1 == 'n' or EquIToHorChoose1 == 'No' or EquIToHorChoose1 == 'no' or EquIToHorChoose1 == 'nO'):
                            LocalSiderealTime = None

                            print("\n>> Is Local Hour Angle given?")
                            EquIToHorChoose2 = input(">> Write \'Y\' or \'N\' (Yes or No): ")

                            if(EquIToHorChoose2 == 'Y' or EquIToHorChoose2 == 'y' or EquIToHorChoose2 == 'Yes' or EquIToHorChoose2 == 'yes' or EquIToHorChoose2 == 'YEs' or EquIToHorChoose2 == 'yEs' or EquIToHorChoose2 == 'yeS' or EquIToHorChoose2 == 'YeS' or EquIToHorChoose2 == 'yES'):
                                print(">> HINT: You can write LHA as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                                LocalHourAngleHours = float(input("> Local Hour Angle (t) Hours: ") or "0")
                                LocalHourAngleMinutes = float(input("> Local Hour Angle (t) Minutes: ") or "0")
                                LocalHourAngleSeconds = float(input("> Local Hour Angle (t) Seconds: ") or "0")
                                LocalHourAngle = LocalHourAngleHours + LocalHourAngleMinutes/60 + LocalHourAngleSeconds/3600
                                break

                            elif(EquIToHorChoose2 == 'N' or EquIToHorChoose2 == 'n' or EquIToHorChoose2 == 'No' or EquIToHorChoose2 == 'no' or EquIToHorChoose2 == 'nO'):
                                LocalHourAngle = None
                                print("\n From the given data, you can calculate Azimuth (A),\n>> If Altitude (m) is given.")

                                Azimuth == None
                                Altitude = float(input("> Altitude (m): "))
                                break

                elif(Declination != None and RightAscension == None):

                    print("\n>> Is Local Hour Angle given?")
                    EquIToHorChooseD = input(">> Write \'Y\' or \'N\' (Yes or No): ")

                    if(EquIToHorChooseD == 'Y' or EquIToHorChooseD == 'y' or EquIToHorChooseD == 'Yes' or EquIToHorChooseD == 'yes' or EquIToHorChooseD == 'YEs' or EquIToHorChooseD == 'yEs' or EquIToHorChooseD == 'yeS' or EquIToHorChooseD == 'YeS' or EquIToHorChooseD == 'yES'):
                        print(">> HINT: You can write LHA as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                        LocalHourAngleHours = float(input("> Local Hour Angle (t) Hours: ") or "0")
                        LocalHourAngleMinutes = float(input("> Local Hour Angle (t) Minutes: ") or "0")
                        LocalHourAngleSeconds = float(input("> Local Hour Angle (t) Seconds: ") or "0")
                        LocalHourAngle = LocalHourAngleHours + LocalHourAngleMinutes/60 + LocalHourAngleSeconds/3600
                        break

                    elif(EquIToHorChooseD == 'N' or EquIToHorChooseD == 'n' or EquIToHorChooseD == 'No' or EquIToHorChooseD == 'no' or EquIToHorChooseD == 'nO'):
                        LocalHourAngle = None
                        print("\n From the given data, you can calculate Azimuth (A),\n>> If Altitude (m) is given.")

                        Azimuth == None
                        Altitude = float(input("> Altitude (m): "))
                        break

                    else:
                        print(">>>> ERROR: Invalid option! Try Again!")

                # Starting parameters could be:
                # 1. Latitude, RightAscension, Declination, LocalSiderealTime   # φ,α,δ,S:  S,α -> t; t -> H; H,δ,φ -> m; H,δ,m -> A    # Output: A,m
                # 2. Latitude, RightAscension, Declination, LocalHourAngle      # φ,α,δ,t:  t -> H; H,δ,φ -> m; H,δ,m -> A              # Output: A,m
                # 3. Latitude, RightAscension, Declination, Azimuth             # φ,α,δ,A:  Not Enough Parameters!                      # Output: None
                # 4. Latitude, RightAscension, Declination, Altitude            # φ,α,δ,m:  m,δ,φ -> H; H,δ,m -> A                      # Output: A from m
                # 5. Latitude, RightAscension, LocalSiderealTime                # φ,α,S:    Not Enough Parameters!                      # Output: None
                # 6. Latitude, RightAscension, LocalHourAngle                   # φ,α,t:    Not Enough Parameters!                      # Output: None
                # 7. Latitude, RightAscension, Azimuth                          # φ,α,A:    Not Enough Parameters!                      # Output: None
                # 8. Latitude, RightAscension, Altitude                         # φ,α,m:    Not Enough Parameters!                      # Output: None
                # 9. Latitude, Declination, LocalSiderealTime                   # φ,δ,S:    Not Enough Parameters!                      # Output: None
                # 10. Latitude, Declination, LocalHourAngle                     # φ,δ,t:    t -> H; H,δ,φ -> m; H,δ,m -> A              # Output: A,m
                # 11. Latitude, Declination, Azimuth                            # φ,δ,A:    Not Enough Parameters!                      # Output: None
                # 12. Latitude, Declination, Altitude                           # φ,δ,m:    m,δ,φ -> H; H,δ,m -> A                      # Output: A from m
                # !!!! Now only those could be selected, which has any kind of output !!!!


                # Used formulas:
                # t = S - α
                # sin(m) = sin(δ) * sin(φ) + cos(δ) * cos(φ) * cos(H)
                if(LocalSiderealTime != None or LocalHourAngle != None):
                    Altitude, Azimuth = EquIToHor(Latitude, RightAscension, Declination, Altitude, Azimuth, LocalSiderealTime, LocalHourAngle)

                    # Print Results
                    print("\n> Calculated Parameters in Horizontal Coord. Sys.:")

                    azimmsg = "- Azimuth (A):  {0}°"
                    altitmsg = "- Altitude (m): {0}°"
                    print(azimmsg.format(Azimuth))
                    print(altitmsg.format(Altitude))
                    print('\n')

                # Used formulas:
                # cos(H) = (sin(m) - sin(δ) * sin(φ)) / cos(δ) * cos(φ)
                # sin(A) = - sin(H) * cos(δ) / cos(m)
                elif(Altitude != None):
                    Altitude, Azimuth1, Azimuth2, H_dil = EquIToHor(Latitude, RightAscension, Declination, Altitude, Azimuth, LocalSiderealTime, LocalHourAngle)

                    # Print Results
                    print(">> Available Data are only suited for Calculating Rising/Setting Altitudes!")
                    print("\n> Calculated Parameter of Rising/Setting Object in Horizontal Coord. Sys.:")

                    azimmsg = "- Rising and Setting Azimuths (A) are:\n- {0}° and {1}°"
                    print(azimmsg.format(Azimuth2, Azimuth1))
                    print('\n')
                    
            #    ___   
            #   /   |  
            #  / /| |  
            # / /_| |  
            # \___  |_ 
            #     |_(_)
            # 4. Equatorial I to Equatorial II Coordinate System
            elif(CoordMode == '4'):
                print(">> Conversion from Equatorial I to Equatorial II Coordinate System")
                print(">> Give Parameters!")

                print(">> Would you like to give the stellar object's Coordinates by yourself,\n>> Or would like just to choose a predefined object's Coordinates?")
                print(">> Write \'1\' for User defined Coordinates, and\n>> Write \'2\' for a Predefined Stellar Object's Coordinates!")

                EquIToEquIIStellarChoose = input(">> (1) User Defined, (2) Predefined: ")

                while(True):
                    if(EquIToEquIIStellarChoose == '1'):
                        print(">> HINT: You can write RA as a Decimal Fraction. For this you need to write Hours as a float-type value, and type 0\n>> For both Minutes and Seconds.")
                        RightAscensionHours = float(input("> Right Ascension (α) Hours: ") or "0")
                        RightAscensionMinutes = float(input("> Right Ascension (α) Minutes: ") or "0")
                        RightAscensionSeconds = float(input("> Right Ascension (α) Seconds: ") or "0")
                        RightAscension = RightAscensionHours + RightAscensionMinutes/60 + RightAscensionSeconds/3600

                        print(">> Is Declination given?")
                        while(True):
                            EquIToEquIIChoose = input(">> Write \'Y\' or \'N\' (Yes or No): ")
                            
                            if(EquIToEquIIChoose == 'Y' or EquIToEquIIChoose == 'y' or EquIToEquIIChoose == 'Yes' or EquIToEquIIChoose == 'yes' or EquIToEquIIChoose == 'YEs' or EquIToEquIIChoose == 'yEs' or EquIToEquIIChoose == 'yeS' or EquIToEquIIChoose == 'YeS' or EquIToEquIIChoose == 'yES'):
                                Declination = float(input("> Declination (δ): "))
                                break
                            
                            elif(EquIToEquIIChoose == 'N' or EquIToEquIIChoose == 'n' or EquIToEquIIChoose == 'No' or EquIToEquIIChoose == 'no' or EquIToEquIIChoose == 'nO'):
                                Declination = None

                            else:
                                print(">>>> ERROR: Invalid option! Try Again!")
                    
                    elif(EquIToEquIIStellarChoose == '2'):
                        while(True):
                            StellarObject = input("> Stellar object's name (type \'H\' for Help): ")

                            if(StellarObject == "Help" or StellarObject == "help" or StellarObject == "H" or StellarObject == "h"):
                                print(">> Predefined Objects you can choose from:")
                                for keys in StellarDict.items():
                                    print(keys)
                            
                            else:
                                try:
                                    TestVariable = StellarDict[StellarObject][0]
                                    del TestVariable

                                except KeyError:
                                    print(">>>> ERROR: The Stellar Object, named \"" + StellarObject + "\" is not in the Database!")
                                    print(">>>> Type \"Help\" to list Available Stellar Objects in Database!")

                                else:
                                    RightAscension = StellarDict[StellarObject][0]

                                    print(">> Is Declination given?")
                                    while(True):
                                        EquIToEquIIChoose = input(">> Write \'Y\' or \'N\' (Yes or No): ")

                                        if(EquIToEquIIChoose == 'Y' or EquIToEquIIChoose == 'y' or EquIToEquIIChoose == 'Yes' or EquIToEquIIChoose == 'yes' or EquIToEquIIChoose == 'YEs' or EquIToEquIIChoose == 'yEs' or EquIToEquIIChoose == 'yeS' or EquIToEquIIChoose == 'YeS' or EquIToEquIIChoose == 'yES'):
                                            Declination = StellarDict[StellarObject][1]
                                            break

                                        elif(EquIToEquIIChoose == 'N' or EquIToEquIIChoose == 'n' or EquIToEquIIChoose == 'No' or EquIToEquIIChoose == 'no' or EquIToEquIIChoose == 'nO'):
                                            Declination = None

                                        else:
                                            print(">>>> ERROR: Invalid option! Try Again!")

                        break

                    else:
                        print(">>>> ERROR: Invalid option! Try Again!")

                print(">> You should input LHA (t) manually!")
                print(">> HINT: You can write LHA as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                LocalHourAngleHours = float(input("> Local Hour Angle (t) Hours: ") or "0")
                LocalHourAngleMinutes = float(input("> Local Hour Angle (t) Minutes: ") or "0")
                LocalHourAngleSeconds = float(input("> Local Hour Angle (t) Seconds: ") or "0")
                LocalHourAngle = LocalHourAngleHours + LocalHourAngleMinutes/60 + LocalHourAngleSeconds/3600

                LocalSiderealTime = EquIToEquII(RightAscension, LocalHourAngle)

                LocalSiderealTimeHours = int(LocalSiderealTime)
                LocalSiderealTimeMinutes = int((LocalSiderealTime - LocalSiderealTimeHours) * 60)
                LocalSiderealTimeSeconds = int((((LocalSiderealTime - LocalSiderealTimeHours) * 60) - LocalSiderealTimeMinutes) * 60)

                # Print Results
                print("\n> Calculated Parameters in Equatorial II Coord. Sys.:")

                sidermsg = "- Local Mean Sidereal Time (S): {0}:{1}:{2}"
                print(sidermsg.format(LocalSiderealTime))
                
                if(Declination != None):

                    DeclinationHours = int(Declination)
                    DeclinationMinutes = int((Declination - DeclinationHours) * 60)
                    DeclinationSeconds = int((((Declination - DeclinationHours) * 60) - DeclinationMinutes) * 60)

                    declinmsg = "- Declination (δ): {0}° {1}\' {2}\""
                    print(declinmsg.format(Declination))

                else:
                    print("Declination is Unknown!")

                print('\n')

            #  _____  
            # |  ___| 
            # |___ \  
            #     \ \ 
            # /\__/ / 
            # \____(_)
            # 5. Equatorial II to Equatorial I Coordinate System
            elif(CoordMode == '5'):
                print(">> Conversion from Equatorial II to Equatorial I Coordinate System")
                print(">> Give Parameters!")

                print(">> You should input LMST (S) manually!")
                print(">> HINT: You can write LMST as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                LocalSiderealTimeHours = float(input("> Local Mean Sidereal Time (S) Hours: ") or "0")
                LocalSiderealTimeMinutes = float(input("> Local Mean Sidereal Time (S) Minutes: ") or "0")
                LocalSiderealTimeSeconds = float(input("> Local Mean Sidereal Time (S) Seconds: ") or "0")
                LocalSiderealTime = LocalSiderealTimeHours + LocalSiderealTimeMinutes/60 + LocalSiderealTimeSeconds/3600

                print(">> Is Declination given?")
                while(True):
                    EquIIToEquIChoose = input(">> Write \'Y\' or \'N\' (Yes or No): ")
                    
                    if(EquIIToEquIChoose == 'Y' or EquIIToEquIChoose == 'y' or EquIIToEquIChoose == 'Yes' or EquIIToEquIChoose == 'yes' or EquIIToEquIChoose == 'YEs' or EquIIToEquIChoose == 'yEs' or EquIIToEquIChoose == 'yeS' or EquIIToEquIChoose == 'YeS' or EquIIToEquIChoose == 'yES'):
                        Declination = float(input("> Declination (δ): "))
                        break
                    
                    elif(EquIIToEquIChoose == 'N' or EquIIToEquIChoose == 'n' or EquIIToEquIChoose == 'No' or EquIIToEquIChoose == 'no' or EquIIToEquIChoose == 'nO'):
                        Declination = None

                    else:
                        print(">>>> ERROR: Invalid option! Try Again!")

                while(True):
                    print(">> Which essential Parameter Is given?")
                    EquIIToEquIDecChoose = input(">> Right Ascension (write \'A\'), or Local Hour Angle in Hours (write \'T\')?: ")
                    if(EquIIToEquIDecChoose == 'A' or EquIIToEquIDecChoose == 'a'):
                        LocalHourAngle = None
                        RightAscension = float(input("> Right Ascension (α): "))
                        break

                    elif(EquIIToEquIDecChoose == 'T' or EquIIToEquIDecChoose == 't'):
                        print(">> HINT: You can write LHA as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                        LocalHourAngleHours = float(input("> Local Hour Angle (t) Hours: ") or "0")
                        LocalHourAngleMinutes = float(input("> Local Hour Angle (t) Minutes: ") or "0")
                        LocalHourAngleSeconds = float(input("> Local Hour Angle (t) Seconds: ") or "0")
                        LocalHourAngle = LocalHourAngleHours + LocalHourAngleMinutes/60 + LocalHourAngleSeconds/3600
                        RightAscension = None
                        break

                    else:
                        print(">>>> ERROR: Invalid option! Try Again! Write \'A\' or \'T\'!")

                LocalHourAngle, RightAscension = EquIIToEquI(LocalSiderealTime, RightAscension, LocalHourAngle)

                RightAscensionHours = int(RightAscension)
                RightAscensionMinutes = int((RightAscension - RightAscensionHours) * 60)
                RightAscensionSeconds = int((((RightAscension - RightAscensionHours) * 60) - RightAscensionMinutes) * 60)

                # Print Results
                print("\n> Calculated parameters in Equatorial I Coord. Sys.:")

                RAmsg = "- Right Ascension (α): {0}h {1}m {2}s"
                print(RAmsg.format(RightAscension))

                if(Declination != None):

                    DeclinationHours = int(Declination)
                    DeclinationMinutes = int((Declination - DeclinationHours) * 60)
                    DeclinationSeconds = int((((Declination - DeclinationHours) * 60) - DeclinationMinutes) * 60)

                    declinmsg = "- Declination (δ): {0}° {1}\' {2}\""
                    print(declinmsg.format(Declination))

                else:
                    print("Declination is Unknown!")

                print('\n')

                hourangmsg = "- Local Hour Angle (t): {0}h {1}m {2}s"
                print(hourangmsg.format(LocalHourAngle))
                
                print('\n')

            #   ____   
            #  / ___|  
            # / /___   
            # | ___ \  
            # | \_/ |_ 
            # \_____(_)
            # 6. Equatorial II to Horizontal Coordinate System
            elif(CoordMode == '6'):
                print(">> Conversion from Equatorial II to Horizontal Coordinate System")
                print(">> Give Parameters!")

                print(">>> LOCATION")
                print(">> Would you like to give Geographical Coordinates by yourself,\n>> Or would like just to choose a predefined Location's Coordinates?")
                print(">> Write \'1\' for User defined Coordinates, and\n>> Write \'2\' for Predefined Locations' Coordinates!")

                EquIIToHorLocationChoose = input(">> (1) User Defined, (2) Predefined: ")

                while(True):
                    if(EquIIToHorLocationChoose == '1'):
                        print(">> HINT: You can write Latitude as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                        LatitudeHours = float(input("> Latitude (φ) Hours: ") or "0")
                        LatitudeMinutes = float(input("> Latitude (φ) Minutes: ") or "0")
                        LatitudeSeconds = float(input("> Latitude (φ) Seconds: ") or "0")
                        Latitude = LatitudeHours + LatitudeMinutes/60 + LatitudeSeconds/3600
                        break

                    elif(EquIIToHorLocationChoose == '2'):
                        while(True):
                            Location = input("> Location's name (type \'H\' for Help): ")

                            if(Location == "Help" or Location == "help" or Location == "H" or Location == "h"):
                                print(">> Predefined Locations you can choose from:")
                                for keys in LocationDict.items():
                                    print(keys)

                            else:
                                try:
                                    Latitude = LocationDict[Location][0]

                                except KeyError:
                                    print(">>>> ERROR: The Location, named \"" + Location + "\" is not in the Database!")
                                    print(">>>> Type \"Help\" to list Available Cities in Database!")

                                else:
                                    break

                        break

                    else:
                        print(">>>> ERROR: Invalid option! Try Again!")

                print("\n>>> STELLAR OBJECT")
                print(">> Would you like to give the stellar object's Coordinates by yourself,\n>> Or would like just to choose a predefined object's Coordinates?")
                print(">> Write \'1\' for User defined Coordinates, and\n>> Write \'2\' for a Predefined Stellar Object's Coordinates!")

                EquIIToHorStellarChoose = input(">> (1) User Defined, (2) Predefined: ")

                while(True):
                    if(EquIIToHorStellarChoose == '1'):
                        
                        print(">> Which essential Parameter Is given?")
                        EquIIToEquIDecChoose = input(">> Right Ascension (write \'A\'), or Local Hour Angle in Hours (write \'T\')?: ")
                        if(EquIIToEquIDecChoose == 'A' or EquIIToEquIDecChoose == 'a'):
                            LocalHourAngle = None
                            print(">> HINT: You can write RA as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                            RightAscensionHours = float(input("> Right Ascension (α) Hours: ") or "0")
                            RightAscensionMinutes = float(input("> Right Ascension (α) Minutes: ") or "0")
                            RightAscensionSeconds = float(input("> Right Ascension (α) Seconds: ") or "0")
                            RightAscension = RightAscensionHours + RightAscensionMinutes/60 + RightAscensionSeconds/3600
                            break

                        elif(EquIIToEquIDecChoose == 'T' or EquIIToEquIDecChoose == 't'):
                            print(">> HINT: You can write LHA as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                            LocalHourAngleHours = float(input("> Local Hour Angle (t) Hours: ") or "0")
                            LocalHourAngleMinutes = float(input("> Local Hour Angle (t) Minutes: ") or "0")
                            LocalHourAngleSeconds = float(input("> Local Hour Angle (t) Seconds: ") or "0")
                            LocalHourAngle = LocalHourAngleHours + LocalHourAngleMinutes/60 + LocalHourAngleSeconds/3600
                            RightAscension = None
                            break

                        else:
                            print(">>>> ERROR: Invalid option! Try Again! Write \'A\' or \'T\'!")
                    
                    elif(EquIIToHorStellarChoose == '2'):
                        while(True):
                            StellarObject = input("> Stellar object's name (type \'H\' for Help): ")

                            if(StellarObject == "Help" or StellarObject == "help" or StellarObject == "H" or StellarObject == "h"):
                                print(">> Predefined Objects you can choose from:")
                                for keys in StellarDict.items():
                                    print(keys)

                            else:
                                try:
                                    TestVariable = StellarDict[StellarObject][0]
                                    del TestVariable

                                except KeyError:
                                    print(">>>> ERROR: The Stellar Object, named \"" + StellarObject + "\" is not in the Database!")
                                    print(">>>> Type \"Help\" to list Available Stellar Objects in Database!")

                                else:
                                    print(">> Which essential Parameter Is given?")
                                    EquIIToEquIDecChoose = input(">> Right Ascension (write \'A\'), or Local Hour Angle in Hours (write \'T\')?: ")
                                    if(EquIIToEquIDecChoose == 'A' or EquIIToEquIDecChoose == 'a'):
                                        LocalHourAngle = None
                                        RightAscension = StellarDict[StellarObject][0]
                                        break

                                    elif(EquIIToEquIDecChoose == 'T' or EquIIToEquIDecChoose == 't'):
                                        print(">> You should input LHA (t) manually!")
                                        print(">> HINT: You can write LHA as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                                        LocalHourAngleHours = float(input("> Local Hour Angle (t) Hours: ") or "0")
                                        LocalHourAngleMinutes = float(input("> Local Hour Angle (t) Minutes: ") or "0")
                                        LocalHourAngleSeconds = float(input("> Local Hour Angle (t) Seconds: ") or "0")
                                        LocalHourAngle = LocalHourAngleHours + LocalHourAngleMinutes/60 + LocalHourAngleSeconds/3600
                                        RightAscension = None
                                        break

                                    else:
                                        print(">>>> ERROR: Invalid option! Try Again! Write \'A\' or \'T\'!")

                        break

                    else:
                        print(">>>> ERROR: Invalid option! Try Again!")

                print(">> You should input LMST (S) manually!")
                print(">> HINT: You can write LMST as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                LocalSiderealTimeHours = float(input("> Local Mean Sidereal Time (S) Hours: ") or "0")
                LocalSiderealTimeMinutes = float(input("> Local Mean Sidereal Time (S) Minutes: ") or "0")
                LocalSiderealTimeSeconds = float(input("> Local Mean Sidereal Time (S) Seconds: ") or "0")
                LocalSiderealTime = LocalSiderealTimeHours + LocalSiderealTimeMinutes/60 + LocalSiderealTimeSeconds/3600

                Altitude, Azimuth = EquIIToHor(Latitude, RightAscension, Declination, Altitude, Azimuth, LocalSiderealTime, LocalHourAngle)

                # Print Results
                print("> Calculated Parameters in Horizontal Coord. Sys.:")

                azimmsg = ">>> Azimuth (A):  {0}°"
                altitmsg = ">>> Altitude (m): {0}°"
                print(azimmsg.format(Azimuth))
                print(altitmsg.format(Altitude))
                print('\n')

            elif(CoordMode == 'Q' or CoordMode == 'q'):
                break

            else:
                print(">>>> ERROR: Invalid option! Try Again!\n")

    #    _____                    _____  _     _      _____      _      
    #   / ____|                  |  __ \(_)   | |    / ____|    | |     
    #  | |  __  ___  ___   __ _  | |  | |_ ___| |_  | |     __ _| | ___ 
    #  | | |_ |/ _ \/ _ \ / _` | | |  | | / __| __| | |    / _` | |/ __|
    #  | |__| |  __/ (_) | (_| | | |__| | \__ \ |_  | |___| (_| | | (__ 
    #   \_____|\___|\___/ \__, | |_____/|_|___/\__|  \_____\__,_|_|\___|
    #                      __/ |                                        
    #                     |___/                                         
    # GEOGRAPHICAL DISTANCE CALCULATION
    elif(mode == '2'):
        while(True):
            print(">> Geographical Distance Calculator\n")
            print(">> Please choose a mode you'd like to use!")
            print("(1) Positional Coordinates from User Input")
            print("(2) Positional Coordinates of Predefined Locations")
            print("(Q) Quit to Main Menu")
            DistMode = input("> Choose a mode and press enter...: ")

            print('\n')
            if(DistMode == '1'):
                print(">> Calculate Distance from given Coordinates\n")
                print(">> Give Parameters!")
                Latitude1 = float(input("> Latitude #1 (φ1): "))
                Longitude1 = float(input("> Longitude #1 (λ1): "))
                Latitude2 = float(input("> Latitude #2 (φ2): "))
                Longitude2 = float(input("> Longitude #2 (λ2): "))

                Distance = GeogDistCalc(Latitude1, Latitude2, Longitude1, Longitude2)
                # Convert Distance to Km
                Distance = float(Distance / 1000)

                distmsg = "\n>>> The Geographical Distance Between\n>>> {0}°,{1}°\n>>> and\n>>> {2}°,{3}°\n>>> is\n>>> {4:.3f} km\n"
                print(distmsg.format(Latitude1,Longitude1,Latitude2,Longitude2, Distance))

            elif(DistMode == '2'):
                print(">> Calculate Distance of Choosen Predefined Locations\n")
                print(">> Write the Names of Two Choosen Cities to the Input!")
                while(True):
                    Location1 = input("Location #1 (type \'H\' for Help): ")

                    if(Location1 == "Help" or Location1 == "help" or Location1 == "H" or Location1 == "h"):
                        print(">> Predefined Locations you can choose from:")
                        for keys in LocationDict.items():
                            print(keys)

                    else:
                        try:
                            Latitude1 = LocationDict[Location1][0]
                            Longitude1 = LocationDict[Location1][1]

                        except KeyError:
                            print(">>>> ERROR: The Location, named \"" + Location1 + "\" is not in the Database!")
                            print(">>>> Type \"Help\" to list Available Cities in Database!")

                        else:
                            break

                while(True):
                    Location2 = input("Location #2 (type \'H\' for Help): ")

                    if(Location2 == "Help" or Location2 == "help" or Location2 == "H" or Location2 == "h"):
                        print(">> Predefined Locations you can choose from:")
                        for keys in LocationDict.items():
                            print(keys)

                    else:
                        try:
                            Latitude2 = LocationDict[Location2][0]
                            Longitude2 = LocationDict[Location2][1]

                        except KeyError:
                            print(">>>> ERROR: The Location, named \"" + Location2 + "\" is not in the Database!")
                            print(">>>> Type \"Help\" to list Available Cities in Database!")
                            
                        else:
                            break

                Distance = GeogDistLocationCalc(Latitude1, Latitude2, Longitude1, Longitude2)
                # Convert Distance to Km
                Distance = float(Distance / 1000)

                distmsg = "\n>>> The Geographical Distance Between\n>>> {0} and {1} is\n>>> {2:.3f} km\n"
                print(distmsg.format(Location1, Location2, Distance))

            elif(DistMode == 'Q' or DistMode == 'q'):
                break

            else:
                print(">>>> ERROR: Invalid option! Try Again!")

    #   _      __  __  _____ _______    _____      _      
    #  | |    |  \/  |/ ____|__   __|  / ____|    | |     
    #  | |    | \  / | (___    | |    | |     __ _| | ___ 
    #  | |    | |\/| |\___ \   | |    | |    / _` | |/ __|
    #  | |____| |  | |____) |  | |    | |___| (_| | | (__ 
    #  |______|_|  |_|_____/   |_|     \_____\__,_|_|\___|
    # LOCAL MEAN SIDEREAL TIME CALCULATION
    elif(mode == '3'):
        while(True):
            print(">> Local Mean Sidereal Time Calculator\n")
            print(">> Please choose a mode you'd like to use!")
            print("(1) Parameters from User Input")
            print("(2) Parameters of Predefined Locations")
            print("(Q) Quit to Main Menu")
            DistMode = input("> Choose a mode and press enter...: ")

            print('\n')

            if(DistMode == '1'):
                print(">> Calculate LMST from given Parameters\n")
                print(">> Give Parameters!")
                
                # Input Positional Parameters
                print(">> HINT: You can write Latitude as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                LatitudeHours = float(input("> Latitude (φ) Hours: ") or "0")
                LatitudeMinutes = float(input("> Latitude (φ) Minutes: ") or "0")
                LatitudeSeconds = float(input("> Latitude (φ) Seconds: ") or "0")
                Latitude = LatitudeHours + LatitudeMinutes/60 + LatitudeSeconds/3600

                print(">> HINT: You can write Longitude as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                LongitudeHours = float(input("> Longitude (λ) Hours: ") or "0")
                LongitudeMinutes = float(input("> Longitude (λ) Minutes: ") or "0")
                LongitudeSeconds = float(input("> Longitude (λ) Seconds: ") or "0")
                Longitude = LongitudeHours + LongitudeMinutes/60 + LongitudeSeconds/3600

                # Input Time Parameters
                while(True):
                    DateYear = int(input("> Year: "))
                    if(DateYear != 0):
                        break
                    else:
                        print(">>>> ERROR: Year 0 is not defined! Please write another date!\n")

                while(True):
                    DateMonth = int(input("> Month: "))
                    if(DateMonth > 0 and DateMonth < 13):
                        break
                    else:
                        print(">>>> ERROR: Months should be inside [1,12] interval, and should be Integer!\n")

                while(True):
                    DateDay = int(input("> Day: "))
                    if(DateYear%4 == 0 and (DateYear%100 != 0 or DateYear%400 == 0)):
                        if(MonthLengthListLeapYear[DateMonth - 1] >= DateDay and DateDay > 0):
                            break
                        else:
                            daysmsg = ">>>> ERROR: Days should be inside [1,{0}] interval, and should be Integer!\n"
                            print(daysmsg.format(MonthLengthListLeapYear[DateMonth - 1]))
                    else:
                        if(MonthLengthList[DateMonth - 1] >= DateDay and DateDay > 0):
                            break
                        else:
                            daysmsg = ">>>> ERROR: Days should be inside [1,{0}] interval, and should be Integer!\n"
                            print(daysmsg.format(MonthLengthList[DateMonth - 1]))

                while(True):
                    LocalHours = float(input("> Local Hours: ") or "0")
                    if(LocalHours >= 0 and LocalHours < 24):
                        break
                    else:
                        print(">>>> ERROR: Hours should be inside [0,24[ interval!\n")

                while(True):
                    LocalMinutes = int(input("> Local Minutes: ") or "0")
                    if(LocalMinutes >= 0 and LocalMinutes <= 59):
                        break
                    else:
                        print(">>>> ERROR: Minutes should be inside [0,59] interval, and should be Integer!\n")

                while(True):
                    LocalSeconds = float(input("> Local Seconds: ") or "0")
                    if(LocalSeconds >= 0 and LocalSeconds < 60):
                        break
                    else:
                        print(">>>> ERROR: Seconds should be inside [0,60[ interval!\n")

                LocalSiderealHours, LocalSiderealMinutes, LocalSiderealSeconds, UnitedHours, UnitedMinutes, UnitedSeconds, GreenwichHours, GreenwichMinutes, GreenwichSeconds = LocalSiderealTimeCalc(Longitude, LocalHours, LocalMinutes, LocalSeconds, DateYear, DateMonth, DateDay)

                sidmsg = "\n>>> The Local Mean Sidereal Time\n>>> at {0}:{1}:{2} UT, at location\n>>> {3}°,{4}° with\n>>> {5}:{6}:{7} GMST at 00:00:00 UT\n>>> is {8}:{9}:{10}\n\n"
                print(sidmsg.format(UnitedHours, UnitedMinutes, UnitedSeconds, Latitude, Longitude, GreenwichHours, GreenwichMinutes, GreenwichSeconds, LocalSiderealHours, LocalSiderealMinutes, LocalSiderealSeconds))

            elif(DistMode == '2'):
                print(">> Calculate LMST from the Coordinates of a Predefined Location\n")
                print(">> Write the Name of a Choosen Location to the Input!")

                # Input Choosen Location's Name
                while(True):
                    Location = input("> Location's name (type \'H\' for Help): ")
                    
                    if(Location == "Help" or Location == "help" or Location == "H" or Location == "h"):
                        print(">> Predefined Locations you can choose from:")
                        for keys in LocationDict.items():
                            print(keys)
                    
                    else:
                        try:
                            Longitude = LocationDict[Location][1]

                        except KeyError:
                            print(">>>> ERROR: The Location, named \"" + Location + "\" is not in the Database!")
                            print(">>>> Type \"Help\" to list Available Cities in Database!")
                            
                        else:
                            break

                # Input Time Parameters
                while(True):
                    DateYear = int(input("> Year: "))
                    if(DateYear != 0):
                        break
                    else:
                        print(">>>> ERROR: Year 0 is not defined! Please write another date!\n")
                
                while(True):
                    DateMonth = int(input("> Month: "))
                    if(DateMonth > 0 and DateMonth < 13):
                        break
                    else:
                        print(">>>> ERROR: Months should be inside [1,12] interval, and should be Integer!\n")

                # Leap Year	Handling
                while(True):
                    DateDay = int(input("> Day: "))
                    if(DateYear%4 == 0 and (DateYear%100 != 0 or DateYear%400 == 0)):
                        if(MonthLengthListLeapYear[DateMonth - 1] >= DateDay and DateDay > 0):
                            break
                        else:
                            daysmsg = ">>>> ERROR: Days should be inside [1,{0}] interval, and should be Integer!\n"
                            print(daysmsg.format(MonthLengthListLeapYear[DateMonth - 1]))
                    else:
                        if(MonthLengthList[DateMonth - 1] >= DateDay and DateDay > 0):
                            break
                        else:
                            daysmsg = ">>>> ERROR: Days should be inside [1,{0}] interval, and should be Integer!\n"
                            print(daysmsg.format(MonthLengthList[DateMonth - 1]))

                while(True):
                    LocalHours = float(input("> Local Hours: ") or "0")
                    if(LocalHours >= 0 and LocalHours < 24):
                        break
                    else:
                        print(">>>> ERROR: Hours should be inside [0,24[ interval!\n")

                while(True):
                    LocalMinutes = int(input("> Local Minutes: ") or "0")
                    if(LocalMinutes >= 0 and LocalMinutes <= 59):
                        break
                    else:
                        print(">>>> ERROR: Minutes should be inside [0,59] interval, and should be Integer!\n")

                while(True):
                    LocalSeconds = float(input("> Local Seconds: ") or "0")
                    if(LocalSeconds >= 0 and LocalSeconds < 60):
                        break
                    else:
                        print(">>>> ERROR: Seconds should be inside [0,60[ interval!\n")

                LocalSiderealHours, LocalSiderealMinutes, LocalSiderealSeconds, UnitedHours, UnitedMinutes, UnitedSeconds, GreenwichHours, GreenwichMinutes, GreenwichSeconds = LocalSiderealTimeCalc(Longitude, LocalHours, LocalMinutes, LocalSeconds, DateYear, DateMonth, DateDay)

                sidmsg = "\n>>> The Local Mean Sidereal Time at {0}:{1}:{2} UT\n>>> in {3} with\n>>> {4}:{5}:{6} GMST at 00:00:00 UT\n>>> is {7}:{8}:{9}\n\n"
                print(sidmsg.format(UnitedHours, UnitedMinutes, UnitedSeconds, Location, GreenwichHours, GreenwichMinutes, GreenwichSeconds, LocalSiderealHours, LocalSiderealMinutes, LocalSiderealSeconds))

            elif(DistMode == 'Q' or DistMode == 'q'):
                break

            else:
                print(">>>> ERROR: Invalid option! Try Again!")



    #   _____                      _           _______ _               
    #  /  ___|                    | |         / / ___ (_)              
    #  \ `--. _   _ _ __  ___  ___| |_ ___   / /| |_/ /_ ___  ___  ___ 
    #   `--. \ | | | '_ \/ __|/ _ \ __/ __| / / |    /| / __|/ _ \/ __|
    #  /\__/ / |_| | | | \__ \  __/ |_\__ \/ /  | |\ \| \__ \  __/\__ \
    #  \____/ \__,_|_| |_|___/\___|\__|___/_/   \_| \_|_|___/\___||___/
    # DATETIME CALCULATION FOR SURISES AND SUNSET
    elif(mode == '4'):
        while(True):
            print(">> Calculate Datetimes of Sunset/Rises at Specific Location")
            print(">> Please choose a mode you'd like to use!")
            print("(1) Parameters from User Input")
            print("(2) Parameters of Predefined Locations")
            print("(Q) Quit to Main Menu")
            SunMode = input("> Choose a mode and press enter...: ")

            print('\n')
            if(SunMode == '1'):
                while(True):
                    print(">> Calculate Sunset/Rises from given Parameters\n")
                    print(">> Give Parameters!")

                    # Input Positional Parameters
                    print(">> HINT: You can write Latitude as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                    LatitudeHours = float(input("> Latitude (φ) Hours: ") or "0")
                    LatitudeMinutes = float(input("> Latitude (φ) Minutes: ") or "0")
                    LatitudeSeconds = float(input("> Latitude (φ) Seconds: ") or "0")
                    Latitude = LatitudeHours + LatitudeMinutes/60 + LatitudeSeconds/3600

                    print(">> HINT: You can write Longitude as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                    LongitudeHours = float(input("> Longitude (λ) Hours: ") or "0")
                    LongitudeMinutes = float(input("> Longitude (λ) Minutes: ") or "0")
                    LongitudeSeconds = float(input("> Longitude (λ) Seconds: ") or "0")
                    Longitude = LongitudeHours + LongitudeMinutes/60 + LongitudeSeconds/3600
                    break

            elif(SunMode == '2'):
                print(">> Calculate Datetimes of Sunset/Rises from the Coordinates of a Predefined Location")
                print(">> Write the Name of a Choosen Location to the Input!")

                # Input Choosen Location's Name
                while(True):
                    Location = input("> Location's name (type \'H\' for Help): ")
                    
                    if(Location == "Help" or Location == "help" or Location == "H" or Location == "h"):
                        print(">> Predefined Locations you can choose from:")
                        for keys in LocationDict.items():
                            print(keys)
                    
                    else:
                        try:
                            Latitude = LocationDict[Location][0]
                            Longitude = LocationDict[Location][1]

                        except KeyError:
                            print(">>>> ERROR: The Location, named \"" + Location + "\" is not in the Database!")
                            print(">>>> Type \"Help\" to list Available Cities in Database!")
                            
                        else:
                            break

            elif(SunMode == 'Q' or SunMode == 'q'):
                break

            else:
                print(">>>> ERROR: Invalid option! Try Again!")

            # Input Time Parameters
            while(True):
                LocalDateYear = int(input("> Year: "))
                if(LocalDateYear != 0):
                    break
                else:
                    print(">>>> ERROR: Year 0 is not defined! Please write another date!\n")

            while(True):
                LocalDateMonth = int(input("> Month: "))
                if(LocalDateMonth > 0 and LocalDateMonth < 13):
                    break
                else:
                    print(">>>> ERROR: Months should be inside [1,12] interval, and should be Integer!\n")

            # Leap Year	Handling
            while(True):
                LocalDateDay = int(input("> Day: "))
                if(LocalDateYear%4 == 0 and (LocalDateYear%100 != 0 or LocalDateYear%400 == 0)):
                    if(MonthLengthListLeapYear[LocalDateMonth - 1] >= LocalDateDay and LocalDateDay > 0):
                        break
                    else:
                        daysmsg = ">>>> ERROR: Days should be inside [1,{0}] interval, and should be Integer!\n"
                        print(daysmsg.format(MonthLengthListLeapYear[LocalDateMonth - 1]))
                else:
                    if(MonthLengthList[LocalDateMonth - 1] >= LocalDateDay and LocalDateDay > 0):
                        break
                    else:
                        daysmsg = ">>>> ERROR: Days should be inside [1,{0}] interval, and should be Integer!\n"
                        print(daysmsg.format(MonthLengthList[LocalDateMonth - 1]))

            Planet = "Earth"
            AltitudeOfSun = 0

            (LocalTimeSet, LocalHoursSet, LocalMinutesSet, LocalSecondsSet, LocalDateYearSet, LocalDateMonthSet, LocalDateDaySet, 
            LocalTimeRise, LocalHoursRise, LocalMinutesRise, LocalSecondsRise, LocalDateYearRise, LocalDateMonthRise, LocalDateDayRise) = SunSetAndRiseDateTime(Planet, Latitude, Longitude, AltitudeOfSun, LocalDateYear, LocalDateMonth, LocalDateDay)

            if(SunMode == '1'):
                suncoordmsg = ">>> Calculated Datetimes of Sunset/Rise for Coordinates: \n>>> {0}, {1}"
                print(suncoordmsg.format(Latitude, Longitude))

            elif(SunMode == '2'):
                print("\n>>> Calculated Datetimes of Sunset/Rise for " + Location + ":")

            sunrisemsg = "\n>> The Sunrise will occur on {0}.{1}.{2}.,\n>> At {3}:{4}:{5} LT"
            sunsetmsg = "\n>> The Sunset will occur on {0}.{1}.{2}.,\n>> At {3}:{4}:{5} LT\n"
            print(sunrisemsg.format(LocalDateYearRise, LocalDateMonthRise, LocalDateDayRise, LocalHoursRise, LocalMinutesRise, LocalSecondsRise))
            print(sunsetmsg.format(LocalDateYearSet, LocalDateMonthSet, LocalDateDaySet, LocalHoursSet, LocalMinutesSet, LocalSecondsSet))


    #   _______       _ _ _       _     _      _____      _      
    #  |__   __|     (_) (_)     | |   | |    / ____|    | |     
    #     | |_      ___| |_  __ _| |__ | |_  | |     __ _| | ___ 
    #     | \ \ /\ / / | | |/ _` | '_ \| __| | |    / _` | |/ __|
    #     | |\ V  V /| | | | (_| | | | | |_  | |___| (_| | | (__ 
    #     |_| \_/\_/ |_|_|_|\__, |_| |_|\__|  \_____\__,_|_|\___|
    #                        __/ |                               
    #                       |___/                                
    # DATETIME CALCULATION FOR TWILIGHTS
    elif(mode == '5'):
        while(True):
            print(">> Calculate Datetimes of Twilights at Specific Location")
            print(">> Please choose a mode you'd like to use!")
            print("(1) Parameters from User Input")
            print("(2) Parameters of Predefined Locations")
            print("(Q) Quit to Main Menu")
            TwiMode = input("> Choose a mode and press enter...: ")

            print('\n')
            while(True):
                if(TwiMode == '1'):
                    print(">> Calculate Twilights from given Parameters\n")
                    print(">> Give Parameters!")

                    # Input Positional Parameters
                    print(">> HINT: You can write Latitude as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                    LatitudeHours = float(input("> Latitude (φ) Hours: ") or "0")
                    LatitudeMinutes = float(input("> Latitude (φ) Minutes: ") or "0")
                    LatitudeSeconds = float(input("> Latitude (φ) Seconds: ") or "0")
                    Latitude = LatitudeHours + LatitudeMinutes/60 + LatitudeSeconds/3600

                    print(">> HINT: You can write Longitude as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                    LongitudeHours = float(input("> Longitude (λ) Hours: ") or "0")
                    LongitudeMinutes = float(input("> Longitude (λ) Minutes: ") or "0")
                    LongitudeSeconds = float(input("> Longitude (λ) Seconds: ") or "0")
                    Longitude = LongitudeHours + LongitudeMinutes/60 + LongitudeSeconds/3600
                    break

                elif(TwiMode == '2'):
                    print(">> Calculate Datetimes of Twilights from the Coordinates of a Predefined Location")
                    print(">> Write the Name of a Choosen Location to the Input!")

                    # Input Choosen Location's Name
                    while(True):
                        Location = input("> Location's name (type \'H\' for Help): ")
                        
                        if(Location == "Help" or Location == "help" or Location == "H" or Location == "h"):
                            print(">> Predefined Locations you can choose from:")
                            for keys in LocationDict.items():
                                print(keys)
                        
                        else:
                            try:
                                Latitude = LocationDict[Location][0]
                                Longitude = LocationDict[Location][1]

                            except KeyError:
                                print(">>>> ERROR: The Location, named \"" + Location + "\" is not in the Database!")
                                print(">>>> Type \"Help\" to list Available Cities in Database!")
                                
                            else:
                                break

                elif(TwiMode == 'Q' or TwiMode == 'q'):
                    break

            else:
                print(">>>> ERROR: Invalid option! Try Again!")

            # Input Time Parameters
            while(True):
                LocalDateYear = int(input("> Year: "))
                if(LocalDateYear != 0):
                    break
                else:
                    print(">>>> ERROR: Year 0 is not defined! Please write another date!\n")

            while(True):
                LocalDateMonth = int(input("> Month: "))
                if(LocalDateMonth > 0 and LocalDateMonth < 13):
                    break
                else:
                    print(">>>> ERROR: Months should be inside [1,12] interval, and should be Integer!\n")

            # Leap Year	Handling
            while(True):
                LocalDateDay = int(input("> Day: "))
                if(LocalDateYear%4 == 0 and (LocalDateYear%100 != 0 or LocalDateYear%400 == 0)):
                    if(MonthLengthListLeapYear[LocalDateMonth - 1] >= LocalDateDay and LocalDateDay > 0):
                        break
                    else:
                        daysmsg = ">>>> ERROR: Days should be inside [1,{0}] interval, and should be Integer!\n"
                        print(daysmsg.format(MonthLengthListLeapYear[LocalDateMonth - 1]))
                else:
                    if(MonthLengthList[LocalDateMonth - 1] >= LocalDateDay and LocalDateDay > 0):
                        break
                    else:
                        daysmsg = ">>>> ERROR: Days should be inside [1,{0}] interval, and should be Integer!\n"
                        print(daysmsg.format(MonthLengthList[LocalDateMonth - 1]))

            Planet = "Earth"

            (LocalHoursNoon, LocalMinutesNoon, LocalSecondsNoon, LocalDateYearNoon, LocalDateMonthNoon, LocalDateDayNoon,
            LocalHoursMidnight, LocalMinutesMidnight, LocalSecondsMidnight, LocalDateYearMidnight, LocalDateMonthMidnight, LocalDateDayMidnight,
            LocalHoursRiseDaylight, LocalMinutesRiseDaylight, LocalSecondsRiseDaylight, LocalDateYearRiseDaylight, LocalDateMonthRiseDaylight, LocalDateDayRiseDaylight,
            LocalHoursSetDaylight, LocalMinutesSetDaylight, LocalSecondsSetDaylight, LocalDateYearSetDaylight, LocalDateMonthSetDaylight, LocalDateDaySetDaylight,
            LocalHoursRiseCivil, LocalMinutesRiseCivil, LocalSecondsRiseCivil, LocalDateYearRiseCivil, LocalDateMonthRiseCivil, LocalDateDayRiseCivil,
            LocalHoursSetCivil, LocalMinutesSetCivil, LocalSecondsSetCivil, LocalDateYearSetCivil, LocalDateMonthSetCivil, LocalDateDaySetCivil,
            LocalHoursRiseNaval, LocalMinutesRiseNaval, LocalSecondsRiseNaval, LocalDateYearRiseNaval, LocalDateMonthRiseNaval, LocalDateDayRiseNaval,
            LocalHoursSetNaval, LocalMinutesSetNaval, LocalSecondsSetNaval, LocalDateYearSetNaval, LocalDateMonthSetNaval, LocalDateDaySetNaval,
            LocalHoursRiseAstro, LocalMinutesRiseAstro, LocalSecondsRiseAstro, LocalDateYearSetAstro, LocalDateMonthSetAstro, LocalDateDaySetAstro,
            LocalHoursSetAstro, LocalMinutesSetAstro, LocalSecondsSetAstro, LocalDateYearRiseAstro, LocalDateMonthRiseAstro, LocalDateDayRiseAstro) = TwilightCalc(Planet, Latitude, Longitude, LocalDateYear, LocalDateMonth, LocalDateDay)


            msgdaylightrise = "\n>> Rising Daylight's time: {0}:{1}:{2} on {3}.{4}.{5}"
            msgdaylightset = ">> Setting Daylight's time: {0}:{1}:{2} on {3}.{4}.{5}\n"

            msgcivilrise = "\n>> Rising Civil Twilight's time is between\n>> {0}:{1}:{2} and {3}:{4}:{5} on {6}.{7}.{8}"
            msgcivilset = ">> Setting Civil Twilight's time is between\n>> {0}:{1}:{2} and {3}:{4}:{5} on {6}.{7}.{8}\n"

            msgnavalrise = "\n>> Rising Nautical Twilight's time is between\n>> {0}:{1}:{2} and {3}:{4}:{5} on {6}.{7}.{8}"
            msgnavalset = ">> Setting Nautical Twilight's time is between\n>> {0}:{1}:{2} and {3}:{4}:{5} on {6}.{7}.{8}\n"

            msgastrorise = "\n>> Rising Astronomical Twilight's time is between\n>> {0}:{1}:{2} and {3}:{4}:{5} on {6}.{7}.{8}"
            msgastroset = ">> Setting Astronomical Twilight's time is between\n>> {0}:{1}:{2} and {3}:{4}:{5} on {6}.{7}.{8}\n"

            msgnoon = "\n>> Noon occurs at {0}:{1}:{2} on {3}.{4}.{5}"
            msgmidnight = ">> Midnight occurs at {0}:{1}:{2} on {3}.{4}.{5}\n"

            # +4 and -6 are Corrections for more accurate times

            print(msgdaylightrise.format(LocalHoursRiseDaylight, LocalMinutesRiseDaylight, LocalSecondsRiseDaylight, LocalDateYearRiseDaylight, LocalDateMonthRiseDaylight, LocalDateDayRiseDaylight))
            print(msgdaylightset.format(LocalHoursSetDaylight, LocalMinutesSetDaylight, LocalSecondsSetDaylight, LocalDateYearSetDaylight, LocalDateMonthSetDaylight, LocalDateDaySetDaylight))
        
            print(msgcivilrise.format(LocalHoursRiseCivil, LocalMinutesRiseCivil + 4, LocalSecondsRiseCivil, LocalHoursRiseDaylight, LocalMinutesRiseDaylight, LocalSecondsRiseDaylight, LocalDateYearRiseCivil, LocalDateMonthRiseCivil, LocalDateDayRiseCivil))
            print(msgcivilset.format(LocalHoursSetDaylight, LocalMinutesSetDaylight, LocalSecondsSetDaylight, LocalHoursSetCivil, LocalMinutesSetCivil - 6, LocalSecondsSetCivil, LocalDateYearSetCivil, LocalDateMonthSetCivil, LocalDateDaySetCivil))

            print(msgnavalrise.format(LocalHoursRiseNaval, LocalMinutesRiseNaval + 4, LocalSecondsRiseNaval, LocalHoursRiseCivil, LocalMinutesRiseCivil + 4, LocalSecondsRiseCivil, LocalDateYearRiseNaval, LocalDateMonthRiseNaval, LocalDateDayRiseNaval))
            print(msgnavalset.format(LocalHoursSetCivil, LocalMinutesSetCivil - 6, LocalSecondsSetCivil, LocalHoursSetNaval, LocalMinutesSetNaval - 6, LocalSecondsSetNaval, LocalDateYearSetNaval, LocalDateMonthSetNaval, LocalDateDaySetNaval))

            print(msgastrorise.format(LocalHoursRiseAstro, LocalMinutesRiseAstro + 4, LocalSecondsRiseAstro, LocalHoursRiseNaval, LocalMinutesRiseNaval + 4, LocalSecondsRiseNaval, LocalDateYearSetAstro, LocalDateMonthSetAstro, LocalDateDaySetAstro))
            print(msgastroset.format(LocalHoursSetNaval, LocalMinutesSetNaval - 6, LocalSecondsSetNaval, LocalHoursSetAstro, LocalMinutesSetAstro - 6, LocalSecondsSetAstro, LocalDateYearRiseAstro, LocalDateMonthRiseAstro, LocalDateDayRiseAstro))

            print(msgnoon.format(LocalHoursNoon, LocalMinutesNoon, LocalSecondsNoon, LocalDateYearNoon, LocalDateMonthNoon, LocalDateDayNoon))
            print(msgmidnight.format(LocalHoursMidnight, LocalMinutesMidnight, LocalSecondsMidnight, LocalDateYearMidnight, LocalDateMonthMidnight, LocalDateDayMidnight))



    #   _____                 _ _       _ 
    #  /  ___|               | (_)     | |
    #  \ `--. _   _ _ __   __| |_  __ _| |
    #   `--. \ | | | '_ \ / _` | |/ _` | |
    #  /\__/ / |_| | | | | (_| | | (_| | |
    #  \____/ \__,_|_| |_|\__,_|_|\__,_|_|
    # Plot Sundial for Choosen Locations
    elif(mode == '6'):
        while(True):
            print(">> Plot Sun's Path on a Sundial at Choosen Location on Earth")
            print(">> Please choose a mode you'd like to use!")
            print("(1) Parameters from User Input")
            print("(2) Parameters of Predefined Locations")
            print("(Q) Quit to Main Menu")
            TwiMode = input("> Choose a mode and press enter...: ")

            # Constants for calculation
            Planet = "Earth"

            print('\n')
            if(TwiMode == '1'):
                while(True):
                    print(">> Calculate Twilights from given Parameters\n")
                    print(">> Give Parameters!")

                    # Input Positional Parameters
                    print(">> HINT: You can write Latitude as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                    LatitudeHours = float(input("> Latitude (φ) Hours: ") or "0")
                    LatitudeMinutes = float(input("> Latitude (φ) Minutes: ") or "0")
                    LatitudeSeconds = float(input("> Latitude (φ) Seconds: ") or "0")
                    Latitude = LatitudeHours + LatitudeMinutes/60 + LatitudeSeconds/3600

                    print(">> HINT: You can write Longitude as a Decimal Fraction. For this you need to write Hours as a float-type value, then you can\n>> Press Enter for both Minutes and Seconds.")
                    LongitudeHours = float(input("> Longitude (λ) Hours: ") or "0")
                    LongitudeMinutes = float(input("> Longitude (λ) Minutes: ") or "0")
                    LongitudeSeconds = float(input("> Longitude (λ) Seconds: ") or "0")
                    Longitude = LongitudeHours + LongitudeMinutes/60 + LongitudeSeconds/3600
                    break

            elif(TwiMode == '2'):
                print(">> Calculate Datetimes of Twilights from the Coordinates of a Predefined Location")
                print(">> Write the Name of a Choosen Location to the Input!")

                # Input Choosen Location's Name
                while(True):
                    Location = input("> Location's name (type \'H\' for Help): ")
                    
                    if(Location == "Help" or Location == "help" or Location == "H" or Location == "h"):
                        print(">> Predefined Locations you can choose from:")
                        for keys in LocationDict.items():
                            print(keys)
                    
                    else:
                        try:
                            Latitude = LocationDict[Location][0]
                            Longitude = LocationDict[Location][1]

                        except KeyError:
                            print(">>>> ERROR: The Location, named \"" + Location + "\" is not in the Database!")
                            print(">>>> Type \"Help\" to list Available Cities in Database!")
                            
                        else:
                            break

            elif(TwiMode == 'Q' or TwiMode == 'q'):
                break

            else:
                print(">>>> ERROR: Invalid option! Try Again!")

            print(">> For which Year would You like to Draw the Sundial?")
            while(True):
                SunDialYear = float(input("> Choosen Year: "))
                if(SunDialYear != 0):
                    break
                else:
                    print(">>>> ERROR: Year 0 is not defined! Please write another date!\n")

            
            while(True):
                print(">> Would you like to plot the Sun's path for a Choosen Date in This Year too?")
                SunDialChoose = input(">> Write Y for Yes or N for No: ")
                if(SunDialChoose == 'Y' or SunDialChoose == 'y' or SunDialChoose == 'Yes' or SunDialChoose == 'yes' or SunDialChoose == 'YEs' or SunDialChoose == 'yEs' or SunDialChoose == 'yeS' or SunDialChoose == 'YeS' or SunDialChoose == 'yES'):
                    # Input Time Parameters
                    while(True):
                        LocalDateMonth = int(input("> Month: "))
                        if(LocalDateMonth > 0 and LocalDateMonth < 13):
                            break
                        else:
                            print(">>>> ERROR: Months should be inside [1,12] interval, and should be Integer!\n")

                    # Leap Year	Handling
                    while(True):
                        LocalDateDay = int(input("> Day: "))
                        if(LocalDateYear%4 == 0 and (LocalDateYear%100 != 0 or LocalDateYear%400 == 0)):
                            if(MonthLengthListLeapYear[LocalDateMonth - 1] >= LocalDateDay and LocalDateDay > 0):
                                break
                            else:
                                daysmsg = ">>>> ERROR: Days should be inside [1,{0}] interval, and should be Integer!\n"
                                print(daysmsg.format(MonthLengthListLeapYear[LocalDateMonth - 1]))
                        else:
                            if(MonthLengthList[LocalDateMonth - 1] >= LocalDateDay and LocalDateDay > 0):
                                break
                            else:
                                daysmsg = ">>>> ERROR: Days should be inside [1,{0}] interval, and should be Integer!\n"
                                print(daysmsg.format(MonthLengthList[LocalDateMonth - 1]))

                    break

                elif(SunDialChoose == 'N' or SunDialChoose == 'n' or SunDialChoose == 'No' or SunDialChoose == 'no' or SunDialChoose == 'nO'):
                    break

                else:
                    print(">>>> ERROR: Invalid option! Try Again!")

            if(SunDialChoose == 'Y' or SunDialChoose == 'y' or SunDialChoose == 'Yes' or SunDialChoose == 'yes' or SunDialChoose == 'YEs' or SunDialChoose == 'yEs' or SunDialChoose == 'yeS' or SunDialChoose == 'YeS' or SunDialChoose == 'yES'):

                ### CHOOSEN DATE ###
                LocalHourAngleRiseChoosen, LocalHourAngleSetChoosen, DeclinationSunChoosen = SundialPrecalculations(Planet, Latitude, Longitude, LocalDateYear, LocalDateMonth, LocalDateDay)

                # Create lists for plot parameters
                LocalHourAngleChoosen = []
                AltitudesChoosen = []
                AzimuthsChoosen = []

                # Calculate plot parameters
                for LocalHourAngleActual in range(int(LocalHourAngleRiseChoosen * 100000), int(LocalHourAngleSetChoosen * 100000), 300):
                    
                    # Calculate parameters by ~10 seconds interval
                    AltitudeActual, AzimuthActual = SundialParametersCalc(Latitude, LocalHourAngleActual, DeclinationSunChoosen)

                    # Append parameters to lists
                    LocalHourAngleChoosen.append(LocalHourAngleActual)
                    AltitudesChoosen.append(AltitudeActual)
                    AzimuthsChoosen.append(AzimuthActual)


            ### SUMMER SOLSTICE ###
            LocalDateMonthSummer = 6
            if(SunDialYear%4 == 0):
                LocalDateDaySummer = 20
            
            else:
                LocalDateDaySummer = 21
            
            LocalHourAngleRiseSummer, LocalHourAngleSetSummer, DeclinationSunSummer = SundialPrecalculations(Planet, Latitude, Longitude, SunDialYear, LocalDateMonthSummer, LocalDateDaySummer)

            # Create lists for plot parameters
            LocalHourAngleSummer = []
            AltitudesSummer = []
            AzimuthsSummer = []

            # Calculate plot parameters
            for LocalHourAngleActual in range(int(LocalHourAngleRiseSummer * 100000), int(LocalHourAngleSetSummer * 100000), 300):
                
                # Norm back to normal
                LocalHourAngleActual/100000

                # Calculate parameters by ~10 seconds interval
                AltitudeActual, AzimuthActual = SundialParametersCalc(Latitude, LocalHourAngleActual, DeclinationSunSummer)

                # Append parameters to lists
                LocalHourAngleSummer.append(LocalHourAngleActual)
                AltitudesSummer.append(AltitudeActual)
                AzimuthsSummer.append(AzimuthActual)


            ### WINTER SOLSTICE ###
            LocalDateMonthWinter = 12
            if((SunDialYear + 1)%4 == 0):
                LocalDateDayWinter = 22
            
            else:
                LocalDateDayWinter = 21

            LocalHourAngleRiseWinter, LocalHourAngleSetWinter, DeclinationSunWinter = SundialPrecalculations(Planet, Latitude, Longitude, SunDialYear, LocalDateMonthWinter, LocalDateDayWinter)

            # Create lists for plot parameters
            LocalHourAngleWinter = []
            AltitudesWinter = []
            AzimuthsWinter = []

            # Calculate plot parameters
            for LocalHourAngleActual in range(int(LocalHourAngleRiseWinter * 100000), int(LocalHourAngleSetWinter * 100000), 300):
                
                # Norm back to normal
                LocalHourAngleActual/100000
                
                # Calculate parameters by ~10 seconds interval
                AltitudeActual, AzimuthActual = SundialParametersCalc(Latitude, LocalHourAngleActual, DeclinationSunWinter)

                # Append parameters to lists
                LocalHourAngleWinter.append(LocalHourAngleActual)
                AltitudesWinter.append(AltitudeActual)
                AzimuthsWinter.append(AzimuthActual)


            ### MARCH EQUINOX ###
            LocalDateMonthMarch = 3
            LocalDateDayMarch = 20

            LocalHourAngleRiseMarch, LocalHourAngleSetMarch, DeclinationSunMarch = SundialPrecalculations(Planet, Latitude, Longitude, SunDialYear, LocalDateMonthMarch, LocalDateDayMarch)

            # Create lists for plot parameters
            LocalHourAngleMarch = []
            AltitudesMarch = []
            AzimuthsMarch = []

            # Calculate plot parameters
            for LocalHourAngleActual in range(int(LocalHourAngleRiseMarch * 100000), int(LocalHourAngleSetMarch * 100000), 300):
                
                # Norm back to normal
                LocalHourAngleActual/100000
                
                # Calculate parameters by ~10 seconds interval
                AltitudeActual, AzimuthActual = SundialParametersCalc(Latitude, LocalHourAngleActual, DeclinationSunMarch)

                # Append parameters to lists
                LocalHourAngleMarch.append(LocalHourAngleActual)
                AltitudesMarch.append(AltitudeActual)
                AzimuthsMarch.append(AzimuthActual)


            ### SEPTEMBER EQIUNOX ###
            LocalDateMonthSeptember = 9
            if(SunDialYear%4 == 0 or (SunDialYear - 1)%4 == 0):
                LocalDateDaySeptember = 22

            else:
                LocalDateDaySeptember = 23

            LocalHourAngleRiseSeptember, LocalHourAngleSetSeptember, DeclinationSunSeptember = SundialPrecalculations(Planet, Latitude, Longitude, SunDialYear, LocalDateMonthSeptember, LocalDateDaySeptember)

            print(24-(LocalHourAngleRiseSeptember - LocalHourAngleSetSeptember))

            # Create lists for plot parameters
            LocalHourAngleSeptember = []
            AltitudesSeptember = []
            AzimuthsSeptember = []

            # Calculate plot parameters
            for LocalHourAngleActual in range(int(LocalHourAngleRiseSeptember * 100000), int(LocalHourAngleSetSeptember * 100000), 300):
                
                # Norm back to normal
                LocalHourAngleActual/100000
                
                # Calculate parameters by ~10 seconds interval
                AltitudeActual, AzimuthActual = SundialParametersCalc(Latitude, LocalHourAngleActual, DeclinationSunSeptember)

                # Append parameters to lists
                LocalHourAngleSeptember.append(LocalHourAngleActual)
                AltitudesSeptember.append(AltitudeActual)
                AzimuthsSeptember.append(AzimuthActual)


            print(len(LocalHourAngleSeptember), len(AltitudesSeptember), len(AzimuthsSeptember))


    #   _   _                                         _    
    #  | | | |                                       | |   
    #  | |_| | ___  _ __ ___   _____      _____  _ __| | __
    #  |  _  |/ _ \| '_ ` _ \ / _ \ \ /\ / / _ \| '__| |/ /
    #  | | | | (_) | | | | | |  __/\ V  V / (_) | |  |   < 
    #  \_| |_/\___/|_| |_| |_|\___| \_/\_/ \___/|_|  |_|\_\
    # HOMEWORK MODE
    elif(mode == 'Home' or mode == 'home' or mode == 'H' or mode == 'h'):

        print("###  Csillesz II end-semesterhomework results, solved by the program  ###")
        print("_________________________________________________________________________")

        print("1.1/1:")

        Location = "Szombathely"
        Longitude = LocationDict[Location][1]
        LocalDateYear = 2017
        LocalDateMonth = 12
        LocalDateDay = 27
        LocalHours = 14
        LocalMinutes = 0
        LocalSeconds = 0
        LocalSiderealHours, LocalSiderealMinutes, LocalSiderealSeconds, UnitedHours, UnitedMinutes, UnitedSeconds, GreenwichHours, GreenwichMinutes, GreenwichSeconds = LocalSiderealTimeCalc(Longitude, LocalHours, LocalMinutes, LocalSeconds, LocalDateYear, LocalDateMonth, LocalDateDay)

        sidmsg = "\n>>> The Local Mean Sidereal Time at {0}:{1}:{2} UT\n>>> in {3} with\n>>> {4}:{5}:{6} GMST at 00:00:00 UT\n>>> is {7}:{8}:{9}\n\n"
        print(sidmsg.format(UnitedHours, UnitedMinutes, UnitedSeconds, Location, GreenwichHours, GreenwichMinutes, GreenwichSeconds, LocalSiderealHours, LocalSiderealMinutes, LocalSiderealSeconds))
        print("_________________________________________________________________________")

        print("1.1/2:")

        Latitude = LocationDict["Szeged"][0]
        RightAscensionVenus = 18 + 41/60 + 54/3600
        DeclinationVenus = -(24 + 4/60 + 9/3600)
        Altitude, Azimuth1, Azimuth2, H_dil = EquIToHor(Latitude, RightAscensionVenus, DeclinationVenus, 0, None, None, None)

        # Print Results
        print(">>> INFO: Available Data are only suited for Calculating Rising or\n>>> Setting Altitudes!")
        print("\n>>> Calculated Parameter of Rising/Setting Object in Horizontal Coord. Sys.:")

        azimmsg = ">>> Rising and Setting Azimuths (A) are:\n>>> {0:.4f}° and {1:.4f}°"
        timemsg = ">>> Elapsed time between them: is {0:.2f}h\n"
        print(azimmsg.format(Azimuth2, Azimuth1))
        print(timemsg.format(H_dil/15))
        print("_________________________________________________________________________")

        print("1.1/3:")

        Planet = "Earth"
        Location = "Piszkesteto"
        Latitude = LocationDict[Location][0]
        Longitude = LocationDict[Location][1]
        LocalDateYear = 2018
        LocalDateMonth = 12
        LocalDateDay1 = 21
        LocalDateDay2 = 22

        (LocalHoursNoon1, LocalMinutesNoon1, LocalSecondsNoon1, LocalDateYearNoon1, LocalDateMonthNoon1, LocalDateDayNoon1,
            LocalHoursMidnight1, LocalMinutesMidnight1, LocalSecondsMidnight1, LocalDateYearMidnight1, LocalDateMonthMidnight1, LocalDateDayMidnight1,
            LocalHoursRiseDaylight1, LocalMinutesRiseDaylight1, LocalSecondsRiseDaylight1, LocalDateYearRiseDaylight1, LocalDateMonthRiseDaylight1, LocalDateDayRiseDaylight1,
            LocalHoursSetDaylight1, LocalMinutesSetDaylight1, LocalSecondsSetDaylight1, LocalDateYearSetDaylight1, LocalDateMonthSetDaylight1, LocalDateDaySetDaylight1,
            LocalHoursRiseCivil1, LocalMinutesRiseCivil1, LocalSecondsRiseCivil1, LocalDateYearRiseCivil1, LocalDateMonthRiseCivil1, LocalDateDayRiseCivil1,
            LocalHoursSetCivil1, LocalMinutesSetCivil1, LocalSecondsSetCivil1, LocalDateYearSetCivil1, LocalDateMonthSetCivil1, LocalDateDaySetCivil1,
            LocalHoursRiseNaval1, LocalMinutesRiseNaval1, LocalSecondsRiseNaval1, LocalDateYearRiseNaval1, LocalDateMonthRiseNaval1, LocalDateDayRiseNaval1,
            LocalHoursSetNaval1, LocalMinutesSetNaval1, LocalSecondsSetNaval1, LocalDateYearSetNaval1, LocalDateMonthSetNaval1, LocalDateDaySetNaval1,
            LocalHoursRiseAstro1, LocalMinutesRiseAstro1, LocalSecondsRiseAstro1, LocalDateYearSetAstro1, LocalDateMonthSetAstro1, LocalDateDaySetAstro1,
            LocalHoursSetAstro1, LocalMinutesSetAstro1, LocalSecondsSetAstro1, LocalDateYearRiseAstro1, LocalDateMonthRiseAstro1, LocalDateDayRiseAstro1) = TwilightCalc(Planet, Latitude, Longitude, LocalDateYear, LocalDateMonth, LocalDateDay1)

        (LocalHoursNoon2, LocalMinutesNoon2, LocalSecondsNoon2, LocalDateYearNoon2, LocalDateMonthNoon2, LocalDateDayNoon2,
            LocalHoursMidnight2, LocalMinutesMidnight2, LocalSecondsMidnight2, LocalDateYearMidnight2, LocalDateMonthMidnight2, LocalDateDayMidnight2,
            LocalHoursRiseDaylight2, LocalMinutesRiseDaylight2, LocalSecondsRiseDaylight2, LocalDateYearRiseDaylight2, LocalDateMonthRiseDaylight2, LocalDateDayRiseDaylight2,
            LocalHoursSetDaylight2, LocalMinutesSetDaylight2, LocalSecondsSetDaylight2, LocalDateYearSetDaylight2, LocalDateMonthSetDaylight2, LocalDateDaySetDaylight2,
            LocalHoursRiseCivil2, LocalMinutesRiseCivil2, LocalSecondsRiseCivil2, LocalDateYearRiseCivil2, LocalDateMonthRiseCivil2, LocalDateDayRiseCivil2,
            LocalHoursSetCivil2, LocalMinutesSetCivil2, LocalSecondsSetCivil2, LocalDateYearSetCivil2, LocalDateMonthSetCivil2, LocalDateDaySetCivil2,
            LocalHoursRiseNaval2, LocalMinutesRiseNaval2, LocalSecondsRiseNaval2, LocalDateYearRiseNaval2, LocalDateMonthRiseNaval2, LocalDateDayRiseNaval2,
            LocalHoursSetNaval2, LocalMinutesSetNaval2, LocalSecondsSetNaval2, LocalDateYearSetNaval2, LocalDateMonthSetNaval2, LocalDateDaySetNaval2,
            LocalHoursRiseAstro2, LocalMinutesRiseAstro2, LocalSecondsRiseAstro2, LocalDateYearSetAstro2, LocalDateMonthSetAstro2, LocalDateDaySetAstro2,
            LocalHoursSetAstro2, LocalMinutesSetAstro2, LocalSecondsSetAstro2, LocalDateYearRiseAstro2, LocalDateMonthRiseAstro2, LocalDateDayRiseAstro2) = TwilightCalc(Planet, Latitude, Longitude, LocalDateYear, LocalDateMonth, LocalDateDay2)

        LocalDateDaySetAstroTime1 = LocalHoursSetAstro1 + LocalMinutesSetAstro1/60 + LocalSecondsSetAstro1/3600
        LocalDateDayRiseAstroTime2 = LocalHoursRiseAstro2 + LocalMinutesRiseAstro2/60 + LocalSecondsRiseAstro2/3600

        # Length of the astronomical night
        AstroNightLength = 24 - (LocalDateDaySetAstroTime1 - LocalDateDayRiseAstroTime2)
        AstroNightHours = int(AstroNightLength)
        AstroNightMinutes = int((AstroNightLength - AstroNightHours) * 60)
        AstroNightSeconds = int((((AstroNightLength - AstroNightHours) * 60) - AstroNightMinutes) * 60)

        astrotimemsg = ">>> The astronomical night's lenght at " + Location + " is\n>>> {0}:{1}:{2} long\n>>> On between {3}.{4}.{5}, and {6} evening.\n"
        print(astrotimemsg.format(AstroNightHours, AstroNightMinutes, AstroNightSeconds, LocalDateYear, LocalDateMonth, LocalDateDay1, LocalDateDay2))
        print("_________________________________________________________________________")

        print("1.2/1.")

        print("_________________________________________________________________________")

        print("1.2/2.")

        Location = "Baja"
        Star = "Altair"
        Latitude = LocationDict[Location][0]
        Longitude = LocationDict[Location][1]
        RightAscension = StellarDict[Star][0]
        Declination = StellarDict[Star][1]
        Altitude = None
        Azimuth = None
        LocalHourAngle = None
        LocalHours = 20
        LocalMinutes = 45
        LocalSeconds = 0
        LocalDateYear = 2013
        LocalDateMonth = 6
        LocalDateDay = 21

        # Calculate Local Mean Sidereal Time
        LocalSiderealHours, LocalSiderealMinutes, LocalSiderealSeconds, UnitedHours, UnitedMinutes, UnitedSeconds, GreenwichHours, GreenwichMinutes, GreenwichSeconds = LocalSiderealTimeCalc(Longitude, LocalHours, LocalMinutes, LocalSeconds, LocalDateYear, LocalDateMonth, LocalDateDay)
        
        # Convert to decimal
        LocalSiderealTime = LocalSiderealHours + LocalSiderealMinutes/60 + LocalSiderealSeconds/3600
        
        # Normalize result
        LocalSiderealTime = NormalizeZeroBounded(LocalSiderealTime, 24)

        Altitude, Azimuth = EquIIToHor(Latitude, RightAscension, Declination, Altitude, Azimuth, LocalSiderealTime, LocalHourAngle)

        # For printing this step too
        LocalHourAngle = LocalSiderealTime - RightAscension
        # Normalize Result
        LocalHourAngle = NormalizeZeroBounded(LocalHourAngle, 24)

        LocalHourAngleHours = int(LocalHourAngle)
        LocalHourAngleMinutes = int((LocalHourAngle - LocalHourAngleHours) * 60)
        LocalHourAngleSeconds = int((((LocalHourAngle - LocalHourAngleHours) * 60) - LocalHourAngleMinutes) * 60)

        print(">>> Used formulas:\n>>> 1. S_0 (Greenwich Mean Sidereal Time) at 00:00 UT was calculated\n>>> 2. S (Local Mean Sidereal Time) = S_0 + Longitude/15 + dS * UnitedTime\n>>> 3. S - α = t; H = 15*t")
        print(">>> 4. sin(m) = sin(δ) * sin(φ) + cos(δ) * cos(φ) * cos(H); Altitude (m) should been between [-π/2,+π/2]\n>>> 5. sin(A) = - sin(H) * cos(δ) / cos(m), Azimuth at given H hour angle\n")

        # Print Results
        timemsg = ">>> Altitude and Azimuth of Altair from Baja On {0}.{1}.{2}"
        grwmsg = ">>> GMST: {0}:{1}:{2}"
        print(timemsg.format(LocalDateYear, LocalDateMonth, LocalDateDay))
        print(grwmsg.format(GreenwichHours, GreenwichMinutes, GreenwichSeconds))

        print(">>> Calculated Parameters in Horizontal Coord. Sys.:")
        locsidmsg = ">>> Local Mean Siderel Time (S): {0}:{1}:{2}"
        lhamsg = ">>> Local Hour Angle (t): {0}h {1}m {2}s"
        azimmsg = ">>> Azimuth (A):  {0}°"
        altitmsg = ">>> Altitude (m): {0}°\n"
        print(locsidmsg.format(LocalSiderealHours, LocalSiderealMinutes, LocalSiderealSeconds))
        print(lhamsg.format(LocalHourAngleHours, LocalHourAngleMinutes, LocalHourAngleSeconds))
        print(azimmsg.format(Azimuth))
        print(altitmsg.format(Altitude))

        print("_________________________________________________________________________")

        print("1.2/3.")

        Location = "Rio"
        Latitude = LocationDict[Location][0]
        Longitude = LocationDict[Location][1]

        Altitude = 55.656388
        Azimuth = 208.113611

        LocalHours = 20
        LocalMinutes = 34
        LocalSeconds = 53
        LocalDateYear = 2018
        LocalDateMonth = 4
        LocalDateDay = 17

        LocalSiderealHours, LocalSiderealMinutes, LocalSiderealSeconds, UnitedHours, UnitedMinutes, UnitedSeconds, GreenwichHours, GreenwichMinutes, GreenwichSeconds = LocalSiderealTimeCalc(Longitude, LocalHours, LocalMinutes, LocalSeconds, LocalDateYear, LocalDateMonth, LocalDateDay)
        
        # Convert to decimal
        LocalSiderealTime = LocalSiderealHours + LocalSiderealMinutes/60 + LocalSiderealSeconds/3600
        
        # Normalize result
        LocalSiderealTime = NormalizeZeroBounded(LocalSiderealTime, 24)

        Declination, RightAscension, LocalSiderealTime = HorToEquII(Latitude, Altitude, Azimuth, LocalSiderealTime)

        # Normalize Parameters
        DeclinationHours = int(Declination)
        DeclinationMinutes = int((Declination - DeclinationHours) * 60)
        DeclinationSeconds = int((((Declination - DeclinationHours) * 60) - DeclinationMinutes) * 60)

        RightAscensionHours = int(RightAscension)
        RightAscensionMinutes = int((RightAscension - RightAscensionHours) * 60)
        RightAscensionSeconds = int((((RightAscension - RightAscensionHours) * 60) - RightAscensionMinutes) * 60)

        LocalSiderealTimeHours = int(LocalSiderealTime)
        LocalSiderealTimeMinutes = int((LocalSiderealTime - LocalSiderealTimeHours) * 60)
        LocalSiderealTimeSeconds = int((((LocalSiderealTime - LocalSiderealTimeHours) * 60) - LocalSiderealTimeMinutes) * 60)

        equIImsg = ">>> Calculated Parameters of the Star in Equatorial II Coord. Sys. from {0}:"
        print(equIImsg.format(Location))

        declinmsg = ">>> Declination (δ): {0}° {1}\' {2}\""
        RAmsg = ">>> Right Ascension (α): {0}h {1}m {2}s"
        sidermsg = ">>> Local Mean Sidereal Time (S): {0}:{1}:{2}\n"
        print(declinmsg.format(DeclinationHours, DeclinationMinutes, DeclinationSeconds))
        print(RAmsg.format(RightAscensionHours, RightAscensionMinutes, RightAscensionSeconds))
        print(sidermsg.format(LocalSiderealTimeHours, LocalSiderealTimeMinutes, LocalSiderealTimeSeconds))

        print("_________________________________________________________________________")

    # MAIN MENU MODE
    # QUIT PROGRAM
    elif(mode == 'Q' or mode == 'q'):
        print("#### All Rights Reserved to Balage Paliere Co.! ####")
        exit()

    else:
        print(">>>> ERROR: Invalid option! Try Again!")