import sqlite3


def remSess():
    conn = sqlite3.connect('DataOutput', isolation_level=None, timeout=10)
    c = conn.cursor()
    c.execute("PRAGMA TEMP_STORE = OFF")
    c.execute("PRAGMA SYNCHRONOUS = OFF")
    c.execute("PRAGMA JOURNAL_MODE = DELETE")

    #Sessions without HR,FAR, D, and C
    SID_no_responses = c.execute("SELECT SID FROM Summary WHERE (criterion = ? AND dprime = ? AND HR = ? AND FAR = ?) OR SessionLength < 2700", (str('0'), str('0'), str('0'), str('0')))
    SID_no_responses = SID_no_responses.fetchall()
    print (SID_no_responses)


    for i in SID_no_responses:
        currentSession = str(i[0])
        c.execute("DELETE FROM Summary WHERE SID = ?", (currentSession,))

    for i in SID_no_responses:
        currentSession = str(i[0])
        c.execute("DELETE FROM Strategy_Indications WHERE SID = ?", (currentSession,))

    for i in SID_no_responses:
        currentSession = str(i[0])
        c.execute("DELETE FROM Bins_5min_HR WHERE SID = ?", (currentSession,))

    for i in SID_no_responses:
        currentSession = str(i[0])
        c.execute("DELETE FROM Bins_5min_FAR WHERE SID = ?", (currentSession,))

    for i in SID_no_responses:
        currentSession = str(i[0])
        c.execute("DELETE FROM Bins_5min_Dprime WHERE SID = ?", (currentSession,))

    for i in SID_no_responses:
        currentSession = str(i[0])
        c.execute("DELETE FROM Bins_5min_C WHERE SID = ?", (currentSession,))

    for i in SID_no_responses:
        currentSession = str(i[0])
        c.execute("DELETE FROM Bins_5min_ISI_touch WHERE SID = ?", (currentSession,))

    for i in SID_no_responses:
        currentSession = str(i[0])
        c.execute("DELETE FROM FAR_each_Stimulus WHERE SID = ?", (currentSession,))


    conn.commit()
    conn.close()






