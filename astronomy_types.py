from typing import NewType, Tuple, Union

type Year = int
type Month = int
type Day = Union[int, float]
type Hour = int
type Minutes = int
type Seconds = float
type JulianDate = float
type DecimalTime = float
type Epoch = float
type Angle = int
type RightAscension = Time
type DecimalDegrees = float
type Obliquity = DecimalDegrees


Degrees = NewType('Degrees', Tuple[Angle, Minutes, Seconds])
Date = NewType('Date', Tuple[Year, Month, Day])
Time = NewType('Time', Tuple[Hour, Minutes, Seconds])
FullDate = NewType('FullDate', Tuple[Date, Time])
Declination = NewType('Declination', Degrees)
HourAngle = NewType('HourAngle', Time)
Longitude = Union[Degrees, DecimalDegrees, Angle]
Latitude =  Union[Degrees, DecimalDegrees, Angle]
Azimuth = NewType('Azimuth', Degrees)
Altitude = NewType('Altitude', Degrees)
GeographicCoordinates = NewType('GeographicCoordinates', Tuple[Latitude, Longitude])
HorizontalCoordinates = NewType('HorizontalCoordinates', Tuple[Altitude, Azimuth])
EquatorialCoordinatesHourAngle = NewType('EquatorialCoordinatesHourAngle', Tuple[Declination, HourAngle])
EquatorialCoordinatesRightAscension = NewType('EquatorialCoordinatesRightAscension', Tuple[Declination, RightAscension])
EclipticCoordinates = NewType('EclipticCoordinates', Tuple[Latitude, Longitude])