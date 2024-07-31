import unittest
import time_functions

class TimeTestMethods(unittest.TestCase):

  def test_date_of_easter(self):
    msg = 'test_date_of_easter fail'

    self.assertEqual(time_functions.date_of_easter(2009), (12,4,2009), msg)
    self.assertEqual(time_functions.date_of_easter(2010), (4,4,2010), msg)
    self.assertEqual(time_functions.date_of_easter(2024), (31,3,2024), msg)

  def test_date_to_day_number(self):
    msg = 'test_date_to_day_number fail'

    self.assertEqual(time_functions.date_to_day_number(1,1,2000), 1, msg)
    self.assertEqual(time_functions.date_to_day_number(12,31,2000), 366, msg)
    self.assertEqual(time_functions.date_to_day_number(12,31), 365, msg)

  def test_greenwich_date_to_julian_date(self):
    msg = 'test_greenwich_date_to_julian_date fail'

    self.assertEqual(time_functions.greenwich_date_to_julian_date(2009,6,19.75), 2455002.25, msg)
    self.assertEqual(time_functions.greenwich_date_to_julian_date(1969,1,5), 2440226.5, msg)

  def test_julian_date_to_j2000(self):
    msg = 'test_julian_date_to_j2000'

    self.assertEqual(time_functions.julian_date_to_j2000(2440227.54513888889), -11317.454861111008, msg)

  def test_julian_date_to_greenwich_date(self):
    msg = 'test_julian_date_to_greenwich_date fail'

    self.assertEqual(time_functions.julian_date_to_greenwich_date(2455002.25), (2009, 6, 19.75), msg)

  def test_finding_day_of_week(self):
    msg = 'test_finding_day_of_week fail'

    self.assertEqual(time_functions.finding_day_of_week(2455001.5), "Friday", msg)
    self.assertEqual(time_functions.finding_day_of_week(time_functions.greenwich_date_to_julian_date(2024,4,7)), "Sunday", msg)

  def test_hours_minute_seconds_to_decimal_time(self):
    msg = 'test_hours_minute_seconds_to_decimal_time fail'

    self.assertEqual(time_functions.hours_minute_seconds_to_decimal_time(18,31,27), 18.524166666666666, msg)
    self.assertEqual(time_functions.hours_minute_seconds_to_decimal_time(18,31,27,False), 6.524166666666666, msg)
    self.assertEqual(time_functions.hours_minute_seconds_to_decimal_time(11,31,5,False), 11.518055555555556, msg)
    self.assertEqual(time_functions.hours_minute_seconds_to_decimal_time(12,00,00,False), 12, msg)
    self.assertEqual(time_functions.hours_minute_seconds_to_decimal_time(12,00,00), 12, msg)

  def test_decimal_hours_to_hours_minutes_seconds(self):
    msg = 'test_decimal_hours_to_hours_minutes_seconds fail'

    self.assertEqual(time_functions.decimal_hours_to_hours_minutes_seconds(18.52416667), (18, 31, 27), msg)

  def test_local_civil_time_to_universal_time(self):
    msg = 'test_local_civil_time_to_universal_time fail'

    self.assertEqual(time_functions.local_civil_time_to_universal_time(2013,7,1,3,37,5,1,4), (2013, 6, 30, 22, 37, 5.0), msg)

  def test_universal_time_to_local_civil_time(self):
    msg = 'test_universal_time_to_local_civil_time fail'

    self.assertEqual(time_functions.universal_time_to_local_civil_time(22,37,0,2013,6,30,4,1), (2013, 7, 1, 3, 37, 0), msg)

  def test_universal_time_to_greenwich_sidereal_time(self):
    msg = 'test_universal_time_to_greenwich_sidereal_time fail'

    self.assertEqual(time_functions.universal_time_to_greenwich_sidereal_time(1980,4,22,14,36,51.67), (4, 40, 5.23), msg)

  def test_greenwich_sidereal_time_to_universal_time(self):
    msg = 'test_greenwich_sidereal_time_to_universal_time fail'

    self.assertEqual(time_functions.greenwich_sidereal_time_to_universal_time(4,40,5.23,1980,4,22), (1980, 4, 22, 14, 36, 51.67), msg)

  def test_greenwich_sidereal_time_to_local_sidereal_time(self):
    msg = 'test_greenwich_sidereal_time_to_local_sidereal_time fail'

    self.assertEqual(time_functions.greenwich_sidereal_time_to_local_sidereal_time(4,40,5.23,-64), (0, 24, 5.23), msg)

  def test_local_sidereal_time_to_greenwich_sidereal_time(self):
    msg = 'test_local_sidereal_time_to_greenwich_sidereal_time fail'

    self.assertEqual(time_functions.local_sidereal_time_to_greenwich_sidereal_time(0,24,5.23,-64), (4, 40, 5.23), msg)

  def test_year_is_leap(self):
    msg = 'test_year_is_leap fail'

    self.assertEqual(time_functions.year_is_leap(1600), True, msg)
    self.assertEqual(time_functions.year_is_leap(1900), False, msg)
    self.assertEqual(time_functions.year_is_leap(1992), True, msg)
    self.assertEqual(time_functions.year_is_leap(2000), True, msg)
    self.assertEqual(time_functions.year_is_leap(2023), False, msg)
    self.assertEqual(time_functions.year_is_leap(2024), True, msg)
    self.assertEqual(time_functions.year_is_leap(2048), True, msg)


if __name__ == '__main__':
    unittest.main()