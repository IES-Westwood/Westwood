# import System modules
import arcpy
from arcpy import management
from arcpy import da as data

# set up functions
def checkPri(r):
    if "p" in str(r[6]).lower():
        return "primary"
    if "a" in str(r[6]).lower():
        return "alternate"
    if "me" in str(r[6]).lower():
        return "MET"
def checkID(r):
    if "a" in str(r[6]).lower():
        return "alternate"
    if "me" in str(r[6]).lower():
        return "MET"
    else:
        return "primary"
def extractdigits(string):
    res = ''.join(filter(lambda i: i.isdigit(), string))
    return res

# Get User Inputs
TA_Path = arcpy.GetParameterAsText(0)
CADv = arcpy.GetParameterAsText(1)
PA_Field = arcpy.GetParameterAsText(2)
TIDField = arcpy.GetParameterAsText(3)
Source = arcpy.GetParameterAsText(4)
OnlyMets = arcpy.GetParameterAsText(5)

# Fields to add
field_names = ["TURB_NUM", "TURB_NUM2", "TURB_NUM_S", "LAYER", "BLOCK", "SOURCE"]

# Add required fields
for x in field_names:
    arcpy.management.AddField(TA_Path, x, "text")

# If given primary/alternate field and a turbine ID field add to field names list for cursor
if PA_Field != "":
    field_names.append(PA_Field)
    q1 = False
else:
    q1 = True
if TIDField != "":
    field_names.append(TIDField)
    q2 = False
else:
    q2 = True

if OnlyMets == True: #if this is only a MET Tower only shapefile
    with data.UpdateCursor(TA_Path, field_names) as cursor:
        for row in cursor:
            row[5] = Source
            if CADv == "2017":
                row[0] = str(row[7])
                row[1] = str(row[7])
                row[2] = str(row[7])
                row[3] = "PTO-ANEM-SYM"
                row[4] = "P-MET"
                cursor.updateRow(row)
            if CADv == "2018":
                row[0] = str(row[7])
                row[1] = str(row[7])
                row[2] = str(row[7])
                row[3] = "C-MET-SYMB"
                row[4] = "P-MET"
                cursor.updateRow(row)
else:
    if (q1, q2) == (False, False): # If there is a TurbineID field and there is a Primary Alternate Field
        print(field_names)
        with data.UpdateCursor(TA_Path, field_names) as cursor:
            for row in cursor:
                row[5] = Source
                if CADv == "2017":
                    if checkPri(row) == "primary":
                        row[0] = "T-" + str(row[7])
                        row[1] = "T-" + str(row[7])
                        row[2] = "T-" + str(row[7])
                        row[3] = "PTO-TRB-SYM"
                        row[4] = "P-TURB"
                        cursor.updateRow(row)
                    if checkPri(row) == "alternate":
                        row[0] = "ALT-" + str(row[7])
                        row[1] = "ALT-" + str(row[7])
                        row[2] = "ALT-" + str(row[7])
                        row[3] = "PTO-TRB-SYM-ALT"
                        row[4] = "P-TURB-ALT"
                        cursor.updateRow(row)
                    if checkPri(row) == "MET":
                        row[0] = "MET-" + str(row[7])
                        row[1] = "MET-" + str(row[7])
                        row[2] = "MET-" + str(row[7])
                        row[3] = "PTO-ANEM-SYM"
                        row[4] = "P-MET"
                        cursor.updateRow(row)
                if CADv == "2018":
                    if checkPri(row) == "primary":
                        row[0] = "T-" + str(row[7])
                        row[1] = "T-" + str(row[7])
                        row[2] = "T-" + str(row[7])
                        row[3] = "C-TURB-SYMB"
                        row[4] = "P-TURB"
                        cursor.updateRow(row)
                    if checkPri(row) == "alternate":
                        row[0] = "ALT-" + str(row[7])
                        row[1] = "ALT-" + str(row[7])
                        row[2] = "ALT-" + str(row[7])
                        row[3] = "C-TURB-SYMB-ALT"
                        row[4] = "P-TURB-ALT"
                        cursor.updateRow(row)
                    if checkPri(row) == "MET":
                        row[0] = str(row[7])
                        row[1] = str(row[7])
                        row[2] = str(row[7])
                        row[3] = "C-MET-SYMB"
                        row[4] = "P-MET"
                        cursor.updateRow(row)
    # If there is just a turbineID field
    if (q1,q2) == (True, False):
        arcpy.AddMessage("No Primary Alternate Feild provided, Turbine Type determined by TurbineID feild")
        with data.UpdateCursor(TA_Path, field_names) as cursor:
            for row in cursor:
                row[5] = Source
                if CADv == "2017":
                    if checkID(row) == "primary":
                        row[0] = "T-" + str(row[6])
                        row[1] = "T-" + str(row[6])
                        row[2] = "T-" + str(row[6])
                        row[3] = "PTO-TRB-SYM"
                        row[4] = "P-TURB"
                        cursor.updateRow(row)
                    if checkID(row) == "alternate":
                        row[0] = "ALT-" + str(extractdigits(row[6]))
                        row[1] = "ALT-" + str(extractdigits(row[6]))
                        row[2] = "ALT-" + str(extractdigits(row[6]))
                        row[3] = "PTO-TRB-SYM-ALT"
                        row[4] = "P-TURB-ALT"
                        cursor.updateRow(row)
                    if checkID(row) == "MET":
                        row[0] = "MET-" + str(extractdigits(row[6]))
                        row[1] = "MET-" + str(extractdigits(row[6]))
                        row[2] = "MET-" + str(extractdigits(row[6]))
                        row[3] = "PTO-ANEM-SYM"
                        row[4] = "P-MET"
                        cursor.updateRow(row)
                if CADv == "2018":
                    if checkID(row) == "primary":
                        row[0] = "T-" + str(row[6])
                        row[1] = "T-" + str(row[6])
                        row[2] = "T-" + str(row[6])
                        row[3] = "C-TURB-SYMB"
                        row[4] = "P-TURB"
                        cursor.updateRow(row)
                    if checkID(row) == "alternate":
                        row[0] = "ALT-" + str(extractdigits(row[6]))
                        row[1] = "ALT-" + str(extractdigits(row[6]))
                        row[2] = "ALT-" + str(extractdigits(row[6]))
                        row[3] = "C-TURB-SYMB-ALT"
                        row[4] = "P-TURB-ALT"
                        cursor.updateRow(row)
                    if checkID(row) == "MET":
                        row[0] = "MET-" + str(extractdigits(row[6]))
                        row[1] = "MET-" + str(extractdigits(row[6]))
                        row[2] = "MET-" + str(extractdigits(row[6]))
                        row[3] = "C-MET-SYMB"
                        row[4] = "P-MET"
                        cursor.updateRow(row)
    # if niether fields are given
    if (q1,q2) == (True, True):
        arcpy.AddMessage("No Turbine ID Field or Primary/Alternate Field given. Fields Created, but table not populated")
