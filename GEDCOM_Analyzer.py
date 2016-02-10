
f = open('My-Family-2-Feb-2016.ged', 'r');

for line in f:    
    print(line, end='');

    print("Level: " + line.split()[0]);
        
    if (line.split()[1] ==  "INDI" or line.split()[1] ==  "FAM" or line.split()[1] ==  "HEAD" or line.split()[1] ==  "TRLR" or line.split()[1] ==  "NOTE" or line.split()[1] ==  "NAME" or line.split()[1] ==  "SEX" or line.split()[1] ==  "BIRT" or line.split()[1] ==  "DEAT" or line.split()[1] ==  "FAMC" or line.split()[1] ==  "FAMS" or line.split()[1] ==  "MARR" or line.split()[1] ==  "HUSB" or line.split()[1] ==  "WIFE" or line.split()[1] ==  "CHIL" or line.split()[1] ==  "DIV" or line.split()[1] ==  "DATE"):
        print("Tag: " + line.split()[1], end="\r\n\r\n");
    else:
        print("Tag: Invalid tag", end='\r\n\r\n');
