import pandas as pd
import numpy as np

class Read(object):

    def __init__(self,filesPath):
        self.trainPath=filesPath+"/train.csv"
        self.structurePath=filesPath+"/structure.txt"
        self.testPath=filesPath+"/test.csv"

    def readStructure(self):
        structure_file = open(self.structurePath, "r")
        raw = structure_file.read()
        structure_file.close()
        structure_lines = raw.split('\n')
        structure = dict()
        for line in structure_lines:
            line_parts=line.split(' ')
            if(line_parts[1]=='NUMERIC'):
                structure[line_parts[1]]=line_parts[2]
            else:
                values=line_parts[2].strip('{}').split(',')
                structure[line_parts[1]]=values
        return structure

    def readTrain(self):
        trainData = pd.read_csv(self.trainPath)
        return trainData

    def readTest(self):
        testData = pd.read_csv(self.testPath)
        return testData





