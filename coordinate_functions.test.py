import unittest
import astronomy_types as astronomy_types
import coordinate_functions


class CoordinateTestMethods(unittest.TestCase):

  def test_decimal_degrees_to_degrees_minutes_seconds(self):
    msg = 'test_decimal_degrees_to_degrees_minutes_seconds fail'

    self.assertEqual(coordinate_functions.decimal_degrees_to_degrees(182.52416666666667), (182,31,27), msg)

  def test_degrees_minutes_seconds_to_decimal_degrees(self):
    msg = 'test_decimal_degrees_to_degrees_minutes_seconds fail'

    degrees = astronomy_types.Degrees((182,31,27))

    self.assertEqual(coordinate_functions.degrees_to_decimal_degrees(degrees), (182.52416666666667), msg)

  def test_right_ascension_to_hour_angle(self):
    msg = 'test_right_ascension_to_hour_angle fail'

    full_date = astronomy_types.FullDate((astronomy_types.Date((1980,4,22)),astronomy_types.Time((14,36,51.67))))

    self.assertEqual(coordinate_functions.right_ascension_to_hour_angle(astronomy_types.Time((18,32,21)),full_date,0,-4,-64), (9, 52, 23.66), msg)

  def test_hour_angle_to_right_ascension(self):
    msg = 'test_hour_angle_to_right_ascension fail'

    full_date = astronomy_types.FullDate((astronomy_types.Date((1980,4,22,)),astronomy_types.Time((14,36,51.67))))

    self.assertEqual(coordinate_functions.hour_angle_to_right_ascension(astronomy_types.HourAngle(astronomy_types.Time((9,52,23.66))),full_date,0,-4,-64), (18, 32, 21.0), msg)

  def test_equatorial_to_horizon_coordinates(self):
    msg = 'test_equatorial_to_horizon_coordinates fail'
    
    coordinates = astronomy_types.EquatorialCoordinatesHourAngle((astronomy_types.Declination(astronomy_types.Degrees((23,13,10))),astronomy_types.HourAngle(astronomy_types.Time((5,51,44)))))

    self.assertEqual(coordinate_functions.equatorial_to_horizon_coordinates(coordinates,52), ((19,20,3.64), (283,16,15.7)), msg)

  def test_horizon_to_equatorial_coordinates(self):
    msg = 'test_horizon_to_equatorial_coordinates fail'

    coordinates = astronomy_types.HorizontalCoordinates((astronomy_types.Altitude(astronomy_types.Degrees((19,20,3.64))), astronomy_types.Azimuth(astronomy_types.Degrees((283,16,15.76)))))

    self.assertEqual(coordinate_functions.horizon_to_equatorial_coordinates(coordinates,52), ((23,13,10.04), (5,51,44.0)), msg)

  def test_mean_obliquity_ecliptic(self):
    msg = 'test_mean_obliquity_ecliptic fail'

    self.assertEqual(coordinate_functions.mean_obliquity_ecliptic(astronomy_types.Date((2009, 7, 6))), 23.438055312466062, msg)

  def test_ecliptic_to_equatorial_coordinates(self):
    msg = 'test_ecliptic_to_equatorial_coordinates fail'

    coordinates = astronomy_types.EclipticCoordinates((astronomy_types.Degrees((4,52,31)), astronomy_types.Degrees((139,41,10))))
    date = astronomy_types.Date((2009,7,6))

    self.assertEqual(coordinate_functions.ecliptic_to_equatorial_coordinates(coordinates,date), ((19,32,8.52), (9,34,53.4)), msg)

  def test_equatorial_to_ecliptic_coordinates(self):
    msg = 'test_equatorial_to_ecliptic_coordinates fail'

    coordinates = astronomy_types.EquatorialCoordinates((astronomy_types.Declination(astronomy_types.Degrees((19,32,8.52))), astronomy_types.Time((9,34,53.4))))

    self.assertEqual(coordinate_functions.equatorial_to_ecliptic_coordinates(coordinates,astronomy_types.Date((2009,7,6))), ((4,52,30.99), (139,41,10.25)), msg)

  def test_equatorial_to_galactic_coordinates(self):
    msg = 'test_equatorial_to_galactic_coordinates fail'

    coordinates = astronomy_types.EquatorialCoordinates((astronomy_types.Declination(astronomy_types.Degrees((10,3,11))), astronomy_types.Time((10,21,0))))

    self.assertEqual(coordinate_functions.equatorial_to_galactic_coordinates(coordinates), ((51,7,20.16), (232,14,52.38)), msg)

  def test_galactic_to_equatorial_coordinates(self):
    msg = 'test_galactic_to_equatorial_coordinates fail'

    coordinates = astronomy_types.GalacticCoordinates((astronomy_types.Degrees((51,7,20.16)), astronomy_types.Degrees((232, 14, 52.38))))

    self.assertEqual(coordinate_functions.galactic_to_equatorial_coordinates(coordinates), ((10,3,11.0), (10,21,0)), msg)



if __name__ == '__main__':
    unittest.main()