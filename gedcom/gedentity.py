"""
    SSW 555
    2016 Spring
    Team 4
"""

class GEDEntity(object):

    def __init__(self, id_number):
        self._id_number = id_number

    @property
    def id_number(self):
        return self._id_number

