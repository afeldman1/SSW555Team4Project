"""
    SSW 555
    2016 Spring
    Team 4
"""

import glob


def perform_gedfile_sanity_check():
    
    gedfiles = glob.glob('datafiles/US*.ged')
    print(str.join('\n',gedfiles))
    
    
if __name__ == '__main__':
    perform_gedfile_sanity_check()    
