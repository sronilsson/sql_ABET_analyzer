import sqlite3
import os
import csv
import shutil
import subprocess
import time



def createSQLiteDBs(): #CONVERT ABETdb to csv, convert relevant CSVs to mdb.
    print('\n' + 'Searching for ABET databases and re-formatting ABET databases into SQLite format... ' + '\n')
    fileName = []
    workingDir = os.getcwd()
    loop = 0
    DBsFound = []
    for i in os.listdir(os.curdir):                             #find file names
        if i.__contains__(".ABETdb"):
            fileName.append(i)
    for i in fileName:                                          #convert each found file to csv files and place them in folder
        Pcommand = "bash mdb-export-all.sh " + i
        p = subprocess.Popen(Pcommand, stdout = subprocess.PIPE, close_fds = True, shell = True)
        stdout, stderr = p.communicate()
    for i in fileName:                                          #move the files to the main folder, and convert each batch of relevant csv files a single .mdb file
        folderName, fileExt = fileName[loop].split(".")
        folderName = str(folderName) + str('/')
        file1, file2, file3, file4 = (str(folderName) + str('tbl_Data.csv')), (str(folderName) + str('tbl_Schedules.csv')), (str(folderName) + str('tbl_Schedule_Notes.csv')), str(folderName) + str('tbl_Version.csv')
        shutil.copy2(file1, 'tbl_Data.csv')
        shutil.copy2(file2, 'tbl_Schedules.csv')
        shutil.copy2(file3, 'tbl_Schedule_Notes.csv')
        shutil.copy2(file4, 'tbl_Version.csv')
        dbName, dbExt = fileName[loop].split('.')
        folderRM = dbName
        dbName = dbName + str('.db')
        DBsFound.append(dbName)
        conn = sqlite3.connect(dbName, isolation_level=None, timeout=10)
        c = conn.cursor()
        c.execute("CREATE TABLE tbl_Data (SID integer, DTime integer, DAuto integer, DEvent integer, DEventText integer, DEffectText integer, DAltText integer, DGroup integer, DArgCount integer, DText1 integer, DValue1 integer, DText2 integer, DValue2 integer, DText3 integer, DValue3 integer, DText4 integer, DValue4 integer, DText5 integer, DValue5 integer)")
        c.execute("CREATE TABLE tbl_Schedules (SID integer,SName text, SEnviro text,SMachineName text,SVersion integer,SRunDate text,SFinal integer,ZE_GUID integer,ZS_GUID integer,SRecCount integer)")
        c.execute("CREATE TABLE tbl_Schedule_Notes (SID integer,NName integer,NValue integer)")
        c.execute("CREATE TABLE tbl_Version (BuildNum integer,CompactDate integer)")
        with open('tbl_Data.csv', 'r') as f:
            dr = csv.DictReader(f)
            to_tbl_data = [(i['SID'], i['DTime'], i['DAuto'], i['DEvent'],i['DEventText'], i['DEffectText'],i['DAltText'], i['DGroup'], i['DArgCount'], i['DText1'],i['DValue1'],i['DText2'],i['DValue2'],i['DText3'], i['DValue3'], i['DText4'],i['DValue4'],i['DText5'], i['DValue5']) for i in dr]
        with open('tbl_Schedules.csv', 'r') as f:
            dr = csv.DictReader(f)
            to_tbl_Schedules = [(i['SID'], i['SName'], i['SEnviro'], i['SMachineName'],i['SRunDate'], i['SFinal'],i['ZE_GUID'], i['ZS_GUID'], i['SRecCount']) for i in dr]
        with open('tbl_Schedule_Notes.csv', 'r') as f:
            dr = csv.DictReader(f)
            to_tbl_Schedule_Notes = [(i['SID'], i['NName'], i['NValue']) for i in dr]
        with open('tbl_Version.csv', 'r') as f:
            dr = csv.DictReader(f)
            to_tbl_Version = [(i['BuildNum'], i['CompactDate']) for i in dr]
        c.executemany("INSERT INTO tbl_Data (SID, DTime, DAuto, DEvent, DEventText, DEffectText, DAltText, DGroup, DArgCount, DText1, DValue1, DText2, DValue2, DText3, DValue3, DText4, DValue4, DText5, DValue5) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", to_tbl_data)
        c.executemany("INSERT INTO tbl_Schedules (SID, SName, SEnviro, SMachineName, SRunDate, SFinal, ZE_GUID, ZS_GUID, SRecCount) VALUES (?,?,?,?,?,?,?,?,?);", to_tbl_Schedules)
        c.executemany("INSERT INTO tbl_Schedule_Notes (SID, NName, NValue) VALUES (?,?,?);", to_tbl_Schedule_Notes)
        c.executemany("INSERT INTO tbl_Version (BuildNum, CompactDate) VALUES (?,?);", to_tbl_Version)
        loop += 1
        conn.commit()

        #REMOVE CSV FILES AND FOLDERS
        shutil.rmtree(folderRM)
        files = os.listdir(workingDir)
        for item in files:
            if item.endswith(".csv"):
                os.remove(os.path.join(workingDir, item))
        time.sleep(1)

    conn.commit()
    conn.execute("VACUUM")
    conn.close()

    return DBsFound

