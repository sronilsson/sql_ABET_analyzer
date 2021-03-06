## ABET SQL analyzer in python 3.x

#### Coverts Campden Lafayette [ABETdb touchscreen databases](http://lafayetteneuroscience.com/products/abetii-touch-screen-software) to [SQL](https://docs.python.org/2/library/sqlite3.html) and analyses [rCPT data](https://campdeninstruments.com/products/image-cpt-mice) generated in the Campden Lafayette system. The output provided in two multi-sheet excel files.

![alt-text-1](images/Pic1.jpg "Touchscreen operant box version 1") ![alt-text-1](images/Pic2.jpg "Touchscreen operant box version 2")

Can save time, and produces more performance variables (about 70 organised behavioural outcomes measures) than default ABET method. 
- The program can save time as databases doesn't have to be analysed separately, e.g., run a single analysis on as many ABETdb files you want. 
- The program recognises the Animal IDs even though the animal was run on different sets and stored in different databases.
- The program calculates collapsed mean, for all the sessions for each animal that the user specified to analyse, for all outcomes variables, in seperate excel sheet. 

To run, place all databases (.ABETdb files) that should be analysed in same folder as the program and run abet_cal.py.

##### The CLI program gives six options for specifying which sessions to analyse:

* 1 - Animal IDs: Extract and Analyse data defined by animal IDs
* 2 - Calender: Extract and Analyse data defined by experiment dates
* 3 - Animal IDs / Calender: Extract and Analyse data defined by experiment dates AND animal IDs
* 4 - Schedule: Extract and Analyse data defined by schedule/stage name(s)
* 5 - Computer: Extract and Analyse data from specific computer(s)
* 6 - All data: Extract and Analyse entire database(s)

##### The program extracts then extracts the following, standard, behavioural variables for each session, as well as collapsed descriptive statistics for the analyzed sessions:

* Hits, misses, false alarms, and correct rejections
* Hit rate, False alarm rate
* Response criterion (c)
* Discrimination sensivitity (d')
* Hit latency, false alarm latency, reward retrieval latency
* ISI touches
* Front beam breakes, Back beam breaks
* The data in 5min bins for: Hit rate, False alarm rate, Discrimination sensivitity (d'), Response criterion (c)

##### The program also extracts the following additional behavioural variables for each session and their collapsed descriptive statistics:

* Latency Between Hits (MEAN)
* Latency Between Hits (STDEV)
* Latency Between Hits (MAX)
* Latency Between Stimuli Responses (MEAN)
* Latency Between Stimuli Responses (STDEV)
* Latency Between Stimuli Responses (MAX)
* Trials Between Stimuli Responses (MEAN)
* Trials Between Stimuli Responses (STDEV)
* Trials Between Stimuli Responses (MAX)
* False Alarm Bout Length (MEAN)
* False Alarm Bout Length (STDEV)
* False Alarm Bout Length (MAX)
* Hit Bout Length (MEAN)
* Hit Bout Length (STDEV)
* Hit Bout Length (MAX)
* Latency Reward Retrieval --> Front Beam Break (MEAN)
* Latency Reward Retrieval --> Front Beam Break (STDEV)
* Latency Retrieval --> Front Beam Break (MAX)

##### The program also extracts the following additional behavioural, for analysing distributions and lapses/on-task bouts relevant for attentional control:

* Time Between Hits (MIN)
* Time Between Hits (RANGE)
* Time Between Hits (SKEW)
* Time Between Hits (KURTOSIS)
* Time Between Hits (VARIANCE)
* Inactivity time (MIN)
* Inactivity time (RANGE)
* Inactivity time (SKEW)
* Inactivity time (KURTOSIS)
* Inactivity time (VARIANCE)
* Inactivity trials (MIN)
* Inactivity trials (RANGE)
* Inactivity trials (SKEW)
* Inactivity trials (KURTOSIS)
* Inactivity trials (VARIANCE)
* False Alarm Bout (MIN)
* False Alarm Bout (RANGE)
* False Alarm Bout (SKEW)
* False Alarm Bout (KURTOSIS)
* False Alarm Bout (VARIANCE)
* Hit Bout (MIN)
* Hit Bout (RANGE)
* Hit Bout (SKEW)
* Hit Bout (KURTOSIS)
* Hit Bout (VARIANCE)
* Latency Retrieval --> Front Beam Break (MIN)
* Latency Retrieval --> Front Beam Break (RANGE)
* Latency Retrieval --> Front Beam Break (SKEW)
* Latency Retrieval --> Front Beam Break (KURTOSIS)
* Latency Retrieval --> Front Beam Break (VARIANCE)

##### The code also extracts false alarm rates for each of four non-target stimuli, in output-sheet FAR_by_Stimuli:
* FAR stimulus 1/2
* FAR stimulus 3
* FAR stimulus 4
* FAR stimulus 5

##### Dependencies
* The microsoftdB --> SQLite conversion requires [mdb-export-all](https://github.com/pavlov99/mdb-export-all)
* statistics
* pandas
* sqlite3
* scipy
* tqdm
* csv
* shutil
* tabulate
* glob
* xlwt


