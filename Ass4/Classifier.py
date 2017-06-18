import pandas as pd
import numpy as np
import matplotlib as pt
import operator

class Classifier(object):

    def __init__(self):
        self.apriorProbDict=dict()
        self.condProbDict=dict()

    #Used to calculate the aprior probability for each attribute. based on uniform distribution assumption (no count made)
    def setApriorProbability(self,train,structure):
        self.apriorProbDict=dict()
        for attName in structure.keys():
            self.apriorProbDict[attName]=1/sum(1 for x in structure[attName].values())

    #Used to calculate for each attribute value and class value intersection the conditional probability using m-estimator
    def calcM_EstimatorProbability(self,train,structure,m):
        classValuesCountDict=dict()
        for classValue in structure["class"]:
            classValuesCountDict[classValue]=len(train["class"]==classValue)

        self.condProbDict=dict()
        for attName in structure.keys():
            if(attName != "class"):
                self.condProbDict[attName]=dict()
            for attValue in structure[attName]:
                if(attName!= "class"):
                    self.condProbDict[attName][attValue]=dict()
                    for classValue in structure["class"]:
                        countIntersection=len((train[attName]==attValue) & (train["class"]==classValue))
                        self.condProbDict[attName][attValue][classValue]=(countIntersection+m*apriorProbDict[attValue])/(classValuesCountDict[classValue]+m)
    
    def classifyTestFile(self,test,classValues):
        for index, row in test.iterrows():
            predictClass=self.__classifyPredict(row,classValues)
            stringToWrite= index.str()+' '+predictClass
            #write the string to output.txt here


    def __classifyPredict(self, row,classValues):
        bayesCalc=dict()
        for classValue in classValues:
            bayesCalc[classValue]=1 #value before multiplying
        for column in row:
            for classValue in classValues:              #attName #attValue    #classValue 
                bayesCalc[classValue]*=self.condProbDict[column][row[column]][classValue]
        return max(bayesCalc.iteritems(), key=operator.itemgetter(1))[0] #get Max

        
                 

