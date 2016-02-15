"""
    SSW 555
    2016 Spring
    Team 4
"""

import gedcom

from gedcom.gedcomline import GEDCOMLine
from gedcom.individual import Individual
from gedcom.family import Family

def main():

    fName = input('Enter the file name: ')
    try:
        f = open(fName)
    except:
        print ('File cannot be opened:', fname)
        exit()

    inds = dict()
    fams = dict()
    processInd = False
    processFam = False

    gedcom_lines = [GEDCOMLine(line) for line in f]
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
                elif tag == "BIRT":
                    pass
                elif tag == "DEAT":
                    pass
                elif tag == "DATE":
                    if prevTag == "BIRT":
                        inds[uid].birthday = payload
                    elif prevTag == "DEAT":
                        inds[uid].death_date = payload
            elif processFam:                    #If gathering data on family
                if tag == "MARR":               #Check tag and store appropriately
                    pass
                elif tag == "HUSB":
                    fams[uid].husband = payload
                elif tag == "WIFE":
                    fams[uid].wife = payload
                elif tag == "CHIL":
                    fams[uid].add_child(payload)
                elif tag == "DIV":
                    pass
            elif gedline.tag == "INDI":         #If start of individual record
                uid = gedline.payload           #Store identifier in dictionary and
                inds[uid] = Individual()        #prepare for more individual info
                processInd = True
                processFam = False
            elif gedline.tag == "FAM":          #If start of family record
                uid = gedline.payload           #Store identifier in dictionary and
                fams[uid] = Family()            #prepare for more family info
                processFam = True
                processInd = False

            prevTag = tag    #Save tag to associate date on next gedline

    for key in sorted(inds):
        print("%s %s" % (key, inds[key].name))

    for key in sorted(fams):
        husband_name = inds[fams[key].husband].name if fams[key].husband else ''
        wife_name = inds[fams[key].wife].name if fams[key].wife else ''
        print("%s %s %s" % (key, husband_name, wife_name))

if __name__ == '__main__':
    main()
