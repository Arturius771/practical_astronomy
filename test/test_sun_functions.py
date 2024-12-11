import unittest
from af_practical_astronomy import sun_functions
from astronomy_types import FullDate, Date, Time


class SunTestMethods(unittest.TestCase):

    def test_sun_position_approximate(self):
        msg = 'test_sun_position_approximate fail'

        local_date = FullDate((Date((2003,7,27)),Time((0,0,0))))

        self.assertEqual(sun_functions.sun_position_approximate(local_date,0,0), ((19,21,13.81), (8,23,33.72)), msg)