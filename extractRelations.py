import sqlite3 as db
import nltk.tree
import cPickle as pickle
from getResults import *
import sys
from config import *

pt = nltk.tree.Tree

conn = db.connect(dbName)
c = conn.cursor()

f = open('parseTreeStringDict.pickle', "rb")
parseTreeStringDict = pickle.load(f)
f.close()

ptsd = parseTreeStringDict


f = open('depParseDict.pickle', "rb")
depParseDict = pickle.load(f)
f.close()

def getint(s):
    s =s.replace("'", "")
    return int(s)

def parseDep(dep):
    f = dep.split('(')
    one = f[0].split('_')
    if len(one) == 1:
        one.append("")
    rem = "".join(f[1:])
    rem = rem.replace(')', "")
    f = rem.split(' ')
    try:
        assert(len(f) == 2)
    except:
        print dep, f
        print "Exiting"
        sys.exit(0)
    try:
        a = f[0][0:-1]
        b = f[1]
        a = a.split('-')
        two = ["-".join(a[0:-1]), getint(a[-1])]
        b = b.split('-')
        three = ["-".join(b[0:-1]), getint(b[-1])]
    except:
        print "Value Error",dep, a, b
        print "Exiting"
        sys.exit(0)
        
    return [one, two, three]


dpDict = {}
for key in depParseDict.keys():
    dpDict[key] = []
    for dep in depParseDict[key]:
        f = dep.split('(')
        if 'prep_' in f[0]:
            depp = parseDep(dep)
            dpDict[key].append(depp)
        if 'det' == f[0]:
            depp = parseDep(dep)
            dpDict[key].append(depp)
        if 'aux' == f[0]:
            depp = parseDep(dep)
            dpDict[key].append(depp)


c.execute('Select * from Sent')
sentResults = c.fetchall()

sentDict = {}

for (id, sent) in sentResults:
    sentDict[id] = sent.encode('utf-8')

del sentResults


c.execute('Select * from FEAnnotation')
results = c.fetchall()

FEAnnotation = {}
Type = type(int())
for row in results:
    newRow = []
    for i in range(len(row)):
        if type(row[i]) != Type:
            newRow.append(row[i].encode('utf-8'))
        else:
            newRow.append(row[i])
    sentID = row[7]
    FEAnnotation.setdefault(sentID, [])
    FEAnnotation[sentID].append(row)

totalAnnotations =  len(results)
conn.close()
del results

sentIDs = FEAnnotation.keys()


lines1 = []
lines2 = []
lines3 = []
total = len(sentIDs)

parsedAnnotations = 0
parseError = 0

for sentID in sentIDs:
    sentence = sentDict[sentID]
    t = pt(ptsd[sentID])
    subtrees = list(t.subtrees())
    pos = t.pos()
    leaves = t.leaves()
    depList = dpDict[sentID]
    rows = FEAnnotation[sentID]
    
    for row in rows:

        target = row[1]
        fe = row[4]
        start = row[8]
        end = row[9]
        phrase = getPhrase(sentence, start, end)
        wc = len(phrase.split())

        results = getResults(sentence, start, end, subtrees, leaves, pos, depList, fe, target)
        
        if results:
            (headWord, phraseHeadWordPOS, phraseWordPOS, fe) = results
            s1 = "{0};{1};{2};{3};{4};{5}\n".format(target, fe, headWord, phraseHeadWordPOS, phrase.replace(';', ''), sentID)
            s2 = ""
            for p in phraseWordPOS:
                stemp = "{0};{1}\n".format(fe, p)
                s2 = s2+stemp
            s3 = "{0};{1}\n".format(fe, len(phraseWordPOS))
            lines1.append(s1)
            lines2.append(s2)
            lines3.append(s3)
        else:
            parseError += 1
        
        parsedAnnotations += 1
        if parsedAnnotations%1000 == 0:
            print "{0}/{1};{2}".format(parsedAnnotations, totalAnnotations, parseError)

print "{0}/{1};{2}".format(parsedAnnotations, totalAnnotations, parseError)
f1 = open('target-fe-head-headPOS.csv', 'w')
f2 = open('fe-POS.csv', 'w')
f3 = open('fe-count.csv', 'w')

f1.writelines(lines1)
f2.writelines(lines2)
f3.writelines(lines3)

f1.close()
f2.close()
f3.close()
