try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
    
import sqlite3 as db
import sys
import os


def parseFrameFiles(c, framePath, tagPrefix =  "{http://framenet.icsi.berkeley.edu}"):


    fileNames = os.listdir(framePath)

    FrameTableData=[]
    FETableData = []
    LUTableData = []

    for fileName in fileNames:
        if fileName.split('.')[-1] != 'xml':
            continue
        tree = ET.ElementTree(file = framePath+fileName)
        root = tree.getroot()

        frameID = int(root.attrib.get('ID'))
        frameName = root.attrib.get('name')

        frameData = (frameID, frameName) 
        FrameTableData.append(frameData)
        
        for child in root:
            if child.tag == tagPrefix+"FE":
                feID = child.attrib.get('ID')
                feName = child.attrib.get('name')
                feCoreType = child.attrib.get('coreType')
                feAbbrev = child.attrib.get('abbrev')
                feData = (feID, feName, frameID, feCoreType, feAbbrev)
                FETableData.append(feData)
            if child.tag == tagPrefix+"lexUnit":
                luID = child.attrib.get('ID')
                luName = child.attrib.get('name')
                luPOS = child.attrib.get('POS')
                for subchild in child:
                    if subchild.tag == tagPrefix+"sentenceCount":
                        luAnnotated = int(subchild.attrib.get('annotated'))
                luData = (luID, luName, frameID, luPOS, luAnnotated)
                LUTableData.append(luData)          

    print "Frame Table # rows: ", len(FrameTableData)
    print "FE Table # rows: ", len(FETableData)
    print "LU Table # rows: ", len(LUTableData)

    c.executemany('Insert into FRAME Values(?, ?)', FrameTableData)
    c.executemany('Insert into FE Values(?, ?, ?, ?, ?)', FETableData)
    c.executemany('Insert into LU Values(?, ?, ?, ?, ?)', LUTableData)

