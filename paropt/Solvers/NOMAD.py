import sys
import os
from ..core.solver import Solver

class Parameter:
    def __init__(self,name=None,value=None,**kwargs):
        self.name = name
        self.value = value
        pass
    
    def str(self):
        if (self.name is not None) and (self.value is not None):
            return self.name + ' ' + str(self.value)
        return ""
    

class NOMADSolver(Solver):
    def __init__(self,**kwargs):
        Solver.__init__(self,name='NOMAD',command='nomad',parameter='nomad-param.txt',**kwargs)
        self.paramFileName = 'nomad-param.txt'
        self.resultFileName = 'nomad-result.txt'
        self.solutionFileName = 'nomad-solution.txt'
        self.parameter_settings = [] # List of line in parameter file
        pass

    def read_input(self,argv):
        inputValues = []
        if len(argv) < 1:
            return inputValues
        f = open(argv[1])
        map(lambda l: inputValues.extend(l.strip('\n').strip(' ').split(' ')), f.readlines()) # Extract every words from the file and save to a list
        f.close()
        return inputValues

    def write_output(self,objectiveValue,constraintValues):
        print >> sys.stdout, objectiveValue,
        if len(constraintValues) > 0:
            for i in range(len(constraintValues)):
                print >> sys.stdout,constraintValues[i],
            print ""
        return
    
    def initialize(self,blackbox):
        descriptionFile = open(self.paramFileName,"w")
        descriptionFile.write('DIMENSION ' + str(blackbox.n_var) + '\n')
        descriptionFile.write('DISPLAY_DEGREE 4\n')
        descriptionFile.write('DISPLAY_STATS EVAL& BBE & SOL&  &OBJ \\\\ \n')
        descriptionFile.write('BB_EXE "$python ' + blackbox.executableFileName + '"\n')
        #descriptionFile.write('BB_EXE ' + blackbox.executableFileName + '\n')
        bbTypeStr = 'BB_OUTPUT_TYPE OBJ'
        for i in range(blackbox.m_con):
            bbTypeStr = bbTypeStr + ' PB'
        descriptionFile.write(bbTypeStr + '\n')
        descriptionFile.write('SOLUTION_FILE ' + self.solutionFileName + '\n')
        pointStr = str(blackbox.initial_points)
        descriptionFile.write('X0 ' +  pointStr.replace(',',' ') + '\n')
        #print 'NOMAD.py',[bound[0] for bound in blackbox.bounds]
        lowerBoundStr = str([bound[0] for bound in blackbox.bounds]).replace('None','-').replace(',',' ')
        upperBoundStr = str([bound[1] for bound in blackbox.bounds]).replace('None','-').replace(',',' ')
        descriptionFile.write('LOWER_BOUND ' + lowerBoundStr + '\n')
        descriptionFile.write('UPPER_BOUND ' + upperBoundStr + '\n')
        descriptionFile.write('STATS_FILE ' + self.resultFileName + ' EVAL& BBE & BBO & SOL&  &OBJ \\\\ \n')
        for param_setting in self.parameter_settings:
            descriptionFile.write(param_setting + '\n')
        descriptionFile.close()
        return

    def set_parameter(self,name=None,value=None):
        #descriptionFile = open(self.paramFileName,'a')
        #descriptionFile.write(param.str() + '\n')
        #descriptionFile.close()
        param = Parameter(name=name,value=value)
        self.parameter_settings.append(param.str())
        return

NOMAD = NOMADSolver()
