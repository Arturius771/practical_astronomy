import math
import time_functions
import utils

def degrees_minutes_seconds_to_decimal_degrees(angle: int, minutes: int, seconds: int) -> float:
  a = abs(seconds) / 60
  b = (abs(minutes) + a) / 60
  c = abs(angle) + b
  decimal_degrees = -c if angle < 0 or minutes < 0 or seconds < 0 else c
  return decimal_degrees


def decimal_degrees_to_degrees_minutes_seconds(decimal_degree: float) -> tuple:
    unsigned_degrees, minutes, seconds = utils.decimal_to_hours_minutes_seconds(decimal_degree)
    signed_degrees = -1 * unsigned_degrees if decimal_degree < 0 else unsigned_degrees
  
    return (signed_degrees, minutes, seconds)
  
def right_ascension_to_hour_angle(right_ascension_hours: int, right_ascension_minutes: int, right_ascension_seconds: float, local_hours: int, local_minutes: int, local_seconds: float, daylight_savings: int, zone_correction: int, local_day: int, local_month: int, local_year: int, longitude: float) -> tuple:
  # H = LST - a
  greenwich_year, greenwich_month, greenwich_day, utc_hour, utc_minute, utc_second = time_functions.local_civil_time_to_universal_time(local_year,local_month, local_day,local_hours,local_minutes,local_seconds,daylight_savings,zone_correction)
  gst_hours, gst_minutes, gst_seconds = time_functions.universal_time_to_greenwich_sidereal_time(greenwich_year,greenwich_month,greenwich_day,utc_hour,utc_minute,utc_second)
  lst_hours, lst_minutes, lst_seconds = time_functions.greenwich_sidereal_time_to_local_sidereal_time(gst_hours, gst_minutes, gst_seconds, longitude)
  lst = utils.hours_minute_seconds_to_decimal(lst_hours, lst_minutes, lst_seconds)
  ra_decimal = utils.hours_minute_seconds_to_decimal(right_ascension_hours,right_ascension_minutes,right_ascension_seconds)
  hour_angle = lst - ra_decimal

  if hour_angle < 0:
    hour_angle += 24
  
  return decimal_degrees_to_degrees_minutes_seconds(hour_angle)

def hour_angle_to_right_ascension(hour_angle_hour: int, hour_angle_minutes: int, hour_angle_seconds: float, local_hours: int, local_minutes: int, local_seconds: float, daylight_savings: int, zone_correction: int, local_day: int, local_month: int, local_year: int, longitude: float) -> tuple:
  greenwich_year, greenwich_month, greenwich_day, utc_hour, utc_minute, utc_second = time_functions.local_civil_time_to_universal_time(local_year,local_month, local_day,local_hours,local_minutes,local_seconds,daylight_savings,zone_correction)
  gst_hours, gst_minutes, gst_seconds = time_functions.universal_time_to_greenwich_sidereal_time(greenwich_year,greenwich_month,greenwich_day,utc_hour,utc_minute,utc_second)
  lst_hours, lst_minutes, lst_seconds = time_functions.greenwich_sidereal_time_to_local_sidereal_time(gst_hours, gst_minutes, gst_seconds, longitude)
  lst = utils.hours_minute_seconds_to_decimal(lst_hours, lst_minutes, lst_seconds)
  ha_decimal = utils.hours_minute_seconds_to_decimal(hour_angle_hour,hour_angle_minutes,hour_angle_seconds)
  right_ascension = lst - ha_decimal

  if right_ascension < 0:
    right_ascension += 24

  return decimal_degrees_to_degrees_minutes_seconds(right_ascension)

def equatorial_coordinates_to_horizon_coordinates(hour_angle_hour: int, hour_angle_minutes: int, hour_angle_seconds: float, declination_degrees: int, declination_minutes: int, declination_seconds: float, latitude: float) -> tuple:
  ha_decimal = utils.hours_minute_seconds_to_decimal(hour_angle_hour,hour_angle_minutes,hour_angle_seconds)
  ha_degrees = ha_decimal * 15
  ha_radians = math.radians(ha_degrees)
  declination_decimal = utils.hours_minute_seconds_to_decimal(declination_degrees, declination_minutes, declination_seconds)
  declination_radians = math.radians(declination_decimal)
  lat_radians = math.radians(latitude)
  sin_a = math.sin(declination_radians) * math.sin(lat_radians) + math.cos(declination_radians) * math.cos(lat_radians) * math.cos(ha_radians)
  a_radians = math.asin(sin_a)
  a_degrees = math.degrees(a_radians)
  y = -math.cos(declination_radians) * math.cos(lat_radians) * math.sin(ha_radians)
  x = math.sin(declination_radians) - math.sin(lat_radians) * sin_a
  a = math.atan2(y, x) # Python takes y as first argument
  b = math.degrees(a)

  if b < 0:
    b += 360 # b - (360 * math.floor(b/360))

  azimuth_degrees, azimuth_minutes, azimuth_seconds = decimal_degrees_to_degrees_minutes_seconds(b)
  altitude_degrees, altitude_minutes, altitude_seconds = decimal_degrees_to_degrees_minutes_seconds(a_degrees)

  return (azimuth_degrees, azimuth_minutes, azimuth_seconds, altitude_degrees, altitude_minutes, altitude_seconds)

def horizon_coordinates_to_equatorial_coordinates(azimuth_degrees, azimuth_minutes, azimuth_seconds, altitude_degrees, altitude_minutes, altitude_seconds, latitude) -> tuple:
  azimuth_decimal = degrees_minutes_seconds_to_decimal_degrees(azimuth_degrees, azimuth_minutes, azimuth_seconds)
  altitude_decimal = degrees_minutes_seconds_to_decimal_degrees(altitude_degrees, altitude_minutes, altitude_seconds)
  azimuth_radians = math.radians(azimuth_decimal)
  altitude_radians = math.radians(altitude_decimal)
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

  ha_hours, ha_minutes, ha_seconds = decimal_degrees_to_degrees_minutes_seconds(ha_hms)
  declination_hours, declination_minutes, declination_seconds = decimal_degrees_to_degrees_minutes_seconds(declination_degrees)

  return (ha_hours, ha_minutes, ha_seconds, declination_hours, declination_minutes, declination_seconds)