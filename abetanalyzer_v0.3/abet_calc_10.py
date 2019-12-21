import sqlite3
import os
import time

from calc2 import calc2
from userDefinitions2 import userDefinitions2
from extractUserData2 import extractUserData2
from createSQLiteDBs import createSQLiteDBs
from summary import summaryPres
from remSess import remSess
from sortCSVfile import sortCSVfile

loop = 0
DBs = []
extractIDs = []
extractDAYS = []
extractSch = []
extractComp = []
extractSet = 0
input1 = 0
perfFunc = 0
filesFound = []
dataBasesProcessed = 0

perfFunc, input1, extractSet, extractIDs, extractDAYS, extractSch, extractComp = userDefinitions2(perfFunc, input1, extractSet, extractIDs, extractDAYS, extractSch, extractComp)


if (perfFunc == 1 or perfFunc == 2):
    DBsFound = createSQLiteDBs()
    DBsFound = sorted(DBsFound)
    DB1 = DBsFound[0]
    print ('Databases organised...' + '\n')

if (perfFunc == 3):
    print ('Searching for available databases... ' + ('\n'))
    DBsFound = []
    for i in os.listdir(os.curdir):  # find file names
        if i.__contains__(".db"):
            filesFound.append(i)
    DBsFound = sorted(filesFound)
    DB1 = filesFound[0]
    print ('The following databases where found:')
    for i in DBsFound:
        print(i)
    print('\n')

