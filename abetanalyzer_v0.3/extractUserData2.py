import sqlite3


def extractUserData2(currentDB, input1, extractSet, extractIDs, extractDAYS, extractSch, extractComp):
    print(('Extracting user-defined data ') + str('from ') + str(currentDB) + ('\n'))
    loop = 0
    loopy = 0
    SIDs = 0
    conn = sqlite3.connect(currentDB, isolation_level=None, timeout=10)
    c = conn.cursor()
    c.execute("PRAGMA TEMP_STORE = OFF")
    c.execute("PRAGMA SYNCHRONOUS = OFF")
    c.execute("PRAGMA JOURNAL_MODE = OFF")
    c.execute('DROP TABLE IF EXISTS tbl_data2')
    c.execute('DROP TABLE IF EXISTS TempTable')
    c.execute('DROP TABLE IF EXISTS TempTable2')
    c.execute('DROP TABLE IF EXISTS ALL_DATA')
    c.execute("CREATE TABLE tbl_data2 (SID integer, DTime integer, DAuto integer, DEvent integer, DEventText integer, DEffectText integer, DAltText integer, DGroup integer, DArgCount integer, DText1 integer, DValue1 integer, DText2 integer, DValue2 integer, DText3 integer, DValue3 integer, DText4 integer, DValue4 integer, DText5 integer, DValue5 integer)")
    c.execute("CREATE TABLE TempTable (SID integer, NName text, NValue text, ExpDay text)")
    c.execute("CREATE TABLE TempTable2 (SID integer)")

    # User has choose to analyse based on animal ID
    if extractSet == 1: 
        if len(extractIDs) == 1:
            relevantSID = c.execute("SELECT SID FROM tbl_Schedule_Notes WHERE NName = 'Animal ID' AND NValue = ?", (extractIDs))
            relevantSID = relevantSID.fetchall()
            for i in relevantSID:
                currSID = relevantSID[loop]
                c.execute("INSERT INTO tbl_data2 SELECT * FROM tbl_data WHERE SID = ?", (currSID))
                loop += 1
        if len(extractIDs) > 1:
            for i in extractIDs:
                currID = extractIDs[loop]
                relevantSID = c.execute("SELECT SID FROM tbl_Schedule_Notes WHERE NName = 'Animal ID' AND NValue = ?", (currID,))
                relevantSID = relevantSID.fetchall()
                for i in relevantSID:
                    currSID = relevantSID[loopy]
                    c.execute("INSERT INTO tbl_data2 SELECT * FROM tbl_data WHERE SID = ?", (currSID))
                    loopy += 1
                loopy = 0
                loop += 1

    # User has choose to analyse based on dates
    if extractSet == 2:
        c.execute("ALTER TABLE tbl_Schedule_Notes ADD COLUMN 'ExpDay' 'TEXT'")
        c.execute("UPDATE tbl_Schedule_Notes SET ExpDay = SUBSTR(NValue, 1,10) WHERE NName = 'Schedule_Start_Time'")
        if input1 == 1: # User has choose to analyse based on date range
            firstday = extractDAYS[0]
            lastday = extractDAYS[1]
            relevantSID = c.execute("SELECT SID FROM tbl_Schedule_Notes WHERE NName = ? AND ExpDay BETWEEN ? AND ?", (str('Schedule_Start_Time'), str(firstday), str(lastday)))
            relevantSID = relevantSID.fetchall()
            for i in relevantSID:
                currSID = relevantSID[loop]
                c.execute("INSERT INTO tbl_data2 SELECT * FROM tbl_data WHERE SID = ?", (currSID))
                loop += 1
        if input1 == 2: # User has choose to analyse based individual days
            for i in extractDAYS:
                currentDay = extractDAYS[loop]
                relevantSID = c.execute("SELECT SID FROM tbl_Schedule_Notes WHERE ExpDay = ?", (currentDay,))
                relevantSID = relevantSID.fetchall()
                for i in relevantSID:
                    currDay = relevantSID[loopy]
                    currDay = int(currDay[0])
                    c.execute("INSERT INTO tbl_data2 SELECT * FROM tbl_data WHERE SID = ?", (currDay,))
                    loopy += 1


    # User has choose to analyse based on IDs and dates
    if extractSet == 3:
        c.execute("ALTER TABLE tbl_Schedule_Notes ADD COLUMN 'ExpDay' 'TEXT'")
        c.execute("UPDATE tbl_Schedule_Notes SET ExpDay = SUBSTR(NValue, 1,10) WHERE NName = 'Schedule_Start_Time'")
        if input1 == 1:  # User has choose to analyse based on date range
            for i in extractIDs:
                if len(extractIDs) == 1:
                    currID = extractIDs[0]
                if len(extractIDs) > 1:
                    currID = extractIDs[loopy]
                firstday = extractDAYS[0]
                lastday = extractDAYS[1]
                c.execute("INSERT INTO TempTable SELECT * FROM tbl_Schedule_Notes WHERE ExpDay BETWEEN ? AND ?", (str(firstday), str(lastday)))
                relevantDays = c.execute("SELECT SID FROM TempTable")
                relevantDays = relevantDays.fetchall()
                for i in relevantDays:
                    currSID = relevantDays[loop]
                    currSID = currSID[0]
                    c.execute("INSERT INTO TempTable2 SELECT SID FROM tbl_Schedule_Notes WHERE SID = ? AND NName = ? AND NValue = ?", (currSID, str('Animal ID'), currID))
                    loop += 1
                loop = 0
                relevantSID = c.execute("SELECT * FROM TempTable2")
                relevantSID = relevantSID.fetchall()
                for i in relevantSID:
                    currSID = relevantSID[loop]
                    c.execute("INSERT INTO tbl_data2 SELECT * FROM tbl_data WHERE SID = ?", (currSID))
                    loop += 1
                loop = 0
                loopy += 1

        if input1 == 2:  # User has choose to analyse based on individual days
            for i in extractIDs:
                if len(extractIDs) == 1:
                    currID = extractIDs[0]
                if len(extractIDs) > 1:
                    currID = extractIDs[loopy]
                for i in extractDAYS:
                    currDay = extractDAYS[loop]
                    c.execute("INSERT INTO TempTable SELECT * FROM tbl_Schedule_Notes WHERE ExpDay =?", (currDay,))
                    loop += 1
                loop = 0
                relevantDays = c.execute("SELECT SID FROM TempTable")
                relevantDays = relevantDays.fetchall()
                for i in relevantDays:
                    currSID = relevantDays[loop]
                    currSID = currSID[0]
                    c.execute("INSERT INTO TempTable2 SELECT SID FROM tbl_Schedule_Notes WHERE SID = ? AND NName = ? AND NValue = ?", (currSID, str('Animal ID'), currID))
                    loop += 1
                loop = 0
                relevantSID = c.execute("SELECT * FROM TempTable2")
                relevantSID = relevantSID.fetchall()
                for i in relevantSID:
                    currSID = relevantSID[loop]
                    c.execute("INSERT INTO tbl_data2 SELECT * FROM tbl_data WHERE SID = ?", (currSID))
                    loop += 1
                loop = 0
                loopy += 1
    
    
    # User has choose to analyse based on Schedule Name
    if extractSet == 4:
        if len(extractSch) == 1:
            relevantSID = c.execute("SELECT SID FROM tbl_Schedules WHERE SName = ?", (extractSch))
            relevantSID = relevantSID.fetchall()
            for i in relevantSID:
                currSID = relevantSID[loop]
                c.execute("INSERT INTO tbl_data2 SELECT * FROM tbl_data WHERE SID = ?", (currSID))
                loop += 1
        if len(extractSch) > 1:
            for i in extractSch:
                currSch = extractSch[loopy]
                relevantSID = c.execute("SELECT SID FROM tbl_Schedules WHERE SName = ?", (currSch,))
                relevantSID = relevantSID.fetchall()
                for i in relevantSID:
                    currSID = relevantSID[loop]
                    c.execute("INSERT INTO tbl_data2 SELECT * FROM tbl_data WHERE SID = ?", (currSID))
                    loop += 1
                loop = 0
                loopy += 1


    # User has choose to analyse based on Computer Name
    if extractSet == 5:
        if len(extractComp) == 1:
            relevantSID = c.execute("SELECT SID FROM tbl_Schedules WHERE SMachineName = ?", (extractComp))
            relevantSID = relevantSID.fetchall()
            for i in relevantSID:
                currSID = relevantSID[loop]
                c.execute("INSERT INTO tbl_data2 SELECT * FROM tbl_data WHERE SID = ?", (currSID))
                loop += 1
        if len(extractComp) > 1:
            for i in extractComp:
                extractComp = extractComp[loopy]
                relevantSID = c.execute("SELECT SID FROM tbl_Schedules WHERE SMachineName = ?", (extractComp,))
                relevantSID = relevantSID.fetchall()
                for i in relevantSID:
                    currSID = relevantSID[loop]
                    c.execute("INSERT INTO tbl_data2 SELECT * FROM tbl_data WHERE SID = ?", (currSID))
                    loop += 1
                loop = 0
                loopy += 1

    if extractSet == 6:
        SIDs = 1

    if extractSet < 6:
        c.execute("ALTER TABLE tbl_data RENAME TO ALL_DATA")
        c.execute("ALTER TABLE tbl_data2 RENAME TO tbl_data")

    c.execute('DROP TABLE IF EXISTS TempTable')
    c.execute('DROP TABLE IF EXISTS TempTable2')


    
    conn.commit()
    conn.execute("VACUUM")
    conn.close()

    return SIDs



