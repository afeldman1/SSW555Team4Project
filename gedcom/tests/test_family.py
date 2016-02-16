"""
    SSW 555
    2016 Spring
    Team 4
"""

import unittest
from gedcom.family import Family

class GEDEntitiesTest(unittest.TestCase):

    def test_Family(self):
        entity = Family(uid = '@F01@',
                        husband = 'Mr.',
                        wife = 'Mrs.',
                        marriage_date = '20 OCT 1983',
                        divorce_date = None)

        entity.add_child('Kid1')
        entity.add_child('Kid2')

        self.assertEqual(entity.uid, '@F01@')
        self.assertEqual(entity.husband, 'Mr.')
        self.assertEqual(entity.wife, 'Mrs.')
        self.assertTrue('Kid1' in entity.children)
        self.assertTrue('Kid2' in entity.children)
        self.assertFalse('Kid3' in entity.children)
        self.assertEqual(entity.marriage_date, '20 OCT 1983')
        self.assertTrue(entity.divorce_date is None)

if __name__ == '__main__':
    unittest.main()
