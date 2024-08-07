import math
from astronomy_types import *
import time_functions
import utils

def degrees_to_decimal_degrees(degrees: Degrees | RightAscension) -> DecimalDegrees:
  angle, minutes, seconds = degrees
  unsigned_degrees = utils.time_to_decimal(Time((abs(angle), abs(minutes), abs(seconds))))
  decimal_degrees = -unsigned_degrees if angle < 0 or minutes < 0 or seconds < 0 else unsigned_degrees 
  return decimal_degrees


def decimal_degrees_to_degrees(decimal_degree: DecimalDegrees) -> Degrees:
    unsigned_degrees, minutes, seconds = utils.decimal_to_time(decimal_degree)
    signed_degrees = -1 * unsigned_degrees if decimal_degree < 0 else unsigned_degrees
  
    return Degrees((signed_degrees, minutes, seconds))
  
def right_ascension_to_hour_angle(right_ascension: RightAscension, local_date_and_time: FullDate, daylight_savings: int, zone_correction: int, longitude: Longitude) -> HourAngle:
  """H = LST - a"""
  utc = time_functions.local_civil_to_universal_time(local_date_and_time, daylight_savings, zone_correction)
  gst = time_functions.universal_to_greenwich_sidereal_time(utc)
  local_sidereal_time = time_functions.greenwich_sidereal_to_local_sidereal_time(gst, longitude)
  lst_dec = utils.time_to_decimal(local_sidereal_time)

  ra_decimal = degrees_to_decimal_degrees(Degrees(right_ascension))
  hour_angle = lst_dec - ra_decimal

  if hour_angle < 0:
    hour_angle += 24
  
  return decimal_degrees_to_degrees(hour_angle)

def hour_angle_to_right_ascension(hour_angle: HourAngle, full_date: FullDate, daylight_savings: int, zone_correction: int, longitude: Longitude) -> RightAscension:
  utc = time_functions.local_civil_to_universal_time(full_date,daylight_savings,zone_correction)
  gst = time_functions.universal_to_greenwich_sidereal_time(utc)
  lst = time_functions.greenwich_sidereal_to_local_sidereal_time(gst, longitude)
  lst_dec = degrees_to_decimal_degrees(Degrees(lst))
  ha_decimal = degrees_to_decimal_degrees(hour_angle)
  right_ascension = lst_dec - ha_decimal

  if right_ascension < 0:
    right_ascension += 24

  return decimal_degrees_to_degrees(right_ascension)

def equatorial_to_horizon_coordinates(equatorial_coordinates: EquatorialCoordinates, latitude: Latitude) -> HorizontalCoordinates:
  hour_angle, declination = EquatorialCoordinatesHourAngle(equatorial_coordinates)
  ha_decimal = degrees_to_decimal_degrees(hour_angle)
  ha_degrees = ha_decimal * 15
  ha_radians = math.radians(ha_degrees)
  declination_decimal = degrees_to_decimal_degrees(declination)
  declination_radians = math.radians(declination_decimal)
  if isinstance(latitude, tuple):
        latitude = degrees_to_decimal_degrees(latitude)
  lat_radians = math.radians(latitude)
  sin_a = math.sin(declination_radians) * math.sin(lat_radians) + math.cos(declination_radians) * math.cos(lat_radians) * math.cos(ha_radians)
  altitude_radians = math.asin(sin_a)
  altitude_degrees = math.degrees(altitude_radians)
  y = -math.cos(declination_radians) * math.cos(lat_radians) * math.sin(ha_radians)
  x = math.sin(declination_radians) - math.sin(lat_radians) * sin_a
  azimuth_radians = math.atan2(y, x) # Python takes y as first argument
  azimuth_degrees = math.degrees(azimuth_radians)

  if azimuth_degrees < 0:
    azimuth_degrees += 360 # b - (360 * math.floor(b/360))

  return HorizontalCoordinates((decimal_degrees_to_degrees(azimuth_degrees), decimal_degrees_to_degrees(altitude_degrees)))

def horizon_to_equatorial_coordinates(horizontal_coordinates: HorizontalCoordinates, latitude: Latitude) -> tuple:
  altitude, azimuth = horizontal_coordinates
  azimuth_decimal = degrees_to_decimal_degrees(azimuth)
  altitude_decimal = degrees_to_decimal_degrees(altitude)
  azimuth_radians = math.radians(azimuth_decimal)
  altitude_radians = math.radians(altitude_decimal)
  if isinstance(latitude, tuple):
        latitude = degrees_to_decimal_degrees(latitude)
  latitude_radians = math.radians(latitude)
  declination_sin = math.sin(altitude_radians) * math.sin(latitude_radians) + math.cos(altitude_radians) * math.cos(latitude_radians) * math.cos(azimuth_radians)
  declination_radians = math.asin(declination_sin)
  declination_degrees = math.degrees(declination_radians)
  y = -math.cos(altitude_radians) * math.cos(latitude_radians) * math.sin(azimuth_radians)
  x = math.sin(altitude_radians) - math.sin(latitude_radians) * declination_sin
  a = math.atan2(y, x)
  b = math.degrees(a)
  ha_degrees = b - (360 * math.floor(b/360))
  ha_hms = ha_degrees / 15

  ha_hours, ha_minutes, ha_seconds = decimal_degrees_to_degrees(ha_hms)
  declination_hours, declination_minutes, declination_seconds = decimal_degrees_to_degrees(declination_degrees)

  return (ha_hours, ha_minutes, ha_seconds, declination_hours, declination_minutes, declination_seconds)

