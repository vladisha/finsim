# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 09:29:31 2017

@author: vladis
"""
import numpy as np
import pandas as pd 
from enum import Enum
import random
import collections
import matplotlib.pyplot as plt
import datetime as dt
import sys
sys.path.insert(0, r'../TestFrameWork/')
from ShareAttributes import ShareAttributes as sa
import math


class Share (object):
    def __init__(self, symbol=""):
        self.date   = ""
        self.symbol = symbol
        self.high   = 0
        self.low    = 0
        self.open   = 0
        self.close  = 0
        self.volume = 0
        self.record = None
        
    def init (self,shareRecord,symbol=""):
        self.record = shareRecord 
        self.date   = shareRecord [sa.DATE]
        self.symbol = symbol
        self.high   = shareRecord [sa.HIGH]
        self.low    = shareRecord [sa.LOW]
        self.open   = shareRecord [sa.OPEN]
        self.close  = shareRecord [sa.CLOSE]
        self.volume = shareRecord [sa.VOLUME]
        
    def getAuxAttribute (self,attributeName):
        return self.record[attributeName]
    
    def isValid (self):
        if ( math.isnan(self.high) or math.isnan(self.open) or math.isnan(self.low) or math.isnan(self.close) ):
            return False
        return True
        
        

class OrderStatus (Enum):
    PENDING =0
    OPEN=1
    CLOSED=2
    
class PositionType (Enum):
    SHORT = 1
    LONG  = 2
    
class PortfolioItem (object):    
    myGlobalId = 1000
    def __init__(self, symbol, price, volume,date, position = PositionType.LONG):                
        self.orderId    = PortfolioItem.myGlobalId #random.randint (1000, 100000000)
        self.symbol     = symbol
        self.price      = price
        self.volume     = volume
        self.status     = OrderStatus.PENDING        
        self.position   = position
        self.closePrice = 0
        self.profit     = 0
        self.date       = date
        PortfolioItem.myGlobalId = PortfolioItem.myGlobalId + 1
        
    
    def closePosition (self, price):
        self.closePrice = price
        self.status = OrderStatus.CLOSED
        if (self.position == PositionType.LONG):
            self.profit = (self.closePrice - self.price )*self.volume
        else:
            self.profit = (self.price - self.closePrice)*self.volume
    
    def getRelativeProfit (self):
        if (self.closePrice == 0):
            return 0
        return self.profit * 100 / (self.closePrice*self.volume)
            
    
                                

class Portfolio (object):
    def __init__(self, balance):
        self.openList = collections.OrderedDict ()
        self.history  = collections.OrderedDict ()
        self.balance  = balance
        self.shortProfits = 0
        self.longProfits  = 0
    
    def canOpenOrder (self, symbol, price, volume):
        if (price * volume < self.balance):
            return True
        return False
        
    def openLongPosition (self, symbol, price, volume,date):
      #  print ("Date:"+ date +" Open long position for price " + "{:.2f}".format(price)  + " volume " + str(volume)  +  "  balance before " + "{:.2f}".format( self.balance) + "  balance after:" +  "{:.2f}".format( self.balance - price * volume) )
        pi = PortfolioItem (symbol, price, volume,date)
        pi.status = OrderStatus.OPEN
        self.balance =  self.balance - price * volume 
        self.openList[pi.orderId] = pi
        
    
    def openShortPosition (self, symbol, price, volume,date):
      #  print ("Date:"  + date +" Open short position for price " + "{:.2f}".format( price) + " volume " + str(volume) +  "  balance before:" + "{:.2f}".format( self.balance)  + "  balance after:" +  "{:.2f}".format( self.balance - price * volume) )
        pi = PortfolioItem (symbol, price, volume, date, position = PositionType.SHORT )
        pi.status = OrderStatus.OPEN
        self.balance =  self.balance - price * volume 
        self.openList[pi.orderId] = pi
    
    def getLatestPosition (self):
        if (self.hasOpenPositions()):          
            for key, value in self.openList.items():
                return value
        return None
        
    
        
    def closePosition (self, orderId, price):
      
        #self.openList.
        pi = self.openList[orderId]
        pi.closePosition (price)
        #self.balance = self.balance + pi.profit
        if (pi.position == PositionType.LONG):
            self.balance = self.balance +  price*pi.volume
            self.longProfits += pi.profit
        else:
            self.balance = self.balance +  2*(pi.price * pi.volume) - price * pi.volume
            self.shortProfits += pi.profit
        
       # print ("close position for price " + str(price) + " Profit:  " + "{:.2f}".format( pi.profit)  +  "  balance " + "{:.2f}".format( self.balance) + " short profit " + "{:.2f}".format( self.shortProfits) + " long profit " + "{:.2f}".format( self.longProfits) )          
        self.history[orderId] = pi
        del self.openList [orderId]
        return pi
        
    def hasOpenPositions (self):
        return (len(self.openList)>0)
        
    def printPortfolio (self):
        print ("Portfolio value" , self.balance , " long profits " + "{:.2f}".format( self.longProfits) + " shorts " + "{:.2f}".format( self.shortProfits))
        

    def toDataFrame (self):
        hist = [("date",[value.date   for key, value in self.history.iteritems()]),
         ("orderId",[value.orderId   for key, value in self.history.iteritems()] ),
         ("symbol",[value.symbol   for key, value in self.history.iteritems()] ),
         ("price",[value.price   for key, value in self.history.iteritems()] ),
         ("volume",[value.volume   for key, value in self.history.iteritems()]),
         ("status",[value.status   for key, value in self.history.iteritems()]),
         ("position",[value.position   for key, value in self.history.iteritems()]),
         ("closePrice",[value.closePrice   for key, value in self.history.iteritems()]),
         ("profit",[value.profit   for key, value in self.history.iteritems()]),
         ("rp%",    [((value.profit/value.volume)*100)/value.price   for key, value in self.history.iteritems()]),
         ("perDeal%", [ (value.profit*100)/(value.price*value.volume )  for key, value in self.history.iteritems()])
         ]
        df = pd.DataFrame.from_items(hist)
        return df
        
        
        
    
    
        

class TestFramework (object):
    def __init__(self, strategy, portfolio, symbol=""):
        self.symbol      = symbol
        self.myPortfolio = portfolio
        self.strategy    = strategy
    
    def run (self, fileName):        
        df = pd.read_csv(fileName)                
        for index, row in df.iterrows():
            sh = Share (self.symbol)            
            sh.init (row,symbol=self.symbol)
            self.strategy.onPriceUpdate (sh) 
            
        self.strategy.onTestFinished (df)        
        self.myPortfolio.printPortfolio()
        
class TradeActionRecord (object):
     def __init__(self):
        self.date      = None
        self.shortSale = None
        self.shortBuy  = None
        self.longSale  = None
        self.longBuy   = None
        
        self.profit    = None
        self.balance   = None
        self.relativeProfit    = None
        
        self.description = ""
   # def printme (self):
    #    print ('date:' + self.date + " ss: " + self.shortSale + ' sb:' + self.shortBuy + ' ls:' + self.longSale + ' lb:' + self.longBuy )
        
        
class TradeActionRecords (object):
    def __init__(self):
        self.tradeAction = collections.OrderedDict ()
        
    def addItem (self, key, Value):
        self.tradeAction[key] = Value
        
    def toShortSaleArray (self):
        shortSell = []
        for key, value in self.tradeAction.items():
            shortSell.append (value.shortSale)
        return shortSell
    
    def toShortBuyArray (self):
        shortBuy = []
        for key, value in self.tradeAction.items():
            shortBuy.append (value.shortBuy)
        return shortBuy
    
    def toLongBuyArray (self):
        longBuy = []
        for key, value in self.tradeAction.items():
            longBuy.append (value.longBuy)
        return longBuy
    def toLongSellArray (self):
        longSell = []
        for key, value in self.tradeAction.items():
            longSell.append (value.longSale)
        return longSell
    
    def toProfitArray (self):
        desc = []
        for key, value in self.tradeAction.items():
            desc.append (value.profit)
        return desc
    
    def toRelativeProfitArray (self):
        desc = []
        for key, value in self.tradeAction.items():
            desc.append (value.relativeProfit)
        return desc
    
    def toBalanceArray (self):
        desc = []
        for key, value in self.tradeAction.items():
            desc.append (value.balance)
        return desc
    
    def toDescriptionArray (self):
        desc = []
        for key, value in self.tradeAction.items():
            desc.append (value.description)
        return desc
                        
            





        
        
                
        
        

        
