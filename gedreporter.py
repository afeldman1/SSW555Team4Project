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
    
    def less_than_150_years_old(self):
        """
            US07: Less than 150 years old
            Death should be less than 150 years after birth for dead people,
            and current date should be less than 150 years after birth for all
            living people
        """
        return filter(lambda ind: _calc_age(ind) >= 150, self._inds.values())
        
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
