# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 11:42:29 2018

@author: vladis
"""
import sys
sys.path.insert(0, r'../')
import Preferencies as pref

sys.path.insert(0, r'../PreProccessing/')
import commonPreprocess as cp
import time



suffix = time.strftime("%d%b%H%M%S", time.localtime(time.time()))
directoryName = pref.Preferencies.TEST_FOLDER  + "Test-" + suffix + "\\"
 
try:   
   if not os.path.exists(directoryName):
       os.makedirs(directoryName)
except:
   print ("Failed to build " , directoryName)
else:
   print ("Created " , directoryName)
   
   
cp.processSharesFromFile ("../CL/CompanyList.csv", directoryName)
   





#

