import os
import glob
import csv
import copy
import re
import datetime

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def get_TSV_list(source_path):
    with open(source_path,"rt",encoding = 'iso-8859-1') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        tsvlist = list(tsvreader)
        return tsvlist

def list_to_String(list):
    d=','
    return d.join(list)

def VAfile_to_Colrow (textpath):
    # assumes input file at textpath is in format
    # MRN,09/15/2010,Snellen - Linear,VA - Method,1
    # MRN,10/18/2010,Glasses,VA - Correction,1
    # MRN,09/21/2009,CF x 5,VA - Right Distance CC,1
    # MRN,10/18/2010,CF at 2',VA - Right Distance CC,1
    # load txt file into allrows(list) and separate into header and datarows
    newdatarows = []
    header = "PAT_MRN_ID, CONTACT_DATE, EXAM_CODE, EXAM_VALUE, EXAM_Method, Correction"
    if os.path.exists(textpath):

        f = open(textpath, "r",encoding = 'iso-8859-1')
        readfile = csv.reader(f)
        allrows = list(readfile)
        f.close()
        if len(allrows) > 1:
            datarows = allrows[1:]
        else:
            return header, newdatarows

    # convert to dashes datetimes, place quotation marks
    date_indices = [1]
    freeText_indices = [2]
    for i in range(len(datarows)):

        # converting the data String to d/m/y,  converting the data String to d/m/y
        for date_index in date_indices:
            datarows[i][date_index] = datarows[i][date_index].replace("/", "-")
        for freeText_index in freeText_indices:
            datarows[i][freeText_index] = '"' +datarows[i][freeText_index] + '"'
        for j in range(len(datarows[i])):
            datarows[i][j] = datarows[i][j].lower()
            if datarows[i][j] == "":
                datarows[i][j] = '""'
    # sort the list of data by their dates using 2nd index as lambda key
    sortedrows = sorted(datarows, key=lambda rows: datetime.datetime.strptime(rows[1], '%m-%d-%Y'))
    # create newdatarows
    temprow = []

    PAT_MRN_ID =  sortedrows[0][0]

    Acuity_Method, Correction = "",""
    current_date = sortedrows[0][1]
    RVA,LVA = "",""
    R_EXAM_CODE,L_EXAM_CODE = "",""

    for i in range(len(sortedrows)):

        if sortedrows[i][1] != current_date:
            # initiate appending / resetting variables protocol
            if RVA != "":
                #build right vision row
                temprow.append(PAT_MRN_ID)
                temprow.append(current_date)
                temprow.append(R_EXAM_CODE)
                temprow.append(RVA)
                temprow.append(Acuity_Method)
                temprow.append(Correction)
                #appendrow to final datalist
                newdatarows.append(temprow)
                #reset temprow
                temprow = []

            if LVA != "":
                #build right vision row
                temprow.append(PAT_MRN_ID)
                temprow.append(current_date)
                temprow.append(L_EXAM_CODE)
                temprow.append(LVA)
                temprow.append(Acuity_Method)
                temprow.append(Correction)
                #appendrow to final datalist
                newdatarows.append(temprow)
                #reset temprow
                temprow = []

            # reset variable and set current date to new in prep for next set
            Acuity_Method, Correction = "",""
            current_date = sortedrows[i][1]
            RVA,LVA = "",""
            R_EXAM_CODE,L_EXAM_CODE = "",""

        if "method" in sortedrows[i][3]:
            Acuity_Method = sortedrows[i][2]
        if "correction" in sortedrows[i][3]:
            Correction = sortedrows[i][2]
        if "right" in sortedrows[i][3] and not "+-" in sortedrows[i][3]  and not "ni" in sortedrows[i][2]:
            RVA = sortedrows[i][2]
            R_EXAM_CODE = sortedrows[i][3]
        if "left" in sortedrows[i][3] and not "+-" in sortedrows[i][3]  and not "ni" in sortedrows[i][2]:
            LVA = sortedrows[i][2]
            L_EXAM_CODE = sortedrows[i][3]
        if ("right" in sortedrows[i][3] and "ph" in sortedrows[i][3] and not "+-" in sortedrows[i][3]
            and not "ni" in sortedrows[i][2]):
            RVA = sortedrows[i][2]
            R_EXAM_CODE = sortedrows[i][3]
        if ("left" in sortedrows[i][3] and "ph" in sortedrows[i][3] and not "+-" in sortedrows[i][3]
            and not "ni" in sortedrows[i][2]):
            LVA = sortedrows[i][2]
            L_EXAM_CODE = sortedrows[i][3]
        if ("right" in sortedrows[i][3] and "cc" in sortedrows[i][3] and not "+-" in sortedrows[i][3]
            and not "ni" in sortedrows[i][2]):
            RVA = sortedrows[i][2]
            R_EXAM_CODE = sortedrows[i][3]
        if ("left" in sortedrows[i][3] and "cc" in sortedrows[i][3] and not "+-" in sortedrows[i][3]
            and not "ni" in sortedrows[i][2]):
            LVA = sortedrows[i][2]
            L_EXAM_CODE = sortedrows[i][3]
        if ("right" in sortedrows[i][3] and "cc" in sortedrows[i][3]  and "ph" in sortedrows[i][3]
            and not "+-" in sortedrows[i][3] and not "ni" in sortedrows[i][2]):
            RVA = sortedrows[i][2]
            R_EXAM_CODE = sortedrows[i][3]
        if ("left" in sortedrows[i][3] and "cc" in sortedrows[i][3] and "ph" in sortedrows[i][3]
            and not "+-" in sortedrows[i][3] and not "ni" in sortedrows[i][2]):
            LVA = sortedrows[i][2]
            L_EXAM_CODE = sortedrows[i][3]

    return header, newdatarows

