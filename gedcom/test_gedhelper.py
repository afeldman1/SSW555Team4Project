"""
    SSW 555
    2016 Spring
    Team 4
"""

import unittest
import gedhelper
from gedentity import GEDEntity
from family import Family
from individual import Individual

class gedhelperTest(unittest.TestCase):

    def test_sort_by_id(self):

        entities = [Individual('@I13@'),
                    Family('@F05@'),
                    Family('@F01@'),
                    Individual('@I02@'),
                    Individual('@I01@'),
                    Family('@F07@'),
                    Family('@F12@'),
                    Individual('@I09@'),
                    Family('@F08@'),
                    Individual('@I03@')]
        sorted_entities = gedhelper.sort_by_id(entities)

        expected_sorted_ids = sorted([entity.id_number for entity in entities])
        actual_sorted_ids = [entity.id_number for entity in sorted_entities]
        self.assertEqual(expected_sorted_ids, actual_sorted_ids)

if __name__ == '__main__':
    unittest.main()
