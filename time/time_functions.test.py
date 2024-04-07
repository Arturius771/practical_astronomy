import unittest
import time_functions

class TestDateMethods(unittest.TestCase):

  def test_date_of_easter(self):
    msg = 'test_date_of_easter fail'
    self.assertEqual(time_functions.date_of_easter(2009), (12,4,2009), msg)

    self.assertEqual(time_functions.date_of_easter(2010), (4,4,2010), msg)

    self.assertEqual(time_functions.date_of_easter(2024), (31,3,2024), msg)

  def test_date_to_day_number(self):
    msg = 'test_date_to_day_number fail'

    self.assertEqual(time_functions.date_to_day_number(1,1,True), 1, msg)

    self.assertEqual(time_functions.date_to_day_number(12,31,True), 366, msg)

    self.assertEqual(time_functions.date_to_day_number(12,31,False), 365, msg)

  def test_greenwich_date_to_julian_date(self):
    msg = 'test_greenwich_date_to_julian_date fail'

    self.assertEqual(time_functions.greenwich_date_to_julian_date(2009,6,19.75), 2455002.25, msg)

  def test_julian_date_to_greenwich_date(self):
    msg = 'test_julian_date_to_greenwich_date fail'

    self.assertEqual(time_functions.julian_date_to_greenwich_date(2455002.25), (2009, 6, 19.75), msg)

  def test_finding_day_of_week(self):
    msg = 'test_finding_day_of_week fail'

    self.assertEqual(time_functions.finding_day_of_week(2009,6,19), "Friday", msg)
    self.assertEqual(time_functions.finding_day_of_week(2024,4,7), "Sunday", msg)

  def test_convert_hours_minute_seconds_to_decimal_time(self):
    msg = 'test_convert_hours_minute_seconds_to_decimal_time fail'

    self.assertEqual(time_functions.convert_hours_minute_seconds_to_decimal_time(18,31,27), 18.524166666666666, msg)

  def test_convert_decimal_hours_to_hours_minutes_seconds(self):
    msg = 'test_convert_decimal_hours_to_hours_minutes_seconds fail'

    self.assertEqual(time_functions.convert_decimal_hours_to_hours_minutes_seconds(18.52416667), (18, 31, 27.0), msg)


if __name__ == '__main__':
    unittest.main()