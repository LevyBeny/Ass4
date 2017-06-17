import pandas as pd
import numpy as np
import matplotlib as pt

class PreProcess(object):
    def __init__(self,structure,train):
        self.structure=structure
        self.train=train

    def fillNA(self):
        print("Befor#################################################################################")
        print(self.train)
        for column in self.structure.keys():
            if (self.structure[column]=='NUMERIC'):
                self.train[column].fillna(self.train[column].mean(), inplace=True)
            else:
                self.train[column].fillna((self.train[column]).mode().iloc[0], inplace=True)
        print("after #################################################################################")
        print(self.train)

    def discretize(self,numOfBins):
        for column in self.structure.keys():
            if (self.structure[column]=='NUMERIC'):
                self.train[column]=binning(self.train[column],numOfBins)

    def binning(col,numOfBins):
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

        # Binning using cut function of pandas
        colBin = pd.cut(col, bin=break_points, labels=labels, include_lowest=True)

        return colBin
           
