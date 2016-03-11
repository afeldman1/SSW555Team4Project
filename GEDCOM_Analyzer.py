"""
    SSW 555
    2016 Spring
    Team 4
"""

import sys
import gedcom.parser
import gedreporter

def main():
    """
        main subprogram
    """

    fname = sys.argv[1] if len(sys.argv) > 1 else input('Enter the file name: ')
    try:
        (inds, fams) = gedcom.parser.parse_file(fname)
    except IOError:
        print ('File cannot be opened:', fname)
        exit()

    reporter = gedreporter.GedReporter(inds, fams)

    print('')
    print('Individuals:')
    for key in sorted(inds):
        print("%s %s" % (key, inds[key].name))
    print('')

    print('Families:')
    for key in sorted(fams):
        husband_name = inds[fams[key].husband].name if fams[key].husband else ''
        wife_name = inds[fams[key].wife].name if fams[key].wife else ''
        print("%s %s %s" % (key, husband_name, wife_name))
    print('')

    for (ent, event) in reporter.dates_before_current_date():
        print('Error US01: {ent} {event} occurs after today.\n'.format(ent=ent.short_repr, event=event))

    for (ind, fam) in reporter.birth_before_marriage():
        print('Error US02: {ind} was born after marriage into {fam}.\n'.format(
                ind = ind.short_repr, fam = fam.short_repr))

    for ind in reporter.birth_before_death():
        print('Error US03: {} died before they were born.\n'.format(ind.short_repr))

    for fam in reporter.marriage_before_divorce():
        print('Error US04: {} marriage date occurs after divorce date.\n'.format(fam.short_repr))

    for (ind, fam) in reporter.marriage_before_death():
        print('Error US05: {ind} died before marriage into {fam}.\n'.format(
                ind = ind.short_repr, fam = fam.short_repr))

    for (ind, fam) in reporter.marriage_before_death():
        print('Error US06: {ind} died before divorce from {fam}.\n'.format(
                ind=ind.short_repr, fam=fam.short_repr))

    for ind in reporter.less_than_150_years_old():
        print('Error US07: {} is >= 150 years old.\n'.format(ind.short_repr))

    for (child, when, family) in reporter.birth_before_marriage_of_parents():
        print('Anomaly US08: {child} was born {when} of parents in {family_uid}.\n'.format(
            child = child.short_repr, when = when, family_uid = family.short_repr ))

    for ind in reporter.marriage_after_14():
        print('Error US10: {spouse} birth date occurs fewer than 14 years before marriage date.\n'.format(
            spouse=ind.short_repr))

    for (child, year_diff, which_parent, parent) in reporter.parents_not_too_old():
        print('Anomaly US12: {child} was born {years} years after {which_parent} {parent} was born.\n'.format(
            child = child.short_repr, years = year_diff, which_parent = which_parent, parent = parent.short_repr ))

    for (sibling1, sibling2) in reporter.siblings_spacing():
        print('Anomaly US13: Siblings {sibling1} and {sibling2} were born less than 8 months apart.\n'.format(
            sibling1 = sibling1.short_repr, sibling2 = sibling2.short_repr ))
        
    for fam in reporter.mult_births_less_five():
        print ('Anomaly US14: Family {fam} had 5 or more children born at the same time. \n'.format( fam = fam.short_repr))
        
    for fam in reporter.fewer_than_15():
        print ('Anomaly US15: Family {fam} has 15 or more siblings. \n'.format( fam = fam.short_repr))

    for (ind, fam) in reporter.male_last_names():
        print('Anomaly US16: {ind} is a male'.format(ind=ind.short_repr) +
              " who's surname does not match his families, " + '{fam}.\n'.format(fam=fam.short_repr))

if __name__ == '__main__':
    main()
