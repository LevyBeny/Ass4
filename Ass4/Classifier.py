import pandas as pd
import numpy as np
import matplotlib as pt
import operator

class Classifier(object):

    def __init__(self,outputPath):
        self.apriorProbDict=dict()
        self.condProbDict=dict()
        self.__outputPath=outputPath

    #Used to calculate the aprior probability for each attribute. based on uniform distribution assumption (no count made)
    def setApriorProbability(self,train,structure):
        self.__structure=structure
        self.apriorProbDict=dict()
        for attName in structure.keys():
            self.apriorProbDict[attName]=float(1.0)/float(len(structure[attName]))

    #Used to calculate for each attribute value and class value intersection the conditional probability using m-estimator
    def calcM_EstimatorProbability(self,train,structure,m):
        classValuesCountDict=dict()
        for classValue in structure["class"]:
            classValuesCountDict[classValue]=len(train[train["class"]==classValue])

        self.condProbDict=dict()
        for attName in structure.keys():
            if(attName != "class"):
                self.condProbDict[attName]=dict()
                for attValue in structure[attName]:
                        self.condProbDict[attName][attValue]=dict()
                        for classValue in structure["class"]:
                            countIntersection=len(train[(train[attName]==attValue) & (train["class"]==classValue)])
                            self.condProbDict[attName][attValue][classValue]=float(countIntersection+float(m*self.apriorProbDict[attName]))/float(classValuesCountDict[classValue]+m)
    
    def classifyTest(self,test):
        self.test=test
        self.classification_results=[]
        f = open(self.__outputPath+'/output.txt', "w")
        for index, row in test.iterrows():
            predictClass=self.__classifyPredict(row,self.__structure["class"])
            stringToWrite= str(index)+' '+str(predictClass)+'\n'
            f.write(stringToWrite)
            self.classification_results.append(predictClass)
        f.close()
        self.get_accuracy()

    def __classifyPredict(self, row,classValues):
        bayesCalc=dict()
        for classValue in classValues:
            bayesCalc[classValue]=1.0 #value before multiplying
        for column in self.__structure.keys():
            if (column!="class"):
                for classValue in classValues:              #attName #attValue    #classValue 
                    bayesCalc[classValue]*=float(self.condProbDict[column][row[column]][classValue])
        return max(bayesCalc.iteritems(), key=operator.itemgetter(1))[0] #get Max

    def get_accuracy(self):
        hits = int(0)
        test_class = self.test["class"]
        classifier_class = self.classification_results
        for i in range(0, self.classification_results.__len__() - 1):
            if test_class[i] == classifier_class[i]:
                hits = hits + 1
        accuracy = "%.3f" % ((float(hits) / float(self.classification_results.__len__())) * 100)
        print (accuracy)


        
                 

