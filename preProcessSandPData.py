import os
from shutil import copy
from datetime import datetime

qstkDataDir = './Yahoo'
newDataDir = './recentSandp500'

qstkStockList = sorted(os.listdir(qstkDataDir))
newDataStockList = sorted(os.listdir(newDataDir))

#names after list renamed
newNameList = []

headers = 'Date, Open, High, Low, Close, Volume, Adj Close\n'

def reverseCSV(fileName):
    #reverse the order of tuples into a csv file
    fileHandle = open(fileName, "r+")
    contents = fileHandle.readlines()

    #test if file is already in the correct order already
    firstTupleDate = datetime.strptime(contents[1].split(",")[0], '%Y-%m-%d')
    lastTupleDate = datetime.strptime(contents[-1].split(",")[0], '%Y-%m-%d')
    if (firstTupleDate < lastTupleDate):
       #delete file contents
       fileHandle.seek(0)
       fileHandle.truncate()

       #write new headers
       fileHandle.write(headers)

       #remove original headers
       del contents[0]

       for line in contents[::-1]:
           temp = line.split(",")

           #remove symbol
           del temp[-1]

           #index 4 is close
           #use daily close as adjusted close
           temp.append(temp[4])

           #add newline to end of string
           fileHandle.write(",".join(temp) + "\n")

    fileHandle.close()

def renameNewData(changeList):
    #change names of new data to have names that follow the same pattern as qstk
    newNames = []

    #if file has no underscore then nothing needs to be changed
    for fileName in changeList:
       if ("_" in fileName):
           newName = fileName.split("_")[0] + ".csv"
           os.rename(os.path.join(newDataDir, fileName), os.path.join(newDataDir, newName))
       else:
          newName = fileName
       newNames.append(newName)

    newNames = sorted(newNames)
    return newNames

def combineFiles(qstkStockList, newStockList):
    for stock in newStockList:
       if (stock in qstkStockList):
           fileQstkHandle = open(os.path.join(qstkDataDir, stock), "r+")
           fileNewDataHandle = open(os.path.join(newDataDir, stock), "r")
      
           qstkContents = fileQstkHandle.readlines()
           newDataContents = fileNewDataHandle.readlines()

           mostRecentQstkDate = datetime.strptime(qstkContents[1].split(",")[0], '%Y-%m-%d')
           oldestNewDataDate = datetime.strptime(newDataContents[-1].split(",")[0], '%Y-%m-%d')

           if (mostRecentQstkDate < oldestNewDataDate):
               #delete file contents
               fileQstkHandle.seek(0)
               fileQstkHandle.truncate()

               #write header
               fileQstkHandle.write(headers)

               #write combined data into QSTK file
               fileQstkHandle.write("".join(newDataContents[1:]))
               fileQstkHandle.write("".join(qstkContents[1:]))
           else:
               print("Date mix: %s" % (stock))
           fileQstkHandle.close()
           fileNewDataHandle.close()
       else:
           #if stock isn't in qstk then add it
           copy(os.path.join(newDataDir, stock),os.path.join(qstkDataDir, stock))

def reverseNewFiles(listToReverse):
   for stockFile in listToReverse:
       reverseCSV(os.path.join(newDataDir, stockFile))



#reverseNewFiles(newDataStockList)
#newNameList = renameNewData(newDataStockList)
#combineFiles(qstkStockList, newNameList)
