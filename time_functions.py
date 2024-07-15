import math
import helpers

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

def date_to_day_number(month: int, day: int, year = 1900) -> int:
  if month > 2:
    j = math.floor((month + 1) * 30.6)

    if (year_is_leap(year)):
      k = j - 62
    else:
      k = j - 63

    return k + day
  
  else:
    if (year_is_leap(year)):
      d = (month - 1) * 62
    else:
      d = (month - 1) * 63
    f = math.floor(d / 2)

    return f + day    
  
def year_is_leap(year: int) -> bool:
  if(((year % 4 == 0) and (year % 100 == 0) and (year % 400 == 0)) or ((year % 4 == 0) and (year % 100 != 0))):
    return True
    
  return False

  

def greenwich_date_to_julian_date(year: int, month: int, day: float | int) -> float:
  if month == 1 or month == 2:
    y = year -1
    m = month + 12
  else:
    y = year
    m = month

  if year > 1582 or year == 1582 and month > 10 or year == 1582 and month == 10 and day > 15:
    a = math.floor(y / 100)
    b = 2 - a + math.floor(a / 4)
  else:
    b = 0
  
  if y < 0:
    c = math.floor((365.25 * y) - 0.75)
  else:
    c = math.floor(365.25 * y)

  d = math.floor(30.6001 * (m + 1))

  jd = b + c + d + day + 1720994.5

  return jd

def julian_date_to_greenwich_date(julianDate: float) -> tuple:
  
  jd = julianDate + 0.5
  i = math.floor(jd)
  f = jd - i
  
  if i > 2299160:
    a = math.floor((i - 1867216.25) / 36524.25)
    b = i + a - math.floor(a / 4) + 1
  else:
    b = 1

  c = b + 1524
  d = math.floor((c - 122.1) / 365.25)
  e = math.floor(365.25 * d)
  g = math.floor((c - e) / 30.6001)

  day = c - e + f - math.floor(30.6001 * g)

  month = g - 1 if g < 13.5 else g - 13

  year = d - 4716 if month > 2.5 else d - 4715

  return (year, month, day)

def finding_day_of_week(julianDate: float) -> str:
  a = (julianDate + 1.5) % 7

  if a < 1: return "Sunday"
  if a < 2: return "Monday"
  if a < 3: return "Tuesday"
  if a < 4: return "Wednesday"
  if a < 5: return "Thursday"
  if a < 6: return "Friday"
  if a < 7: return "Saturday"

def convert_hours_minute_seconds_to_decimal_time(hours: int, minutes: int, seconds: int, twenty_four_hour_clock = True) -> float:
  c = helpers.convert_hours_minute_seconds_to_decimal(hours, minutes, seconds)

  return c if twenty_four_hour_clock else c + 12

def convert_decimal_hours_to_hours_minutes_seconds(decimalTime: float) -> tuple:
  hms = helpers.convert_decimal_to_hours_minutes_seconds(decimalTime)
  hours = hms[0] * -1 if decimalTime < 0 else hms[0]

  return (hours, hms[1], hms[2])

def convert_local_civil_time_to_universal_time(local_year: int, local_month: int, local_day: int, local_hours: int, local_minutes: int, local_seconds: float, daylight_savings_correction = 0, timezone_offset_correction = 0) -> tuple:

  zone_time = local_hours - daylight_savings_correction
  decimal_zone_time = convert_hours_minute_seconds_to_decimal_time(zone_time, local_minutes, local_seconds)
  ut = decimal_zone_time - timezone_offset_correction
  greenwich_calendar_day = local_day + (ut / 24)
  jd = greenwich_date_to_julian_date(local_year, local_month, greenwich_calendar_day)
  greenwich_year, greenwich_month, greenwich_day = julian_date_to_greenwich_date(jd)
  utc = convert_decimal_hours_to_hours_minutes_seconds(24 * (greenwich_calendar_day - math.floor(greenwich_calendar_day)))

  return (greenwich_year, greenwich_month, math.floor(greenwich_day)) + utc

