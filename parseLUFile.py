try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
    
import sqlite3 as db
import sys
import os

def parseLUFiles(c, luPath, tagPrefix = "{http://framenet.icsi.berkeley.edu}"):

    fileNames = os.listdir(luPath)

    sentDict = {}
    FEAnnotationTableData = []

    totalFiles = len(fileNames)
    count = 0
    for fileName in fileNames:
        
        if count%1000 == 0:
            print "Parsed LU files %d/%d" %(count, totalFiles)
        count +=1 
        
        if fileName.split('.')[-1] != 'xml':
            continue
            
        tree = ET.ElementTree(file = luPath+fileName)
        root = tree.getroot()
        
        frameID = int(root.attrib.get('frameID'))
        luID = int(root.attrib.get('ID'))
        luName = root.attrib.get('name')
        luPOS = root.attrib.get('POS')
        
        for child in root.iter():
            if child.tag == tagPrefix+'sentence':
                annotationDict = {}
                sentTree = child
                sentID = int(sentTree.attrib.get('ID'))
                sentText = ""
                for sentChild in sentTree.iter():
                    if sentChild.tag == tagPrefix+'text':
                        sentText = sentChild.text
                        
                    if sentChild.tag == tagPrefix+'layer':
                        layer = sentChild
                        layerName = layer.attrib.get('name')
                        
                        for label in layer:
                            if label.tag != tagPrefix+'label':
                                continue
                            
                            start = int(label.attrib.get('start', -1))
                            end = int(label.attrib.get('end', - 1))
                            labelName = label.attrib.get('name')
                            labelID = int(label.attrib.get('feID', -1))
                            
                            if start == -1 or end == -1:
                                #print "ERROR", fileName, label.attrib
                                continue
                                
                            if (start, end) not in annotationDict:
                                annotationDict[(start, end)] = {}
                            
                            annotationDict[(start, end)][layerName] = (labelName, labelID)
                    #end if layer
                #end for sentChild
                sentDict[sentID] = sentText
                
                for key in annotationDict.keys():
                    ad = annotationDict[key]
                    if ad.get('FE', None) == None:
                        continue
                    start = key[0]
                    end = key[1]
                    feName = ad.get('FE')[0]
                    feID = ad.get('FE')[1]
                    ptName = ad.get('PT', ("", 0))[0]
                    gfName = ad.get('GF', ("", 0))[0]
                    wc = len(sentText[start:end+1].strip().split())
                    
                    feAnnotationData = (frameID, luName, luID, feID, feName, ptName, gfName, sentID, start, end, wc)
                    FEAnnotationTableData.append(feAnnotationData)
            #end if sentence
        #end root.iter
                           
    print "Parsed LU file %d/%d" %(count, totalFiles)
    print "Number of Sentences: ", len(sentDict.keys())
    print "Number of rows in FEAnnotation: ", len(FEAnnotationTableData)

    c.executemany('Insert into Sent Values(?, ?)', sentDict.items())
    c.executemany('Insert into FEAnnotation Values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', FEAnnotationTableData)

