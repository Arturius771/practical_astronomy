import math
import time_functions
import utils
import astronomy_types


def degrees_to_decimal_degrees(degrees: astronomy_types.Degrees) -> astronomy_types.DecimalDegrees:
  angle, minutes, seconds = degrees
  unsigned_degrees = utils.time_to_decimal(astronomy_types.Time((abs(angle), abs(minutes), abs(seconds))))
  decimal_degrees = -unsigned_degrees if angle < 0 or minutes < 0 or seconds < 0 else unsigned_degrees 

  return decimal_degrees

def decimal_degrees_to_degrees(decimal_degree: astronomy_types.DecimalDegrees) -> astronomy_types.Degrees:
    unsigned_degrees, minutes, seconds = utils.decimal_to_time(decimal_degree)
    signed_degrees = -1 * unsigned_degrees if decimal_degree < 0 else unsigned_degrees
  
    return astronomy_types.Degrees((signed_degrees, minutes, seconds))

def hours_to_degrees(degrees: astronomy_types.DecimalDegrees) -> astronomy_types.DecimalDegrees:
  return degrees / 15

def degrees_to_hours(degrees: astronomy_types.DecimalDegrees) -> astronomy_types.DecimalDegrees:
  return degrees * 15
  
def right_ascension_to_hour_angle(right_ascension: astronomy_types.RightAscension, local_date_and_time: astronomy_types.FullDate, daylight_savings: int, zone_correction: int, longitude: astronomy_types.Longitude) -> astronomy_types.HourAngle:
  """H = LST - a"""
  utc = time_functions.local_civil_to_universal_time(local_date_and_time, daylight_savings, zone_correction)
  gst = time_functions.universal_to_greenwich_sidereal_time(utc)
  local_sidereal_time = time_functions.greenwich_sidereal_to_local_sidereal_time(gst, longitude)
  lst_dec = utils.time_to_decimal(local_sidereal_time)
  ra_decimal = degrees_to_decimal_degrees(astronomy_types.Degrees(right_ascension))
  hour_angle = lst_dec - ra_decimal

  if hour_angle < 0:
    hour_angle += 24
  
  return astronomy_types.HourAngle(astronomy_types.Time(decimal_degrees_to_degrees(hour_angle)))

def hour_angle_to_right_ascension(hour_angle: astronomy_types.HourAngle, full_date: astronomy_types.FullDate, daylight_savings: int, zone_correction: int, longitude: astronomy_types.Longitude) -> astronomy_types.RightAscension:
  utc = time_functions.local_civil_to_universal_time(full_date,daylight_savings,zone_correction)
  gst = time_functions.universal_to_greenwich_sidereal_time(utc)
  lst = time_functions.greenwich_sidereal_to_local_sidereal_time(gst, longitude)
  lst_dec = degrees_to_decimal_degrees(astronomy_types.Degrees(lst))
  ha_decimal = degrees_to_decimal_degrees(astronomy_types.Degrees(hour_angle))
  right_ascension = lst_dec - ha_decimal

  if right_ascension < 0:
    right_ascension += 24

  return astronomy_types.Time(decimal_degrees_to_degrees(right_ascension))

def equatorial_to_horizon_coordinates(equatorial_coordinates: astronomy_types.EquatorialCoordinatesHourAngle, latitude: astronomy_types.Latitude) -> astronomy_types.HorizontalCoordinates:
  declination, hour_angle = equatorial_coordinates

  if isinstance(latitude, tuple):
        latitude = degrees_to_decimal_degrees(latitude)

  ha_decimal = degrees_to_decimal_degrees(astronomy_types.Degrees(hour_angle))
  ha_degrees =  degrees_to_hours(ha_decimal)
  ha_radians = math.radians(ha_degrees)
  declination_decimal = degrees_to_decimal_degrees(declination)
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
    azimuth_degrees += 360 # TODO: b - (360 * math.floor(b/360))

  altitude = astronomy_types.Altitude(decimal_degrees_to_degrees(altitude_degrees))
  azimuth = astronomy_types.Azimuth(decimal_degrees_to_degrees(azimuth_degrees))

  return astronomy_types.HorizontalCoordinates((altitude, azimuth))

