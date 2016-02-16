"""
    SSW 555
    2016 Spring
    Team 4
"""

class Individual(object):

    def __init__(self,
                 name = None,
                 sex = None,
                 family_by_blood = None,
                 family_in_law = None,
                 birthday = None,
                 death_date = None):
        self._name = name
        self._sex = sex
        self._family_by_blood = family_by_blood
        self._family_in_law = family_in_law
        self._birthday = birthday
        self._death_date = death_date

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def sex(self):
        return self._sex
    @sex.setter
    def sex(self, sex):
        self._sex = sex

    @property
    def family_by_blood(self):
        return self._family_by_blood
    @family_by_blood.setter
    def family_by_blood(self, family_by_blood):
        self._family_by_blood = family_by_blood

    @property
    def family_in_law(self):
        return self._family_in_law
    @family_in_law.setter
    def family_in_law(self, family_in_law):
        self._family_in_law = family_in_law

    @property
    def birthday(self):
        return self._birthday
    @birthday.setter
    def birthday(self, birthday):
        self._birthday = birthday

    @property
    def death_date(self):
        return self._death_date
    @death_date.setter
    def death_date(self, death_date):
        self._death_date = death_date
        
    def __repr__(self):
        return 'Individual({name}, {sex}, {fam}, {inlaw}, {birth}-{death})'.format(
                name = self.name,
                sex = self.sex,
                fam = self.family_by_blood,
                inlaw = self.family_in_law,
                birth = self.birthday,
                death = self.death_date)
        