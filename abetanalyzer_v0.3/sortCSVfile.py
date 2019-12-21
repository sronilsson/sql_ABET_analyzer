import pandas as pd
from pandas import ExcelWriter

def sortCSVfile():
    workbook = pd.ExcelFile('Compiled.xls')
    SummaryTable = pd.read_excel(workbook, 'CSV_summary')

    MeanCompiled = 'MeanCompiled.xls'

    meanHits = SummaryTable.groupby('Animal ID')['Hits'].mean()
    meanMisses = SummaryTable.groupby('Animal ID')['Misses'].mean()
    meanFA = SummaryTable.groupby('Animal ID')['False alarms'].mean()
    meanCR = SummaryTable.groupby('Animal ID')['Correct Rejections'].mean()
    meanISI = SummaryTable.groupby('Animal ID')['ISI touches'].mean()
    meanHR = SummaryTable.groupby('Animal ID')['Hit rate'].mean()
    meanFAR = SummaryTable.groupby('Animal ID')['False alarm rate'].mean()
    meanD = SummaryTable.groupby('Animal ID')['D-prime'].mean()
    meanC = SummaryTable.groupby('Animal ID')['Criterion'].mean()
    meanResponseLat = SummaryTable.groupby('Animal ID')['Mean Response Latency'].mean()
    meanHitLat = SummaryTable.groupby('Animal ID')['Mean Hit Latency'].mean()
    meanFAlat = SummaryTable.groupby('Animal ID')['Mean False Alarm Latency'].mean()
    meanRETlat = SummaryTable.groupby('Animal ID')['Mean Retrieval Latency'].mean()
    meanMagEntries = SummaryTable.groupby('Animal ID')['Magazine Entries'].mean()
    meanBIRBeam = SummaryTable.groupby('Animal ID')['Back Beam Breaks'].mean()
    meanFIRBeam = SummaryTable.groupby('Animal ID')['Front Beam Breaks'].mean()

    strategyTable = pd.read_excel(workbook, 'CSV_strategy')
    meanLatBetweenHits = strategyTable.groupby('Animal ID')['Latency Between Hits (MEAN)'].mean()
    stdevLatBetweenHits = strategyTable.groupby('Animal ID')['Latency Between Hits (STDEV)'].mean()
    maxLatBetweenHits = strategyTable.groupby('Animal ID')['Latency Between Hits (MAX)'].mean()
    meanLatBetweenResponses = strategyTable.groupby('Animal ID')['Latency Between Stimuli Responses (MEAN)'].mean()
    stdevLatBetweenResponses = strategyTable.groupby('Animal ID')['Latency Between Stimuli Responses (STDEV)'].mean()
    maxLatBetweenResponses = strategyTable.groupby('Animal ID')['Latency Between Stimuli Responses (MAX)'].mean()
    meanTrialsBetweenResponses = strategyTable.groupby('Animal ID')['Trials Between Stimuli Responses (MEAN)'].mean()
    stdevTrialsBetweenResponses = strategyTable.groupby('Animal ID')['Trials Between Stimuli Responses (STDEV)'].mean()
    maxTrialsBetweenResponses = strategyTable.groupby('Animal ID')['Trials Between Stimuli Responses (MAX)'].mean()

    meanFAboutLength = strategyTable.groupby('Animal ID')['False Alarm Bout Length (MEAN)'].mean()
    stdevFAboutLength = strategyTable.groupby('Animal ID')['False Alarm Bout Length (STDEV)'].mean()
    maxFAboutLength = strategyTable.groupby('Animal ID')['False Alarm Bout Length (MAX)'].mean()

    meanHitboutLength = strategyTable.groupby('Animal ID')['Hit Bout Length (MEAN)'].mean()
    stdevHitboutLength = strategyTable.groupby('Animal ID')['Hit Bout Length (STDEV)'].mean()
    maxHitboutLength = strategyTable.groupby('Animal ID')['Hit Bout Length (MAX)'].mean()

    mean_retrievalFrontBeam = strategyTable.groupby('Animal ID')['Latency Retrieval --> Front Beam Break (MEAN)'].mean()
    stdev_retrievalFrontBeam = strategyTable.groupby('Animal ID')['Latency Retrieval --> Front Beam Break (STDEV)'].mean()
    max_retrievalFrontBeam = strategyTable.groupby('Animal ID')['Latency Retrieval --> Front Beam Break (MAX)'].mean()


    hitBinTable = pd.read_excel(workbook, 'CSV_binsHR')
    hitsBin1 = hitBinTable.groupby('Animal ID')['Bin1'].mean()
    hitsBin2 = hitBinTable.groupby('Animal ID')['Bin2'].mean()
    hitsBin3 = hitBinTable.groupby('Animal ID')['Bin3'].mean()
    hitsBin4 = hitBinTable.groupby('Animal ID')['Bin4'].mean()
    hitsBin5 = hitBinTable.groupby('Animal ID')['Bin5'].mean()
    hitsBin6 = hitBinTable.groupby('Animal ID')['Bin6'].mean()
    hitsBin7 = hitBinTable.groupby('Animal ID')['Bin7'].mean()
    hitsBin8 = hitBinTable.groupby('Animal ID')['Bin8'].mean()
    hitsBin9 = hitBinTable.groupby('Animal ID')['Bin9'].mean()
    hitsBin10 = hitBinTable.groupby('Animal ID')['Bin10'].mean()
    hitsBin11 = hitBinTable.groupby('Animal ID')['Bin11'].mean()
    hitsBin12 = hitBinTable.groupby('Animal ID')['Bin12'].mean()


    FABinTable = pd.read_excel(workbook, 'CSV_binsFAR')
    FARBin1 = FABinTable.groupby('Animal ID')['Bin1'].mean()
    FARBin2 = FABinTable.groupby('Animal ID')['Bin2'].mean()
    FARBin3 = FABinTable.groupby('Animal ID')['Bin3'].mean()
    FARBin4 = FABinTable.groupby('Animal ID')['Bin4'].mean()
    FARBin5 = FABinTable.groupby('Animal ID')['Bin5'].mean()
    FARBin6 = FABinTable.groupby('Animal ID')['Bin6'].mean()
    FARBin7 = FABinTable.groupby('Animal ID')['Bin7'].mean()
    FARBin8 = FABinTable.groupby('Animal ID')['Bin8'].mean()
    FARBin9 = FABinTable.groupby('Animal ID')['Bin9'].mean()
    FARBin10 = FABinTable.groupby('Animal ID')['Bin10'].mean()
    FARBin11 = FABinTable.groupby('Animal ID')['Bin11'].mean()
    FARBin12 = FABinTable.groupby('Animal ID')['Bin12'].mean()

    DBinTable = pd.read_excel(workbook, 'CSV_binsD')
    DBin1 = DBinTable.groupby('Animal ID')['Bin1'].mean()
    DBin2 = DBinTable.groupby('Animal ID')['Bin2'].mean()
    DBin3 = DBinTable.groupby('Animal ID')['Bin3'].mean()
    DBin4 = DBinTable.groupby('Animal ID')['Bin4'].mean()
    DBin5 = DBinTable.groupby('Animal ID')['Bin5'].mean()
    DBin6 = DBinTable.groupby('Animal ID')['Bin6'].mean()
    DBin7 = DBinTable.groupby('Animal ID')['Bin7'].mean()
    DBin8 = DBinTable.groupby('Animal ID')['Bin8'].mean()
    DBin9 = DBinTable.groupby('Animal ID')['Bin9'].mean()
    DBin10 = DBinTable.groupby('Animal ID')['Bin10'].mean()
    DBin11 = DBinTable.groupby('Animal ID')['Bin11'].mean()
    DBin12 = DBinTable.groupby('Animal ID')['Bin12'].mean()

    CBinTable = pd.read_excel(workbook, 'CSV_binsC')
    CBin1 = CBinTable.groupby('Animal ID')['Bin1'].mean()
    CBin2 = CBinTable.groupby('Animal ID')['Bin2'].mean()
    CBin3 = CBinTable.groupby('Animal ID')['Bin3'].mean()
    CBin4 = CBinTable.groupby('Animal ID')['Bin4'].mean()
    CBin5 = CBinTable.groupby('Animal ID')['Bin5'].mean()
    CBin6 = CBinTable.groupby('Animal ID')['Bin6'].mean()
    CBin7 = CBinTable.groupby('Animal ID')['Bin7'].mean()
    CBin8 = CBinTable.groupby('Animal ID')['Bin8'].mean()
    CBin9 = CBinTable.groupby('Animal ID')['Bin9'].mean()
    CBin10 = CBinTable.groupby('Animal ID')['Bin10'].mean()
    CBin11 = CBinTable.groupby('Animal ID')['Bin11'].mean()
    CBin12 = CBinTable.groupby('Animal ID')['Bin12'].mean()

    ISIBinTable = pd.read_excel(workbook, 'CSV_binsISI')
    ISIBin1 = ISIBinTable.groupby('Animal ID')['Bin1'].mean()
    ISIBin2 = ISIBinTable.groupby('Animal ID')['Bin2'].mean()
    ISIBin3 = ISIBinTable.groupby('Animal ID')['Bin3'].mean()
    ISIBin4 = ISIBinTable.groupby('Animal ID')['Bin4'].mean()
    ISIBin5 = ISIBinTable.groupby('Animal ID')['Bin5'].mean()
    ISIBin6 = ISIBinTable.groupby('Animal ID')['Bin6'].mean()
    ISIBin7 = ISIBinTable.groupby('Animal ID')['Bin7'].mean()
    ISIBin8 = ISIBinTable.groupby('Animal ID')['Bin8'].mean()
    ISIBin9 = ISIBinTable.groupby('Animal ID')['Bin9'].mean()
    ISIBin10 = ISIBinTable.groupby('Animal ID')['Bin10'].mean()
    ISIBin11 = ISIBinTable.groupby('Animal ID')['Bin11'].mean()
    ISIBin12 = ISIBinTable.groupby('Animal ID')['Bin12'].mean()

    FARbyStimTable = pd.read_excel(workbook, 'CSV_FARbyStim')
    FARbyStim1 = FARbyStimTable.groupby('Animal ID')['FAR stimulus 1/2'].mean()
    FARbyStim2 = FARbyStimTable.groupby('Animal ID')['FAR stimulus 3'].mean()
    FARbyStim3 = FARbyStimTable.groupby('Animal ID')['FAR stimulus 4'].mean()
    FARbyStim4 = FARbyStimTable.groupby('Animal ID')['FAR stimulus 5'].mean()

    allSummary = (meanFA, meanCR, meanISI, meanHR, meanFAR, meanD, meanC, meanResponseLat, meanHitLat, meanFAlat, meanRETlat, meanMagEntries, meanBIRBeam, meanFIRBeam)
    allStrategy = (maxLatBetweenHits, meanLatBetweenResponses, stdevLatBetweenResponses, maxLatBetweenResponses, meanTrialsBetweenResponses, stdevTrialsBetweenResponses, maxTrialsBetweenResponses, meanFAboutLength, stdevFAboutLength, maxFAboutLength, meanHitboutLength, stdevHitboutLength, maxHitboutLength, mean_retrievalFrontBeam, stdev_retrievalFrontBeam, max_retrievalFrontBeam)
    allHR = (hitsBin3, hitsBin4, hitsBin5, hitsBin6, hitsBin7, hitsBin8, hitsBin9, hitsBin10, hitsBin11, hitsBin12)
    allFAR = (FARBin3, FARBin4, FARBin5, FARBin6, FARBin7, FARBin8, FARBin9, FARBin10, FARBin11, FARBin12)
    allD = (DBin3, DBin4, DBin5, DBin6, DBin7, DBin8, DBin9, DBin10, DBin11, DBin12)
    allC = (CBin3, CBin4, CBin5, CBin6, CBin7, CBin8, CBin9, CBin10, CBin11, CBin12)
    allISI = (ISIBin3, ISIBin4, ISIBin5, ISIBin6, ISIBin7, ISIBin8, ISIBin9, ISIBin10, ISIBin11, ISIBin12)
    allFARbyStim = (FARbyStim3, FARbyStim4)

    #SUMMARY TABLE
    meanHits = meanHits.to_frame().reset_index()
    summaryTable = meanHits.merge(meanMisses.to_frame(), left_on='Animal ID', right_index=True)
    for i in allSummary:
        summaryTable = summaryTable.merge(i.to_frame(), left_on='Animal ID', right_index=True)
    summaryTable.set_index('Animal ID', inplace=True)

    #STRATEGY TABLE
    meanLatBetweenHits = meanLatBetweenHits.to_frame().reset_index()
    stratTable = meanLatBetweenHits.merge(stdevLatBetweenHits.to_frame(), left_on='Animal ID', right_index=True)
    for i in allStrategy:
        stratTable = stratTable.merge(i.to_frame(), left_on='Animal ID', right_index=True)
    stratTable.set_index('Animal ID', inplace=True)

    #HIT TABLE
    hitsBin1 = hitsBin1.to_frame().reset_index()
    hitTable = hitsBin1.merge(hitsBin2.to_frame(), left_on='Animal ID', right_index=True)
    for i in allHR:
        hitTable = hitTable.merge(i.to_frame(), left_on='Animal ID', right_index=True)
    hitTable.set_index('Animal ID', inplace=True)

    #FAR TABLE
    FARBin1 = FARBin1.to_frame().reset_index()
    FARTable = FARBin1.merge(FARBin2.to_frame(), left_on='Animal ID', right_index=True)
    for i in allFAR:
        FARTable = FARTable.merge(i.to_frame(), left_on='Animal ID', right_index=True)
    FARTable.set_index('Animal ID', inplace=True)

    #D TABLE
    DBin1 = DBin1.to_frame().reset_index()
    DTable = DBin1.merge(DBin2.to_frame(), left_on='Animal ID', right_index=True)
    for i in allD:
        DTable = DTable.merge(i.to_frame(), left_on='Animal ID', right_index=True)
    DTable.set_index('Animal ID', inplace=True)

    #C TABLE
    CBin1 = CBin1.to_frame().reset_index()
    CTable = CBin1.merge(CBin2.to_frame(), left_on='Animal ID', right_index=True)
    for i in allC:
        CTable = CTable.merge(i.to_frame(), left_on='Animal ID', right_index=True)
    CTable.set_index('Animal ID', inplace=True)

    #ISI TABLE
    ISIBin1 = ISIBin1.to_frame().reset_index()
    ISITable = ISIBin1.merge(ISIBin2.to_frame(), left_on='Animal ID', right_index=True)
    for i in allISI:
        ISITable = ISITable.merge(i.to_frame(), left_on='Animal ID', right_index=True)
    ISITable.set_index('Animal ID', inplace=True)

    # FARbySTim TABLE
    FARbyStim1 = FARbyStim1.to_frame().reset_index()
    FStimTable = FARbyStim1.merge(FARbyStim2.to_frame(), left_on='Animal ID', right_index=True)
    for i in allFARbyStim:
        FStimTable = FStimTable.merge(i.to_frame(), left_on='Animal ID', right_index=True)
    FStimTable.set_index('Animal ID', inplace=True)

    list_dfs = (summaryTable, stratTable, hitTable, FARTable, DTable, CTable, ISITable, FStimTable)

    writer = ExcelWriter(MeanCompiled)
    nameList = (str('Summary'), str('Strategies'), str('Hit Bins'), str('False Alarm Bins'), str('D prime bins'), str('Criterion bins'), str('ISI bins'), str('FAR by non-target'))
    loop = 0
    for n, df in enumerate(list_dfs):
        sheetName = (nameList[loop])
        df.to_excel(writer, sheetName)
        loop += 1
    writer.save()
