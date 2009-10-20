import os

class Solver:
    def __init__(self,name='',command=None,input=None,parameter='',output=None,**kwargs):
        self.name = name
        self.command = command
        self.args = [input,parameter,output]
        return
    def run(self):
        cmdStr = self.command
        for argv in self.args:
            if argv != None:
                cmdStr = cmdStr + ' ' + str(argv)
        os.system(cmdStr)
        return
