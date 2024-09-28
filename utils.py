# This should eventually be added to afmaths and reimported

import math
import astronomy_types as at

# def degrees_to_radians(degrees):
#     return degrees * (math.pi / 180) or math.radians(degrees)

# def radians_to_degrees(radians):
#     return radians * (180 / math.pi) or math.degrees(radians)


def time_to_decimal(time: at.Time) -> DecimalTime:
  hours, minutes, seconds = time
  a = seconds / 60
  b = (a + minutes) / 60
  unsigned_decimal = b + hours

  return unsigned_decimal

def decimal_to_time(decimal_value: DecimalTime) -> at.Time:
  unsigned_decimal = abs(decimal_value)
  total_seconds = unsigned_decimal * 3600
  total_seconds_rounded = round((total_seconds % 60), 2)
  seconds = 0 if total_seconds_rounded == 60 else total_seconds_rounded
  remainder = total_seconds + 60 if total_seconds_rounded == 60 else total_seconds
  minutes = math.floor((remainder) / 60) % 60
  unsigned_value = math.floor(remainder / 3600)

  return at.Time((unsigned_value, minutes, seconds))
