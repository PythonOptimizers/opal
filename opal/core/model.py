import os
import sys
import os.path
import pickle
import log

from platform import Platform
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
        # Update the running options from data
        self.evaluating_options.update(modelData.running_options)
        # If there is an option with the same name, it is overwritten by
        # the setting in model
        if evaluatingOptions is not None:
            self.evaluating_options.update(evaluatingOptions)
        self.evaluating_options.update(kwargs)

        # Get the information about used platform. Normally, platform object
        # is not be picklable, So we try to get the information to save
        # along with the model data, and use it to reconstruct the platform
        # object in run-time.
        # By default, LINUX is used 
        self.platform_description = {'name':'LINUX',
                                     'settings':{}}
        if 'platform' in self.evaluating_options.keys():
            platform = self.evaluating_options['platform']
            if type(platform) == type('a platform name'):
                self.platform_description['name'] = platform
            elif isinstance(platform, Platform): # A Platform object
                self.platform_description['name'] = platform.name
                self.platform_description['settings'] = platform.settings
            else: # Unable to recognize the specified platfom
                pass # Do nothing and use the default platform
            del self.evaluating_options['platform'] # Remove platform setting
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
        
        # Initial points has at least one point that is the default values
        # of the parameters.
        self.initial_points = [[var.value for var in self.variables]]
        
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

    def get_initial_points(self):
        return self.initial_points

    def add_initial_point(self, point):
        converters = {'real':float,
                      'integer':int,
                      'categorical':str}
        initialPoint = []
        for param, val in map(None, self.variables, point):
            if param is None: # The point is longer
                pass # do nothing
            elif val is None: # Set to default value
                initialPoint.append(param.get_default())
            else: # Convert automatically to the corresponding type
                initialPoint.append(converters[param.kind](val))
        self.initial_points.append(initialPoint)
        
    def get_bound_constraints(self):
        return self.bounds

    # The methods to get information of a OPAL model

    def get_algorithm(self):
        return self.data.get_algorithm()

    def get_parameters(self):
        return self.data.get_parameters()
    
    def get_problems(self):
        return self.data.get_problems()

    def get_measures(self):
        return self.data.get_measures()

    def get_structure(self):
        return self.structure

    # The following methods are used for serialization 
    # The serialized content is two lines, one for data
    # and the other for structure

    ## def __getstate__(self):
    ##     content = {}
    ##     content['data'] = pickle.dumps(self.data)
    ##     content['structure'] = pickle.dumps(self.structure)
    ##     content['options'] = pickle.dumps(self.evaluating_options)
    ##     content['platform'] = pickle.dumps(self.platform_description)
    ##     return content

    ## def __setstate__(self, content):
    ##     self.data = pickle.loads(content['data'])
    ##     self.structure = pickle.loads(content['structure'])
    ##     self.evaluating_options = pickle.loads(content['options'])
    ##     self.platform_description = pickle.loads(content['platform'])
    ##     self.initialize()
    ##     return
    

