import os
import shutil
import re
from ..core.testproblem import *

class CUTErTestProblem(OptimizationTestProblem):

    def __init__(self, name=None, description=None, classifyStr=None,nvar=0, ncon=0,
                 paramString=None, **kwargs):
        OptimizationTestProblem.__init__(self, name, description, classifyStr, nvar, ncon,
                                         **kwargs)
        self.paramString = None

class CUTErQuery:

    def __init__(self,qName=None,
                 name='',
                 nMin=0,nMax=1000000,
                 mMin=0,mMax=1000000,
                 objectiveType='NCLQSO',
                 constraintType='UXBNLQO',
                 smoothType='IR',
                 infoOrder=0,
                 problemType="AMR",
                 internalVar='YN',
                 **kwargs):
        """
        An example of a query
        query = Query(name='HS',nMin=0,nMax=10,objectiveType="N",constraintType="U")
        """
        self.name = name
        self.nMin = nMin
        self.nMax = nMax
        self.mMin = mMin
        self.mMax = mMax
        self.objectiveType = objectiveType
        self.constraintType = constraintType
        self.smoothType = smoothType
        self.infoOrder = infoOrder
        self.problemType = problemType
        self.internalVar = internalVar

    def match(self,problem_name,probDescStr):
        #print self.nMax, self.mMax,  probDescStr,
        descFields = probDescStr.split("-")
        for i in range(len(descFields)):
            descFields[i] = descFields[i].strip()
        #descFields[0:] = descFields[0:].strip()
        if re.compile(self.name).match(problem_name) is None:
            return False
        if self.objectiveType.count(descFields[0][0]) <= 0:
            #print self.objectiveType, 'is not sastified'
            return False
        if self.constraintType.count(descFields[0][1]) <= 0:
            #print self.constraintType, 'is not sastified'
            return False
        if self.smoothType.count(descFields[0][2]) <= 0:
            #print self.smoothType, 'is not sastified'
            return False
        if self.infoOrder > int(descFields[0][3:]):
            #print 'info order is not sastified'
            return False
        if self.problemType.count(descFields[1][0]) <= 0:
            #print self.problemType, 'is not satisfied'
            return False
        if self.internalVar.count(descFields[1][1]) <= 0:
            return False
        if descFields[2].count("V") <= 0:
            if self.nMin > int(descFields[2]):
                #print descFields[2],  'variables is not satisifed'
                return False
            if self.nMax < int(descFields[2]):
                #print descFields[2], 'variables is not satisifed'
                return False
        if descFields[3].count("V") <= 0:
            if self.mMin > int(descFields[3]):
                #print descFields[3], 'constraints is not satisifed'
                return False
            if self.mMax < int(descFields[3]):
                #print descFields[3], 'constraints is not satisifed'
                return False
        #print 'Query is matched'
        return True

#==========
    
class CUTErFactory:
    def __init__(self,classifyFile=None,**kwargs):
        self.classifyFile = classifyFile
        self.decoder = 'sifdecode'
        self.dbDir = os.environ['MASTSIF']
        pass

    def extract(self,**kwargs):
        queryResult = []
        queryPharse = Query(**kwargs)
        if self.classifyFile == None:
            return queryResult
        f = open(self.classifyFile,'r')
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.strip()
            if len(line) <= 2:
                continue
            #print line
            fields = line.split(' ',1)
            if queryPharse.match(fields[0].strip(),fields[1].strip()):
                #print fields[0], 'is added'
                queryResult.append(fields[0].strip())
        return queryResult

    def generate_collection(self):
        f = open(self.classifyFile,'r')
        lines = f.readlines()
        f.close()
        CUTEr =  ProblemCollection(name='CUTEr collection')
        for line in lines:
            line = line.strip()
            if len(line) <= 2:
                # Emtry line with new line symbol
                continue
            #print line
            fields = line.split(' ',1)
            prob = self.generate_problem(fields[0].strip(),fields[1].strip())
            if prob is not None:
                CUTEr.all.add_problem(prob)
        return CUTEr
    
    def generate_problem(self,problem_name,classify_string=None,param=None):      
        decode_cmd = self.decoder
        if param is None:
            decode_cmd = decode_cmd + ' ' + problem_name
        else:
            decode_cmd = decode_cmd + ' -param ' + param + ' ' + problem_name 
        f = os.popen(decode_cmd)
        decode_log = f.read()
        f.close()
        variable_query = re.compile('[0-9]+[ a-z]+variable[s]?')
        constraint_query = re.compile('[0-9]+[ a-z]+constraint[s]?')
        number_query = re.compile('\d+')
        nvar = 0
        variable_declarations = variable_query.findall(decode_log)
        #print problem_name,
        for var_decl in variable_declarations:
            #print var_decl,
            nvar = nvar + int(number_query.findall(var_decl)[0])
        #print ''
        constraint_declarations = constraint_query.findall(decode_log)
        ncon = 0
        for cons_decl in constraint_declarations:
            ncon = ncon + int(number_query.findall(cons_decl)[0])
        if (nvar + ncon <= 0):
            return None
            # There is no problem nvar + ncon = 0
        problem = CUTErTestProblem(name=problem_name,classifyStr=classify_string,nvar=nvar,ncon=ncon)
        return problem          
