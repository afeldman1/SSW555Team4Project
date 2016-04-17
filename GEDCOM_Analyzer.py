"""
    SSW 555
    2016 Spring
    Team 4
"""

import sys

from dateutil.relativedelta import relativedelta

import gedcom.parser
import gedreporter
from datetime import date

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
        print("%s %s, Age %s" % (key, inds[key].name, relativedelta(date.today(), inds[key].birthday).years))
    print('')

    print('Families:')
    for key in sorted(fams):
        husband_name = inds[fams[key].husband].name if fams[key].husband else ''
        wife_name = inds[fams[key].wife].name if fams[key].wife else ''
        print("%s %s %s" % (key, husband_name, wife_name))
        
        # US28: Order siblings by age
        # List siblings in families by age  
        for child_uid in sorted(fams[key].children,
                                key = lambda ind_id: inds[ind_id].birthday):                                
            print("    " + inds[child_uid].name)
        
        
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

    for (child, when, parent) in reporter.birth_before_death_of_parents():
        print('Error US09: {child} was born {when} {parent} died.\n'.format(
            child = child.short_repr, when = when, parent = parent.short_repr))

    for ind in reporter.marriage_after_14():
        print('Error US10: {spouse} birth date occurs fewer than 14 years before marriage date.\n'.format(
            spouse=ind.short_repr))

    for (ind, spouse1, spouse2) in reporter.bigamy():
        print('Anomaly US011: {ind} was married to {spouse1} and {spouse2} concurrently.\n'.format(
            ind = ind.short_repr, spouse1 = spouse1.short_repr, spouse2 = spouse2.short_repr))

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
        
    for (ind, ind2) in reporter.marriage_to_descendants():
        print('Anomaly US17: {ind} is married to {ind2}, who is a descendant of {ind}'.format(ind=ind.short_repr, ind2=ind2.short_repr))
        
    for (ind,ind2) in reporter.sibling_marriage():
        print('Anomaly US18: {ind} is married to {ind2} and they are siblings'.format(ind=ind.short_repr, ind2=ind2.short_repr)) 

    for (spouse1, spouse2, parent1, parent2) in reporter.first_cousins_should_not_marry():
        print('Anomaly US19: First cousins {spouse1} and {spouse2} are married thru parents {parent1} and {parent2}.'.format(
                spouse1 = spouse1.short_repr,
                spouse2 = spouse2.short_repr,
                parent1 = parent1.short_repr,
                parent2 = parent2.short_repr))

    for ind in reporter.correct_gender_role():
        print('Anomaly US21: Individual {ind} has an incorrect gender role. \n'.format(ind=ind.short_repr))

    for (ind1, ind2) in reporter.unique_name_and_birth_date():
        print('Anomaly US23: {ind1} and {ind2} have the same name and birth date.'.format(ind1 = ind1, ind2 = ind2))

    for (ind1, ind2, fam) in reporter.unique_first_names():
        print('Anomaly US25: {ind1} and {ind2} of family {fam} have the same first name and birthday'.format(ind1=ind1.short_repr, ind2=ind2.short_repr, fam=fam))

    for ind in reporter.list_deceased():
        print('US29: Individual {ind} is deceased'.format(ind=ind.short_repr))

    for ind in reporter.list_living_married():
        print('US30: Individual {ind} is living and married.'.format(ind=ind.short_repr))
        
    for ind in reporter.list_living_single():
        print('US31: Individual {ind} is single and over the age of 30.'.format(ind=ind.short_repr))
        
    for (entity1, relationship, entity2) in reporter.corresponding_entries():
        print('Error US26: {entity1} is missing a corresponding {role} entry for {entity2}'.format(
            entity1 = entity1, role = relationship, entity2 = entity2))
        
if __name__ == '__main__':
    main()