def horizon_to_equatorial_coordinates(horizontal_coordinates: astronomy_types.HorizontalCoordinates, latitude: astronomy_types.Latitude) -> astronomy_types.EquatorialCoordinatesHourAngle:
  altitude, azimuth = horizontal_coordinates

  if isinstance(latitude, tuple):
        latitude = degrees_to_decimal_degrees(latitude)

  azimuth_decimal = degrees_to_decimal_degrees(azimuth)
  altitude_decimal = degrees_to_decimal_degrees(altitude)
  azimuth_radians = math.radians(azimuth_decimal)
  altitude_radians = math.radians(altitude_decimal)
  latitude_radians = math.radians(latitude)

  declination_sin = math.sin(altitude_radians) * math.sin(latitude_radians) + math.cos(altitude_radians) * math.cos(latitude_radians) * math.cos(azimuth_radians)

  declination_radians = math.asin(declination_sin)
  declination_degrees_decimal = math.degrees(declination_radians)
  declination = astronomy_types.Declination(decimal_degrees_to_degrees(declination_degrees_decimal))

  y = -math.cos(altitude_radians) * math.cos(latitude_radians) * math.sin(azimuth_radians)
  x = math.sin(altitude_radians) - math.sin(latitude_radians) * declination_sin
  a = math.atan2(y, x)
  b = math.degrees(a)
  ha_hours = b - (360 * math.floor(b/360))
  ha = hours_to_degrees(ha_hours)

  hour_angle = astronomy_types.HourAngle(astronomy_types.Time(decimal_degrees_to_degrees(ha)))

  return astronomy_types.EquatorialCoordinatesHourAngle((declination, hour_angle))

def mean_obliquity_ecliptic(greenwich_date: astronomy_types.Date) -> astronomy_types.Obliquity:
  julianDate = time_functions.greenwich_to_julian_date(greenwich_date)
  j2000 = time_functions.julian_date_to_j2000(julianDate)
  t = j2000 / 36525
  de = (t * (46.815 + t * (0.0006-(t * 0.00181)))) / 3600
  obliquity = 23.439292 - de

  return obliquity 

def ecliptic_to_equatorial_coordinates(ecliptic_coordinates: astronomy_types.EclipticCoordinates, greenwich_date: astronomy_types.Date) -> astronomy_types.EquatorialCoordinates:
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
  declination_degrees_decimal = math.degrees(declination_rad)
  declination_deg = astronomy_types.Declination(decimal_degrees_to_degrees(declination_degrees_decimal))

  y = math.sin(eclon_rad) * math.cos(obliquity_rad) - math.tan(eclat_rad) * math.sin(obliquity_rad)
  x = math.cos(eclon_rad)
  right_ascension_rad = math.atan2(y,x)
  right_ascension_deg = math.degrees(right_ascension_rad)
  right_ascension_deg_corrected = right_ascension_deg - 360 * math.floor(right_ascension_deg/360)
  right_ascension_degrees =  hours_to_degrees(right_ascension_deg_corrected)

  right_ascension = astronomy_types.Time(decimal_degrees_to_degrees(right_ascension_degrees))

  return astronomy_types.EquatorialCoordinates((declination_deg, right_ascension))

def equatorial_to_ecliptic_coordinates(equatorial_coordinates: astronomy_types.EquatorialCoordinates, greenwich_date: astronomy_types.Date) -> astronomy_types.EclipticCoordinates:
  declination, right_ascension = equatorial_coordinates

  right_ascension_degrees = degrees_to_hours(degrees_to_decimal_degrees(astronomy_types.Degrees(right_ascension))) 
  declination_deg = degrees_to_decimal_degrees(declination)
  right_ascension_rad = math.radians(right_ascension_degrees)
  declination_rad = math.radians(declination_deg)
  obliquity_deg = mean_obliquity_ecliptic(greenwich_date)
  obliquity_rad = math.radians(obliquity_deg)

  ecliptic_lat_sin = math.sin(declination_rad) * math.cos(obliquity_rad) - math.cos(declination_rad) * math.sin(obliquity_rad) * math.sin(right_ascension_rad) # TODO: common pattern can be extracted to a util

  ecliptic_lat_rad = math.asin(ecliptic_lat_sin) - 1.3284561980173026e-05 # this value is needed to correct, cannot be applied globally TODO investigat
  ecliptic_lat_deg = math.degrees(ecliptic_lat_rad)

  y = math.sin(right_ascension_rad) * math.cos(obliquity_rad) + math.tan(declination_rad) * math.sin(obliquity_rad) # TODO: common pattern can be extracted to a util
  x = math.cos(right_ascension_rad)
  ecliptic_long_rad = math.atan2(y, x)
  ecliptic_long_deg = math.degrees(ecliptic_long_rad)
  ecliptic_long_deg_corrected = ecliptic_long_deg - 360 * math.floor(ecliptic_long_deg / 360) # TODO

  latitude = decimal_degrees_to_degrees(ecliptic_lat_deg)
  longitude = decimal_degrees_to_degrees(ecliptic_long_deg_corrected)

  return astronomy_types.EclipticCoordinates((latitude, longitude))

