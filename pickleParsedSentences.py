import cPickle as pickle
import sys
from config import *

def main():
    if (not sentencesFile) or (not sentIDMapFile) or (not parsedSentencesFile):
        print "Varibles not set in config.py"
        sys.exit(0)
    
    f = open(sentencesFile, 'r')
    sentences = f.readlines()
    f.close()
    
    f = open(sentIDMapFile, 'r')
    lines = f.readlines()
    f.close()
    
    sentIDMap = {}
    for line in lines:
        (lineNum, sentID) = line.strip().split(',')
        lineNum = int(lineNum)
        sentID = int(sentID)
        sentIDMap[lineNum] = sentID
    
    f = open(parsedSentencesFile, 'r')
    lines = f.readlines()
    f.close()
    
    parseTreeStringDict = {}
    depParseDict = {}
    
    i = 0
    totalSentences = len(sentIDMap.keys())
    totalLines = len(lines)
    while i < totalLines:
        if "Sentence#" in lines[i]:
            sentNum = int(lines[i].strip().split('#')[1])
            if sentNum%10000 == 0:
                print "Parsing sentence %d/%d" %(sentNum, totalSentences)
            sentID = sentIDMap[sentNum]
            i += 1
            ptString = ""
            while lines[i].strip() and i < totalLines:
                 ptString += lines[i]
                 i += 1
            ptString = ptString.replace("\n", " ")
            i += 1
            depString = ""
            while lines[i].strip() and i < totalLines:
                 depString += lines[i]
                 i += 1
            depList = depString.strip().split('\n')

            parseTreeStringDict[sentID] = ptString
            depParseDict[sentID] = depList
        i += 1

    f = open('parseTreeStringDict.pickle', "wb")
    pickle.dump(parseTreeStringDict, f)
    f.close()

    f = open('depParseDict.pickle', "wb")
    pickle.dump(depParseDict, f)
    f.close()

            


if __name__ == "__main__":
    main()
