# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 12:50:23 2018

@author: vladis
"""

class MyStrategy (object):
      def __init__(self):
          self.result =0
          
      def initStrategy (self, df):
           print ('initStrategy')
           
      def startExecution (self, df):
          print ('initStrategy')
      
      def finishProcessing (self, df):
           print ('onTestFinished')