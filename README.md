# Astronomical Survey

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

The program was developed in Python first, and I first comitted it to this repository.

At 2018.05.04, 11:50 UT, I migrated the files to the https://github.com/masterdesky/ELTE_Tools_of_Information_2018 repository and continued to translate the source code to C++. Now it's moved backed into this repository, and will stay here.

## Main ojectives of the application:

The main goal was - primarily - to create an application, which could be helpful at solving simple astronomical problems, like coordinate system conversions. Secondly to implement many informative functionality, like calculating datetime of the sunrise/sunset at given date and location on Earth or even on other planets in the Solar System.

### Currently the following functions are implemented:

1. Conversion of primitive astronomical coordinate systems (Hor., Eq. I, Eq. II)
2. Geographical distance of given locations on the spherical Earth
3. Local Mean Sidereal Time (LMST) for given date and location
4. First equatorial coordinates of the Sun at given date
5. Local Hour Angle of the Sun at given location
6. Exact datetime of sunrise/sunset and twilights for given date and location
7. Solving astronomical (spherical) triangle
8a. Sun's annual path on the sky at given location
8b. Shadow on a horizontal sun-dial at given date and location
9. Solar analemma at given date and location
