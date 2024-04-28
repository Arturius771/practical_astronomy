import math
import time_functions

def convert_degrees_minutes_seconds_to_decimal_degrees(angle: int, minutes: int, seconds: int) -> float:
  a = abs(seconds) / 60
  b = (abs(minutes) + a) / 60
  c = abs(angle) + b
  decimal_degrees = -c if angle < 0 or minutes < 0 or seconds < 0 else c

  return decimal_degrees


def convert_decimal_degrees_to_degrees_minutes_seconds(decimal_degree: float) -> tuple:
  unsigned_decimal = abs(decimal_degree)
  total_seconds = unsigned_decimal * 3600
  total_seconds_rounded = round(total_seconds % 60, 2)
  corrected = 0 if total_seconds_rounded == 60 else total_seconds_rounded
  corrected_remainder = total_seconds + 60 if total_seconds_rounded == 60 else total_seconds
  minutes = math.floor(corrected_remainder / 60) % 60
  unsigned_degrees = math.floor(corrected_remainder / 3600)
  signed_degrees = -1 * unsigned_degrees if decimal_degree < 0 else unsigned_degrees
  
  return (signed_degrees, minutes, math.floor(corrected))
  
def convert_right_ascension_to_hour_angle(right_ascension_hours: int, right_ascension_minutes: int, right_ascension_seconds: float, local_hours: int, local_minutes: int, local_seconds: float, daylight_savings: int, zone_correction: int, local_day: int, local_month: int, local_year: int, longitude: float) -> tuple:
  # H = LST - a
  greenwich_year, greenwich_month, greenwich_day, utc_hour, utc_minute, utc_second = time_functions.convert_local_civil_time_to_universal_time(local_year,local_month, local_day,local_hours,local_minutes,local_seconds,daylight_savings,zone_correction)

  gst_hours, gst_minutes, gst_seconds = time_functions.convert_universal_time_to_greenwich_sidereal_time(greenwich_year,greenwich_month,greenwich_day,utc_hour,utc_minute,utc_second)

  lst_hours, lst_minutes, lst_seconds = time_functions.convert_greenwich_sidereal_time_to_local_sidereal_time(gst_hours, gst_minutes, gst_seconds, longitude)

  lst = time_functions.convert_hours_minute_seconds_to_decimal_time(lst_hours, lst_minutes, lst_seconds)

  ra_in_decimal = time_functions.convert_hours_minute_seconds_to_decimal_time(right_ascension_hours,right_ascension_minutes,right_ascension_seconds)

  hour_angle = lst - ra_in_decimal

  if hour_angle < 0:
    hour_angle += 24
  
  return time_functions.convert_decimal_hours_to_hours_minutes_seconds(hour_angle)

def convert_hour_angle_to_right_ascension(hour_angle_hour: int, hour_angle_minutes: int, hour_angle_seconds: float, local_hours: int, local_minutes: int, local_seconds: float, daylight_savings: int, zone_correction: int, local_day: int, local_month: int, local_year: int, longitude: float) -> tuple:
  greenwich_year, greenwich_month, greenwich_day, utc_hour, utc_minute, utc_second = time_functions.convert_local_civil_time_to_universal_time(local_year,local_month, local_day,local_hours,local_minutes,local_seconds,daylight_savings,zone_correction)

  gst_hours, gst_minutes, gst_seconds = time_functions.convert_universal_time_to_greenwich_sidereal_time(greenwich_year,greenwich_month,greenwich_day,utc_hour,utc_minute,utc_second)

  lst_hours, lst_minutes, lst_seconds = time_functions.convert_greenwich_sidereal_time_to_local_sidereal_time(gst_hours, gst_minutes, gst_seconds, longitude)

  lst = time_functions.convert_hours_minute_seconds_to_decimal_time(lst_hours, lst_minutes, lst_seconds)

  ha_in_decimal = time_functions.convert_hours_minute_seconds_to_decimal_time(hour_angle_hour,hour_angle_minutes,hour_angle_seconds)

  right_ascension = lst - ha_in_decimal

  if right_ascension < 0:
    right_ascension += 24

  return time_functions.convert_decimal_hours_to_hours_minutes_seconds(right_ascension)

# def convert_horizon_coordinates_to_equatorial_coordinates
