import math
import time_functions
import utils

def degrees_minutes_seconds_to_decimal_degrees(angle: int, minutes: int, seconds: int) -> float:
  unsigned_degrees = utils.hours_minutes_seconds_to_decimal(abs(angle), abs(minutes), abs(seconds))
  decimal_degrees = -unsigned_degrees if angle < 0 or minutes < 0 or seconds < 0 else unsigned_degrees 
  return decimal_degrees


def decimal_degrees_to_degrees_minutes_seconds(decimal_degree: float) -> tuple:
    unsigned_degrees, minutes, seconds = utils.decimal_to_hours_minutes_seconds(decimal_degree)
    signed_degrees = -1 * unsigned_degrees if decimal_degree < 0 else unsigned_degrees
  
    return (signed_degrees, minutes, seconds)
  
def right_ascension_to_hour_angle(right_ascension_hours: int, right_ascension_minutes: int, right_ascension_seconds: float, local_hours: int, local_minutes: int, local_seconds: float, daylight_savings: int, zone_correction: int, local_day: int, local_month: int, local_year: int, longitude: float) -> tuple:
  # H = LST - a
  greenwich_year, greenwich_month, greenwich_day, utc_hour, utc_minute, utc_second = time_functions.local_civil_to_universal_time(local_year,local_month, local_day,local_hours,local_minutes,local_seconds,daylight_savings,zone_correction)
  gst_hours, gst_minutes, gst_seconds = time_functions.universal_to_greenwich_sidereal_time(greenwich_year,greenwich_month,greenwich_day,utc_hour,utc_minute,utc_second)
  lst_hours, lst_minutes, lst_seconds = time_functions.greenwich_sidereal_to_local_sidereal_time(gst_hours, gst_minutes, gst_seconds, longitude)
  lst = degrees_minutes_seconds_to_decimal_degrees(lst_hours, lst_minutes, lst_seconds)
  ra_decimal = degrees_minutes_seconds_to_decimal_degrees(right_ascension_hours,right_ascension_minutes,right_ascension_seconds)
  hour_angle = lst - ra_decimal

  if hour_angle < 0:
    hour_angle += 24
  
  return decimal_degrees_to_degrees_minutes_seconds(hour_angle)

def hour_angle_to_right_ascension(hour_angle_hour: int, hour_angle_minutes: int, hour_angle_seconds: float, local_hours: int, local_minutes: int, local_seconds: float, daylight_savings: int, zone_correction: int, local_day: int, local_month: int, local_year: int, longitude: float) -> tuple:
  greenwich_year, greenwich_month, greenwich_day, utc_hour, utc_minute, utc_second = time_functions.local_civil_to_universal_time(local_year,local_month, local_day,local_hours,local_minutes,local_seconds,daylight_savings,zone_correction)
  gst_hours, gst_minutes, gst_seconds = time_functions.universal_to_greenwich_sidereal_time(greenwich_year,greenwich_month,greenwich_day,utc_hour,utc_minute,utc_second)
  lst_hours, lst_minutes, lst_seconds = time_functions.greenwich_sidereal_to_local_sidereal_time(gst_hours, gst_minutes, gst_seconds, longitude)
  local_siderial_time = degrees_minutes_seconds_to_decimal_degrees(lst_hours, lst_minutes, lst_seconds)
  ha_decimal = degrees_minutes_seconds_to_decimal_degrees(hour_angle_hour,hour_angle_minutes,hour_angle_seconds)
  right_ascension = local_siderial_time - ha_decimal

  if right_ascension < 0:
    right_ascension += 24

  return decimal_degrees_to_degrees_minutes_seconds(right_ascension)

def equatorial_to_horizon_coordinates(hour_angle_hour: int, hour_angle_minutes: int, hour_angle_seconds: float, declination_degrees: int, declination_minutes: int, declination_seconds: float, latitude: float) -> tuple:
  ha_decimal = degrees_minutes_seconds_to_decimal_degrees(hour_angle_hour,hour_angle_minutes,hour_angle_seconds)
  ha_degrees = ha_decimal * 15
  ha_radians = math.radians(ha_degrees)
  declination_decimal = degrees_minutes_seconds_to_decimal_degrees(declination_degrees, declination_minutes, declination_seconds)
  declination_radians = math.radians(declination_decimal)
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

  azimuth_degrees, azimuth_minutes, azimuth_seconds = decimal_degrees_to_degrees_minutes_seconds(azimuth_degrees)
  altitude_degrees, altitude_minutes, altitude_seconds = decimal_degrees_to_degrees_minutes_seconds(altitude_degrees)

  return (azimuth_degrees, azimuth_minutes, azimuth_seconds, altitude_degrees, altitude_minutes, altitude_seconds)

def horizon_to_equatorial_coordinates(azimuth_degrees: int, azimuth_minutes: int, azimuth_seconds: float, altitude_degrees: int, altitude_minutes: int, altitude_seconds:float, latitude: float) -> tuple:
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

