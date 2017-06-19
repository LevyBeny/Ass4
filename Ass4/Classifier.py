import pandas as pd
import numpy as np
import matplotlib as pt
import operator

class Classifier(object):

    def __init__(self,outputPath,train,structure,m):
        self.__apriorProbDict=dict()
        self.__condProbDict=dict()
        self.__classProb=dict()
        self.__structure=structure
        self.__outputPath=outputPath
        self.__setApriorProbability(train)
        self.__calcM_EstimatorProbability(train,m)

    #Used to calculate the aprior probability for each attribute. based on uniform distribution assumption (no count made)
    def __setApriorProbability(self,train):
        self.__apriorProbDict=dict()
        for attName in self.__structure.keys():
            self.__apriorProbDict[attName]=float(1.0)/float(len(self.__structure[attName]))

    #Used to calculate for each attribute value and class value intersection the conditional probability using m-estimator
    def __calcM_EstimatorProbability(self,train,m):
        classValuesCountDict=dict()
        size=len(train)
        for classValue in self.__structure["class"]:
            classValuesCountDict[classValue]=float(len(train[train["class"]==classValue]))
            self.__classProb[classValue]=classValuesCountDict[classValue]/float(size)
        self.__condProbDict=dict()
        for attName in self.__structure.keys():
            if(attName != "class"):
                self.__condProbDict[attName]=dict()
                for attValue in self.__structure[attName]:
                        self.__condProbDict[attName][attValue]=dict()
                        for classValue in self.__structure["class"]:
                            countIntersection=float(len(train[(train[attName]==attValue) & (train["class"]==classValue)]))
                            self.__condProbDict[attName][attValue][classValue]=float(countIntersection+m*self.__apriorProbDict[attName])/float(classValuesCountDict[classValue]+m)
    
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
        for classValue in classValues:
            for column in self.__structure.keys():          #attName #attValue    #classValue 
                if (column!="class"):
                    bayesCalc[classValue]*=float(self.__condProbDict[column][row[column]][classValue])
            bayesCalc[classValue]*=self.__classProb[classValue]
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


        
                 

