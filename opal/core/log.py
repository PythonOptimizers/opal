import re

class TestLogging:
    def __init__(self,**kwarg):
        self.testIdReg = re.compile("# Test number: [0-9]+")
        pass
        
    def write(self,empiricalModel,fileName='test.log'):
        f = open(fileName,'a')
        print >> f, '# Test number:', empiricalModel.test_number
        print >> f, '# Parameters:', [(param.name,param.value) for param in empiricalModel.parameters if not param.is_const()]
        print >> f, '# Non relaxable constraints are violated:', empiricalModel.test_is_failed
        if not empiricalModel.test_is_failed:
            print >> f, '# PROB',
            for m in sorted([measure.name for measure in empiricalModel.measures]):
                print >> f, m,
            print >> f, ''
            print >> f, empiricalModel.measure_value_table.__string__()
        f.close()
        return

    def read(self,fileName,id):
        f = open(fileName)
        content = f.read()
        f.close()

        positions = []
        iters = testIdReg.finditer(content)
        for it in iters:
            positions.append(it.span())

        idReg = re.compile('[0-9]+')
        tests = {}
        for i in range(len(positions)):
            testId = content[positions[i][0]:positions[i][1]]
            ids = idReg.findall(testId)
            if ids[0] == id:
                if i < len(positions) - 1:
                    tests[ids[0]] = (positions[i][0],positions[i+1][0])
                else:
                    tests[ids[0]] = (positions[i][0],None)
                break

        if tests[id][1] is None:
            return content[tests[id][0]:]
        else:
            return content[tests[id][0]:tests[id][1]]

class PythonLogging:
    def __init__(self,**kwarg):
        pass

    def write(self,empiricalModel,fileName='test.log'):
        f = open(fileName,'a')
        print >> f, '# Test number:'
        print >> f, empiricalModel.test_number
        print >> f, '# Parameters:'
        print >> f, [(param.name,param.value) for param in empiricalModel.parameters]
        #print >> f, '# Non relaxable constraints are violated:', empiricalModel.test_is_failed
        if not empiricalModel.test_is_failed:
            print >> f, '# Table format'
            print >> f, "{ 'PROB' : ", [measure.name for measure in empiricalModel.measures], '}'
            print >> f, '# Measure table'
            tableStr = '{'
            firstRow = True
            for prob in sorted(empiricalModel.measure_value_table.get_problems()):
                if firstRow :
                    tableStr = tableStr + "'" + prob + "' : "
                    firstRow = False
                else:
                    tableStr = tableStr + ',\n' + "'" + prob + "' : "
                tableStr = tableStr + str(empiricalModel.measure_value_table.get_row(prob))
            tableStr = tableStr + '}'
            print >> f, tableStr
        f.close()
        return
        
