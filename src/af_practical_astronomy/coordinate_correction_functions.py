
import math
from typing import NewType, Tuple
from .coordinate_functions import decimal_degrees_to_degrees, degrees_to_decimal_degrees, degrees_to_hours, hours_to_degrees
from .time_functions import greenwich_sidereal_to_universal_time, greenwich_to_julian_date, julian_date_to_epoch, local_sidereal_to_greenwich_sidereal_time
from .utils import decimal_time_to_time
from .sun_functions import sun_longitude
from astronomy_types import Date, Time, FullDate, Degrees, DecimalDegrees, RightAscension, EquatorialCoordinates,  EclipticCoordinates, Declination, GeographicCoordinates, Epoch ,Azimuth


RisingAndSetting = NewType('RisingAndSetting', Tuple[bool, Time, Time, Azimuth, Azimuth])

def angle_difference(object1_coordinates: EquatorialCoordinates, object2_coordinates: EquatorialCoordinates) -> Degrees:
  declination1, right_ascension1 = object1_coordinates
  decimal_declination1 = degrees_to_decimal_degrees(declination1)
  decimal_right_ascension1 = degrees_to_hours(degrees_to_decimal_degrees(Degrees(right_ascension1)))
  radians_declination1 = math.radians(decimal_declination1)
  radians_right_ascension1 = math.radians(decimal_right_ascension1)
  
  declination2, right_ascension2 = object2_coordinates
  decimal_declination2 = degrees_to_decimal_degrees(declination2)
  decimal_right_ascension2 = degrees_to_hours(degrees_to_decimal_degrees(Degrees(right_ascension2)))
  radians_declination2 = math.radians(decimal_declination2)
  radians_right_ascension2 = math.radians(decimal_right_ascension2)
  
  difference = radians_right_ascension1 - radians_right_ascension2
  cos_d = math.sin(radians_declination1) * math.sin(radians_declination2) + math.cos(radians_declination1) * math.cos(radians_declination2) * math.cos(difference)
  
  rad_d = math.acos(cos_d)
  deg_d = math.degrees(rad_d)

  return decimal_degrees_to_degrees(deg_d)
  
def rising_and_setting(target_coordinates: EquatorialCoordinates, observer_coordinates: GeographicCoordinates, greenwich_date: Date, vertical_shift: DecimalDegrees) -> RisingAndSetting:
  """
  Calculates a tuple containing the targets rising and setting time and position. 
  """
  dec, ra = target_coordinates
  decimal_right_ascension = degrees_to_decimal_degrees(Degrees(ra))
  radians_declination = math.radians(degrees_to_decimal_degrees(dec))
  radians_vertical_shift = math.radians(vertical_shift)
  lat, long = observer_coordinates

  if isinstance(lat, tuple):
    lat = degrees_to_decimal_degrees(lat)
    
  radians_geographic_latitude = math.radians(lat)

  cosine_ha = -(math.sin(radians_vertical_shift) + math.sin(radians_geographic_latitude) * math.sin(radians_declination)) / (math.cos(radians_geographic_latitude) * math.cos(radians_declination))
  hours_h = hours_to_degrees(math.degrees(math.acos(cosine_ha)))
  rise_lst = (decimal_right_ascension - hours_h) - 24 * int(((decimal_right_ascension - hours_h))/ 24)
  set_lst = (decimal_right_ascension + hours_h) - 24 * int(((decimal_right_ascension + hours_h))/ 24)

  a = math.degrees(math.acos((math.sin(radians_declination) + math.sin(radians_vertical_shift) * math.sin(radians_geographic_latitude)) / (math.cos(radians_vertical_shift) * math.cos(radians_geographic_latitude))))
  rise_az = Azimuth(a - 360 * int(a / 360))
  set_az = Azimuth((360 - a) - 360 * int((360 - a)/ 360))

  rise_greenwich_sidereal_time = local_sidereal_to_greenwich_sidereal_time(decimal_time_to_time(rise_lst), long)
  rise_full_date = FullDate((greenwich_date, rise_greenwich_sidereal_time))
  set_greenwich_sidereal_time = local_sidereal_to_greenwich_sidereal_time(decimal_time_to_time(set_lst), long)
  set_full_date = FullDate((greenwich_date, set_greenwich_sidereal_time))
  _, (r_h, r_m, r_s) = greenwich_sidereal_to_universal_time(rise_full_date)
  _, (s_h, s_m, s_s) = greenwich_sidereal_to_universal_time(set_full_date)
  rise_time_adjusted = Time((r_h, r_m, r_s + 0.008333))
  set_time_adjusted = Time((s_h, s_m, s_s + 0.008333))

  # Circumpolar if the target never sets below the horizon. 
  circumpolar = True if cosine_ha < 1 else False

  return RisingAndSetting((circumpolar, rise_time_adjusted, set_time_adjusted, rise_az, set_az))

