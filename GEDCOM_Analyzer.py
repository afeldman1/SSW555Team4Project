"""
    SSW 555
    2016 Spring
    Team 4
"""

import sys
import gedcom
import gedreporter

from datetime import datetime
from gedcom.gedcomline import GEDCOMLine
from gedcom.individual import Individual
from gedcom.family import Family
from gedreporter import GedReporter

def parse_date(date_text):
    """
        Parses a GEDCOM format date into an internal date object.
    """
    return datetime.strptime(date_text, '%d %b %Y').date()

def main():
    """
        main subprogram
    """

    fname = sys.argv[1] if len(sys.argv) > 1 else input('Enter the file name: ')
    try:
        f = open(fname)
    except IOError:
        print ('File cannot be opened:', fname)
        exit()

    inds = dict()
    fams = dict()
    processInd = False
    processFam = False

    gedcom_lines = (GEDCOMLine(line) for line in f)
    lineno = 0

    for gedline in gedcom_lines:
        lineno += 1

        if not gedline.has_valid_tag:
            #print('No valid tag on line ', lineno, '\n')
            pass
        else:
            tag = gedline.tag
            payload = gedline.payload
            if gedline.level == 0:              #If top level record, clear state
                processInd = False
                processFam = False

            if processInd:                      #If gathering data on individual
                if tag == "NAME":               #Check tag and store appropriately
                    inds[uid].name = payload.replace("/","")
                elif tag == "SEX":
                    inds[uid].sex = payload
                elif tag == "FAMC":
                    inds[uid].family_by_blood = payload
                elif tag == "FAMS":
                    inds[uid].family_in_law = payload
                elif tag == "DATE":
                    if prevTag == "BIRT":
                        inds[uid].birthday = parse_date(payload)
                    elif prevTag == "DEAT":
                        inds[uid].death_date = parse_date(payload)

            elif processFam:                    #If gathering data on family
                if tag == "HUSB":               #Check tag and store appropriately
                    fams[uid].husband = payload
                elif tag == "WIFE":
                    fams[uid].wife = payload
                elif tag == "CHIL":
                    fams[uid].add_child(payload)
                elif tag == "DATE":
                    if prevTag == "MARR":
                        fams[uid].marriage_date = parse_date(payload)
                    elif prevTag == "DIV":
                        fams[uid].divorce_date = parse_date(payload)

            elif gedline.tag == "INDI":         #If start of individual record
                uid = gedline.payload           #Store identifier in dictionary and
                inds[uid] = Individual(uid)     #prepare for more individual info
                processInd = True
                processFam = False
            elif gedline.tag == "FAM":          #If start of family record
                uid = gedline.payload           #Store identifier in dictionary and
                fams[uid] = Family(uid)         #prepare for more family info
                processFam = True
                processInd = False

            prevTag = tag    #Save tag to associate date on next gedline

    reporter = GedReporter(inds, fams)

    for key in sorted(inds):
        print("%s %s" % (key, inds[key].name))

    for key in sorted(fams):
        husband_name = inds[fams[key].husband].name if fams[key].husband else ''
        wife_name = inds[fams[key].wife].name if fams[key].wife else ''
        print("%s %s %s" % (key, husband_name, wife_name))

    print('Dates before current date:')
    for ent in reporter.dates_before_current_date():
        print(ent)
#
#     print('Divorce before death:')
#     for fam in reporter.divorce_before_death():
#         print(fam)

    print('Individuals over 150:')
    for ind in reporter.less_than_150_years_old():
        print(ind)

    print('Individuals born before marriage or after divorce of parents:')
    for ind in reporter.birth_before_marriage_of_parents():
        print(ind)

if __name__ == '__main__':
    main()
