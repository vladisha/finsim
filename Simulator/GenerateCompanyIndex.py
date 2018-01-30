# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 16:52:12 2018

@author: vladis
"""
import sys
import os
import pandas as pd 
import glob
import random as rnd
import time
sys.path.insert(0, r'../')
import Preferencies as pref

files = glob.glob(os.path.join(pref.Preferencies.PATH_DATA_FOLDER , '*.csv'))

rnd.shuffle(files)

df = pd.DataFrame()
result = []
tickers = []
for index in range (0, len(files)):
    print (files[index] + " ")
    result.append(files[index])
    mystr =  files[index]
    a = mystr.replace(".csv","")
    index = a.rfind ("\\")
    name = a[index+1:]
    tickers.append (name)
    



suffix = time.strftime("%d%b%H%M%S", time.localtime(time.time()))
directoryName = "Test-" + suffix + "/"
try:   
   if not os.path.exists(directoryName):
       os.makedirs(directoryName)
except:
   print ("Failed to build " , directoryName)
else:
   print ("Created " , directoryName)
 
companies = [("ticker",tickers), ("path",result)]
df = pd.DataFrame.from_items(companies)   
df.to_csv (directoryName + 'CompanyList.csv')







    

    

    

    
    
    

    
    
    
    
    