def convert_universal_time_to_local_civil_time(ut_hours: int, ut_minutes: int, ut_seconds: int, greenwich_year: int, greenwich_month: int, greenwich_day: int, timezone_offset_correction = 0, daylight_savings_correction = 0) -> tuple:
  decimalHours = convert_hours_minute_seconds_to_decimal_time(ut_hours, ut_minutes, ut_seconds)
  lct = decimalHours + timezone_offset_correction + daylight_savings_correction
  jd = greenwich_date_to_julian_date(greenwich_year,greenwich_month,greenwich_day)
  ljd = jd + (lct / 24)
  local_civil_year, local_civil_month, local_civil_day = julian_date_to_greenwich_date(ljd)
  integer_day = math.floor(local_civil_day)
  local_date = (local_civil_year, local_civil_month, integer_day)
  lct = convert_decimal_hours_to_hours_minutes_seconds((local_civil_day - integer_day) * 24)
  
  return local_date + (lct)

def convert_universal_time_to_greenwich_sidereal_time(greenWich_year: int, greenwich_month: int, greenwich_day: int, ut_hours: int, ut_minutes: int, ut_seconds: float) -> tuple:
  julianDate = greenwich_date_to_julian_date(greenWich_year,greenwich_month,greenwich_day) 
  s = julianDate - 2451545.0
  t = s / 36525.0
  t0 = 6.697374558+(2400.051336*t)+(0.000025862*t**2)
  t1 = t0 - (24 * math.floor(t0 / 24))
  ut = convert_hours_minute_seconds_to_decimal_time(ut_hours,ut_minutes,ut_seconds)
  a = ut * 1.002737909
  gst0 = a + t1
  gst = gst0 - (24 * math.floor(gst0 / 24))

  return convert_decimal_hours_to_hours_minutes_seconds(gst)

def convert_greenwich_sidereal_time_to_universal_time(gst_hours: int, gst_minutes: int, gst_seconds: float, greenWich_year: int, greenwich_month: int, greenwich_day: int) -> tuple:
  julianDate = greenwich_date_to_julian_date(greenWich_year,greenwich_month,greenwich_day) 
  s = julianDate - 2451545.0
  t = s / 36525.0
  t0 = 6.697374558+(2400.051336*t)+(0.000025862*t**2)
  t1 = t0 - (24 * math.floor(t0 / 24))
  gst_decimal = convert_hours_minute_seconds_to_decimal_time(gst_hours,gst_minutes,gst_seconds)
  a = gst_decimal - t1
  b = a - (24 * math.floor(a / 24))
  ut = b * 0.9972695663
  utc = convert_decimal_hours_to_hours_minutes_seconds(ut)

  return (greenWich_year, greenwich_month, greenwich_day) + utc

def convert_greenwich_sidereal_time_to_local_sidereal_time(gst_hours: int, gst_minutes: int, gst_seconds: float, longitude: int) -> tuple:
  gst_decimal = convert_hours_minute_seconds_to_decimal_time(gst_hours,gst_minutes,gst_seconds)
  offset = longitude / 15
  lst = gst_decimal + offset
  lst1 = lst - (24 * math.floor(lst / 24))
  non_decimal_lst = convert_decimal_hours_to_hours_minutes_seconds(lst1)

  return non_decimal_lst

def convert_local_sidereal_time_to_greenwich_sidereal_time(lst_hours: int, lst_minutes: int, lst_seconds: float, longitude: int) -> tuple:
  lst_decimal = convert_hours_minute_seconds_to_decimal_time(lst_hours,lst_minutes,lst_seconds)
  offset = longitude / 15
  gst = lst_decimal - offset
  gst1 = gst - (24 * math.floor(gst / 24))
  non_decimal_lst = convert_decimal_hours_to_hours_minutes_seconds(gst1)

  return non_decimal_lst
