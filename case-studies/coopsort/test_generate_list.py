from coopsort import create_test_list
import sys

if len(sys.argv) > 1:
    listSpecs = eval(sys.argv[1])
else:
    listSpecs = [[8, 0.0125]]
if len(sys.argv) > 2:
    numberOfList = int(sys.argv[2])
else:
    numberOfList = 200
if len(sys.argv) > 3:
    listLengthUnit = int(sys.argv[3])
else:
    listLengthUnit = 20

generatedLists = {}
for listSpec in listSpecs:
    listType = listSpec[0]
    for k in range(numberOfList):
        n = listLengthUnit * (k + 1)
        #for n in [250, 500, 750, 1000, 1250, 1500, 1750, 2000]:
        listName = str(listSpec) + 'l' + str(n)
        generatedLists[listName] = create_test_list(listSpec, n, 0)
print generatedLists
