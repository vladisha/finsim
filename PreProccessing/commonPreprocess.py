# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 13:40:34 2018

@author: vladis
"""
import sys
import os
import pandas as pd 
import glob
import preprocessShare as ps
sys.path.insert(0, r'../Data2/')

directory = os.fsencode('../Data2/')

dir = '../Data2/'
#files = glob.glob(os.path.join('..\\Data2', '*.csv'))


def processSingleShare (sourcePath, targetPath):
        ops = ps.PreprocessShare ();         
        print (sourcePath, targetPath)        
        ops.preprocessFN (sourcePath, targetPath)                        
    
    
def processSharesFromFile (sourcePath, destinationFolder):        
    companyDF = pd.read_csv (sourcePath)
    for i in range(0, len(companyDF)):        
        companyName =  companyDF.iloc[i]['ticker']    
        path =  companyDF.iloc[i]['path']        
        destinationFileName = destinationFolder+companyName+".csv"
        processSingleShare (path, destinationFileName)
        
            
# =============================================================================
# for filename in files:
#     suffix = ".csv"    
#     if filename.endswith (suffix):    
#         print (filename)
#        
#         sourcePath = "../Data2/" + str(filename)
#         targetPath = "../PData/" + str(filename)
#         print (sourcePath)
#         print (targetPath)
#         
#        # try:                
#             
#             #md = pd.read_csv ("C:/Users/vladis/finsim//Data2/AAP.csv")
#             #print (targetPath + "OK")            
#         ops = ps.PreprocessShare (); 
#         
#         print (sourcePath)
#         
#         ops.preprocessFN (sourcePath, targetPath)                        
#         #except:       
#         #   print ("ERROR" + targetPath)   
#         #   continue   
#         #print(os.path.join(directory, filename))        
#         
#     else:
#         continue
# =============================================================================
