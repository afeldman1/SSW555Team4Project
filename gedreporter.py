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
   
            
def _calc_age(ind):
    """
        Calaculates the current age of an individual. If the individual has
        passed away, then calculates their age at the time of passing.
    """
    born = ind.birthday
    end_date = ind.death_date if ind.death_date else date.today()
    
    if not born:
        return 0
    
    offset = int((end_date.month, end_date.day) < (born.month, born.day))
    return end_date.year - born.year - offset
