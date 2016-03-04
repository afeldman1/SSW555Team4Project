"""
    SSW 555
    2016 Spring
    Team 4
"""

from datetime import date

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
                    yield ind;
            if ind.death_date:
                if ind.death_date > date.today():
                    yield ind;

        for fam in self._fams.values():
            if fam.marriage_date:
                if fam.marriage_date > date.today():
                    yield fam;
            if fam.divorce_date:
                if fam.divorce_date > date.today():
                    yield fam;

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
                        yield ind

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
                yield self._inds[fam.wife]
                yield self._inds[fam.husband]
                #yield fam


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
                    yield self._inds[fam.wife]
            if self._inds[fam.husband].death_date is not None:
                if self._inds[fam.husband].death_date < fam.marriage_date:
                    yield self._inds[fam.husband]

    def divorce_before_death(self):
        """
            US06: Divorce before death
            Divorce can only occur before death of both spouses
        """
        for ind in self._inds.values():
            if ind.family_in_law and self._fams[ind.family_in_law].divorce_date and ind.death_date:
                if self._fams[ind.family_in_law].divorce_date > ind.death_date:
                    yield ind

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

            if not ind.family_by_blood:
                # skip over orphans
                continue

            born = ind.birthday
            fam = self._fams[ind.family_by_blood]
            married = self._fams[ind.family_by_blood].marriage_date
            divorced = self._fams[ind.family_by_blood].divorce_date

            if not married:
                pass
            elif born < married:
                yield ind
            elif divorced and divorced < born:
                yield ind

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


