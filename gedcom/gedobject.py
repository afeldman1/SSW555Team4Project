"""
    SSW 555
    2016 Spring
    Team 4
"""

class GedObject(object):

    def __init__(self, uid):
        self._uid = uid
        
    @property
    def uid(self):
        return self._uid
