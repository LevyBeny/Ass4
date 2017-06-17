import pandas as pd
import numpy as np
import matplotlib as pt

class PreProcess(object):

    def __init__(self,structure):
        self.__structure=structure
    
    # fill the given train data with missing valuse 
    def fillNA(self,train):
        for column in self.__structure.keys():
            if (self.__structure[column]=='NUMERIC'):
                train[column].fillna(train[column].mean(), inplace=True)
            else:
                train[column].fillna((train[column]).mode().iloc[0], inplace=True)
        return train

    # discretize a given data to given number of bins
    def discretize(self,numOfBins,data):
        for column in self.__structure.keys():
            if (self.__structure[column]=='NUMERIC'):
                data[column]=self.__binning(data[column],column,numOfBins)
        return data

    def __binning(self,col,colName,numOfBins):
        # Define min and max values:
        minval = col.min()
        maxval = col.max()        
        interval_size=(maxval-minval)/numOfBins

        # Create list of break points
        break_points=[]
        i=minval
        for j in range(numOfBins+1):
            break_points.append(i)
            i+=interval_size

        # use default labels 0 ... (n-1)
        labels = range(numOfBins)

        # update structure
        self.__structure[colName]=labels

        # Binning using cut function of pandas
        colBin = pd.cut(col, bin=break_points, labels=labels, include_lowest=True)

        return colBin

    # returns the updated structure
    def getStructure(self):
        return self.__structure
           
