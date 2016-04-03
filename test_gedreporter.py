"""
    SSW 555
    2016 Spring
    Team 4
"""

import glob
import os
import os.path
import subprocess
import unittest

import gedcom
import gedcom.parser
from gedreporter import GedReporter


def perform_gedfile_sanity_check():
    """
        Opens all user story .ged files and makes sure they don't break/cause
        exceptions with the user story methods in GedReporter.
    """
    # grab all user story .ged files
    ged_filenames = glob.glob('datafiles/US*.ged')

    # create acceptance test directory
    outfiles_dir_name = 'outfiles'
    if not os.path.exists(outfiles_dir_name):
        os.makedirs(outfiles_dir_name)
    
    for ged_filename in ged_filenames:
    
        bare_ged_filename = os.path.splitext(os.path.basename(ged_filename))[0]
        outfilename = bare_ged_filename + '.out'
        outfilepath = os.path.join(outfiles_dir_name, outfilename)
        
        with open(outfilepath, 'w') as outfile:
            retcode = subprocess.call(['python', 'GEDCOM_Analyzer.py', ged_filename],
                                        stdout = outfile,
                                        stderr = outfile)
            if retcode == 0:
                print('{}: ok'.format(outfilename))
            else:
                print('{}: ERROR retcode {}'.format(outfilename, retcode))


class GedReporterTest(unittest.TestCase):

    def test_US05_marriage_before_death(self):
        
        (inds, fams) = gedcom.parser.parse_file('datafiles/US05_marriage_before_death.ged')
        reporter = GedReporter(inds, fams)
        
        ind_fam_ids = [(ind.uid, fam.uid) for (ind, fam) in reporter.marriage_before_death()]
        
        self.assertTrue(('@I2@','@F1@') in ind_fam_ids)
        self.assertTrue(('@I2@','@F1@') in ind_fam_ids)
        
    def test_US06_divorce_before_death(self):
        
        (inds, fams) = gedcom.parser.parse_file('datafiles/US06_divorce_before_death.ged')
        reporter = GedReporter(inds, fams)
        
        ind_fam_ids = [(ind.uid, fam.uid) for (ind, fam) in reporter.divorce_before_death()]
        
        self.assertTrue(('@I2@','@F1@') in ind_fam_ids)

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

    def test_US_09_birth_before_death_of_parents(self):
        (inds, fams) = gedcom.parser.parse_file('datafiles/US09_birth_before_parent_death.ged')
        reporter = GedReporter(inds, fams)
        ids = [(child.uid, when, parent.uid)
                for (child, when, parent)
                in reporter.birth_before_death_of_parents()]

        self.assertTrue(('@I2@', 'after', '@I6@') in ids)
        self.assertTrue(('@I2@', 'more than nine months after', '@I5@') in ids)
        self.assertTrue(('@I9@', 'after', '@I6@') in ids)

    def test_US_10_marriage_after_14(self):
        (inds, fams) = gedcom.parser.parse_file('datafiles/US10_marriage_after_14.ged')
        reporter = GedReporter(inds, fams)
        ids = [ind.uid for ind in reporter.marriage_after_14()]

        self.assertTrue('@I4@' in ids)
        self.assertTrue('@I3@' in ids)

    def test_US_11_bigamy(self):
        (inds, fams) = gedcom.parser.parse_file('datafiles/US11_bigamy.ged')
        reporter = GedReporter(inds, fams)
        ids = [(ind.uid, spouse1.uid, spouse2.uid) for (ind, spouse1, spouse2) in reporter.bigamy()]

        self.assertTrue(('@I4@', '@I1@', '@I7@') in ids)

    def test_US_12_parents_not_too_old(self):
        (inds, fams) = gedcom.parser.parse_file('datafiles/US12_parents_not_too_old.ged')
        reporter = GedReporter(inds, fams)
        ids = [(child, year_diff, which_parent, parent) for (child, year_diff, which_parent, parent) in reporter.parents_not_too_old()]

        self.assertTrue(('Born tooLate @I12@', '60', 'mother', 'Mother ofTheFamily @I2@') in ids)
        self.assertTrue(('Born tooLate @I12@', '80', 'father', 'Father ofTheFamily @I1@') in ids)
        
    def test_US19_first_cousins_should_not_marry(self):
    
        (inds, fams) = gedcom.parser.parse_file('datafiles/US19_first_cousins_should_not_marry.ged')
        reporter = GedReporter(inds, fams)
        
        # use a set because we want to ignore order when using equality
        ids = [frozenset((ind1.uid, ind2.uid, parent1.uid, parent2.uid))
                for (ind1, ind2, parent1, parent2)
                in reporter.first_cousins_should_not_marry()]
        
        self.assertTrue(frozenset(('@I07@', '@I08@', '@I04@', '@I05@')) in ids)
        
    def test_US23_unique_name_and_birth_date(self):
    
        (inds, fams) = gedcom.parser.parse_file('datafiles/US23_unique_name_and_birth_date.ged')
        reporter = GedReporter(inds, fams)
        
        # use a set because we want to ignore order when using equality
        ids = [frozenset((ind1.uid, ind2.uid))
                for (ind1, ind2)
                in reporter.unique_name_and_birth_date()]
                
        self.assertTrue(frozenset(('@I12@', '@I11@')) in ids)
        self.assertTrue(frozenset(('@I10@', '@I13@')) in ids)

if __name__ == '__main__':
    
    print('\nGenerating .ged acceptance test files...\n')
    perform_gedfile_sanity_check()

    print('\nRunning user story unit tests...\n')
    unittest.main()

