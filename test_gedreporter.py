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
    
    print('\nGenerating .ged acceptance test files...\n')
    perform_gedfile_sanity_check()

    print('\nRunning user story unit tests...\n')
    unittest.main()

