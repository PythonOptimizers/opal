

#from optpack.log import *
#from mynumalg.visualization.profiles import *
from optpack.visualization.profiles import *
import sys
import string


#solverNames = ['default','TIME','EVAL','STPTHR']
#problemSet = 'cross-' + sys.argv[1]
problemSet = sys.argv[1]
opalProb = sys.argv[2]
col = string.atoi(sys.argv[3])
defaultFile = '../measure-tables/' + problemSet + '-default'
defaultLegend = 'Default'
optimalFile = '../measure-tables/' + problemSet + '-' + opalProb 
optimalLegend = problemSet + '-' + opalProb
measures =  ["prob",'time','descent','exitcode','eval','fval'] 

metricTable = MetricTable()
metricTable.add_solver(defaultFile,col,'Default')
metricTable.add_solver(optimalFile,col,'Optimal')

profiles = []


profiles.append(ComparativeProfile(metricTable=metricTable,
                                   firstSolver=0,secondSolver=1))

#profiles.append(PerformanceProfile(metricTable=metricTable,solver=1))
#profiles.append(PerformanceProfile(metricTable=metricTable,solver=0))

profilesGraph = ProfilesGraph( profiles,
                               backend='pdf',
                               logscale=10
                             )

profilesGraph.plot(colors=['b','r'],linestyles=['-','-'])
#profilesGraph.savefig(problemSet + "-" + opalProb + '-perprof-' +  measures[col - 1]  +  '.pdf')
profilesGraph.savefig(problemSet + "-" + opalProb + '-comprof-' +  measures[col - 1]  +  '.pdf')

