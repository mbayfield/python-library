"""
Filename: SearchLogsForStrings.py

Description:
    Search IIS Logfiles:
    
    Report counts on searchParams

Author: Mark Bayfield
Date: 2009-07-02

Revisions:

"""
#! /usr/bin/env python

import re, os
path = "[logfile-path]"
logs = os.listdir(path)

searchParams = [
]

for param in searchParams :
    count = 0
    monthCount = 0
    searchMonth = '2009-07'
    for logDir in logs:
        logFileDir = os.path.join(path, logDir)
        
        #print( logFileDir )
        
        for logFile in os.listdir(logFileDir) :
            #print (logFile)
            file = os.path.join(logFileDir, logFile)
            #print (file)
            
            text = open(file, "r")
            
            for line in text:
                if ( str(line).find( param ) != -1 ):
                    #date = line[0:10]
                    dateYearMonth = line[0:7]
                    count += 1
                    #thisMonth = line[0:7]
                    
                    #if ( lastMonth != thisMonth ):
                    #    lastMonth = thisMonth
                    #    monthCount = 0
                        
                    #monthCount += 1
                    if ( str(dateYearMonth) == searchMonth ):
                        monthCount += 1
                        #print (line)
                            
    print (param + ' Total: ' + str(count))
    print (searchMonth + ' Total: ' + str(monthCount))
