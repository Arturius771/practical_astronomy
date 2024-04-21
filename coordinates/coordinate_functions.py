import math

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
  print(corrected)
  corrected_remainder = total_seconds + 60 if total_seconds_rounded == 60 else total_seconds
  minutes = math.floor(corrected_remainder / 60) % 60
  unsigned_degrees = math.floor(corrected_remainder / 3600)
  signed_degrees = -1 * unsigned_degrees if decimal_degree < 0 else unsigned_degrees
  
  return (signed_degrees, minutes, math.floor(corrected))
  

