import pandas as pd
import numpy as np
import matplotlib as pt

class PreProcess(object):

    def __init__(self,structure):
        self.__structure=structure
        self.__breakPoints=dict()
        self.__numOfBins=0
    
    # fill the given train data with missing valuse 
    def fillNA(self,train):
        for column in self.__structure.keys():
            if (self.__structure[column]=='NUMERIC'):
                train[column].fillna(train[column].mean(), inplace=True)
            else:
                train[column].fillna((train[column]).mode().iloc[0], inplace=True)
        return train

    # discretize the given train set to given number of bins
    def discretizeTrain(self,numOfBins,train):
        self.__numOfBins=numOfBins
        for column in self.__structure.keys():
            if (self.__structure[column]=='NUMERIC'):
                self.__breakPoints[column]=self.__createBreakPoints(train[column],numOfBins)
                self.__structure[colName]=range(numOfBins)# update structure
                train[column]=self.__binning(train[column],self.__breakPoints[column],numOfBins)
        return train

    # discretize the given test set to given number of bins
    def discretizeTest(self,test):
        for column in self.__breakPoints.keys():
            test[column]=self.__binning(test[column],self.__breakPoints[column],self.__numOfBins)
        return test

    def __createBreakPoints(self,col,numOfBins):
        # Define min and max values:
        minval = col.min()
        maxval = col.max()        
        interval_size=float(maxval-minval)/float(numOfBins)

        # Create list of break points
        break_points=[]
        i=minval
        for j in range(numOfBins+1):
            break_points.append(i)
            i+=interval_size
        return break_points

    def __binning(self,col,break_points,numOfBins):

        # use default labels 0 ... (n-1)
        labels = range(numOfBins)

        # Binning using cut function of pandas
        colBin = pd.cut(col, bin=break_points, labels=labels, include_lowest=True)

        return colBin

    # returns the updated structure
    def getStructure(self):
        return self.__structure


           
