import os
import sys
import os.path
import pickle

from .. import config
from .modelstructure import ModelEvaluator

class BlackBox:
    """
    This class represent to all communication with direct solver
    This is an abstract class. The specific implementation depends 
    on the used solver. For example, when the solver is NOMAD, an 
    object of this class represents for 
    an executable file whose I/O methods depend from the specific solver.
    """
    def __init__(self,solver=None,model=None,**kwargs):
        self.solver = solver
        self.model = model
        pass

    
    def run(self,*args,**kwargs):
        inputValues = []
        paramValues = []
        #print args
        (inputValues,paramValues) = self.read_input(*args,**kwargs)
        if self.model is None:
            return
        #print inputValues
        (objective,constraints) = self.model.evaluate(inputValues)
        self.write_output(objective,constraints)
        return

    def read_input(self,*args,**kwargs):
        return (None,None)

    def write_output(self,objectiveValue, constraintValues):
        return

    def set_parameter(self,*args,**kwargs):
        return

class BlackBoxModel:
    def __init__(self, modelData=None, modelStructure=None,
                 runFileName='blackbox.py',dataFile='blackbox.dat',logFileName='test.log',**kwargs):
        """
        This class represent a black box that encapsulates the 
        information of a parameter optimization problem.
        From the parameter problem point of view, this class contains
        two descriptions: model data and model struture
        An object of this class have to contain the link to 
        used solver.
        To create an BlackBox object, users have to specify two mains 
        component
        blackbox = BlackBox(modelStructure,modelData)
        The link to solver is created by the solver and add to BlackBox
        object when the solving is activated.
        """

        self.model_data = modelData
        self.model_structure = modelStructure
        #self.runFileName = runFileName
        self.data_file = dataFile
        self.logFileName = logFileName
        activeParameters = self.model_data.get_active_parameters()
        
        self.n_var = len(activeParameters)
        self.m_con = len(self.model_structure.constraints)
        self.initial_points = [param.value for param in activeParameters]
       
        self.bounds = [param.bound for param in activeParameters]
        # The "simple constraints" that contain only the function of
        # parameters. This constraints will be verified before running 
        # the test.
        # In the futre, the bound constraints will be considered as
        # simple_constraints too
        self.simple_constraints = []

        
        #self.solver = None 
        #self.surrogate = None
        # if no solver is specified, the blackbox is a general 
        # executable file with two arguments: input file and parameter file
        # The output is standard screen
        self.save()
        pass

    def set_options(self,**kwargs):
        return
    
    #def has_surrogate(self):
    #    return self.surrogate is not None

    #def get_surrogate(self):
    #    return self.surrogate

 
    def evaluate(self,inputValues):
        '''
        Evaluate the model at given point
        Input: evaluated point coordinate
        Output: Value of objective function and constrains values list
        In the case of error, two None values are returned
        '''
       
       
        self.model_data.run(inputValues)
        testResult = self.model_data.get_test_result()
        #print 'ho ho after getTestResult', self.modelData.measures[0],\
        #      self.modelData.measures[0].valuetable
        # An evaluator object may be redudant, remove it in the future
        modelEvaluator = ModelEvaluator(self.model_structure,self.model_data.measures)
        (funcObj,constraints) = modelEvaluator.evaluate(testResult)
        #print funcObj
        #print constraints
        self.log()
        return (funcObj,constraints)
    
    def save(self):
        try:
            blackboxDataFile = open(self.data_file,"w")
            pickle.dump(self,blackboxDataFile)
            blackboxDataFile.close()
        except TypeError:
            print "Error in saving"
        return
    
    def log(self):
        if self.model_data.log != None:
            self.model_data.log(self.logFileName)
        if self.model_structure.log != None:
            self.model_structure.log(self.logFileName)
        return
    
    def get_iniitial_points(self):
        return self.initial_points

    def get_bound_constraints(self):
        return self.bounds

    def generate_surrogate(self):
        reducedModelData = self.model_data.reduce_problem_set()
        surrogate = BlackBoxModel(modelData=reducedModelData, modelStructure=self.model_structure,
                             dataFileName=self.dataFileName.strip('.dat') + '_surrogate.dat',
                             logFileName=self.logFileName.strip('.log') + '_surrogate.log')
        return surrogate
