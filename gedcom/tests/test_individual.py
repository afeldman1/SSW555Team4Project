"""
    SSW 555
    2016 Spring
    Team 4
"""

import unittest
from gedcom.individual import Individual

class GEDEntitiesTest(unittest.TestCase):

    def test_Individual(self):
        entity = Individual(name = 'Homer /Simpson/',
                            sex = 'M',
                            family_by_blood = 'Simpson',
                            family_in_law = 'Bouvier',
                            birthday = '12 MAY 1955',
                            death_date = None)
        self.assertEqual(entity.name, 'Homer /Simpson/')
        self.assertEqual(entity.sex, 'M')
        self.assertEqual(entity.family_by_blood, 'Simpson')
        self.assertEqual(entity.family_in_law, 'Bouvier')
        self.assertEqual(entity.birthday, '12 MAY 1955')
        self.assertTrue(entity.death_date is None)

if __name__ == '__main__':
    unittest.main()
