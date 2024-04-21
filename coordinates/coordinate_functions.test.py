import unittest
import coordinate_functions


class CoordinateTestMethods(unittest.TestCase):

  def test_convert_decimal_degrees_to_degrees_minutes_seconds(self):
    msg = 'test_convert_decimal_degrees_to_degrees_minutes_seconds fail'

    self.assertEqual(coordinate_functions.convert_decimal_degrees_to_degrees_minutes_seconds(182.52416666666667), (182,31,27), msg)

  def test_convert_degrees_minutes_seconds_to_decimal_degrees(self):
    msg = 'test_convert_decimal_degrees_to_degrees_minutes_seconds fail'

    self.assertEqual(coordinate_functions.convert_degrees_minutes_seconds_to_decimal_degrees(182,31,27), (182.52416666666667), msg)

if __name__ == '__main__':
    unittest.main()