def equatorial_to_galactic_coordinates(equatorial_coordinates: astronomy_types.EquatorialCoordinates) -> astronomy_types.GalacticCoordinates:
  dec, ra = equatorial_coordinates

  dec_decimal = degrees_to_decimal_degrees(dec)
  ra_decimal = degrees_to_hours(degrees_to_decimal_degrees(astronomy_types.Degrees(ra)))
  dec_rad = math.radians(dec_decimal)
  ra_rad = math.radians(ra_decimal)
  b = math.cos(dec_rad) * math.cos(math.radians(27.4)) * math.cos(ra_rad - math.radians(192.25)) + math.sin(dec_rad) * math.sin(math.radians(27.4))
  b_rad = math.asin(b)
  b_deg = math.degrees(b_rad)

  y = math.sin(dec_rad) - b * math.sin(math.radians(27.4))
  x = math.cos(dec_rad) * math.sin(ra_rad - math.radians(192.25)) * math.cos(math.radians(27.4))
  longitude = math.degrees(math.atan2(y,x)) + 33
  longitude_corrected = longitude - 360 * math.floor(longitude/360) # TODO: b - (360 * math.floor(b/360))

  latitude = decimal_degrees_to_degrees(b_deg)
  longitude = decimal_degrees_to_degrees(longitude_corrected)

  return astronomy_types.GalacticCoordinates((latitude, longitude))

def galactic_to_equatorial_coordinates(galactic_coordinates: astronomy_types.GalacticCoordinates) -> astronomy_types.EquatorialCoordinates:
  lat, lon = galactic_coordinates

  if isinstance(lat, tuple):
    lat_dec = degrees_to_decimal_degrees(lat)
  else:
    lat_dec = lat
  if isinstance(lon, tuple):
    lon_dec = degrees_to_decimal_degrees(lon)
  else:
    lon_dec = lon

  lat_rad = math.radians(lat_dec)
  lon_rad = math.radians(lon_dec)

  sin_dec = math.cos(lat_rad) * math.cos(math.radians(27.4)) * math.sin(lon_rad - math.radians(33)) + math.sin(lat_rad) * math.sin(math.radians(27.4))
  declination = math.asin(sin_dec)
  declination_degrees_decimal = math.degrees(declination)
  declination_degrees = astronomy_types.Declination(decimal_degrees_to_degrees(declination_degrees_decimal))

  y = math.cos(lat_rad) * math.cos(lon_rad - math.radians(33))
  x = math.sin(lat_rad) * math.cos(math.radians(27.4)) - math.cos(lat_rad) * math.sin(math.radians(27.4)) * math.sin(lon_rad - math.radians(33))
  right_ascension = math.degrees(math.atan2(y,x)) + 192.25
  right_ascension_corrected = right_ascension - 360 * math.floor(right_ascension/360)
  right_ascension_hours = decimal_degrees_to_degrees(hours_to_degrees(right_ascension_corrected))
  right_ascension = astronomy_types.Time(right_ascension_hours)

  return astronomy_types.EquatorialCoordinates((declination_degrees, right_ascension))


# if __name__ == '__main__':
#     ra = astronomy_types.Time((18,37,47.5))
#     ha = right_ascension_to_hour_angle(ra,astronomy_types.FullDate((astronomy_types.Date((2024,8,7)),astronomy_types.Time((22,10,00)))),1,1,11.40911)
#     al, az = equatorial_to_horizon_coordinates(astronomy_types.EquatorialCoordinatesHourAngle((astronomy_types.Declination(astronomy_types.Degrees((38,48,30.6))), ha)), 48.13979 )
      
#     print(al, az)