if perfFunc == 1 or perfFunc == 3:
    for i in DBsFound:
        currentDB = i
        print ('Processing ' + str(currentDB) + str('...') + ('\n'))
        conn = sqlite3.connect(currentDB, isolation_level=None, timeout=10)
        c = conn.cursor()
        c.execute("PRAGMA TEMP_STORE = OFF")
        c.execute("PRAGMA SYNCHRONOUS = OFF")
        c.execute("PRAGMA JOURNAL_MODE = DELETE")

        if dataBasesProcessed != 0:
            c.execute("UPDATE tbl_Data SET SID = SID + :highestSID", {"highestSID": highestSID})
            c.execute("UPDATE tbl_Schedule_Notes SET SID = SID + :highestSID", {"highestSID": highestSID})
            c.execute("UPDATE tbl_Schedules SET SID = SID + :highestSID", {"highestSID": highestSID})

        ## COUNT TOTAL SESSIONS
        schTable = c.execute("SELECT * FROM tbl_Schedules")
        schTable = schTable.fetchall()
        sessions = len(schTable)
        conn.commit()

        SIDs = extractUserData2(currentDB, input1, extractSet, extractIDs, extractDAYS, extractSch, extractComp)

        highestSID = c.execute("SELECT MAX(SID) FROM tbl_data")
        highestSID = highestSID.fetchone()
        highestSID = highestSID[0]

        calc2(currentDB, SIDs)
        
        dataBasesProcessed += 1
        time.sleep(5)
        conn.execute("VACUUM")
        conn.commit()

    # ATTACH ALL DATABASES
    conn = sqlite3.connect('DataOutput', isolation_level=None, timeout=10)
    c.execute("PRAGMA TEMP_STORE = OFF")
    c.execute("PRAGMA SYNCHRONOUS = OFF")
    c.execute("PRAGMA JOURNAL_MODE = DELETE")
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS Summary')
    c.execute('DROP TABLE IF EXISTS Strategy_Indications')
    c.execute('DROP TABLE IF EXISTS Bins_5min_HR')
    c.execute('DROP TABLE IF EXISTS Bins_5min_FAR')
    c.execute('DROP TABLE IF EXISTS Bins_5min_Dprime')
    c.execute('DROP TABLE IF EXISTS Bins_5min_C')
    c.execute('DROP TABLE IF EXISTS Bins_5min_ISI_touch')
    c.execute('DROP TABLE IF EXISTS Summary_correction_included')
    c.execute('DROP TABLE IF EXISTS FAR_each_Stimulus')
    c.execute("CREATE TABLE Summary (AnimalID text, SID integer, ExpDate text, Schedule text, Machine text, SessionLength integer, Hits text, Misses text, FalseAlarms text, CorrectRejections text, ISItouches text, HR integer, FAR integer, dprime integer, criterion integer, meanResponseLatency integer, meanCorrectLatency integer, meanIncorrectLatency integer, meanRetrievalLatency integer, MagEntries integer, FrontBeamBreaks integer, BackBeamBreaks integer)")
    c.execute("CREATE TABLE Summary_correction_included (AnimalID text, SID integer, ExpDate text, Schedule text, Machine text, SessionLength integer, Hits text, Misses text, FalseAlarms text, CorrectRejections text, ISItouches text, HR integer, FAR integer, dprime integer, criterion integer, beta integer, SI integer, RI integer)")
    c.execute("CREATE TABLE Strategy_Indications (AnimalID text, SID integer, ExpDate text, Schedule text, Machine text, Mean_Time_Between_Hits integer, STDEV_Time_Between_Hits integer, MAX_Time_Between_Hits integer, Mean_Time_Bout_No_Stimuli_Responses integer, STDEV_Time_Bout_No_Stimuli_Responses integer, MAX_Time_Bout_No_Stimuli_Responses integer, Mean_Trial_Bout_No_Stimuli_Responses integer, STDEV_Trial_Bout_No_Stimuli_Responses integer, MAX_Trial_Bout_No_Stimuli_Responses integer, Mean_False_Alarm_bout_trial_length integer, STDEV_False_Alarm_bout_trial_length integer, MAX_False_Alarm_bout_trial_length integer, Mean_Hit_bout_trial_length integer, STDEV_Hit_bout_trial_length integer, MAX_Hit_bout_trial_length integer, Mean_Retreival_FBeam_Time integer, STDEV_Retreival_FBeam_Time integer, MAX_Retreival_FBeam_Time integer)")
    c.execute("CREATE TABLE Bins_5min_HR (AnimalID text, SID integer, ExpDate text, Schedule text, Machine text, Bin1 integer, Bin2 integer, Bin3 integer, Bin4 integer, Bin5 integer, Bin6 integer, Bin7 integer, Bin8 integer, Bin9 integer, Bin10 integer, Bin11 integer, Bin12 integer)")
    c.execute("CREATE TABLE Bins_5min_FAR (AnimalID text, SID integer, ExpDate text, Schedule text, Machine text, Bin1 integer, Bin2 integer, Bin3 integer, Bin4 integer, Bin5 integer, Bin6 integer, Bin7 integer, Bin8 integer, Bin9 integer, Bin10 integer, Bin11 integer, Bin12 integer)")
    c.execute("CREATE TABLE Bins_5min_Dprime (AnimalID text, SID integer, ExpDate text, Schedule text, Machine text, Bin1 integer, Bin2 integer, Bin3 integer, Bin4 integer, Bin5 integer, Bin6 integer, Bin7 integer, Bin8 integer, Bin9 integer, Bin10 integer, Bin11 integer, Bin12 integer)")
    c.execute("CREATE TABLE Bins_5min_C (AnimalID text, SID integer, ExpDate text, Schedule text, Machine text, Bin1 integer, Bin2 integer, Bin3 integer, Bin4 integer, Bin5 integer, Bin6 integer, Bin7 integer, Bin8 integer, Bin9 integer, Bin10 integer, Bin11 integer, Bin12 integer)")
    c.execute("CREATE TABLE Bins_5min_ISI_touch (AnimalID text, SID integer, ExpDate text, Schedule text, Machine text, Bin1 integer, Bin2 integer, Bin3 integer, Bin4 integer, Bin5 integer, Bin6 integer, Bin7 integer, Bin8 integer, Bin9 integer, Bin10 integer, Bin11 integer, Bin12 integer)")
    c.execute("CREATE TABLE FAR_each_Stimulus (AnimalID text, SID integer, ExpDate text, Schedule text, Machine text, FAR_Stim1_2 integer, FAR_Stim3 integer, FAR_Stim4 integer, FAR_Stim5 integer)")

    DBsAttach = DBsFound
    for i in DBsAttach:
        currentDB = str(DBsAttach[loop])
        currentDBname = str('DB') + str(loop)
        c.execute('ATTACH DATABASE ? AS ?', (currentDB,currentDBname))
        loop += 1
    conn.commit()
    loop = 0
    
    for i in DBsAttach: # COMBINE ALL SUMMARY TABLES
        currentDBname = str('DB') + str(loop)
        currentTableName = str(currentDBname) + str('.') + str('Summary')
        c.execute("INSERT INTO Summary SELECT * FROM "+currentTableName+"")
        loop += 1

    loop = 0
    for i in DBsAttach: # COMBINE ALL STRATEGY INDICATIONS
        currentDBname = str('DB') + str(loop)
        currentTableName = str(currentDBname) + str('.') + str('Strategy_Indications')
        c.execute("INSERT INTO Strategy_Indications SELECT * FROM "+currentTableName+"")
        loop += 1

    loop = 0
    for i in DBsAttach: # COMBINE ALL Summary_correction_included
        currentDBname = str('DB') + str(loop)
        currentTableName = str(currentDBname) + str('.') + str('Summary_correction_included')
        c.execute("INSERT INTO Summary_correction_included SELECT * FROM "+currentTableName+"")
        loop += 1

    loop = 0
    for i in DBsAttach: # COMBINE ALL Bins_5min_HR
        currentDBname = str('DB') + str(loop)
        currentTableName = str(currentDBname) + str('.') + str('Bins_5min_HR')
        c.execute("INSERT INTO Bins_5min_HR SELECT * FROM "+currentTableName+"")
        loop += 1

    loop = 0
    for i in DBsAttach: # COMBINE ALL Bins_5min_FAR
        currentDBname = str('DB') + str(loop)
        currentTableName = str(currentDBname) + str('.') + str('Bins_5min_FAR')
        c.execute("INSERT INTO Bins_5min_FAR SELECT * FROM "+currentTableName+"")
        loop += 1

    loop = 0
    for i in DBsAttach: # COMBINE ALL Bins_5min_Dprime
        currentDBname = str('DB') + str(loop)
        currentTableName = str(currentDBname) + str('.') + str('Bins_5min_Dprime')
        c.execute("INSERT INTO Bins_5min_Dprime SELECT * FROM "+currentTableName+"")
        loop += 1

    loop = 0
    for i in DBsAttach: # COMBINE ALL Bins_5min_Cprime
        currentDBname = str('DB') + str(loop)
        currentTableName = str(currentDBname) + str('.') + str('Bins_5min_C')
        c.execute("INSERT INTO Bins_5min_C SELECT * FROM "+currentTableName+"")
        loop += 1

    loop = 0
    for i in DBsAttach: # COMBINE ALL Bins_5min_Cprime
        currentDBname = str('DB') + str(loop)
        currentTableName = str(currentDBname) + str('.') + str('Bins_5min_ISI_touch')
        c.execute("INSERT INTO Bins_5min_ISI_touch SELECT * FROM "+currentTableName+"")
        loop += 1

    loop = 0
    for i in DBsAttach: # COMBINE ALL FAR BY STIMULI
        currentDBname = str('DB') + str(loop)
        currentTableName = str(currentDBname) + str('.') + str('FAR_each_Stimulus')
        c.execute("INSERT INTO FAR_each_Stimulus SELECT * FROM "+currentTableName+"")
        loop += 1

    remSess()

    conn.commit()
    loop = 0
    c.execute('DROP TABLE IF EXISTS ALL_DATA')
    c.execute('DROP TABLE IF EXISTS tbl_Schedule_Notes')
    c.execute('DROP TABLE IF EXISTS tbl_Schedules')
    c.execute('DROP TABLE IF EXISTS tbl_Version')
    c.execute('DROP TABLE IF EXISTS tbl_Data')
    conn.commit()
    print ('Databases has merged into a Summery.db file...' + '\n')

    summaryPres()
    time.sleep(3)

    sortCSVfile()

    #DELETE ALL DBs except the Output db
    for i in DBsAttach:
        currentDB = str(DBsAttach[loop])
        os.remove(currentDB)
        loop += 1
        time.sleep(1)

    conn.execute("VACUUM")
    conn.commit()
    conn.close()
