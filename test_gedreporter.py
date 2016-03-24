"""
    SSW 555
    2016 Spring
    Team 4
"""

import glob
import unittest

import gedcom.parser
from gedreporter import GedReporter

def perform_gedfile_sanity_check():
    
    gedfiles = glob.glob('datafiles/US*.ged')
    print(str.join('\n',gedfiles))
    
    
class GedReporterTest(unittest.TestCase):


    def test_US07_less_than_150_years_old(self):
    
        (inds, fams) = gedcom.parser.parse_file('datafiles/US07_less_than_150_years_old.ged')
        reporter = GedReporter(inds, fams)
        ids = [ind.uid for ind in reporter.less_than_150_years_old()]

        self.assertTrue('@I150@' in ids)
        self.assertTrue('@I151@' in ids)
        self.assertTrue('@I152@' in ids)
        self.assertFalse('@I153@' in ids)

    def test_US08_birth_before_marriage_of_parents(self):
    
        (inds, fams) = gedcom.parser.parse_file('datafiles/US08_birth_before_marriage_of_parents.ged')
        reporter = GedReporter(inds, fams)
        ids = [(child.uid, when, family.uid)
                for (child, when, family)
                in reporter.birth_before_marriage_of_parents()]

        self.assertTrue(('@I14@', 'after divorce', '@F1@') in ids)
        self.assertTrue(('@I11@', 'before marriage', '@F1@') in ids)
        self.assertFalse(('@I13@', 'after divorce', '@F1@') in ids)
        self.assertFalse(('@I12@', 'before marriage', '@F1@') in ids)
    

    
if __name__ == '__main__':
    perform_gedfile_sanity_check()
    unittest.main()