def precession_low_precision(equatorial_coordinates: EquatorialCoordinates, original_epoch: Epoch, new_epoch: Epoch) -> EquatorialCoordinates:
  """
  Precession is the periodic change in orientation of the rotational axis of the central body. 
  """
  dec1, ra1 = equatorial_coordinates
  dec1_rad = math.radians(degrees_to_decimal_degrees(dec1))
  ra1_rad = math.radians(degrees_to_hours(degrees_to_decimal_degrees(Degrees(ra1))))
  t_centuries = julian_date_to_epoch(original_epoch, -2415020.5) / 36525
  m = 3.07234 + (0.00186 * t_centuries)
  n = 20.0468 - (0.0085 * t_centuries)
  n_years = julian_date_to_epoch(new_epoch, -original_epoch)  / 365.25
  s1 = ((m + (n * math.sin(ra1_rad) * math.tan(dec1_rad) / 15)) * n_years) / 3600
  ra2 = degrees_to_decimal_degrees(Degrees(ra1)) + s1
  s2 = (n * math.cos(ra1_rad) * n_years) / 3600
  dec2 = degrees_to_decimal_degrees(dec1) + s2

  return EquatorialCoordinates((Declination(decimal_degrees_to_degrees(dec2)), RightAscension(Time(decimal_degrees_to_degrees(ra2)))))


def nutation_from_date(greenwich_date: Date) -> tuple:
  """
  Nutation occurs due to gravitational effects from other bodies causing the axial precession to vary. 
  """
  jd = greenwich_to_julian_date(greenwich_date)
  t_centuries = julian_date_to_epoch(jd, -2415020) / 36525
  a = 100.0021358 * t_centuries
  l1 = 279.6967 + (0.000303 * t_centuries**2)
  l2 = l1 + 360 * (a - math.floor(a))
  l3 = l2 - 360 * math.floor(l2 / 360)
  l4 = math.radians(l3)
  b = 5.372617 * t_centuries
  n1 = 259.1833 - 360 * (b - math.floor(b))
  n2 = n1 - 360 * (math.floor(n1 / 360))
  n3 = math.radians(n2)
  nutation_longtitude = (-17.2 * math.sin(n3) - 1.3 * math.sin(2 * l4)) / 3600
  nutation_obliquity = (9.2 * math.cos(n3) + 0.5 * math.cos(2 * l4)) / 3600

  return (nutation_longtitude, nutation_obliquity)

def aberration_from_date(ut_date: FullDate, true_ecliptic_coordinates: EclipticCoordinates) -> EclipticCoordinates:
  """
  Aberration is the apparent motion of a subject caused by the displacement of the observer's position. The object will appear to move towards the observer's direction of motion. 
  """
  lat, long = true_ecliptic_coordinates 
  true_long = degrees_to_decimal_degrees(long)
  true_lat = degrees_to_decimal_degrees(lat)
  sun_long = sun_longitude(ut_date,0,0)
  dlong = -20.5 * math.cos(math.radians(sun_long - true_long)) / math.cos(math.radians(true_lat))
  dlat = -20.5 * math.sin(math.radians(sun_long - true_long)) * math.sin(math.radians(true_lat))
  apparent_long = decimal_degrees_to_degrees(true_long + (dlong / 3600))
  apparent_lat = decimal_degrees_to_degrees(true_lat + (dlat / 3600))

  return EclipticCoordinates((apparent_lat, apparent_long))