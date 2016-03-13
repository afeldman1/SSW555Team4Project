"""
    SSW 555
    2016 Spring
    Team 4
"""

from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import itertools

class GedReporter(object):
    """
        This class takes dictionaries of individuals and families taken from a
        GEDCOM file and queries information on them.
    """

    def __init__(self, individuals, families):
        self._inds = individuals
        self._fams = families

    @property
    def individuals(self):
        return self._inds

    @property
    def families(self):
        return self._fams

    def dates_before_current_date(self):
        """
            US01: Dates before current date
            Dates (birth, marriage, divorce, death) should not be after the
            current date
        """
        for ind in self._inds.values():
            if ind.birthday:
                if ind.birthday > date.today():
                    yield (ind, 'birthday')
            if ind.death_date:
                if ind.death_date > date.today():
                    yield (ind, 'death date')

        for fam in self._fams.values():
            if fam.marriage_date:
                if fam.marriage_date > date.today():
                    yield (fam, 'marriage date')
            if fam.divorce_date:
                if fam.divorce_date > date.today():
                    yield (fam, 'divorce date')

    def birth_before_marriage(self):
        """
            US02: Birth before marriage
            Birth should occur before marriage of an individual
        """
        for ind in self._inds.values():
            if not ind.family_in_law is None:
                birthday = ind.birthday
                marriage = self._fams[ind.family_in_law].marriage_date
                if not marriage is None:
                    if marriage < birthday:
                        yield (ind, self._fams[ind.family_in_law])

    def birth_before_death(self):
        """
            US03: Birth before death
            Birth should occur before death of an individual
        """
        for ind in self._inds.values():
            if not ind.death_date is None and ind.birthday:
                if ind.death_date < ind.birthday:
                        yield ind

    def marriage_before_divorce(self):
        """
            US04: Marriage before divorce
            Marriage should only occur before divorce of spouses, and divorce can only
            occur after marriage
        """
        for fam in self._fams.values():
            if not fam.marriage_date or not fam.divorce_date:
                continue
            if fam.marriage_date > fam.divorce_date:
                yield fam

    def marriage_before_death(self):
        """
            US05: Marriage before death
            Marriage should occur before death of either spouse
        """
        for fam in self._fams.values():
            if fam.marriage_date is None:
                continue
            if self._inds[fam.wife].death_date is not None:
                if self._inds[fam.wife].death_date < fam.marriage_date:
                    yield (self._inds[fam.wife], fam)
            if self._inds[fam.husband].death_date is not None:
                if self._inds[fam.husband].death_date < fam.marriage_date:
                    yield (self._inds[fam.husband], fam)

    def divorce_before_death(self):
        """
            US06: Divorce before death
            Divorce can only occur before death of both spouses
        """
        for ind in self._inds.values():
            if ind.family_in_law and self._fams[ind.family_in_law].divorce_date and ind.death_date:
                if self._fams[ind.family_in_law].divorce_date > ind.death_date:
                    yield (ind, self._fams[ind.family_in_law])

    def less_than_150_years_old(self):
        """
            US07: Less than 150 years old
            Death should be less than 150 years after birth for dead people,
            and current date should be less than 150 years after birth for all
            living people
        """
        return filter(lambda ind: _calc_age(ind) >= 150, self._inds.values())

    def birth_before_marriage_of_parents(self):
        """
            US08: Birth before marriage of parents
            Child should be born after marriage of parents (and before their
            divorce)
        """
        for ind in self._inds.values():

            fam = self._blood_family_of(ind)
        
            if not fam:
                # skip over orphans
                continue

            born = ind.birthday
            married = fam.marriage_date
            divorced = fam.divorce_date

            if not married:
                continue
            if born < married:
                yield (ind, 'before marriage', fam)
            if divorced and divorced < born:
                yield (ind, 'after divorce', fam)
                
    def birth_before_death_of_parents(self):
        """"
            US09: Birth before death of parents
            Child should be born before death of mother and before 9 months
            after death of father
        """
        for ind in self._inds.values():
            
            fam = self._blood_family_of(ind)
            
            if not fam:
                continue
            
            born = ind.birthday
            mother = fam.wife
            if self._inds[mother].death_date:
                #mdate = datetime.strptime(mother.death_date, '%d/%m/%Y')
                if born > self._inds[mother].death_date:
                    yield (ind, 'after', self._inds[mother])
            
            father = fam.husband
            if self._inds[father].death_date:
                #fdate = datetime.strptime(father.death_date, '%d/%m/%Y')
                if relativedelta(born, self._inds[father].death_date).months > 9:
                    yield (ind, 'more than nine months after', self._inds[father])


    def marriage_after_14(self):
        """
            US10: Marriage after 14
            Marriage should be at least 14 years after birth of both spouses
        """
        for fam in self._fams.values():
            if fam.marriage_date and self._inds[fam.wife].birthday and relativedelta(
                    fam.marriage_date, self._inds[fam.wife].birthday).years < 14:
                yield fam.wife;
            if fam.marriage_date and self._inds[fam.husband].birthday and relativedelta(
                    fam.marriage_date, self._inds[fam.husband].birthday).years < 14:
                yield fam.husband;

    def bigamy(self):
        """
            US11: No bigamy
            Marriage should not occur during marriage to another spouse
        """
        for (family1, family2) in itertools.combinations(self._fams.values(),2):
            if family1.husband == family2.husband:
                if ((not family1.divorce_date and not family2.divorce_date)
                    or ((family1.divorce_date and not family2.divorce_date) and family2.marriage_date < family1.divorce_date)
                    or ((family2.divorce_date and not family1.divorce_date) and family1.marriage_date < family2.divorce_date)
                    or (family1.marriage_date <= family2.divorce_date and family2.marriage_date <= family1.divorce_date) or (family2.marriage_date <= family1.divorce_date and family1.marriage_date <=family2.divorce_date)):

                    yield (self._inds[family1.husband], self._inds[family1.wife], self._inds[family2.wife])
            
            if family1.wife == family2.wife:
                if ((not family1.divorce_date and not family2.divorce_date)
                    or ((family1.divorce_date and not family2.divorce_date) and family2.marriage_date < family1.divorce_date)
                    or ((family2.divorce_date and not family1.divorce_date) and family1.marriage_date < family2.divorce_date)
                    or (family1.marriage_date <= family2.divorce_date and family2.marriage_date <= family1.divorce_date) or (family2.marriage_date <= family1.divorce_date and family1.marriage_date <=family2.divorce_date)):

                    yield (self._inds[family1.wife], self._inds[family1.husband], self._inds[family2.husband])

    def parents_not_too_old(self):
        """
            US12: Parents not too old
            Mother should be less than 60 years older than her children and
            father should be less than 80 years older than his children.
        """
        for ind in self._inds.values():
            mother = self._mother_of(ind)
            father = self._father_of(ind)
            
            if mother and father:
                mother_age_diff = _year_diff(mother.birthday, ind.birthday)
                father_age_diff = _year_diff(father.birthday, ind.birthday)
            
                if mother_age_diff >= 60:
                    yield (ind, mother_age_diff, 'mother', mother)
                
                if father_age_diff >= 80:
                    yield (ind, father_age_diff, 'father', father)
            
    def siblings_spacing(self):
        """
            US13: Siblings spacing
            Birth dates of siblings should be more than 8 months apart or less
            than 2 days apart.
        """
        for fam in self._fams.values():
            children = [self._inds[ind_uid] for ind_uid in fam.children]
            for (child1, child2) in itertools.combinations(children, 2):
                # For convenience, 1 month = 30 days.
                if timedelta(2) < abs(child2.birthday - child1.birthday) < timedelta(241):
                    yield (child1, child2)
                    
    
    def mult_births_less_five(self):
        """
            US14: Multiple births less than 5
            No more than five siblings should be born at the same time
        """
        
        for fam in self._fams.values():
            
            individuals = [x for x in fam.children]
            
            birthdays = [x.birthday for x in [self._inds[x] for x in individuals]]
            
            atleast_5 = set([x for x in birthdays if birthdays.count(x) >=5])
            
            if atleast_5:
                yield fam
            
            
            
            
    def fewer_than_15(self):
        """
            US15: Fewer than 15 siblings
            No more than five siblings should be born at the same time
        """
        
        for fam in self._fams.values():
            if len(fam.children) >= 14:
                yield fam
            
        
    def male_last_names(self):
        """
            US16: Male last names
            All male members of a family should have the same last name
        """
        for fam in self._fams.values():
            surname = next((ind.name.rsplit(" ", 1)[1] for ind in self._inds.values() if ind.sex == 'M' and (
                ind.family_by_blood == fam.uid or ind.family_in_law == fam.uid) and
                            len(ind.name.rsplit(" ", 1)) == 2), None)

            if surname is None:
                continue

            for ind in self._inds.values():
                if (ind.sex == 'M' and (ind.family_by_blood == fam.uid or ind.family_in_law == fam.uid) and
                            surname != ind.name.rsplit(" ", 1)[1]):
                    yield (ind, fam)

    # Some helper methods to perform common operations on individuals and
    # families.
        
    def _blood_family_of(self, ind):
        """
            Retrieves the family a child was born into.
        """
        if ind.family_by_blood:
            return self._fams[ind.family_by_blood]
        else:
            return None
        
    def _mother_of(self, ind):
        """
            Retrieves the mother of an individual.
        """
        fam = self._blood_family_of(ind)
        return self._inds[fam.wife] if fam else None
        
    def _father_of(self, ind):
        """
            Retrieves the father of an individual.
        """
        fam = self._blood_family_of(ind)
        return self._inds[fam.husband] if fam else None

            
# Some static helper functions

def _calc_age(ind):
    """
        Calaculates the current age of an individual. If the individual has
        passed away, then calculates their age at the time of passing.
    """
    born = ind.birthday

    if not born:
        return 0
    else:
        end_date = ind.death_date if ind.death_date else date.today()
        return _year_diff(born, end_date)

def _year_diff(start_date, end_date):
    """
        Calculates the amount of entire years passed from start date to end
        date.
    """
    offset = int((end_date.month, end_date.day) < (start_date.month, start_date.day))
    return end_date.year - start_date.year - offset


