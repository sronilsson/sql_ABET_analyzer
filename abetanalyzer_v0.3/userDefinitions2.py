from tabulate import tabulate
from printArt import printLogo1, printLogo2


def userDefinitions2(perfFunc, input1, extractSet, extractIDs, extractDAYS, extractSch, extractComp):
    printLogo2()
    input1 = 0
    extractSet = 0
    perfFunc = []
    loop = 0
    extractIDs = []
    extractDAYS = []
    extractSch = []
    extractComp = []
    userInput = 0
    headers = ['INPUT #', 'DESCRIPTION']
    table1 = [["1", "SQL migration and Analyse: Migrate the database(s) to SQLite3 and analyse the data"], \
             ["2", "SQL migration: Migrate the database(s) to SQLite3 but do not analyse the data"], \
             ["3", "Analyse: The databases are already in SQLite3 format and I want to analyse the data"]]
    table1 = tabulate(table1, headers, tablefmt="fancy_grid")
    print(table1)
    print('\n')
    perfFunc = input("INPUT #: ")
    perfFunc = int(perfFunc)
    if perfFunc == 2:
        input1 = 0
        extractSet = 1
        extractIDs = 1
        extractDAYS = 1
        extractSch = 1
        extractComp = 0
    if perfFunc == 1 or perfFunc == 3:
        print('\n' * 100)
        printLogo2()
        table2 = [["1", "Animal IDs: Extract and Analyse data defined by animal IDs"], \
                 ["2", "Calender: Extract and Analyse data defined by experiment dates"], \
                 ["3", "Animal IDs / Calender: Extract and Analyse data defined by experiment dates AND animal IDs"], \
                 ["4", "Schedule: Extract and Analyse data defined by schedule/stage name(s)"], \
                 ["5", "Computer: Extract and Analyse data from specific computer(s)"], \
                 ["6", "All data: Extract and Analyse entire database(s)"]]
        table2 = tabulate(table2, headers, tablefmt="fancy_grid")
        print (table2)
        print('\n')
        extractSet = input("INPUT #: ")
        extractSet = int(extractSet)

        # USER DEFINED IDs
        if extractSet == 1:
            loop += 1
            while userInput != 'XX':
                if loop == 1:
                    userInput = input(str("Animal ID #") + str(loop) + str(": "))
                    extractIDs.append(userInput)
                if loop > 1:
                    userInput = input(str("Animal ID #") + str(loop) + str(" (enter 'XX' if finished): "))
                    if userInput != 'XX':
                        extractIDs.append(userInput)
                loop += 1
        loop = 0
        # USER DEFINED DATES
        if extractSet == 2:
            loop += 1
            input1 = input(str("Specify date range or individual dates (1=Range, 2=Individual): "))
            input1 = int(input1)
            if input1 == 1:
                while loop <= 2:
                    if loop == 1:
                        userInput = input(str("Start date (YYYY-MM-DD): "))
                        extractDAYS.append(userInput)
                    if loop > 1:
                        userInput = input(str("End date (YYYY-MM-DD): "))
                        extractDAYS.append(userInput)
                    loop += 1
            if input1 == 2:
                while userInput != 'XX':
                    if loop == 1:
                        userInput = input(str("Date (YYYY-MM-DD) #") + str(loop) + str(": "))
                        extractDAYS.append(userInput)
                    if loop > 1:
                        userInput = input(str("Date (YYYY-MM-DD) #") + str(loop) + str(" (enter 'XX' if finished): "))
                        if userInput != 'XX':
                            extractDAYS.append(userInput)
                    loop += 1
            loop = 0
        # USER DEFINED DATES AND IDs
        if extractSet == 3:
            loop += 1
            input1 = input(str("Specify date range or individual dates (1=Range, 2=Individual): "))
            input1 = int(input1)
            if input1 == 1:
                while loop <= 2:
                    if loop == 1:
                        userInput = input(str("Start date (YYYY-MM-DD): "))
                        extractDAYS.append(userInput)
                    if loop > 1:
                        userInput = input(str("End date (YYYY-MM-DD): "))
                        extractDAYS.append(userInput)
                    loop += 1
            if input1 == 2:
                while userInput != 'XX':
                    if loop == 1:
                        userInput = input(str("Date (YYYY-MM-DD) #") + str(loop) + str(": "))
                        extractDAYS.append(userInput)
                    if loop > 1:
                        userInput = input(str("Date (YYYY-MM-DD) #") + str(loop) + str(" (enter 'XX' if finished): "))
                        if userInput != 'XX':
                            extractDAYS.append(userInput)
                    loop += 1
            loop = 0
            loop += 1
            userInput = ''
            while userInput != 'XX':
                if loop == 1:
                    userInput = input(str("Animal ID #") + str(loop) + str(": "))
                    extractIDs.append(userInput)
                if loop > 1:
                    userInput = input(str("Animal ID #") + str(loop) + str(" (enter 'XX' if finished): "))
                    if userInput != 'XX':
                        extractIDs.append(userInput)
                loop += 1
        # USER DEFINED Schedule Name
        if extractSet == 4:
            loop += 1
            while userInput != 'XX':
                if loop == 1:
                    userInput = input(str("Name of Schedule #") + str(loop) + str(": "))
                    extractSch.append(userInput)
                if loop > 1:
                    userInput = input(str("Name of Schedule #") + str(loop) + str(" (enter 'XX' if finished): "))
                    if userInput != 'XX':
                        extractSch.append(userInput)
                loop += 1
        # USER DEFINED Computer Name
        if extractSet == 5:
            loop += 1
            while userInput != 'XX':
                if loop == 1:
                    userInput = input(str("Name of Computer #") + str(loop) + str(": "))
                    extractComp.append(userInput)
                if loop > 1:
                    userInput = input(str("Name of Computer #") + str(loop) + str(" (enter 'XX' if finished): "))
                    if userInput != 'XX':
                        extractComp.append(userInput)
                    loop += 1
                loop += 1
        input1 = int(input1)

    return perfFunc, input1, extractSet, extractIDs, extractDAYS, extractSch, extractComp

