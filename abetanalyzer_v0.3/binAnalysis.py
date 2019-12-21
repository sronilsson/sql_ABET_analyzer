from __future__ import division
import sqlite3
from scipy.stats import norm
from math import exp, sqrt
import decimal
from scipy import stats
Z = norm.ppf

fiveBinsArray = [0, 300, 600, 900, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600]

def binAnalysis(currentSID, currentDB, animalID, date, scheduleName, machineName):
    fiveHRarray = []
    fiveFARarray = []
    fiveDarray = []
    fiveCarray = []
    fiveISIarray = []
    loop = 0
    conn = sqlite3.connect(currentDB, isolation_level=None, timeout=10)
    c = conn.cursor()
    c.execute("PRAGMA TEMP_STORE = OFF")
    c.execute("PRAGMA SYNCHRONOUS = OFF")
    c.execute("PRAGMA JOURNAL_MODE = OFF")

    bins5Min = (len(fiveBinsArray)) - 1

    # calculate hits
    for i in range(bins5Min):
        lowerBound = fiveBinsArray[loop]
        upperBound = (fiveBinsArray[loop + 1]) - 1

        fiveHits = c.execute("SELECT COUNT(*) FROM tbl_data WHERE SID = ? AND DEventText = ? AND DEffectText = ? AND (DTime > ? AND DTime < ?)", (currentSID, str('Condition Event'), str('Hit'), lowerBound, upperBound))
        fiveHits = fiveHits.fetchone()
        fiveHits = str(fiveHits[0])
        if fiveHits == 'None':
            fiveHits = 0
        fiveHits = int(fiveHits)

        fiveMisses = c.execute("SELECT COUNT(*) FROM tbl_data WHERE SID = ? AND DEventText = ? AND DEffectText = ? AND (DTime > ? AND DTime < ?)", (currentSID, str('Condition Event'), str('Missed Hit'), lowerBound, upperBound))
        fiveMisses = fiveMisses.fetchone()
        fiveMisses = str(fiveMisses[0])
        if fiveMisses == 'None':
            fiveMisses = 0
        fiveMisses = int(fiveMisses)

        fiveFAs = c.execute("SELECT COUNT(*) FROM tbl_data WHERE SID = ? AND DEventText = ? AND DEffectText = ? AND (DTime > ? AND DTime < ?)", (currentSID, str('Condition Event'), str('Mistake'), lowerBound, upperBound))
        fiveFAs = fiveFAs.fetchone()
        fiveFAs = str(fiveFAs[0])
        if fiveFAs == 'None':
            fiveFAs = 0
        fiveFAs = int(fiveFAs)

        fiveCRs = c.execute("SELECT COUNT(*) FROM tbl_data WHERE SID = ? AND DEventText = ? AND DEffectText = ? AND (DTime > ? AND DTime < ?)", (currentSID, str('Condition Event'), str('Correct Rejection'), lowerBound, upperBound))
        fiveCRs = fiveCRs.fetchone()
        fiveCRs = str(fiveCRs[0])
        if fiveCRs == 'None':
            fiveCRs = 0
        fiveCRs = int(fiveCRs)

        fiveISI = c.execute("SELECT COUNT(*) FROM tbl_data WHERE SID = ? AND DEventText = ? AND DEffectText = ? AND (DTime > ? AND DTime < ?)", (currentSID, str('Condition Event'), str('Correct Rejection'), lowerBound, upperBound))
        fiveISI = fiveISI.fetchone()
        fiveISI = str(fiveISI[0])
        if fiveISI == 'None':
            fiveISI = 0
        fiveISI = int(fiveISI)

        try:
            fiveHR = (fiveHits / (fiveHits + fiveMisses))
        except ZeroDivisionError:
            fiveHR = 0
        try:
            fiveFAR = (fiveFAs / (fiveFAs + fiveCRs))
        except ZeroDivisionError:
            fiveFAR = 0

        # Avoid d' infinity
        if fiveHR == 1:
            fiveHR = (fiveHits - 0.5) / (fiveHits + fiveMisses)
        if fiveHR == 0:
            if (fiveHits + fiveMisses) > 0:
                HR = (fiveHits + 0.5) / (fiveHits + fiveMisses)
            else:
                fiveHR = 0
        if fiveFAR == 1:
            fiveFAR = (fiveFAs - 0.5) / (fiveFAs + fiveCRs)
        if fiveFAR == 0:
            if (fiveFAs + fiveCRs) > 0:
                fiveFAR = (fiveFAs + 0.5) / (fiveFAs + fiveCRs)
            else:
                fiveFAR = 0

        if (fiveFAR != 0) and (fiveHR != 0):
            try:
                fiveDprime = (Z(fiveHR) - Z(fiveFAR))
            except (ZeroDivisionError):
                fiveDprime = 0
            try:
                fiveC = (-(Z(fiveHR) + Z(fiveFAR)) / 2)
            except (ZeroDivisionError):
                fiveC = 0

            fiveHR = round(fiveHR, 2)
            fiveFAR = round(fiveFAR, 2)
            fiveDprime = round(fiveDprime, 2)
            fiveC = round(fiveC, 2)

        else:
            fiveHR = fiveFAR = fiveDprime = fiveC = 0

        fiveHRarray.append(fiveHR)
        fiveFARarray.append(fiveFAR)
        fiveDarray.append(fiveDprime)
        fiveCarray.append(fiveC)
        fiveISIarray.append(fiveISI)

        loop += 1

    conn.commit()
    conn.close()

    return fiveHRarray[0], fiveHRarray[1], fiveHRarray[2], fiveHRarray[3], fiveHRarray[4], fiveHRarray[5], fiveHRarray[6], fiveHRarray[7], fiveHRarray[8], fiveHRarray[9], fiveHRarray[10], fiveHRarray[11], fiveFARarray[0], fiveFARarray[1], fiveFARarray[2],fiveFARarray[3], fiveFARarray[4], fiveFARarray[5], fiveFARarray[6], fiveFARarray[7], fiveFARarray[8], fiveFARarray[9], fiveFARarray[10], fiveFARarray[11], fiveDarray[0], fiveDarray[1], fiveDarray[2], fiveDarray[3], fiveDarray[4], fiveDarray[5], fiveDarray[6], fiveDarray[7], fiveDarray[8],fiveDarray[9], fiveDarray[10], fiveDarray[11], fiveCarray[0], fiveCarray[1], fiveCarray[2], fiveCarray[3], fiveCarray[4], fiveCarray[5], fiveCarray[6], fiveCarray[7], fiveCarray[8], fiveCarray[9], fiveCarray[10], fiveCarray[11], fiveISIarray[0], fiveISIarray[1], fiveISIarray[2], fiveISIarray[3], fiveISIarray[4], fiveISIarray[5], fiveISIarray[6], fiveISIarray[7], fiveISIarray[8], fiveISIarray[9], fiveISIarray[10], fiveISIarray[11]
















