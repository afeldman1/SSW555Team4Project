"""
    SSW 555
    2016 Spring
    Team 4
"""

class Family(object):

    def __init__(self,
                 husband = None,
                 wife = None,
                 children = [],
                 marriage_date = None,
                 divorce_date = None):
        self._husband = husband
        self._wife = wife
        self._children = children
        self._marriage_date = marriage_date
        self._divorce_date = divorce_date

    @property
    def husband(self):
        return self._husband
    @husband.setter
    def husband(self, husband):
        self._husband = husband

    @property
    def wife(self):
        return self._wife
    @wife.setter
    def wife(self, wife):
        self._wife = wife

    @property
    def children(self):
        return self._children
    @children.setter
    def children(self, children):
        self._children = children

    def add_child(self, child):
        self._children.append(child)

    @property
    def marriage_date(self):
        return self._marriage_date
    @marriage_date.setter
    def marriage_date(self, marriage_date):
        self._marriage_date = marriage_date

    @property
    def divorce_date(self):
        return self._divorce_date
    @divorce_date.setter
    def divorce_date(self, divorce_date):
        self._divorce_date = divorce_date
        
    def __repr__(self):
        return 'Family({husband} & {wife}, {marriage}-{divorce})'.format(
                husband = self.husband,
                wife = self.wife,
                marriage = self.marriage_date,
                divorce = self.divorce_date)
        