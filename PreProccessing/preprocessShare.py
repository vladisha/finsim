# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 09:29:02 2017

@author: vladis
"""

import pandas as pd
import numpy as np

from ShareAttributes import ShareAttributes as sa

class PreprocessShare (object):
      #def __init__(self):
      def preprocessFN (self, inputFileName, outputFile):
          df = pd.read_csv (inputFileName )
          df[sa.LOW]  = pd.to_numeric(df[sa.LOW], errors='coerce')
          df[sa.HIGH] = pd.to_numeric(df[sa.HIGH], errors='coerce')
          df[sa.OPEN] = pd.to_numeric(df[sa.OPEN], errors='coerce')
          df[sa.CLOSE] = pd.to_numeric(df[sa.CLOSE], errors='coerce')
          
          #df[sa.OPEN].loc[df[sa.OPEN] == '-'] = None
        #  df[sa.CLOSE].loc[df[sa.CLOSE] == '-'] = None
         # df[sa.VOLUME].loc[df[sa.VOLUME] == '-'] = None
          #df[sa.LOW].loc[df[sa.LOW] == '-'] = None
          #df[sa.HIGH].loc[df[sa.HIGH] == '-'] = None
          #df[sa.OPEN] = df[sa.OPEN].where(df=='-', None)                     
          #preprocess Interactive
          
          self.run (df)
          df.to_csv (outputFile)
    
      def preprocessDF (self, iDF, oDF):
          #preprocess Run
          self.run (iDF)
          return oDF
      
        
      def eitan (self):
          print("aihi")
          
      def preprocessDFToFile (self, iDF, outputFile):
          #preprocess Run
          
          sa.MOVING_AVERAGE10
          self.run (iDF)
          iDF.to_csv (outputFile)
          
      def CO(self,df,shift):
          for j in shift:
              df[sa.CO+str(j)] = df[sa.CLOSE].sub(df[sa.OPEN]).shift(j) 
    
      def HC(self,df,shift):
          for j in shift:
              df[sa.HC+str(j)] = df[sa.HIGH].sub(df[sa.CLOSE]).shift(j) 
    
      def CL(self,df,shift):
          for j in shift:  
              df[sa.CL+str(j)] = df[sa.CLOSE].sub(df[sa.LOW]).shift(j) 
    
      def LO(self,df,shift):
          for j in shift:
              df[sa.LO+str(j)] = df[sa.LOW].sub(df[sa.OPEN]).shift(j)
    
      def HL(self,df,shift):
          for j in shift:
              df[sa.HL+str(j)] = df[sa.HIGH].sub(df[sa.LOW]).shift(j) 

      def COmid(self,df,shift):
          for j in shift:
              df[sa.COmid+str(j)] = (df[sa.CLOSE]+df[sa.OPEN]).shift(j)/2 
    
      def HLmid(self,df,shift):
          for j in shift:
              df[sa.HLmid+str(j)] = (df[sa.HIGH]+df[sa.LOW]).shift(j)/2
            
    #   3.3 Averaging
    
      def ANext(self,index,df,windows):    
          for i in index:
              for w in windows:
                  df[i+sa.AvgN+str(w)]=df[i].rolling(w,1).mean().shift(-w)
    
      def ALast(self,index,df,windows):    
          for i in index:
              for w in windows:
                  df[i+sa.AvgL+str(w)]=df[i].rolling(w,1).mean().shift(1)
       
    
    #   3.4 Normalization
    
      def AL_NormL(self,index,df,windows,norm):    
          for i in index:
              for w in windows:
                  dummy=df[i].rolling(w,1).mean().shift(1)
                  dummyN=df[i].rolling(norm[windows.index(w)],1).mean().shift(1)
                  df[i+sa.AvgL+str(w)+sa.NormL+str(norm[windows.index(w)])]=(dummy-dummyN)/dummyN

      def AL_SubNormL(self,index,df,windows,norm):    
          for i in index:
              for w in windows:
                  dummy=df[i].rolling(w,1).mean().shift(1)
                  dummyN=df[i].rolling(norm[windows.index(w)],1).mean().shift(1)
                  df[i+sa.AvgL+str(w)+sa.SubNormL+str(norm[windows.index(w)])]=(dummy-dummyN.mean())
    
      def AN_Norm(self,index,df,windows,norm):    
          for i in index:
              for w in windows:
                  dummy=df[i].rolling(w,1).mean().shift(-w)
                  dummyN=df[i].rolling(norm[windows.index(w)],1).mean().shift(-w)
                  df[i+sa.AvgN+str(w)+sa.NormL+str(norm[windows.index(w)])]=(dummy-dummyN)/dummyN
                    
      def Scale(self,index,df):
          for i in index:
              data=df[i]
              scaler = preprocessing.StandardScaler().fit(data)
              df[i+sa.Scale] = scaler.transform(df[i])

        
        #   3.5 Indicators
        
      def BB(self,df,window):
          for w in window:
              df[sa.UBB+str(w)]=df[sa.CLOSE].rolling(w,1).mean().shift(1)+2*df[sa.CLOSE].rolling(w,1).std().shift(1)
              df[sa.LBB+str(w)]=df[sa.CLOSE].rolling(w,1).mean().shift(1)-2*df[sa.CLOSE].rolling(w,1).std().shift(1)
              

      def HB(self,df,window):
          for w in window:
              df[sa.UHB+str(w)]=df[sa.HIGH].rolling(w,1).mean().shift(1)+2*df[sa.HIGH].rolling(w,1).std().shift(1)
              df[sa.LHB+str(w)]=df[sa.HIGH].rolling(w,1).mean().shift(1)-2*df[sa.HIGH].rolling(w,1).std().shift(1)

      def LB(self,df,window):
          for w in window:
              df[sa.ULB+str(w)]=df[sa.LOW].rolling(w,1).mean().shift(1)+2*df[sa.LOW].rolling(w,1).std().shift(1)
              df[sa.LLB+str(w)]=df[sa.LOW].rolling(w,1).mean().shift(1)-2*df[sa.LOW].rolling(w,1).std().shift(1)
              
    
    
    
    
    
    
      def HCCO(self,df,shift):
          for j in shift:
              df[sa.HCCO+str(j)]=((df[sa.HIGH].sub(df[sa.CLOSE]))/(df[sa.CLOSE].sub(df[sa.OPEN]))).shift(j)
        
      def absHCCO(self,df,shift):
          for j in shift:
              df[sa.absHCCO+str(j)]=(((df[sa.HIGH].sub(df[sa.CLOSE]))/(df[sa.CLOSE].sub(df[sa.OPEN])))**2).shift(j)
    
      def HCCL(self,df,shift):
          for j in shift:  
              df[sa.HCCL+str(j)]=((df[sa.HIGH].sub(df[sa.CLOSE]))/(df[sa.CLOSE].sub(df[sa.LOW]))).shift(j)
            
      def COOL(self,df,shift):    
          for j in shift:  
              df[sa.COOL+str(j)]=((df[sa.CLOSE].sub(df[sa.OPEN]))/(df[sa.OPEN].sub(df[sa.LOW]))).shift(j)
        
      def LOCO(self,df,shift):    
          for j in shift:  
              df[sa.LOCO+str(j)]=((df[sa.LOW].sub(df[sa.OPEN]))/(df[sa.CLOSE].sub(df[sa.OPEN]))).shift(j)
        
      def HOOL(self,df,shift):    
          for j in shift:    
              df[sa.HOOL+str(j)]=((df[sa.HIGH].sub(df[sa.OPEN]))/(df[sa.OPEN].sub(df[sa.LOW]))).shift(j)   
       
      def HLC(self,df,shift):
          for j in shift:    
              df[sa.HLC+str(j)]=((df[sa.HIGH].sub(df[sa.LOW]))*100/(df[sa.CLOSE])).shift(j)
           
      def COC(self,df,shift):
          for j in shift:    
              df[sa.COC+str(j)]=((df[sa.CLOSE].sub(df[sa.OPEN]))*100/(df[sa.CLOSE])).shift(j)
       
      def SubOMA(self,df,window):      
          for w in window:    
              df[sa.SubOMA+str(w)]=(df[sa.OPEN]-df[sa.OPENAvgL+str(w)])/df[sa.OPEN]
    
      def MinL(self,index,df,windows):    
          for i in index:  
              for w in windows:
                  df[i+sa.MinL+str(w)]=df[i].rolling(w,1).min().shift(1)                
                    
      def MaxL(self,index,df,windows):    
          for i in index:
              for w in windows:
                  df[i+sa.MaxL+str(w)]=df[i].rolling(w,1).min().shift(1)        
    
      def MinMax(self,index,df,windows):    
          for i in index:  
              for w in windows:                
                  df[i+sa.minmax+str(w)] =(df[sa.MinL+str(w)]+ df[sa.MaxL+str(w)])/2
                   
      def Grad(self,index,df):
          for i in index:  
              df[i+sa.Grad]=np.insert(np.diff(df[i]),0,0)
            
      def BOB(self,df,window): 
          for w in window:        
              df[sa.BBuO+str(w)]=(df[sa.UBB+str(w)]-df[sa.OPEN])
              df[sa.OBBl+str(w)]=(df[sa.OPEN]-df[sa.LBB+str(w)])
    
            #print (list(df))
        #   Classify            
      def UpDown(self,index,df,shift): 
          for i in index:
              for j in shift:
                  a=df[i+sa.Grad]
                  values = []
                  for k in range (len(a)):
                      if a.iloc[k] > 0:
                          values.append('Up')
                      else:
                          values.append('Down')                  
                  df[i+sa.Trend+str(j)]=values
                  df[i+sa.Trend+str(j)]=df[i+sa.Trend+str(j)].shift(j)
                             
                    
                    
                    
    # Running operations
      def  run(self, df):      
               
           df[sa.HIGH1] = df[sa.HIGH].shift(1) 
           df[sa.LOW1] = df[sa.LOW].shift(1) 
     
           
           
           yesterday1=1    
           yesterday2=2  
           yesterday3=3
           #self.CO(df,[yesterday1])
           #self.HL(df,[yesterday1,yesterday3])
           #self.HLmid(df,[yesterday1])
           #self.ALast([sa.OPEN],df,[3,5,10])
           self.BB(df,[20])
           #self.HB(df,[20])
           #self.LB(df,[20])
            
            
           #self.SubOMA(df,[3,5,10])
           #self.MinL([sa.OPEN,sa.HL+str(1)],df,[2,3,5])
           #self.MaxL([sa.OPEN,sa.HL+str(1)],df,[2,3,5])
           self.Grad([sa.OPEN],df)
           self.BOB(df,[20])
            
            
           #self.HOOL(df,[1])
           #self.COOL(df,[1])
            
            
           yesterday1=0    
           today=-1  
           next1day=-2 
             
           #self.UpDown([sa.OPEN,sa.HIGH,sa.LOW],df,[yesterday1,today,next1day])
                    