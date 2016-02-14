"""
    SSW 555
    2016 Spring
    Team 4
"""

import unittest
from gedcom.gedcomline import GEDCOMLine

class GEDCOMLineTest(unittest.TestCase):

    def test_level(self):
        line = GEDCOMLine('0 @I2@ INDI')
        self.assertEqual(line.level, 0)

    def test_tag(self):
        normal_line = GEDCOMLine('2 DATE 12 MAR 1936')
        id_line = GEDCOMLine('0 @I2@ INDI')

        self.assertEqual(normal_line.tag, 'DATE')
        self.assertEqual(id_line.tag, 'INDI')

    def test_payload(self):
        normal_line = GEDCOMLine('2 DATE 12 MAR 1936')
        id_line = GEDCOMLine('0 @I2@ INDI')

        self.assertEqual(normal_line.payload, '12 MAR 1936')
        self.assertEqual(id_line.payload, '@I2@')

    def test_has_valid_tag(self):
        normal_line = GEDCOMLine('2 DATE 12 MAR 1936')
        id_line = GEDCOMLine('0 @I2@ INDI')
        bad_normal_line = GEDCOMLine('2 NOPE 12 MAR 1936')
        bad_id_line = GEDCOMLine('0 @I2@ NOPE')

        self.assertTrue(normal_line.has_valid_tag)
        self.assertTrue(id_line.has_valid_tag)
        self.assertFalse(bad_normal_line.has_valid_tag)
        self.assertFalse(bad_id_line.has_valid_tag)

if __name__ == '__main__':
    unittest.main()
