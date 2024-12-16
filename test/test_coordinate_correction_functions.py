import unittest
from af_practical_astronomy import coordinate_correction_functions
from astronomy_types import FullDate, Date, Time, Degrees, EquatorialCoordinates, RightAscension, EclipticCoordinates, Declination, GeographicCoordinates


class CoordinateCorrectionTestMethods(unittest.TestCase):
    
  def test_angle_difference(self): 
    msg = "test_angle_difference fail"

    coordinates1 = EquatorialCoordinates((Declination(Degrees((-8,13,30))), RightAscension(Time((5,13,31.7))))) 
    coordinates2 = EquatorialCoordinates((Declination(Degrees((-16,41,11))), RightAscension(Time((6,44,13.4)))))

    self.assertEqual(coordinate_correction_functions.angle_difference(coordinates1, coordinates2), ((23, 40, 25.86)), msg)

  def test_rising_and_setting(self): 
    msg = "test_rising_and_setting fail"

    coordinates = EquatorialCoordinates((Declination(Degrees((21,42,0))), RightAscension(Time((23,39,20))))) 
    location = GeographicCoordinates((30, 64))
    greenwich_date = Date((2010, 8, 24))

    self.assertEqual(coordinate_correction_functions.rising_and_setting(coordinates, location, greenwich_date, 0.5667), ((True, (14, 16, 18.018333000000002), (4, 10, 1.1783329999999999), 64.3623480385112, 295.6376519614888)), msg)

  def test_precession_low_precision(self): 
    msg = "test_precession_low_precision fail"

    coordinates = EquatorialCoordinates((Declination(Degrees((14,23,25))), RightAscension(Time((9,10,43))))) 
    original_epoch = 2433282.423
    new_epoch = 2444025.5

    self.assertEqual(coordinate_correction_functions.precession_low_precision(coordinates, original_epoch, new_epoch), ((14, 16, 9.12), (9, 12, 20.18)), msg)

  def test_nutation_from_date(self): 
    msg = "test_nutation_from_date fail"

    self.assertEqual(coordinate_correction_functions.nutation_from_date(Date((1988,9,1))), (0.0015258083552917808, 0.0025671004471993584), msg)

  def test_abberation_from_date(self): 
    msg = "test_abberation_from_date fail"

    full_date = FullDate((Date((1988,9,8)),Time((0,0,0))))    
    coordinates = EclipticCoordinates((Degrees((-1,32,56.4)), Degrees((352,37,10.1))))

    self.assertEqual(coordinate_correction_functions.aberration_from_date(full_date, coordinates), ((-1,32,56.33), (352,37,30.45)), msg)