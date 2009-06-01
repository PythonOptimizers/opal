import utility
import os


class Driver:
    def __init__(self,algorithm,source,routine='',**kwargs):
        self.algorithm = algorithm
        self.source = source
        self.routine = routine
        self.libs = []

    def add_lib(self,libDescription):
        self.libs.append(libDescription)
        return

    def set_input(self,input):
        return

    def set_parameter(self,parameters):
        return
    
    def get_measure(self,desirableMeasures):
        return

    def get_output(self):
        return

    def clear_output(self):
        return

