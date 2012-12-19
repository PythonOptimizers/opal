from coopsort_declaration import coopsort

from opal import ModelStructure, ModelData, Model, MeasureFunction, TestProblem
from opal.Solvers import NOMAD


def sum_time(parameters, measures):
    val = sum(measures['TIME'])
    return val


def get_neighbors(parameters):
    def encode(number, base=6):
        numberStr = ''
        if number == 0:
            return '0'
        while number > 0:
            (number, r) = divmod(number, base)
            numberStr = str(r) + numberStr
        return numberStr

    def decode(numberStr, base=6):
        invertedStr = numberStr[::-1]
        number = 0
        quotient = 1
        for c in invertedStr:
            number = number + int(c) * quotient
            quotient = quotient * base
        return number

    import logging
    logger = logging.getLogger(__name__)
    fh = logging.FileHandler('neighborhood.log')
    logger.setLevel(logging.INFO)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    encodedNumber = encode(int(float(parameters[0])), 6)
    logMessage = parameters[0] + ', ' + \
                 str(int(float(parameters[0]))) + ', ' + \
                 encodedNumber + ': '
    # Set of names for the leaf node
    s_s = ['0', '1', '2', '3']
    # Set of names for the internal node
    s_d = ['4', '5']
    # Neighborhood relation for a single node name
    n_s = {'0': ['2', '3'],
           '1': ['2', '3'],
           '2': ['1', '3'],
           '3': ['1', '2'],
           '4': ['5'],
           '5': ['4']
           }
    # Initialize an empty list of neighbors
    neighbors = []
    for i in range(len(encodedNumber)):
        c = encodedNumber[i]
        for n in n_s[c]:
            tmpStr = encodedNumber[0:i] + n + encodedNumber[i + 1:]

            # A neighbor is a parameter point
            neighbor = list(parameters)

            # Change value of the first coordinate of the parameter point
            neighbor[0] = decode(tmpStr)
            logMessage = logMessage + tmpStr + ' -> ' + \
                         str(neighbor[0]) + ', '

            # Add the neighbor to the neighbor list
            neighbors.append(neighbor)

        if c in s_s:  # It is a leaf node
            for d in s_d:
                tmpStr = encodedNumber[0:i] + \
                         d + n_s[c][0] + n_s[c][1] + \
                         encodedNumber[i + 1:]
                neighbor = list(parameters)

                # Change value of the first coordinate of the parameter point
                neighbor[0] = decode(tmpStr)
                logMessage = logMessage + tmpStr + ' -> ' + \
                             str(neighbor[0]) + ', '

                # Add the neighbor to the neighbor list
                neighbors.append(neighbor)

        elif i < len(encodedNumber) - 2:
            s_1 = encodedNumber[i + 1]
            s_2 = encodedNumber[i + 2]
            if (s_1 in s_s) and (s_2 in s_s):
                tmpStr = encodedNumber[0:i] + s_1 + encodedNumber[i + 3:]
                neighbor = list(parameters)
                neighbor[0] = decode(tmpStr)
                logMessage = logMessage + tmpStr + ' -> ' + \
                             str(neighbor[0]) + ', '
                neighbors.append(neighbor)
                tmpStr = encodedNumber[0:i] + s_2 + encodedNumber[i + 3:]
                neighbor = list(parameters)
                neighbor[0] = decode(tmpStr)
                logMessage = logMessage + tmpStr + ' -> ' + \
                             str(neighbor[0]) + ', '
                neighbors.append(neighbor)
    logger.info(logMessage + '\n')
    return neighbors

problems = []
listSpecIndices = [1]
numberOfList = 1
listLengthStep = 4000
numberOfRepetition = 100
for listSpecIndex in listSpecIndices:
    for k in range(numberOfList):
        n = listLengthStep * (k + 1)
        probName = str(listSpecIndex) + \
                   '-' + str(n) + '-' + str(numberOfRepetition)
        problems.append(TestProblem(name=probName))

surrogate_problems = []
for listSpecIndex in listSpecIndices:
    for k in range(numberOfList):
        n = listLengthStep * (k + 1)
        probName = str(listSpecIndex) + \
                   '-' + str(n) + '-10'
        surrogate_problems.append(TestProblem(name=probName))

#SMP.set_parameter(name='MAX_PROC', value=5);

# Define parameter optimization problem.
data = ModelData(algorithm=coopsort, problems=problems)

surrogate_data = ModelData(algorithm=coopsort, problems=surrogate_problems)

struct = ModelStructure(objective=MeasureFunction(sum_time),
                        constraints=[],  # Unconstrained
                        neighborhood=get_neighbors)

prob = Model(modelData=data, modelStructure=struct)
surrogate_prob = Model(modelData=surrogate_data, modelStructure=struct)

# Solve parameter optimization problem.

if __name__ == '__main__':
    from opal.Solvers import NOMAD
    NOMAD.set_parameter(name='MAX_BB_EVAL', value=100)
    NOMAD.set_parameter(name='DISPLAY_DEGREE', value=1)
    NOMAD.set_parameter(name="DISPLAY_STATS",
                        value="%3dEVAL %3dBBE %4dSGTE [ %15lSOL, ] %8.2eBBO %4.2fTIME")
    NOMAD.set_parameter(name="STATS_FILE",
                        value="iterations.txt %3dEVAL %3dBBE %4dSGTE [ %15lSOL, ] %8.2eBBO %4.2fTIME")
    #NOMAD.set_parameter(name='EXTENDED_POLL_TRIGGER', value='r0.1')
    NOMAD.set_parameter(name='MAX_MESH_INDEX', value='2')
    NOMAD.solve(blackbox=prob, surrogate=surrogate_prob)
