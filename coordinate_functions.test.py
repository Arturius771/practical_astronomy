import unittest
import coordinate_functions


class CoordinateTestMethods(unittest.TestCase):

  def test_convert_decimal_degrees_to_degrees_minutes_seconds(self):
    msg = 'test_convert_decimal_degrees_to_degrees_minutes_seconds fail'

    self.assertEqual(coordinate_functions.convert_decimal_degrees_to_degrees_minutes_seconds(182.52416666666667), (182,31,27), msg)

  def test_convert_degrees_minutes_seconds_to_decimal_degrees(self):
    msg = 'test_convert_decimal_degrees_to_degrees_minutes_seconds fail'

    self.assertEqual(coordinate_functions.convert_degrees_minutes_seconds_to_decimal_degrees(182,31,27), (182.52416666666667), msg)

  def test_convert_right_ascension_to_hour_angle(self):
    msg = 'test_convert_right_ascension_to_hour_angle fail'

    self.assertEqual(coordinate_functions.convert_right_ascension_to_hour_angle(18,32,21,14,36,51.67,0,-4,22,4,1980,-64), (9, 52, 23.66), msg)

  def test_convert_hour_angle_to_right_ascension(self):
    msg = 'test_convert_hour_angle_to_right_ascension fail'

    self.assertEqual(coordinate_functions.convert_hour_angle_to_right_ascension(9,52,23.66,14,36,51.67,0,-4,22,4,1980,-64), (18, 32, 21.0), msg)

if __name__ == '__main__':
    unittest.main()