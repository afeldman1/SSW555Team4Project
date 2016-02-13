"""
        William J Pierro
        SSW 555 Agile Development Methods
        Created 2016 FEB 2
"""

import re

class GEDCOMLine(object):

    def __init__(self, line_text):

        line_text_cleaned = line_text.strip()
        tokens = line_text_cleaned.split()

        self._line_text = line_text_cleaned
        self._level = tokens[0]

        # special case:
        # ID preceding INDI or FAM tag
        id_match = re.match('@[I|F][0-9]+@', tokens[1])
        if id_match:
            self._tag = tokens[2]
            self._payload = tokens[1]
        else:
            self._tag = tokens[1]
            self._payload = tokens[2:]

    @property
    def level(self):
        return self._level

    @property
    def tag(self):
        return self._tag

    @property
    def payload(self):
        return self._payload

    @property
    def line_text(self):
        return self._line_text

    def __repr__(self):
        return '[GEDCOMLine: level={level} tag={tag} payload={payload}]'.format(
            level=self.level,
            tag=self.tag,
            payload=self.payload)

    @property
    def has_valid_tag(self):
        valid_tags = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT',
                      'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB',
                      'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD',
                      'TRLR', 'NOTE']
        return self.tag in valid_tags
