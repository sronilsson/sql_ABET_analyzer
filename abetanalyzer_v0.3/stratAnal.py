import sqlite3
import statistics

def stratAnal(currentSID, currentDB, animalID, date, scheduleName, machineName):
    loop = 1
    conn = sqlite3.connect(currentDB, isolation_level=None, timeout=10)
    c = conn.cursor()
    c.execute("PRAGMA TEMP_STORE = OFF")
    c.execute("PRAGMA SYNCHRONOUS = OFF")
    c.execute("PRAGMA JOURNAL_MODE = OFF")

    #TIME BETWEEN EACH HITS
    timeHits = c.execute("SELECT DTime FROM tbl_data WHERE SID = ? AND DEventText = ? AND DEffectText = ? ORDER BY DTime ASC", (currentSID, str('Condition Event'), str('Hit')))
    HitTimes = timeHits.fetchall()
    hitTimesRange = (len(HitTimes)) - 1
    hitDiffArray = []
    for i in range(hitTimesRange):
        currentHit = HitTimes[loop]
        currentHit = currentHit[0]
        lastHit = HitTimes[loop - 1]
        lastHit = lastHit[0]
        hitDiff = currentHit - lastHit
        hitDiffArray.append(hitDiff)
        loop += 1
    try:
        averageTimeBetweenHits = (sum(hitDiffArray) / len(hitDiffArray))
        TimeBetweenHits_STDEV = statistics.stdev(hitDiffArray)
        maxTimeBetweenHits = max(hitDiffArray)
    except (ZeroDivisionError, statistics.StatisticsError):
        averageTimeBetweenHits = 0
        TimeBetweenHits_STDEV = 0
        maxTimeBetweenHits = 0


    #TRIAL/TIME INACTIVITY (I.E MISSES + CORRECT REJECTIONS)
    inactivityCounter = 0
    inactivityTimeArray = []
    inactivityTrialArray = []
    trialEvent = c.execute("SELECT DTime, DEffectText FROM tbl_data WHERE SID = ? AND DEventText = ? AND (DEffectText = ? OR DEffectText = ? OR DEffectText = ? OR DEffectText = ? OR DEffectText = ?) ORDER BY DTime ASC",(currentSID, str('Condition Event'), str('Hit'), str('Mistake'), str('Correct Rejection'), str('Missed Hit'),str('Correction Trial Correct Rejection')))
    trialEvent = trialEvent.fetchall()
    for entries in trialEvent:
        cTime, cEvent = entries
        if cEvent == 'Missed Hit' or cEvent == 'Correct Rejection' or cEvent == 'Correction Trial Correct Rejection':
            inactivityCounter += 1
            if inactivityCounter == 1:
                startTimeInactivity = cTime
        else:
            if inactivityCounter > 0:
               inactivityTime = cTime - startTimeInactivity
               inactivityTimeArray.append(inactivityTime)
               inactivityTrialArray.append(inactivityCounter)
            inactivityCounter = 0
    try:
        mean_inactivity_time = (sum(inactivityTimeArray) / len(inactivityTimeArray))
        mean_inactivity_trials = (sum(inactivityTrialArray) / len(inactivityTrialArray))
        inactivity_trials_STDEV = statistics.stdev(inactivityTrialArray)
        inactivity_time_STDEV = statistics.stdev(inactivityTimeArray)
        max_inactivity_time = max(inactivityTimeArray)
        max_inactivity_trials = max(inactivityTrialArray)
    except (ZeroDivisionError, statistics.StatisticsError):
        mean_inactivity_time = 0
        mean_inactivity_trials = 0
        inactivity_trials_STDEV = 0
        inactivity_time_STDEV = 0
        max_inactivity_time = 0
        max_inactivity_trials = 0

    #NUMBER OF REPEAT FAs
    errorCounter = 0
    errorArray = []
    trialEvents = c.execute("SELECT DTime, DEffectText FROM tbl_data WHERE SID = ? AND DEventText = ? AND (DEffectText = ? OR DEffectText = ? OR DEffectText = ? OR DEffectText = ?) ORDER BY DTime ASC",(currentSID, str('Condition Event'), str('Hit'), str('Mistake'), str('Correct Rejection'), str('Correction Trial Correct Rejection')))
    trialEvents = trialEvents.fetchall()
    for entry in trialEvents:
        currentTime, currentEvent = entry
        if currentEvent == 'Mistake':
            errorCounter += 1
        else:
            if errorCounter > 0:
                errorArray.append(errorCounter)
            errorCounter = 0
    try:
        mean_FA_bout = (sum(errorArray) / len(errorArray))
        FA_bout_STDEV = statistics.stdev(errorArray)
        max_FA_bout = max(errorArray)
    except (ZeroDivisionError, statistics.StatisticsError):
        mean_FA_bout = 0
        FA_bout_STDEV = 0
        max_FA_bout = 0

    #NUMBER OF REPEAT HITS
    hitCounter = 0
    hitArray = []
    trialEvents2 = c.execute("SELECT DTime, DEffectText FROM tbl_data WHERE SID = ? AND DEventText = ? AND (DEffectText = ? OR DEffectText = ? OR DEffectText = ?) ORDER BY DTime ASC",(currentSID, str('Condition Event'), str('Hit'), str('Mistake'), str('Missed Hit')))
    trialEvents2 = trialEvents2.fetchall()
    for entry in trialEvents2:
        currentTime, currentEvent = entry
        if currentEvent == 'Mistake':
            hitCounter += 1
        else:
            if hitCounter > 0:
                hitArray.append(hitCounter)
            hitCounter = 0
    try:
        mean_hit_bout = (sum(hitArray) / len(hitArray))
        hit_bout_STDEV = statistics.stdev(hitArray)
        max_hit_bout = max(hitArray)
    except (ZeroDivisionError, statistics.StatisticsError):
        mean_hit_bout = 0
        hit_bout_STDEV = 0
        max_hit_bout = 0

    # TIME TAKEN TO BREAK FRONT IR BEAM AFTER REWARD RETRIEVAL
    events = c.execute("SELECT DTime, DEffectText FROM tbl_data WHERE SID = ? AND (DEffectText = ? OR DEffectText = ?) ORDER BY DTime ASC",(currentSID, str('Reward Collected Start ITI'), str('FIRBeam #1')))
    events = events.fetchall()
    time2FrontArray = []
    rewardCollected = 0
    for event in events:
        currentTime, currentEvent = event
        if currentEvent == 'Reward Collected Start ITI' and rewardCollected == 0:
            rewardCollectedTime = currentTime
            rewardCollected = 1
        if currentEvent == 'FIRBeam #1' and rewardCollected == 1:
            FBeamTime = currentTime
            rewardCollected = 0
            time2Front = FBeamTime - rewardCollectedTime
            time2FrontArray.append(time2Front)
    try:
        mean_FBeamTime = (sum(time2FrontArray) / len(time2FrontArray))
        FBeamTime_STDEV = statistics.stdev(time2FrontArray)
        max_FBeamTime = max(time2FrontArray)
    except (ZeroDivisionError, statistics.StatisticsError):
        mean_FBeamTime = 0
        FBeamTime_STDEV = 0
        max_FBeamTime = 0

    conn.commit()
    conn.close()

    return averageTimeBetweenHits, TimeBetweenHits_STDEV, maxTimeBetweenHits, mean_inactivity_time, inactivity_time_STDEV, max_inactivity_time, mean_inactivity_trials, inactivity_trials_STDEV, max_inactivity_trials, mean_FA_bout, FA_bout_STDEV, max_FA_bout, mean_hit_bout, hit_bout_STDEV, max_hit_bout, mean_FBeamTime, FBeamTime_STDEV, max_FBeamTime