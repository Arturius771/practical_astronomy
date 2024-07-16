import math
import time_functions
import helpers

def convert_degrees_minutes_seconds_to_decimal_degrees(angle: int, minutes: int, seconds: int) -> float:
  a = abs(seconds) / 60
  b = (abs(minutes) + a) / 60
  c = abs(angle) + b
  decimal_degrees = -c if angle < 0 or minutes < 0 or seconds < 0 else c

  return decimal_degrees


def convert_decimal_degrees_to_degrees_minutes_seconds(decimal_degree: float) -> tuple:
    unsigned_degrees, minutes, seconds = helpers.convert_decimal_to_hours_minutes_seconds(decimal_degree)
    signed_degrees = -1 * unsigned_degrees if decimal_degree < 0 else unsigned_degrees
  
    return (signed_degrees, minutes, seconds)
  
def convert_right_ascension_to_hour_angle(right_ascension_hours: int, right_ascension_minutes: int, right_ascension_seconds: float, local_hours: int, local_minutes: int, local_seconds: float, daylight_savings: int, zone_correction: int, local_day: int, local_month: int, local_year: int, longitude: float) -> tuple:
  # H = LST - a
  greenwich_year, greenwich_month, greenwich_day, utc_hour, utc_minute, utc_second = time_functions.convert_local_civil_time_to_universal_time(local_year,local_month, local_day,local_hours,local_minutes,local_seconds,daylight_savings,zone_correction)
  gst_hours, gst_minutes, gst_seconds = time_functions.convert_universal_time_to_greenwich_sidereal_time(greenwich_year,greenwich_month,greenwich_day,utc_hour,utc_minute,utc_second)
  lst_hours, lst_minutes, lst_seconds = time_functions.convert_greenwich_sidereal_time_to_local_sidereal_time(gst_hours, gst_minutes, gst_seconds, longitude)
  lst = helpers.convert_hours_minute_seconds_to_decimal(lst_hours, lst_minutes, lst_seconds)
  ra_in_decimal = helpers.convert_hours_minute_seconds_to_decimal(right_ascension_hours,right_ascension_minutes,right_ascension_seconds)
  hour_angle = lst - ra_in_decimal

  if hour_angle < 0:
    hour_angle += 24
  
  return convert_decimal_degrees_to_degrees_minutes_seconds(hour_angle)

def convert_hour_angle_to_right_ascension(hour_angle_hour: int, hour_angle_minutes: int, hour_angle_seconds: float, local_hours: int, local_minutes: int, local_seconds: float, daylight_savings: int, zone_correction: int, local_day: int, local_month: int, local_year: int, longitude: float) -> tuple:
  greenwich_year, greenwich_month, greenwich_day, utc_hour, utc_minute, utc_second = time_functions.convert_local_civil_time_to_universal_time(local_year,local_month, local_day,local_hours,local_minutes,local_seconds,daylight_savings,zone_correction)
  gst_hours, gst_minutes, gst_seconds = time_functions.convert_universal_time_to_greenwich_sidereal_time(greenwich_year,greenwich_month,greenwich_day,utc_hour,utc_minute,utc_second)
  lst_hours, lst_minutes, lst_seconds = time_functions.convert_greenwich_sidereal_time_to_local_sidereal_time(gst_hours, gst_minutes, gst_seconds, longitude)
  lst = helpers.convert_hours_minute_seconds_to_decimal(lst_hours, lst_minutes, lst_seconds)
  ha_in_decimal = helpers.convert_hours_minute_seconds_to_decimal(hour_angle_hour,hour_angle_minutes,hour_angle_seconds)
  right_ascension = lst - ha_in_decimal

  if right_ascension < 0:
    right_ascension += 24

  return convert_decimal_degrees_to_degrees_minutes_seconds(right_ascension)

def convert_equatorial_coordinates_to_horizon_coordinates(hour_angle_hour: int, hour_angle_minutes: int, hour_angle_seconds: float, declination_degrees: int, declination_minutes: int, declination_seconds: float, latitude: float) -> tuple:
  ha_in_decimal = helpers.convert_hours_minute_seconds_to_decimal(hour_angle_hour,hour_angle_minutes,hour_angle_seconds)
  ha_in_degrees = ha_in_decimal * 15
  ha_in_radians = math.radians(ha_in_degrees)
  declination_decimal = helpers.convert_hours_minute_seconds_to_decimal(declination_degrees, declination_minutes, declination_seconds)
  declination_radians = math.radians(declination_decimal)
  lat_radians = math.radians(latitude)
  sin_a = math.sin(declination_radians) * math.sin(lat_radians) + math.cos(declination_radians) * math.cos(lat_radians) * math.cos(ha_in_radians)
  a_radians = math.asin(sin_a)
  a_degrees = math.degrees(a_radians)
  y = -math.cos(declination_radians) * math.cos(lat_radians) * math.sin(ha_in_radians)
  x = math.sin(declination_radians) - math.sin(lat_radians) * sin_a
  a = math.atan2(y, x) # Python takes y as first argument
  b = math.degrees(a)

  if b < 0:
    b += 360

  azimuth_degrees, azimuth_minutes, azimuth_seconds = convert_decimal_degrees_to_degrees_minutes_seconds(b)
  altitude_degrees, altitude_minutes, altitude_seconds = convert_decimal_degrees_to_degrees_minutes_seconds(a_degrees)

  return (azimuth_degrees, azimuth_minutes, azimuth_seconds, altitude_degrees, altitude_minutes, altitude_seconds)


