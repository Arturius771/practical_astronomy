import math

def date_of_easter(year: int) -> tuple:
  a = year % 19
  b = math.floor(year / 100)
  c = year % 100
  d = math.floor(b / 4)
  e = b % 4
  f = math.floor((b + 8) / 25)
  g = math.floor((b - f - 1) / 3)
  h = ((19 * a) + b - d - g + 15) % 30
  i = math.floor(c / 4)
  k = c % 4
  l = (32 + (2 * e) + (2 * i) - h - k) % 7
  m = math.floor((a + (11 * h) + (22 * l)) / 451)
  n = math.floor((h + l - (7 * m) + 114) / 31)
  p = (h + l - (7 * m) + 114) % 31
  day = p + 1
  month = n

  return (day, month, year)

def date_to_day_number(month: int, day: int, leap_year: bool) -> int:
  if month > 2:
    j = math.floor((month + 1) * 30.6)
    if (leap_year):
      k = j - 62
    else:
      k = j - 63
    return k + day
  else:
    if (leap_year):
      d = (month - 1) * 62
    else:
      d = (month - 1) * 63
    f = math.floor(d / 2)
    return f + day
    

