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
        return filter(lambda ind: ind.birthday > date.today() if ind.birthday else False and ind.death_date > date.today() if ind.death_date else False, self._inds.values()) and filter(lambda fam: fam.marriage_date > date.today() if fam.marriage_date else False and fam.divorce_date > date.today() if fam.divorce_date else False, self._fams.values())

    def divorce_before_death(self):
        """
            US06: Divorce before death
            Divorce can only occur before death of both spouses
        """
        return filter(lambda fam: fam.divorce_date > fam.husband.death_date if fam.divorce_date and fam.husband.death_date else False and fam.divorce_date > fam.wife.death_date if fam.divorce_date and fam.wife.death_date else False, self._fams.values())

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
            if fam.marriage_date and not fam.divorce_date:
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
            if not self._inds[fam.wife].death_date:
                continue
            if not self._inds[fam.husband].death_date:
                continue
            if self._inds[fam.wife].death_date > fam.marriage_date:
                yield self._inds[fam.wife]
            if self._inds[fam.husband].death_date > fam.marriage_date:
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


