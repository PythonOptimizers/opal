from coopsort_declaration import coopsort

from opal import ModelStructure, ModelData, Model, MeasureFunction, TestProblem
from opal.Solvers import NOMAD


def sum_time(parameters, measures):
    val = sum(measures['TIME'])
    return val


def get_neighbors(parameters):
    tmpStr = parameters[0]
    encodedNumber = tmpStr[0:tmpStr.find('.')]

    # Set of names for the leaf node
    s_s = ['0', '1', '2', '3']
    # Set of names for the internal node
    s_d = ['4', '5']
    # Neighborhood relation for a single node name
    n_s = {'0': ['2', '3'],
           '1': ['2', '3'],
           '2': ['0', '3'],
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
            #print c, n, encodedNumber, tmpStr, parameters
            # A neighbor is a parameter point
            neighbor = list(parameters)
            # Change value of the first coordinate of the parameter point
            neighbor[0] = int(float(tmpStr))
            # Add the neighbor to the neighbor list
            neighbors.append(neighbor)
        if c in s_s:  # Is is a leaf node
            for d in s_d:
                tmpStr = encodedNumber[0:i] + \
                         d + n_s[c][0] + n_s[c][1] + \
                         encodedNumber[i + 1:]
                neighbor = list(parameters)
                # Change value of the first coordinate of the parameter point
                neighbor[0] = int(float(tmpStr))
                # Add the neighbor to the neighbor list
                neighbors.append(neighbor)
        elif i < len(encodedNumber) - 2:
            s_1 = encodedNumber[i + 1]
            s_2 = encodedNumber[i + 2]
            if (s_1 in s_s) and (s_2 in s_s):
                tmpStr = encodedNumber[0:i] + s_1 + encodedNumber[i + 3:]
                neighbor = list(parameters)
                neighbor[0] = int(float(tmpStr))
                neighbors.append(neighbor)
                tmpStr = encodedNumber[0:i] + s_2 + encodedNumber[i + 3:]
                neighbor = list(parameters)
                neighbor[0] = int(float(tmpStr))
                neighbors.append(neighbor)
    return neighbors

problems = []
listTypes = [0, 5, 6, 7]
numberOfList = 16
listLengthStep = 25
for listType in listTypes:
    for k in range(numberOfList):
        n = listLengthStep * (k + 1)
        probName = str(listType) + '-' + str(n) + '-50'
        problems.append(TestProblem(name=probName))

#SMP.set_parameter(name='MAX_PROC', value=5);

# Define parameter optimization problem.
data = ModelData(algorithm=coopsort,
                 problems=problems)

struct = ModelStructure(objective=MeasureFunction(sum_time),
                        constraints=[],  # Unconstrained
                        neighborhood=get_neighbors)

prob = Model(modelData=data,
             modelStructure=struct
             )

# Solve parameter optimization problem.

if __name__ == '__main__':
    from opal.Solvers import NOMAD
    NOMAD.set_parameter(name='MAX_BB_EVAL', value=100)
    NOMAD.set_parameter(name='DISPLAY_DEGREE', value=4)
    NOMAD.set_parameter(name='EXTENDED_POLL_TRIGGER', value='r0.1')
    NOMAD.set_parameter(name='MAX_MESH_INDEX', value='2')
    NOMAD.set_parameter(name='MODEL_SEARCH_OPTIMISTIC', value='no')
    #print get_neighbors([401])
    NOMAD.solve(blackbox=prob)
