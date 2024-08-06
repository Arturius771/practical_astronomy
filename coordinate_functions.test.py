import unittest
from astronomy_types import *
import coordinate_functions


class CoordinateTestMethods(unittest.TestCase):

  def test_decimal_degrees_to_degrees_minutes_seconds(self):
    msg = 'test_decimal_degrees_to_degrees_minutes_seconds fail'

    self.assertEqual(coordinate_functions.decimal_degrees_to_degrees(182.52416666666667), (182,31,27), msg)

  def test_degrees_minutes_seconds_to_decimal_degrees(self):
    msg = 'test_decimal_degrees_to_degrees_minutes_seconds fail'

    degrees = Degrees((182,31,27))

    self.assertEqual(coordinate_functions.degrees_to_decimal_degrees(degrees), (182.52416666666667), msg)

  def test_right_ascension_to_hour_angle(self):
    msg = 'test_right_ascension_to_hour_angle fail'

    ra = Degrees((18,32,21))
    full_date = FullDate((Date((1980,4,22)),Time((14,36,51.67))))

    self.assertEqual(coordinate_functions.right_ascension_to_hour_angle(ra,full_date,0,-4,-64), (9, 52, 23.66), msg)

  def test_hour_angle_to_right_ascension(self):
    msg = 'test_hour_angle_to_right_ascension fail'

    ha = Degrees((9,52,23.66))
    full_date = FullDate((Date((1980,4,22,)),Time((14,36,51.67))))

    self.assertEqual(coordinate_functions.hour_angle_to_right_ascension(ha,full_date,0,-4,-64), (18, 32, 21.0), msg)

  def test_equatorial_to_horizon_coordinates(self):
    msg = 'test_equatorial_to_horizon_coordinates fail'
    
    coordinates = EquatorialCoordinates((Degrees((5,51,44)),Degrees((23,13,10))))

    self.assertEqual(coordinate_functions.equatorial_to_horizon_coordinates(coordinates,52), ((283,16,15.7),(19,20,3.64)), msg)

  def test_horizon_to_equatorial_coordinates(self):
    msg = 'test_horizon_to_equatorial_coordinates fail'

    coordinates = HorizontalCoordinates((Degrees((19,20,3.64)), Degrees((283,16,15.76))))

    self.assertEqual(coordinate_functions.horizon_to_equatorial_coordinates(coordinates,52), (5,51,44.0,23,13,10.04), msg)

  def test_mean_obliquity_ecliptic(self):
    msg = 'test_mean_obliquity_ecliptic fail'

    self.assertEqual(coordinate_functions.mean_obliquity_ecliptic(Date((2009, 7, 6))), 23.438055312466062, msg)

  def test_ecliptic_to_equatorial_coordinates(self):
    msg = 'test_ecliptic_to_equatorial_coordinates fail'

    coordinates = EclipticCoordinates((Degrees((4,52,31)), Degrees((139,41,10))))
    date = Date((2009,7,6))

    self.assertEqual(coordinate_functions.ecliptic_to_equatorial_coordinates(coordinates,date), ((9,34,53.4),(19,32,8.52)), msg)

  def test_equatorial_to_ecliptic_coordinates(self):
    msg = 'test_equatorial_to_ecliptic_coordinates fail'

    date = Date((2009,7,6))
    coordinates = EquatorialCoordinates((Degrees((9,34,53.4)), Degrees((19,32,8.52))))

    self.assertEqual(coordinate_functions.equatorial_to_ecliptic_coordinates(coordinates,date), ((139,41,10.25),(4,52,30.99)), msg)

if __name__ == '__main__':
    unittest.main()