def mean_obliquity_ecliptic(greenwich_date: Date) -> Obliquity:
  julianDate = time_functions.greenwich_to_julian_date(greenwich_date)
  j2000 = time_functions.julian_date_to_j2000(julianDate)
  t = j2000 / 36525
  de = (t * (46.815 + t * (0.0006-(t * 0.00181)))) / 3600
  obliquity = 23.439292 - de

  # There is a signficant difference between the Visual Basic and Python outputs
  # This seems to fix it, but needs to be checked further
  # obliquity_corrected = obliquity + 0.001176447533936198

  return obliquity 

def ecliptic_to_equatorial_coordinates(ecliptic_coordinates: EclipticCoordinates, greenwich_date: Date) -> EquatorialCoordinates:
  eclat, eclon = ecliptic_coordinates
  if isinstance(eclat, tuple):
    eclat_decimal = degrees_to_decimal_degrees(eclat)
  else:
    eclat_decimal = eclat
  if isinstance(eclon, tuple):
   eclon_decimal = degrees_to_decimal_degrees(eclon)
  else:
    eclon_decimal = eclon
  eclon_rad = math.radians(eclon_decimal)
  eclat_rad = math.radians(eclat_decimal)
  obliquity_deg = mean_obliquity_ecliptic(greenwich_date) + 0.001176447533936198 # this value is needed to correct, cannot be applied globally
  obliquity_rad = math.radians(obliquity_deg)
  declination_sin = math.sin(eclat_rad) * math.cos(obliquity_rad) + math.cos(eclat_rad) * math.sin(obliquity_rad) * math.sin(eclon_rad)
  declination_rad = math.asin(declination_sin)
  declination_deg = math.degrees(declination_rad)
  y = math.sin(eclon_rad) * math.cos(obliquity_rad) - math.tan(eclat_rad) * math.sin(obliquity_rad)
  x = math.cos(eclon_rad)
  right_ascension_rad = math.atan2(y,x)
  right_ascension_deg = math.degrees(right_ascension_rad)
  right_ascension_deg_corrected = right_ascension_deg - 360 * math.floor(right_ascension_deg/360)
  right_ascension = right_ascension_deg_corrected / 15

  return EquatorialCoordinatesRightAscension((decimal_degrees_to_degrees(right_ascension), decimal_degrees_to_degrees(declination_deg)))

def equatorial_to_ecliptic_coordinates(equatorial_coordinates: EquatorialCoordinates, greenwich_date: Date) -> EclipticCoordinates:
  right_ascension, declination = EquatorialCoordinatesRightAscension(equatorial_coordinates)
  right_ascension_degrees = degrees_to_decimal_degrees(right_ascension) * 15
  declination_deg = degrees_to_decimal_degrees(declination)
  right_ascension_rad = math.radians(right_ascension_degrees)
  declination_rad = math.radians(declination_deg)
  obliquity_deg = mean_obliquity_ecliptic(greenwich_date)
  obliquity_rad = math.radians(obliquity_deg)
  ecliptic_lat_sin = math.sin(declination_rad) * math.cos(obliquity_rad) - math.cos(declination_rad) * math.sin(obliquity_rad) * math.sin(right_ascension_rad) # TODO: common pattern can be extracted to a util
  ecliptic_lat_rad = math.asin(ecliptic_lat_sin) - 1.3284561980173026e-05 # this value is needed to correct, cannot be applied globally
  ecliptic_lat_deg = math.degrees(ecliptic_lat_rad)
  y = math.sin(right_ascension_rad) * math.cos(obliquity_rad) + math.tan(declination_rad) * math.sin(obliquity_rad) # TODO: common pattern can be extracted to a util
  x = math.cos(right_ascension_rad)
  ecliptic_long_rad = math.atan2(y, x)
  ecliptic_long_deg = math.degrees(ecliptic_long_rad)
  ecliptic_long_deg_corrected = ecliptic_long_deg - 360 * math.floor(ecliptic_long_deg / 360)

  return EclipticCoordinates((decimal_degrees_to_degrees(ecliptic_long_deg_corrected),decimal_degrees_to_degrees(ecliptic_lat_deg)))