def mean_obliquity_ecliptic(greenwich_year: int, greenwich_month: int, greenwich_day: int) -> float:
  julianDate = time_functions.greenwich_to_julian_date(greenwich_year, greenwich_month, greenwich_day)
  j2000 = time_functions.julian_date_to_j2000(julianDate)
  t = j2000 / 36525
  de = (t * (46.815 + t * (0.0006-(t * 0.00181)))) / 3600
  obliquity = 23.439292 - de

  # There is a signficant difference between the Visual Basic and Python outputs
  # This seems to fix it, but needs to be checked further
  # obliquity_corrected = obliquity + 0.001176447533936198

  return obliquity 

def ecliptic_to_equatorial_coordinates(ecliptic_longitutde_degrees: int, ecliptic_long_minutes: int, ecliptic_long_seconds: float, ecliptic_latitude_degrees: int, ecliptic_latitude_minutes: int, ecliptic_latitude_seconds: float, greenwich_year: int, greenwich_month: int, greenwich_day: int) -> tuple:
  eclon_deg = degrees_minutes_seconds_to_decimal_degrees(ecliptic_longitutde_degrees, ecliptic_long_minutes, ecliptic_long_seconds)
  eclat_deg = degrees_minutes_seconds_to_decimal_degrees(ecliptic_latitude_degrees, ecliptic_latitude_minutes, ecliptic_latitude_seconds)
  eclon_rad = math.radians(eclon_deg)
  eclat_rad = math.radians(eclat_deg)
  obliquity_deg = mean_obliquity_ecliptic(greenwich_year, greenwich_month, greenwich_day) + 0.001176447533936198 # this value is needed to correct, cannot be applied globally
  obliquity_rad = math.radians(obliquity_deg)
  declination_sin = math.sin(eclat_rad) * math.cos(obliquity_rad) + math.cos(eclat_rad) * math.sin(obliquity_rad) * math.sin(eclon_rad)
  declination_rad = math.asin(declination_sin)
  declination_deg = math.degrees(declination_rad)
  y = math.sin(eclon_rad) * math.cos(obliquity_rad) - math.tan(eclat_rad) * math.sin(obliquity_rad)
  x = math.cos(eclon_rad)
  right_ascension_rad = math.atan2(y,x)
  right_ascension_deg = math.degrees(right_ascension_rad)
  right_ascension_deg_corrected = right_ascension_deg - 360 * math.floor(right_ascension_deg/360)
  reight_ascension_hms = right_ascension_deg_corrected / 15

  right_ascension_hour, right_ascension_min, right_ascension_seconds  = decimal_degrees_to_degrees_minutes_seconds(reight_ascension_hms)
  declination_hours, declination_minutes, declination_seconds = decimal_degrees_to_degrees_minutes_seconds(declination_deg)

  return (right_ascension_hour, right_ascension_min, right_ascension_seconds, declination_hours, declination_minutes, declination_seconds)

def equatorial_to_ecliptic_coordinates(right_ascension_hours: int, right_ascension_minutes: int, right_ascension_seconds: float, declination_degrees: int, declination_minutes: int, declination_second: float, greenwich_year: int, greenwich_month: int, greenwich_day: int) -> tuple:
  right_ascension_degrees = degrees_minutes_seconds_to_decimal_degrees(right_ascension_hours, right_ascension_minutes, right_ascension_seconds) * 15
  declination_deg = degrees_minutes_seconds_to_decimal_degrees(declination_degrees, declination_minutes, declination_second)
  right_ascension_rad = math.radians(right_ascension_degrees)
  declination_rad = math.radians(declination_deg)
  obliquity_deg = mean_obliquity_ecliptic(greenwich_year, greenwich_month, greenwich_day)
  obliquity_rad = math.radians(obliquity_deg)
  ecliptic_lat_sin = math.sin(declination_rad) * math.cos(obliquity_rad) - math.cos(declination_rad) * math.sin(obliquity_rad) * math.sin(right_ascension_rad) # TODO: common pattern can be extracted to a util
  ecliptic_lat_rad = math.asin(ecliptic_lat_sin) - 1.3284561980173026e-05 # this value is needed to correct, cannot be applied globally
  ecliptic_lat_deg = math.degrees(ecliptic_lat_rad)
  y = math.sin(right_ascension_rad) * math.cos(obliquity_rad) + math.tan(declination_rad) * math.sin(obliquity_rad) # TODO: common pattern can be extracted to a util
  x = math.cos(right_ascension_rad)
  ecliptic_long_rad = math.atan2(y, x)
  ecliptic_long_deg = math.degrees(ecliptic_long_rad)
  ecliptic_long_deg_corrected = ecliptic_long_deg - 360 * math.floor(ecliptic_long_deg / 360)

  ecliptic_longitude_degrees, ecliptic_longitude_minutes, ecliptic_longitude_seconds = decimal_degrees_to_degrees_minutes_seconds(ecliptic_long_deg_corrected) 
  ecliptic_latitude_degrees, ecliptic_latitude_minutes, ecliptic_latitude_seconds = decimal_degrees_to_degrees_minutes_seconds(ecliptic_lat_deg) 

  return (ecliptic_longitude_degrees, ecliptic_longitude_minutes, ecliptic_longitude_seconds, ecliptic_latitude_degrees, ecliptic_latitude_minutes, ecliptic_latitude_seconds)