# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 13:40:34 2018

@author: vladis
"""
import sys
import os
import pandas as pd 
import numpy as np 
import glob
import preprocessShare as ps


sys.path.insert(0, r'../')
import Preferencies as pref


directory = os.fsencode(pref.Preferencies.PATH_DATA_FOLDER)
sys.path.insert(0, pref.Preferencies.PATH_DATA_FOLDER)
#dir = pref.Preferencies.PATH_DATA_FOLDER

#files = glob.glob(os.path.join('..\\Data2', '*.csv'))


def processSingleShare (sourcePath, targetPath):
        ops = ps.PreprocessShare ();         
        print (sourcePath, targetPath)        
        ops.preprocessFN (sourcePath, targetPath)                        
    
    
def processSharesFromFile (sourcePath, destinationFolder):        
    companyDF = pd.read_csv (sourcePath)
    columns= ['ticket', 'count+', 'count-', 'accuracy', 'total+', 'total-', 'profit']
    Data = []
    for i in range(0, len(companyDF)):     
        #try :
            companyName =  companyDF.iloc[i]['ticker']    
            path =  companyDF.iloc[i]['path']        
            destinationFileName = destinationFolder+companyName+".csv"
            processSingleShare (path, destinationFileName)
            df = pd.read_csv (destinationFileName)
            #df1= df[ (df['Gtrue']!= 0 ) & (df['Gtrue']!= None) & (df['Gtrue']!=np.nan) & (df.Gtrue.notnull())] 
            df1= df[ df.N1dTrue.notnull()] 
            destinationFileNameTag = destinationFolder+companyName+'Tag'+".csv"
            df1.to_csv (destinationFileNameTag)                    
            totalP= df1['N1dTrue'][df1['N1dTrue']>0].sum()
            totalN= df1['N1dTrue'][df1['N1dTrue']<0].sum()
            profit= (totalP + totalN)
            countP= df1['N1dTrue'][df1['N1dTrue']>0].count() 
            countN= df1['N1dTrue'][df1['N1dTrue']<0].count()
            acc= countP / (countP + countN) * 100
            Data.append([companyName,countP, countN, acc, totalP, totalN, profit])
            print ("Processed " + str(i+1) + " of " +  str(len(companyDF)) + " " +  str(((i+1) *100) / len(companyDF))  + " %")
        #except:
        #    print "Unexpected error:" + sys.exc_info()[0]
        #    continue;
        
        
        
    df2= pd.DataFrame (data= Data, columns= columns)
    df2.to_csv (destinationFolder + 'result.csv')
    print (df2)
        
        
        
        
        
        
    
            
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
