# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 15:11:27 2017

@author: vladis
"""


import sys
sys.path.insert(0, r'../PreProccessing/')
sys.path.insert(0, r'../')
import TestFramework as tf
import EStrategy as es
import time
import os, sys
import pandas as pd
from preprocessShare import PreprocessShare



#ca.initFS ()

suffix = time.strftime("%d%b%H%M%S", time.localtime(time.time()))
directoryName = "Test-" + suffix + "/"
try:   
   if not os.path.exists(directoryName):
       os.makedirs(directoryName)
except:
   print ("Failed to build " , directoryName)
else:
   print ("Created " , directoryName)
    


companyDF = pd.read_csv('../CL/CompanyList.csv')
myResults = []
labels    = ['SYMBOL','Orders','LongPositions','ShortPositions','ShortProfits', 'LongProfits', 'Total']
for i in range(0, len(companyDF)):    
    
    companyName =  companyDF.iloc[i]['ticker']    
    path =  companyDF.iloc[i]['path']
    targetFile = path
    targetPreprocessedFile = directoryName + companyName + "processed.csv"
    try:            
        print ("handling " + companyName + '  ' + str(i+1) + ' of ' + str(len(companyDF)) + " " + str((i+1)*100/len(companyDF)) +'% finished')
        md = pd.read_csv(targetFile)
        md.set_index ('date')  
    except:       
       print (targetFile +   " found to be corrupted ")   
       continue
       
    print (targetPreprocessedFile)
    ps = PreprocessShare ()
    ps.preprocessFN (targetFile, targetPreprocessedFile)
    portfolio = tf.Portfolio (100000)
    tfi = tf.TestFramework (es.TestStrategy (portfolio, True, companyName, targetDirectory=directoryName), portfolio, companyName)
    tfi.run (targetPreprocessedFile)        
    historydf = portfolio.toDataFrame ()               
    historydf.to_csv (directoryName  + companyName + "-HistoryDeals"+ suffix+".csv")    
    myResults.append ( (companyName, len(portfolio.history), historydf [historydf.position == tf.PositionType.LONG ].count()["date"], historydf [historydf.position == tf.PositionType.SHORT ].count()["date"] , portfolio.shortProfits, portfolio.longProfits,  portfolio.shortProfits + portfolio.longProfits ) )        
        
    
       
dfresult = pd.DataFrame.from_records(myResults, columns=labels)
dfresult.to_csv (directoryName +  'StrategyReport.csv')








class ParametrTesting (object):
     def __init__(self):
         self.parametrs = []
         
     def calibrateBuyLong (self):
         param = es.StrategyParameters ()
         
     def calibrateBuyShort (self):
         param = es.StrategyParameters ()
         
     def calibrateSellLong (self):
         param = es.StrategyParameters ()
         
     def calibrateSellLong (self):
         param = es.StrategyParameters ()
         
         
         





