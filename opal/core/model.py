import os
import sys
import os.path
import pickle
import log

from ..Platforms import LINUX

#from opal.core.modelstructure import ModelEvaluator

__docformat__ = 'restructuredtext'


class Model:
    def __init__(self, modelData=None, 
                 modelStructure=None,
                 evaluatingOptions=None,
                 dataFile='blackbox.dat',
                 **kwargs):
        """

        A `BlackBoxModel` encapsulates the 
        information of a parameter optimization problem.
        From the parameter problem point of view, this class has 
        two components: model data and model struture.

        Example::

            blackbox = Model(modelStructure, modelData)

        An object of this class must contain a link to a solver.
        The link to a solver is created by the solver and added to the
        BlackBoxModel object upon solving the problem.

        """

        self.data = modelData
        self.structure = modelStructure
        #self.runFileName = runFileName
        self.data_file = dataFile
        # The evaluating_options attribute accepts only
        # the options of simple type like boolean, integer
        # or string. In general, it accepts the options 
        # of picklable data type.
        self.evaluating_options = {}
        
        if evaluatingOptions is not None:
            self.evaluating_options.update(evaluatingOptions)
        self.evaluating_options.update(kwargs)

        self.initialize()
        return
    
    def initialize(self):
        # Transformation to information of an optimization model
        # The variables are the parameters
        self.variables = self.data.parameters
        # Refomulate the constraints
        self.inequality_constraints = []  # c_i(x) <= 0
        self.equality_constraints = []  # c_e(x) = 0
        for constraint in self.structure.constraints:
            if constraint.lower_bound == constraint.upper_bound:
                self.equality_constraints.append(constraint)
            else:
                if constraint.lower_bound is not None:
                    self.inequality_constraints.append(constraint)
                if constraint.upper_bound is not None:
                    self.inequality_constraints.append(constraint)
        
        self.bounds = [var.bound for var in self.variables]
        
        # Initial point is the default values of the parameters.
        self.initial_point = [var.value for var in self.variables]
        
        # The "simple constraints" that contain only the function of
        # parameters. This constraints will be verified before running 
        # the test.
        # In the futre, the bound constraints will be considered as
        # simple_constraints too
        self.simple_constraints = []
        pass

    # The methods to get information of a general model

    def get_n_variable(self):
        return len(self.variables)

    def get_n_constraints(self):
        return len(self.inequality_constraints) + len(self.equality_constraints)

    def get_iniitial_points(self):
        return self.initial_points

    def get_bound_constraints(self):
        return self.bounds

    # The methods to get information of a OPAL model

    def get_algorithm(self):
        return self.data.get_algorithm()

    def get_problems(self):
        return self.data.get_problems()

    def get_measures(self):
        return self.data.get_measures()

    def get_structure(self):
        return self.structure

    # The following methods are used for serialization 
    # The serialized content is two lines, one for data
    # and the other for structure

    def __getstate__(self):
        content = {}
        content['data'] = pickle.dumps(self.data)
        content['structure'] = pickle.dumps(self.structure)
        content['options'] = pickle.dumps(self.evaluating_options)
        return content

    def __setstate__(self, content):
        self.data = pickle.loads(content['data'])
        self.structure = pickle.loads(content['structure'])
        self.evaluating_options = pickle.loads(content['options'])
        self.initialize()
        return
    

