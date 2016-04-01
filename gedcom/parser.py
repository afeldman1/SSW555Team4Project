"""
    SSW 555
    2016 Spring
    Team 4
"""

from datetime import datetime
from .gedcomline import GEDCOMLine
from .individual import Individual
from .family import Family


def parse_file(fname):
    """
        Opens and parses GEDCOM file. Returns records as a tuple of lists of
        (individuals, families).
    """
    with open(fname, 'r') as f:
        gedcom_lines = (GEDCOMLine(line) for line in f)

        inds = dict()
        fams = dict()
        processInd = False
        processFam = False

        lineno = 0

        for gedline in gedcom_lines:
            lineno += 1

            if not gedline.has_valid_tag:
                #print('No valid tag on line ', lineno, '\n')
                pass
            else:
                tag = gedline.tag
                payload = gedline.payload
                if gedline.level == 0:              #If top level record, clear state
                    processInd = False
                    processFam = False

                if processInd:                      #If gathering data on individual
                    if tag == "NAME":               #Check tag and store appropriately
                        inds[uid].name = payload.replace("/","")
                    elif tag == "SEX":
                        inds[uid].sex = payload
                    elif tag == "FAMC":
                        inds[uid].family_by_blood = payload
                    elif tag == "FAMS":
                        inds[uid].family_in_law = payload
                    elif tag == "DATE":
                        if prevTag == "BIRT":
                            inds[uid].birthday = parse_date(payload)
                        elif prevTag == "DEAT":
                            inds[uid].death_date = parse_date(payload)

                elif processFam:                    #If gathering data on family
                    if tag == "HUSB":               #Check tag and store appropriately
                        fams[uid].husband = payload
                    elif tag == "WIFE":
                        fams[uid].wife = payload
                    elif tag == "CHIL":
                        fams[uid].add_child(payload)
                    elif tag == "DATE":
                        if prevTag == "MARR":
                            fams[uid].marriage_date = parse_date(payload)
                        elif prevTag == "DIV":
                            fams[uid].divorce_date = parse_date(payload)

                elif gedline.tag == "INDI":  # If start of individual record
                    uid = gedline.payload  # Store identifier in dictionary and

                    if uid in inds:
                        print(
                            "Error US22: Repeating Individual IDs(" + uid + '). The file was unable to be correctly loaded.')
                    else:
                        inds[uid] = Individual(uid)  # prepare for more individual info
                        processInd = True
                        processFam = False
                elif gedline.tag == "FAM":  # If start of family record
                    uid = gedline.payload  # Store identifier in dictionary and

                    if uid in fams:
                        print(
                            "Error US22: Repeating Family IDs(" + uid + "). The file was unable to be correctly loaded.")
                    else:
                        fams[uid] = Family(uid)  # prepare for more family info
                        processFam = True
                        processInd = False

                prevTag = tag    #Save tag to associate date on next gedline

        return inds, fams


def parse_date(date_text):
    """
        Parses a GEDCOM format date into an internal date object.
    """
    return datetime.strptime(date_text, '%d %b %Y').date()
