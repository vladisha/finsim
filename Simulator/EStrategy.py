# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 14:47:49 2017

@author: vladis
"""

import sys
sys.path.insert(0, r'../PreProccessing/')
import TestFramework as tf
import numpy as np
import pandas as pd 
from enum import Enum
import matplotlib.pyplot as plt
import datetime as dt

from ShareAttributes import ShareAttributes as sa


class StrategyParameters (object):
    def __init__(self):
        self.HL0MinL2l = 0.5  #buyLong
        self.HL0MinL2s = 0.5  #buyShort
        self.HL2b      = 1   #sellLong
        self.HL2s      = 1   #buyShort        
        self.OBBl     = 0.05 #sellLong
        self.BBuO     = 0.05 #sellShort
        
    
    
        

class TestStrategy (object):
    def __init__(self, portfolio, interactive = True, paperName = "", params=StrategyParameters(), targetDirectory=""):
        self.portfolio = portfolio
        self.entries = []
        self.prices  = []       
        self.dates  = []
        self.actions = tf.TradeActionRecords()
        self.interactive = interactive
        self.paperName = paperName
        self.strategyParams = params
        self.targetDirectory = targetDirectory
        
        
    
    def onTestFinished (self, df):
        
        myorders = self.portfolio.openList.copy()
        for key, myorder in myorders.items():            
            print ("closing last positions",   myorder.price, myorder.volume, myorder.position, " balance before:" , self.portfolio.balance )
            actionRecord = tf.TradeActionRecord()
            pi = self.portfolio.closePosition(key,myorder.price)
            print ("after closing last positions balance :" , self.portfolio.balance )
            self.entries.append (0.6)                   
            actionRecord.longSale = myorder.price            
            actionRecord.profit   = pi.profit
            actionRecord.relativeProfit =  pi.getRelativeProfit ()
            actionRecord.balance = self.portfolio.balance
            self.actions.addItem (myorder.date, actionRecord )    
                    
            
                    
                    
                    
#        if (self.interactive):
#            time=np.arange(len(self.prices))
#            fig = plt.figure(1)
#            ax1=plt.subplot(2,1,1)    
#            ax1.plot(time,self.prices, 'k-')
#            ax1.plot(time,self.actions.toLongBuyArray() ,'gs',label='longBuy')
#            ax1.plot(time,self.actions.toShortBuyArray() ,'rs',label='shortBuy')
#            ax1.plot(time,self.actions.toShortSaleArray() ,'y*',label='shortSell')
#            ax1.plot(time,self.actions.toLongSellArray(),'b*',label='longSell')
#            ax1.plot(time,df["CRUDEOILdaily_OAvgL3"],'m-',label='OAvgL3')
#            ax1.plot(time,df["CRUDEOILdaily_OAvgL10"],'b-',label='OAvgL10')
#            ax1.plot(time,df["CRUDEOILdaily_H"],'b--',label='H')
#            ax1.plot(time,df["CRUDEOILdaily_L"],'g--',label='L')
#            ax1.plot(time,df["CRUDEOILdaily_UBB"],'k--',label='UBB')
#            ax1.plot(time,df["CRUDEOILdaily_LBB"],'k--',label='LBB')
#            ax1.plot(time,df["CRUDEOILdaily_HLmid"],'r--',label='HLmid')  

        df ['lb'] = self.actions.toLongBuyArray()
        df ['sb'] = self.actions.toShortBuyArray()
        df ['ss'] = self.actions.toShortSaleArray()
        df ['ls'] = self.actions.toLongSellArray()
        
        
        df ['balance'] = self.actions.toBalanceArray ()
        df ['profit'] = self.actions.toProfitArray ();
        df ['rprofit'] = self.actions.toRelativeProfitArray ()
        
        df ['desc'] = self.actions.toDescriptionArray()
        outputName =  self.targetDirectory + self.paperName + '-output.csv'
        df.to_csv (outputName)
        
#        if (self.interactive):
#            ax1.legend()
#            plt.show ()


      
       
        
    def onPriceUpdate (self, sh):    
        
        if (not sh.isValid () or sh.open==0):            
            self.actions.addItem (sh.date, tf.TradeActionRecord() ) 
            return
        
        y1=sh.getAuxAttribute (sa.SubOMA3)
        y2=sh.getAuxAttribute (sa.SubOMA10)
        y3=sh.getAuxAttribute (sa.OPEN)
        #y4=sh.getAuxAttribute (sa.OpenAvgL3)
        #y5=sh.getAuxAttribute(sa.OpenAvgL10)
        y6=sh.getAuxAttribute(sa.HL3)
        y7=sh.getAuxAttribute(sa.HL1MinL3)
        y8=sh.getAuxAttribute(sa.HL1MaxL3)
        y9=sh.getAuxAttribute(sa.OBBl15)
        y10=sh.getAuxAttribute(sa.BBuO15)
        y11=sh.getAuxAttribute(sa.OpenGrad)
        y12=sh.getAuxAttribute(sa.LOWGrad)
        y13=sh.getAuxAttribute(sa.HIGHGrad)

#        passedxDays = False
#        if (self.portfolio.hasOpenPositions()):
#            latestposition = self.portfolio.getLatestPosition ()
#            datetime_object = dt.datetime.strptime(latestposition.date, '%Y-%m-%d')
#            currentDate = dt.datetime.strptime(sh.date, '%Y-%m-%d')
#            delta = currentDate - datetime_object
#            datethreshold = dt.timedelta(days=2)
#            if (delta > datethreshold):
#                passedxDays = True
         
        BuyLong = y1 > 0 and y2 > 0 and y7 > self.strategyParams.HL0MinL2l and y11 > 0 and y10 > 0 and y12 > 0
        SellLong = (y1 < 0 and y2 < 0) or (y3 > y5 and y3 < y4) or (y6 < 1) or y10 < y9*self.strategyParams.OBBl or y12 < 0
        BuyShort = y1 < 0 and y2 < 0 and y7 >self.strategyParams.HL0MinL2s and y11 < 0 and y9 > 0 and y12 < 0
        SellShort= (y1 > 0 and y2 > 0) or (y3 < y5 and y3 > y4) or (y6 < 1) or y9 < y10*self.strategyParams.BBuO
        
        
        sellReason = ""
        
        if (SellLong):
            if ((y1 < 0 and y2 < 0)):
                sellReason = sellReason + " Current point is below 3 day and 10 day moving average"
            if ((y3 > y5 and y3 < y4)):
                sellReason = sellReason + " Daily is bigger than 10 day average and daily is smaller than 3 day average"
            if ((y6 < 1)):
                sellReason = sellReason + " low two days ago is smaller than 1"
            if (( y10 < y9*0.05)):
                sellReason = sellReason + " BB upper - open is smaller than 0.05*open - BB lower"
            if ((  y12 < 0)):
                sellReason = sellReason + " low gradient is smaller than 0 "
        
        if (SellShort):
            if (y1 > 0 and y2 > 0):
                sellReason = sellReason + " Current point is above 3 day and 10 day moving average "
            if ((y3 < y5 and y3 > y4)):
                sellReason = sellReason + " Daily is smaller than 10 day average and daily is bigger than 3 day average "                
            if (y6 < 1):
                sellReason = sellReason + " low two days ago is smaller than 1 "
            if (y9 < y10*0.05):
                sellReason = sellReason + " open - BB lower is smaller than 0.05*BB upper - open "
                
        
        self.prices.append (sh.open)
        self.dates.append (sh.date)
        
        actionRecord = tf.TradeActionRecord()
        actionRecord.description =sellReason
        myorders = self.portfolio.openList.copy()
        for key, myorder in myorders.items():
            if (myorder.position==tf.PositionType.LONG):
                if (SellLong):
                    pi = self.portfolio.closePosition(key,sh.open)
                    self.entries.append (0.6)                   
                    actionRecord.longSale = sh.open
                    
                    actionRecord.profit   = pi.profit
                    actionRecord.relativeProfit =  pi.getRelativeProfit ()
                    actionRecord.balance = self.portfolio.balance
                    
            elif (myorder.position==tf.PositionType.SHORT): #short case
                if (SellShort):
                    pi = self.portfolio.closePosition(key,sh.open)
                    self.entries.append (0.8)
                    actionRecord.shortSale = sh.open
                    actionRecord.profit   = pi.profit
                    actionRecord.relativeProfit =  pi.getRelativeProfit ()
                    actionRecord.balance = self.portfolio.balance
                    
        
        amount = int(self.portfolio.balance * 0.25 / sh.open)
        if y6 < 1:
            amount = int(self.portfolio.balance * 0.12 / sh.open)
        
        
        
        if (amount > 0 and not self.portfolio.hasOpenPositions()):           
            if (BuyLong):
                self.portfolio.openLongPosition ("crude",sh.open , amount,sh.date)    
                self.entries.append (0.2)
                actionRecord.longBuy = sh.open 
                #actionRecord.description ="y1 > 0 and y2 > 0 and y7 > 0.5 and y11 > 0 and y10 > 0 and y12 > 0"
                          
            elif (BuyShort) :
                self.portfolio.openShortPosition ("crude",sh.open , amount,sh.date)  
                self.entries.append (0.4)                  
                actionRecord.shortBuy = sh.open;
                #actionRecord.description =" y1 < 0 and y2 < 0 and y7 > 0.5 and y11 < 0 and y9 > 0 and y12 < 0"
                    
        self.actions.addItem (sh.date, actionRecord )          
        
