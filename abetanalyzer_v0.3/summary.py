import csv
import sqlite3
from tabulate import tabulate
import glob
import xlwt
import os

outFile = 'CSV_summary.csv'
outFile2 = 'CSV_strategy.csv'
outFile3 = 'CSV_binsHR.csv'
outFile4 = 'CSV_binsFAR.csv'
outFile5 = 'CSV_binsD.csv'
outFile6 = 'CSV_binsC.csv'
outFile7 = 'CSV_binsISI.csv'
outFile8 = 'CSV_FARbyStim.csv'
filesFound = []

wb = xlwt.Workbook()


def summaryPres():
    loop = 0
    print('Preparing to print summary and create CSV file... ' + '\n')
    headersCSVsummary = str('Animal ID,') + str('SID,') + str('Session Date,') + str('Schedule,') + str('Machine,') + str('Session Length,') + str('Hits,') + str('Misses,') + str('False alarms,') + \
                 str('Correct Rejections,') + str('ISI touches,') + str('Hit rate,') + str('False alarm rate,') + str('D-prime,') + str('Criterion,') + str('Mean Response Latency,') + str('Mean Hit Latency,') + str('Mean False Alarm Latency,') + str('Mean Retrieval Latency,') + str('Magazine Entries,') + str('Back Beam Breaks,') + str('Front Beam Breaks,') + '\n'
    headersCSVstrategy = str('Animal ID,') + str('SID,') + str('Session Date,') + str('Schedule,') + str('Machine,') + str('Latency Between Hits (MEAN),') + str('Latency Between Hits (STDEV),') + str('Latency Between Hits (MAX),') + str('Latency Between Stimuli Responses (MEAN),') + str('Latency Between Stimuli Responses (STDEV),') + str('Latency Between Stimuli Responses (MAX),') + str('Trials Between Stimuli Responses (MEAN),') + \
                 str('Trials Between Stimuli Responses (STDEV),') + str('Trials Between Stimuli Responses (MAX),') + str('False Alarm Bout Length (MEAN),') + str('False Alarm Bout Length (STDEV),') + str('False Alarm Bout Length (MAX),') + str('Hit Bout Length (MEAN),') + str('Hit Bout Length (STDEV),') + str('Hit Bout Length (MAX),') + str('Latency Retrieval --> Front Beam Break (MEAN),') + str('Latency Retrieval --> Front Beam Break (STDEV),') + str('Latency Retrieval --> Front Beam Break (MAX),') + '\n'
    headersCSVbins = str('Animal ID,') + str('SID,') + str('Session Date,') + str('Schedule,') + str('Machine,') + str('Bin1,') + str('Bin2,') + str('Bin3,') + str('Bin4,') + str('Bin5,') + str('Bin6,') + str('Bin7,') + str('Bin8,') + str('Bin9,') + str('Bin10,') + str('Bin11,') + str('Bin12,') + '\n'
    headersFARstim = str('Animal ID,') + str('SID,') + str('Session Date,') + str('Schedule,') + str('Machine,') + str('FAR stimulus 1/2,') + str('FAR stimulus 3,') + str('FAR stimulus 4,') + str('FAR stimulus 5,') + '\n'
    headersTerminal = ['AnimalID', 'DateTime', 'Schedule', 'S.Length', 'Hits', 'Miss', 'FA', 'CR', 'ISI', 'HR', 'FAR', "d'", 'c']

    conn = sqlite3.connect('DataOutput', isolation_level=None, timeout=10)
    c = conn.cursor()
    c.execute("PRAGMA TEMP_STORE = OFF")
    c.execute("PRAGMA SYNCHRONOUS = OFF")
    c.execute("PRAGMA JOURNAL_MODE = OFF")
    c.execute("SELECT * FROM Summary ORDER BY ExpDate")

    smTable = c.execute("SELECT * FROM Summary")
    smTable = smTable.fetchall()

    stratTable = c.execute("SELECT * FROM Strategy_Indications")
    stratTable = stratTable.fetchall()

    FARbystimTable = c.execute("SELECT * FROM FAR_each_Stimulus")
    FARbystimTable = FARbystimTable.fetchall()


    binsHRTable = c.execute("SELECT * FROM Bins_5min_HR")
    binsHRTable = binsHRTable.fetchall()
    binsFARTable = c.execute("SELECT * FROM Bins_5min_FAR")
    binsFARTable = binsFARTable.fetchall()
    binsDTable = c.execute("SELECT * FROM Bins_5min_Dprime")
    binsDTable = binsDTable.fetchall()
    binsCTable = c.execute("SELECT * FROM Bins_5min_C")
    binsCTable = binsCTable.fetchall()
    binsISITable = c.execute("SELECT * FROM Bins_5min_ISI_touch")
    binsISITable = binsISITable.fetchall()

    terminalTable = c.execute("SELECT AnimalID, ExpDate, Schedule, SessionLength, Hits, Misses, FalseAlarms, CorrectRejections, ISItouches, HR, FAR, dprime, criterion FROM Summary")

    #PRINT SUMMARY CSV
    with open(outFile, 'w') as f:
        f.write(headersCSVsummary)
        f.close()
    with open(outFile, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(smTable)

    # PRINT STRATEGY CSV
    with open(outFile2, 'w') as f:
        f.write(headersCSVstrategy)
        f.close()
    with open(outFile2, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(stratTable)

    # PRINT HIT RATE BINS CSV
    with open(outFile3, 'w') as f:
        f.write(headersCSVbins)
        f.close()
    with open(outFile3, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(binsHRTable)
        f.close()

    # PRINT FALSE ALARM BINS CSV
    with open(outFile4, 'w') as f:
        f.write(headersCSVbins)
        f.close()
    with open(outFile4, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(binsFARTable)
        f.close()

    # PRINT D-PRIME BINS CSV
    with open(outFile5, 'w') as f:
        f.write(headersCSVbins)
        f.close()
    with open(outFile5, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(binsDTable)
        f.close()

    # PRINT C BINS CSV
    with open(outFile6, 'w') as f:
        f.write(headersCSVbins)
        f.close()
    with open(outFile6, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(binsCTable)
        f.close()

    # PRINT ISI BINS CSV
    with open(outFile7, 'w') as f:
        f.write(headersCSVbins)
        f.close()
    with open(outFile7, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(binsISITable)
        f.close()

    # PRINT ISI BINS CSV
    with open(outFile8, 'w') as f:
        f.write(headersFARstim)
        f.close()
    with open(outFile8, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(FARbystimTable)
        f.close()

    tableP = tabulate(terminalTable, headers=headersTerminal, tablefmt='fancy_grid')
    print (tableP)

    # COMBINE DATA TO A SINGLE excel workbook
    for i in os.listdir(os.curdir):  # find file names
        if i.__contains__("CSV_"):
            filesFound.append(i)

    for i in filesFound:
        csvFile = filesFound[loop]
        csvFile = str(csvFile)
        fileName, fileExtention = os.path.splitext(csvFile)
        ws = wb.add_sheet(fileName)
        spamReader = csv.reader(open(csvFile, 'r'))
        for rowx, row in enumerate(spamReader):
            for colx, value in enumerate(row):
                ws.write(rowx, colx, value)
        wb.save("Compiled.xls")
        loop += 1

    loop = 0
    for i in filesFound:
        currentFile = str(filesFound[loop])
        os.remove(currentFile)
        loop += 1

    conn.execute("VACUUM")
    conn.commit()
