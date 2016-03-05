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

    print('Dates before current date:')
    for ent in reporter.dates_before_current_date():
        print(ent)

    print('Birth before marriage:')
    for ind in reporter.birth_before_marriage():
        print (ind)

    print('Birth before death:')
    for ind in reporter.birth_before_death():
        print (ind)

    print('Divorce before death:')
    for fam in reporter.divorce_before_death():
        print(fam)

    for ind in reporter.less_than_150_years_old():
        print('Error US07: Individual {} is >= 150 years old.\n'.format(ind.short_repr))

    for (child, when, family) in reporter.birth_before_marriage_of_parents():
        print('Anomaly US08: Individual {child} was born {when} of parents in Family {family_uid}.\n'.format(
            child = child.short_repr, when = when, family_uid = family.uid ))

    print('Individuals divorced before married:')
    for fam in  reporter.marriage_before_divorce():
        print(fam)

    print('Individuals married before death of spouse:')
    for fam in reporter.marriage_before_death():
        print(fam)

    for (child, year_diff, which_parent, parent) in reporter.parents_not_too_old():
        print('Anomaly US12: Individual {child} was born {years} years after {which_parent} {parent} was born.\n'.format(
            child = child.short_repr, years = year_diff, which_parent = which_parent, parent = parent.short_repr ))


if __name__ == '__main__':
    main()
