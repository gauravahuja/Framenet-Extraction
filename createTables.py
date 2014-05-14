import sqlite3 as db
import sys
import os
from config import *


def createTables(c):

    frameTable = """CREATE TABLE FRAME( ID INT, 
                        Name varchar(200))"""
    luTable = """CREATE TABLE LU(    ID INT, 
                        Name varchar(200), 
                        FrameID INT, 
                        POS varchar(10), 
                        AnnotatedSentences INT)"""
    feTable = """CREATE TABLE FE(    ID INT, 
                        Name varchar(200), 
                        FrameID INT, 
                        CoreType varchar(200), 
                        Abbrev varchar(100))"""
    feAnnotationTable = """CREATE TABLE FEAnnotation(  FrameID INT, 
                                LUName varchar(200), 
                                LUID INT, 
                                FEID INT, 
                                FEName varchar(200), 
                                PT varchar(200), 
                                GF varchar(200), 
                                SentID INT, 
                                start INT, 
                                end INT, 
                                WordCount INT)"""
    sentTable = """CREATE TABLE Sent(  ID INT, 
                        Text varchar(2000))"""

    c.execute(frameTable)
    c.execute(luTable)
    c.execute(feTable)
    c.execute(feAnnotationTable)
    c.execute(sentTable)