def IOPfile_to_Colrow (textpath):
    # load txt file into allrows(list) and separate into header and datarows
    # assumes file at textpath has format:
    # MRN,10/04/2010,Tonopen,Tonometry - Method,1
    # MRN,01/05/2010,15,intraocular pressure - right,1
    # MRN,12/03/2010,Applanation,Tonometry - Method,1
    # MRN,06/04/2013,15,intraocular pressure - left,1
    # MRN,08/13/2010,17,intraocular pressure - left,1
    # MRN,06/04/2013,11:33 AM,Tonometry - Time,1

    newdatarows = []
    header = "PAT_MRN_ID, CONTACT_DATE, EXAM_CODE, EXAM_VALUE, Tonometry_Method, Tonometry_Time"
    if os.path.exists(textpath):
        f = open(textpath, "r",encoding = 'iso-8859-1')
        readfile = csv.reader(f)
        allrows = list(readfile)
        f.close()
        if len(allrows) > 1:
            datarows = allrows[1:]
        else:
            return header, newdatarows
    # convert to dashes datetimes, place quotation marks, converting the data String to d/m/y
    date_indices = [1]
    freeText_indices = [2]
    for i in range(len(datarows)):

        for date_index in date_indices:
            datarows[i][date_index] = datarows[i][date_index].replace("/", "-")
        for freeText_index in freeText_indices:
            datarows[i][freeText_index] = '"' +datarows[i][freeText_index] + '"'
        for j in range(len(datarows[i])):
            if datarows[i][j] == "":
                datarows[i][j] = '""'

    # sort the list of data by their dates using 2nd index as lambda key
    sortedrows = sorted(datarows, key=lambda rows: datetime.datetime.strptime(rows[1], '%m-%d-%Y'))

    # create newdatarows
    temprow = []
    # PAT_MRN_ID, CONTACT_DATE, EXAM_CODE, EXAM_VALUE, Tonometry_Method, Tonometry_Time

    PAT_MRN_ID =  sortedrows[0][0]
    
    Tonometry_Method, Tonometry_Time = "",""
    current_date = sortedrows[0][1]
    RIOP,LIOP = "",""
    R_EXAM_CODE,L_EXAM_CODE = "",""

    for i in range(len(sortedrows)):
        if sortedrows[i][1] != current_date:
            # initiate appending / resetting variables protocol
            if RIOP != "":
                #build right vision row
                temprow.append(PAT_MRN_ID)
                temprow.append(current_date)
                temprow.append(R_EXAM_CODE)
                temprow.append(RIOP)
                temprow.append(Tonometry_Method)
                temprow.append(Tonometry_Time)
                #appendrow to final datalist
                newdatarows.append(temprow)
                #reset temprow
                temprow = []

            if LIOP != "":
                #build right vision row
                temprow.append(PAT_MRN_ID)
                temprow.append(current_date)
                temprow.append(L_EXAM_CODE)
                temprow.append(LIOP)
                temprow.append(Tonometry_Method)
                temprow.append(Tonometry_Time)
                #appendrow to final datalist
                newdatarows.append(temprow)
                #reset temprow
                temprow = []

            # reset variable and set current date to new in prep for next set
            Tonometry_Method, Tonometry_Time = "",""
            current_date = sortedrows[i][1]
            RIOP,LIOP = "",""
            R_EXAM_CODE,L_EXAM_CODE = "",""

        if "Method" in sortedrows[i][3]:
            Tonometry_Method = sortedrows[i][2]
        if "Time" in sortedrows[i][3]:
            Tonometry_Time = sortedrows[i][2]
        if "right" in sortedrows[i][3]:
            RIOP = sortedrows[i][2]
            R_EXAM_CODE = sortedrows[i][3]
        if "left" in sortedrows[i][3]:
            LIOP = sortedrows[i][2]
            L_EXAM_CODE = sortedrows[i][3]

    return header, newdatarows

def delete_files(filename,population_folder):
    dirs = get_immediate_subdirectories(population_folder)
    for MRN in dirs:
        deletefolder = folderpath + str(MRN) + '/' + filename
        if os.path.exists(deletefolder):
            os.remove(deletefolder)
