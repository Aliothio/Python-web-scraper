#!/usr/bin/env python3 


import os
from time import localtime, strftime

# Make the finance directory if it doesn't exist
def makeFinance():
    if not os.path.isdir('.finance'):
        os.mkdir('.finance')

# Check to see if a previous file for the current symbol exists and if so provide the name
def doesFileExist(filename):
    for file in os.listdir('.finance'):
        if file.startswith(filename):
            return True, file
    return False, None

# Remove the file here so I don't need to import os in stock.py
def deleteFile(filename):
    os.remove(filename)

# Format the time to be added to the end of the new file name for the current symbol
def makeFile(filePath):
    file_time = strftime("%Y-%m-%d_%H:%M:%S", localtime())
    return open(filePath+'_'+file_time, 'w')