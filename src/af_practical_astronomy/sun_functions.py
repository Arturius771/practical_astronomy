import math
from .coordinate_functions import ecliptic_to_equatorial_coordinates
from .time_functions import *
from .utils import *
from astronomy_types import  FullDate,  Degrees, EquatorialCoordinates, Longitude, EclipticCoordinates


def sun_longitude(local_date: FullDate, daylight_savings_correction: int, timezone_correction: int) -> Longitude:
  def sun_mean_anomaly_2010(degrees: Degrees) -> float: 
    ecliptic_long = 279.557208
    ecliptic_long_of_perigee =  283.112438
    return degrees + ecliptic_long - ecliptic_long_of_perigee
  
  def sun_true_anomolay_2010(mean_anomaly: float) -> float: 
    eccentricity = 0.016705
    return mean_anomaly + (360/math.pi) * eccentricity * math.sin(math.radians(mean_anomaly))

  def sun_longitude_2010(true_anomaly: float) -> Longitude:
    ecliptic_long_of_perigee =  283.112438
    return true_anomaly + ecliptic_long_of_perigee
  
  greenwich_date, _ = local_civil_to_universal_time(local_date, daylight_savings_correction, timezone_correction)
  julian_date = greenwich_to_julian_date(greenwich_date)
  epoch_date = greenwich_to_julian_date((2010,1,0))
  d = julian_date - epoch_date
  n_degrees = 360 * d / 365.242191
  mean_anomaly = sun_mean_anomaly_2010(n_degrees) 
  mean_anomaly_corrected = mean_anomaly - 360 * math.floor(mean_anomaly/360)
  true_anomaly = sun_true_anomolay_2010(mean_anomaly_corrected)
  longitude = sun_longitude_2010(true_anomaly)
  longitude_corrected = longitude - 360 * math.floor(longitude / 360)

  return longitude_corrected

def sun_position_approximate(local_date: FullDate, daylight_savings_correction: int, timezone_correction: int) -> EquatorialCoordinates:
  greenwich_date, _ = local_civil_to_universal_time(local_date, daylight_savings_correction, timezone_correction)
  longitude = sun_longitude(local_date, daylight_savings_correction, timezone_correction)
  sun_coordinates = ecliptic_to_equatorial_coordinates(EclipticCoordinates((0, longitude)), greenwich_date)

  return sun_coordinates