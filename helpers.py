# This should eventually be added to afmaths and reimported

import math

# def degrees_to_radians(degrees):
#     return degrees * (math.pi / 180) or math.radians(degrees)

# def radians_to_degrees(radians):
#     return radians * (180 / math.pi) or math.degrees(radians)


def convert_hours_minute_seconds_to_decimal(hours: int, minutes: int, seconds: int) -> float:
  a = seconds / 60
  b = (a + minutes) / 60
  c = b + hours

  return c

def convert_decimal_to_hours_minutes_seconds(decimalTime: float) -> tuple:
  a = abs(decimalTime)
  b = a * 3600
  c = round((b % 60), 2)
  seconds = 0 if c == 60 else c
  e = b + 60 if c == 60 else b
  minutes = math.floor((e) / 60) % 60
  unsigned_hours = math.floor(e / 3600)

  return (unsigned_hours, minutes, seconds)