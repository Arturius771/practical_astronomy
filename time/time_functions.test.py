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


if __name__ == '__main__':
    unittest.main()