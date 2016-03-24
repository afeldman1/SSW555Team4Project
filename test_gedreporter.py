"""
    SSW 555
    2016 Spring
    Team 4
"""

import glob
import inspect
import os.path
import subprocess
import unittest

import gedcom
import gedcom.parser
import gedreporter


def perform_gedfile_sanity_check():
    """
        Opens all user story .ged files and makes sure they don't break/cause
        exceptions with the user story methods in GedReporter.
    """

    # grab all user story .ged files
    ged_filenames = glob.glob('datafiles/US*.ged')

    # get all public non-inherited methods from the reporter object
    # reporter_methods = [(method_name, method) for (method_name, method)
                            # in inspect.getmembers(gedreporter.GedReporter)
                            # if  not method_name.startswith('_')
                                # and callable(method)]

    for filename in ged_filenames:

        outfilename = os.path.basename(filename) + '.out'
        with open(outfilename, 'w') as outfile:
                subprocess.call(['python', 'GEDCOM_Analyzer.py', filename],
                                stdout = outfile)

        # (inds, fams) = gedcom.parser.parse_file(filename)
        # reporter = gedreporter.GedReporter(inds, fams)

        # for (method_name, method) in reporter_methods:
            # try:
                # method(reporter)
            # except Exception as ex:
                # print(
                    # str.format('{filename} -> GedReporter.{method_name} : {ex}',
                    # ex = ex,
                    # method_name = method_name,
                    # filename = filename))

#class GedReporterTest(unittest.TestCase):



if __name__ == '__main__':
    perform_gedfile_sanity_check()
