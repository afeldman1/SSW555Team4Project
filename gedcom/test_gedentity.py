"""
    SSW 555
    2016 Spring
    Team 4
"""

import unittest
from gedentity import GEDEntity
from family import Family
from individual import Individual

class GEDEntitiesTest(unittest.TestCase):

    def test_id_number(self):
        entity = GEDEntity(42)
        self.assertEqual(entity.id_number, 42)

    def test_Family(self):
        entity = Family(id_number = 100,
                        husband = 'Mr.',
                        wife = 'Mrs.',
                        marriage_date = '20 OCT 1983',
                        divorce_date = None)

        entity.add_child('Kid1')
        entity.add_child('Kid2')

        self.assertEqual(entity.id_number, 100)
        self.assertEqual(entity.husband, 'Mr.')
        self.assertEqual(entity.wife, 'Mrs.')
        self.assertTrue('Kid1' in entity.children)
        self.assertTrue('Kid2' in entity.children)
        self.assertFalse('Kid3' in entity.children)
        self.assertEqual(entity.marriage_date, '20 OCT 1983')
        self.assertTrue(entity.divorce_date is None)

    def test_Individual(self):
        entity = Individual(id_number = 101,
                            name = 'Homer /Simpson/',
                            sex = 'M',
                            family_by_blood = 'Simpson',
                            family_in_law = 'Bouvier',
                            birthday = '12 MAY 1955',
                            death_date = None)

        self.assertEqual(entity.id_number, 101)
        self.assertEqual(entity.name, 'Homer /Simpson/')
        self.assertEqual(entity.sex, 'M')
        self.assertEqual(entity.family_by_blood, 'Simpson')
        self.assertEqual(entity.family_in_law, 'Bouvier')
        self.assertEqual(entity.birthday, '12 MAY 1955')
        self.assertTrue(entity.death_date is None)

if __name__ == '__main__':
    unittest.main()
