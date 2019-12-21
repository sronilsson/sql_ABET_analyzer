import sqlite3
import time
import csv
from tqdm import tqdm

from signalDetection import signalDetection1, signalDetection2
from latencyCalc import latencyCalc
from binAnalysis import binAnalysis
from stratAnal import stratAnal
from FAsStim import FAsStim

def calc2(currentDB, SIDs):
    loop = 0
    loopy = 0
    mistakeStimListWithCorrectionTrials= []
    conn = sqlite3.connect(currentDB, isolation_level=None, timeout=10)
    c = conn.cursor()
    c.execute("PRAGMA TEMP_STORE = OFF")
    c.execute("PRAGMA SYNCHRONOUS = OFF")
    c.execute("PRAGMA JOURNAL_MODE = OFF")
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

    # FIND NUMBER OF SESSIONS IN DB
    if SIDs == 0:
        sessRun = c.execute("SELECT SID FROM tbl_data GROUP BY SID")
        sessRun = sessRun.fetchall()
        sessNO = len(sessRun)
        print (('User-defined sessions found in ') + str(currentDB) + (' = ') + str(sessNO) + '\n')
        print (str('Processing user-defined session from ') + str(currentDB))
    if SIDs == 1:
        sessRun = c.execute("SELECT SID FROM tbl_data GROUP BY SID")
        sessRun = sessRun.fetchall()
        sessNO = len(sessRun)
        c.execute("ALTER TABLE tbl_data RENAME TO ALL_DATA")
        print(('User-defined sessions found in ') + str(currentDB) + (' = ') + str(sessNO) + '\n')
        print(str('Processing user-defined session from ') + str(currentDB))

    # CALCULATE MEANS AND TOTALS FOR EACH ANIMAL
    for i in tqdm(sessRun):
        if SIDs == 1:
            currentSID = sessRun[loop]
            currentSID = str(currentSID[0])
            c.execute('DROP TABLE IF EXISTS tbl_data')
            c.execute("CREATE TABLE tbl_data (SID integer, DTime integer, DAuto integer, DEvent integer, DEventText integer, DEffectText integer, DAltText integer, DGroup integer, DArgCount integer, DText1 integer, DValue1 integer, DText2 integer, DValue2 integer, DText3 integer, DValue3 integer, DText4 integer, DValue4 integer, DText5 integer, DValue5 integer)")
            c.execute("INSERT INTO tbl_data SELECT * FROM ALL_DATA WHERE SID = ?", (currentSID,))
            loopy += 1
            conn.commit()
        if SIDs == 0:
            currentSID = sessRun[loop]
            currentSID = str(currentSID[0])
        animalID = c.execute( "SELECT NValue FROM tbl_Schedule_Notes WHERE SID = ? AND NName = ?", (currentSID, str('Animal ID')))
        animalID = animalID.fetchone()
        animalID = str(animalID[0])
        date = c.execute("SELECT NValue FROM tbl_Schedule_Notes WHERE NName = ? AND SID = ?", (str('Schedule_Start_Time'), currentSID))
        date = date.fetchone()
        date = str(date[0])
        scheduleName = c.execute("SELECT SName FROM tbl_Schedules WHERE SID = ?", (currentSID,))
        scheduleName = scheduleName.fetchone()
        scheduleName = str(scheduleName[0])
        machineName = c.execute( "SELECT SMachineName FROM tbl_Schedules WHERE SID = ?", (currentSID,))
        machineName = machineName.fetchone()
        machineName = str(machineName[0])

        sLength = c.execute("SELECT MAX(DValue1) FROM tbl_data WHERE SID = ? AND DEffectText = ?",  (currentSID, str('_Schedule_Timer')))
        sLength = sLength.fetchone()
        sLength = str(sLength[0])
        if sLength == 'None':
            sLength = 0

        hits = c.execute("SELECT MAX(DValue1) FROM tbl_data WHERE SID = ? AND DEffectText = ?", (currentSID, str('No_of_hits')))
        hits = hits.fetchone()
        hits = str(hits[0])
        if hits == 'None':
            hits = 0

        misses = c.execute("SELECT MAX(DValue1) FROM tbl_data WHERE SID = ? AND DEffectText = ?", (currentSID, str('No_of_Misses')))
        misses = misses.fetchone()
        misses = str(misses[0])
        if misses == 'None':
            misses = 0

        FAs = c.execute("SELECT MAX(DValue1) FROM tbl_data WHERE SID = ? AND DEffectText = ?", (currentSID, str('No_of_Mistakes')))
        FAs = FAs.fetchone()
        FAs = str(FAs[0])
        if FAs == 'None':
            FAs = 0

        CRs = c.execute("SELECT MAX(DValue1) FROM tbl_data WHERE SID = ? AND DEffectText = ?", (currentSID, str('No_of_correct_rejections')))
        CRs = CRs.fetchone()
        CRs = str(CRs[0])
        if CRs == 'None':
            CRs = 0

        ISItouches = c.execute("SELECT MAX(DValue1) FROM tbl_data WHERE SID = ? AND DEffectText = ?",(currentSID, str('Blank_Touch_Counter')))
        ISItouches = ISItouches.fetchone()
        ISItouches = str(ISItouches[0])
        if ISItouches == 'None':
            ISItouches = 0

        correctionTrial_FAs = c.execute("SELECT MAX(DValue1) FROM tbl_data WHERE SID = ? AND (DEffectText = ? AND DEventText = ?)", (currentSID, str('Correction_Trial_Mistakes'), str('Variable Event')))
        correctionTrial_FAs = correctionTrial_FAs.fetchone()
        correctionTrial_FAs = str(correctionTrial_FAs[0])
        if correctionTrial_FAs == 'None':
            correctionTrial_FAs = 0

        correctionTrial_CRs = c.execute("SELECT MAX(DValue1) FROM tbl_data WHERE SID = ? AND (DEffectText = ? AND DEventText = ?)",(currentSID, str('Correction_Trial_Correct_Rejections'), str('Variable Event')))
        correctionTrial_CRs = correctionTrial_CRs.fetchone()
        correctionTrial_CRs = str(correctionTrial_CRs[0])
        if correctionTrial_CRs == 'None':
            correctionTrial_CRs = 0

        frontBreaks = c.execute("SELECT * FROM tbl_data WHERE SID = ? AND (DEventText = ? AND DEffectText = ?)", (currentSID, str('Input Transition On Event'), str('FIRBeam #1')))
        frontBreaks = frontBreaks.fetchall()
        frontBreaks = len(frontBreaks)

        backBreaks = c.execute("SELECT * FROM tbl_data WHERE SID = ? AND (DEventText = ? AND DEffectText = ?)", (currentSID, str('Input Transition On Event'), str('BIRBeam #1')))
        backBreaks = backBreaks.fetchall()
        backBreaks = len(backBreaks)

        magEntries = c.execute("SELECT * FROM tbl_data WHERE SID = ? AND (DEventText = ? AND DEffectText = ?)", (currentSID, str('Input Transition On Event'), str('Tray #1')))
        magEntries = magEntries.fetchall()
        magEntries = len(magEntries)

        correctionTrial_FAs = int(correctionTrial_FAs)
        correctionTrial_CRs = int(correctionTrial_CRs)

        meanResponseLatency, meanCorrectLatency, meanIncorrectLatency, meanRetrievalLatency = latencyCalc(currentSID, currentDB)

        HR, FAR, d, criterion, beta, SI, RI = signalDetection1(hits, misses, CRs, FAs)

        HR1, HR2, HR3, HR4, HR5, HR6, HR7, HR8, HR9, HR10, HR11, HR12, FAR1, FAR2, FAR3, FAR4, FAR5, FAR6, FAR7, FAR8, FAR9, FAR10, FAR11, FAR12, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, ISI1, ISI2, ISI3, ISI4, ISI5, ISI6, ISI7, ISI8, ISI9, ISI10, ISI11, ISI12 = binAnalysis(currentSID, currentDB, animalID, date, scheduleName, machineName)

        averageTimeBetweenHits, TimeBetweenHits_STDEV, maxTimeBetweenHits, mean_inactivity_time, inactivity_time_STDEV, max_inactivity_time, mean_inactivity_trials, inactivity_trials_STDEV, max_inactivity_trials, mean_FA_bout, FA_bout_STDEV, max_FA_bout, mean_hit_bout, hit_bout_STDEV, max_hit_bout, mean_FBeamTime, FBeamTime_STDEV, max_FBeamTime = stratAnal(currentSID, currentDB, animalID, date, scheduleName, machineName)

        FAstimOne_Two, FAstim_Three, FAstim_Four, FAstim_Five = FAsStim(currentSID, currentDB, animalID, date, scheduleName, machineName)

        c.execute("INSERT INTO FAR_each_Stimulus (AnimalID, SID, ExpDate, Schedule, Machine, FAR_Stim1_2, FAR_Stim3, FAR_Stim4, FAR_Stim5) VALUES (?,?,?,?,?,?,?,?,?)", (animalID, currentSID, date, scheduleName, machineName, FAstimOne_Two, FAstim_Three, FAstim_Four, FAstim_Five))
        c.execute("INSERT INTO Summary (AnimalID, SID, ExpDate, Schedule, Machine, SessionLength, Hits, Misses, FalseAlarms, CorrectRejections, ISItouches, HR, FAR, dprime, criterion, meanResponseLatency, meanCorrectLatency, meanIncorrectLatency, meanRetrievalLatency, MagEntries, BackBeamBreaks, FrontBeamBreaks) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, ?, ?, ?, ?)", (animalID, currentSID, date, scheduleName, machineName, sLength, hits, misses, FAs, CRs, ISItouches, HR, FAR, d, criterion, meanResponseLatency, meanCorrectLatency, meanIncorrectLatency, meanRetrievalLatency, magEntries, backBreaks, frontBreaks))
        c.execute("INSERT INTO Strategy_Indications (AnimalID, SID, ExpDate, Schedule, Machine, Mean_Time_Between_Hits, STDEV_Time_Between_Hits, MAX_Time_Between_Hits, Mean_Time_Bout_No_Stimuli_Responses, STDEV_Time_Bout_No_Stimuli_Responses, MAX_Time_Bout_No_Stimuli_Responses, Mean_Trial_Bout_No_Stimuli_Responses, STDEV_Trial_Bout_No_Stimuli_Responses, MAX_Trial_Bout_No_Stimuli_Responses, Mean_False_Alarm_bout_trial_length, STDEV_False_Alarm_bout_trial_length, MAX_False_Alarm_bout_trial_length, Mean_Hit_bout_trial_length, STDEV_Hit_bout_trial_length, MAX_Hit_bout_trial_length, Mean_Retreival_FBeam_Time, STDEV_Retreival_FBeam_Time, MAX_Retreival_FBeam_Time) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(animalID, currentSID, date, scheduleName, machineName, averageTimeBetweenHits, TimeBetweenHits_STDEV,maxTimeBetweenHits, mean_inactivity_time, inactivity_time_STDEV, max_inactivity_time,mean_inactivity_trials, inactivity_trials_STDEV, max_inactivity_trials, mean_FA_bout, FA_bout_STDEV, max_FA_bout, mean_hit_bout, hit_bout_STDEV, max_hit_bout, mean_FBeamTime, FBeamTime_STDEV, max_FBeamTime))
        c.execute("INSERT INTO Bins_5min_HR (AnimalID, SID, ExpDate, Schedule, Machine, Bin1, Bin2, Bin3, Bin4, Bin5, Bin6, Bin7, Bin8, Bin9, Bin10, Bin11, Bin12) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(animalID, currentSID, date, scheduleName, machineName, HR1, HR2, HR3, HR4, HR5, HR6, HR7, HR8, HR9, HR10, HR11, HR12))
        c.execute("INSERT INTO Bins_5min_FAR (AnimalID, SID, ExpDate, Schedule, Machine, Bin1, Bin2, Bin3, Bin4, Bin5, Bin6, Bin7, Bin8, Bin9, Bin10, Bin11, Bin12) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(animalID, currentSID, date, scheduleName, machineName, FAR1, FAR2, FAR3, FAR4, FAR5, FAR6, FAR7, FAR8, FAR9, FAR10, FAR11, FAR12))
        c.execute("INSERT INTO Bins_5min_Dprime (AnimalID, SID, ExpDate, Schedule, Machine, Bin1, Bin2, Bin3, Bin4, Bin5, Bin6, Bin7, Bin8, Bin9, Bin10, Bin11, Bin12) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(animalID, currentSID, date, scheduleName, machineName, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12))
        c.execute("INSERT INTO Bins_5min_C (AnimalID, SID, ExpDate, Schedule, Machine, Bin1, Bin2, Bin3, Bin4, Bin5, Bin6, Bin7, Bin8, Bin9, Bin10, Bin11, Bin12) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (animalID, currentSID, date, scheduleName, machineName, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12))
        c.execute("INSERT INTO Bins_5min_ISI_touch (AnimalID, SID, ExpDate, Schedule, Machine, Bin1, Bin2, Bin3, Bin4, Bin5, Bin6, Bin7, Bin8, Bin9, Bin10, Bin11, Bin12) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(animalID, currentSID, date, scheduleName, machineName, ISI1, ISI2, ISI3, ISI4, ISI5, ISI6, ISI7, ISI8, ISI9, ISI10, ISI11, ISI12))
        c.execute("SELECT * FROM Summary ORDER BY AnimalID, SID")
        c.execute("SELECT * FROM Bins_5min_HR ORDER BY AnimalID, SID")
        c.execute("SELECT * FROM Bins_5min_FAR ORDER BY AnimalID, SID")
        c.execute("SELECT * FROM Bins_5min_Dprime ORDER BY AnimalID, SID")
        c.execute("SELECT * FROM Bins_5min_C ORDER BY AnimalID, SID")
        c.execute("SELECT * FROM Bins_5min_ISI_touch ORDER BY AnimalID, SID")
        c.execute("SELECT * FROM FAR_each_Stimulus ORDER BY AnimalID, SID")

        CRs = int(CRs)
        FAs = int(FAs)
        CR_corrected = (CRs + correctionTrial_CRs)
        FAs_corrected = (FAs + correctionTrial_FAs)
        HR_corrected, FAR_corrected, d_corrected, c_corrected, beta_corrected, SI_corrected, RI_corrected = signalDetection2(hits, misses, CR_corrected, FAs_corrected)

        c.execute("INSERT INTO Summary_correction_included (AnimalID, SID, ExpDate, Schedule, Machine, SessionLength, Hits, Misses, FalseAlarms, CorrectRejections, ISItouches, HR, FAR, dprime, criterion, beta, SI, RI) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (animalID, currentSID, date, scheduleName, machineName, sLength, hits, misses, FAs_corrected, CR_corrected, ISItouches, HR_corrected, FAR_corrected, d_corrected, c_corrected, beta_corrected, SI_corrected, RI_corrected))
        c.execute("SELECT * FROM Summary_correction_included ORDER BY AnimalID, SID")

        loop += 1


    conn.commit()
    time.sleep(1)
    conn.close()

