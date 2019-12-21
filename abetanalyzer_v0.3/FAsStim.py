import sqlite3
import time

def FAsStim(currentSID, currentDB, animalID, date, scheduleName, machineName):
    conn = sqlite3.connect(currentDB, isolation_level=None, timeout=10)
    c = conn.cursor()
    mistakeStimListWithCorrectionTrials = []
    presStimListWithCorrectionTrials = []
    c.execute("PRAGMA TEMP_STORE = OFF")
    c.execute("PRAGMA SYNCHRONOUS = OFF")
    c.execute("PRAGMA JOURNAL_MODE = OFF")

    # FIND CORRECT IMAGE NUMBER
    corrStim = str('Correct_Image')
    corrStimNo = c.execute('SELECT DValue1 FROM tbl_data WHERE SID = ? AND DEffectText = ?', (currentSID, corrStim))
    corrStimNo = corrStimNo.fetchone()
    corrStimNo = corrStimNo[0]
    corrStimNo = int(corrStimNo)

    # GENERATE LIST NON-TARGET IMAGE NUMBERS
    incorStimNOs = [1,2,3,4,5]
    incorStimNOs.remove(corrStimNo)

    #MISTAKES BY STIMULI
    for i in incorStimNOs:
        currentIncorrStim = str('Image ') + str(i)
        relevantStage = str('6')
        position = str('2')
        position1 = str('Position')
        dValue2 = str(i-1)
        mistakeStim = c.execute('SELECT COUNT(*) FROM tbl_data WHERE (SID = ? AND DEventText = ? AND DEffectText = ? AND DGroup = ? AND DText2 = ? AND DValue1 = ? AND DText1 = ? AND DValue2 = ?)', (currentSID, str("Touch Down Event"), str("Bussey Mouse Operant Mode 3 x 1 x low"), relevantStage, currentIncorrStim, position, position1, dValue2))
        mistakeStim = mistakeStim.fetchone()
        mistakeStim = mistakeStim[0]
        mistakeStim = int(mistakeStim)
        mistakeStimListWithCorrectionTrials.append(mistakeStim)

    # PRESENTATIONS BY STIMULI
    for i in incorStimNOs:
        currentIncorrStim = str('Image ') + str(i)
        relevantStage = str('4')
        position = str('2')
        position1 = str('Position')
        dValue2 = str(i - 1)
        stimPres = c.execute('SELECT COUNT(*) FROM tbl_data WHERE (SID = ? AND DEventText = ? AND DEffectText = ? AND DGroup = ? AND DText2 = ? AND DValue1 = ? AND DText1 = ? AND DValue2 = ?)', (currentSID, str("Whisker - Display Image"), str("Bussey Mouse Operant Mode 3 x 1 x low"), relevantStage, currentIncorrStim, position, position1, dValue2))
        stimPres = stimPres.fetchone()
        stimPres = stimPres[0]
        stimPres = int(stimPres)
        presStimListWithCorrectionTrials.append(stimPres)
    conn.close()

    try:
        FAstimOne_Two = mistakeStimListWithCorrectionTrials[0] / presStimListWithCorrectionTrials[0]
        FAstimOne_Two = round(FAstimOne_Two, 4)
    except ZeroDivisionError:
        FAstimOne_Two = 0
    try:
        FAstim_Three = mistakeStimListWithCorrectionTrials[1] / presStimListWithCorrectionTrials[1]
        FAstim_Three = round(FAstim_Three, 4)
    except ZeroDivisionError:
        FAstim_Three = 0
    try:
        FAstim_Four = mistakeStimListWithCorrectionTrials[2] / presStimListWithCorrectionTrials[2]
        FAstim_Four = round(FAstim_Four, 4)
    except ZeroDivisionError:
        FAstim_Four = 0
    try:
        FAstim_Five = mistakeStimListWithCorrectionTrials[3] / presStimListWithCorrectionTrials[3]
        FAstim_Five = round(FAstim_Five, 4)
    except ZeroDivisionError:
        FAstim_Five = 0

    return FAstimOne_Two, FAstim_Three, FAstim_Four, FAstim_Five










