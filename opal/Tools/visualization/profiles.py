#!/usr/bin/env python
#
# pprof.py, v0.5: Create performance profiles.
# Written by Michael P. Friedlander <michael@mcs.anl.gov>
# Updated by Dominique Orban for use with matplotlib <Dominique.Orban@polymtl.ca>
#

# I'm still learning Python, so bear with me!
#
import getopt, sys, re
from numpy.ma import *
import numpy
from   string import atoi, atof
import matplotlib.ticker as ticker
   
class MetricTable:
    '''
    This table is physical storage of profile relating a measure (metric)
    Each column corresponds to one solver
    Each row corresponds to one test problem
    Physically, each column of the table is an numpy vector
    '''
    def __init__(self, solvers=None,problems=None,**kwargs):
        self.core  = None
        self.number_problem  = 0
        self.number_solver = 0
        # A dictionary mapping between the solver name and it's row index in the table
        self.solvers = None
        # A dictionary mapping between the problem name and it's column index in the table
        self.problems = None
        # The two dictionaries may be empty if we don't need this information
        self.row_minima = None # Each element is the minimum of the corresponding row
        self.column_maxima = None
    
    def add_solver(self, dataFile, column, solverName=None):
        # Reg exp: Any line starting (ignoring white-space)
        # with a comment character. Also col sep.
        comment = re.compile(r'^[\s]*[%#]')
        sep = re.compile('[\s]*')
        # Grab the column from the file
        metrics = []
        file = open(dataFile, 'r')
        for line in file.readlines():
            if len(line.strip('\n').strip()) == 0:
                # Ignore the empty line
                continue
            if  comment.match(line):
                continue
                # Ignore the comment line
            cols = sep.split( line.strip())
            data = atof(cols[column - 1])
            metrics.append(data)
        file.close()
	#print fname, self.core
        if self.core is None:
            self.core = array([metrics])
            self.column_minima = array(metrics)
            self.number_problem = len(metrics)
        else:
            nprobs = len(metrics)
            if self.number_problem <> nprobs:
                commandline_error("All files must have same number of problem")
                return
            self.core = concatenate((self.core, [metrics]))
            # Update the extrema 
            for i in range(len(metrics)):
                if metrics[i] < self.column_minima[i]:
                    self.column_minima[i] = metrics[i]
        # Update the information
        if solverName is not None:
            if self.solvers is None:
                self.solvers = {}
            self.solvers[solverName] = self.number_solver
        self.number_solver = self.number_solver + 1
        return

    def get_column(self,columnIndex):
        return self.core[:,columnIndex]
    
    def get_row(self,rowIndex):
        return self.core[rowIndex,:]

    def get_problem_metric(self, problem):
        #return masked_less_equal( self.core[:,prob], 0.0 )
        return self.get_column(prolem)

    def get_solver_metric(self,solver):
        return self.get_row(solver)
    
    def get_column_minima(self):
        return self.column_minima

    def get_solver_name(self,solverIndex):
        for name in self.solvers.keys():
            if self.solvers[name] == solverIndex:
                return name
        return None

class Profile:
    def __init__(self,metricTable=None,name=None,**kwargs):
        self.metric_table = metricTable
        self.name = name
        return
    
    def get_problem_number(self):
        return self.metric_table.number_problem

    def get_x(self):
        return None

    def get_name(self):
        return None
    
class PerformanceProfile(Profile):
   
    def __init__( self, metricTable=None, solver=0, **kwargs ):
        Profile.__init__(self,metricTable=metricTable,**kwargs)
        # Each solver has a performance profile that indicates it's perofrmance
        # relative to the other solvers in metricTable
        self.solver = solver
        # Set the x-axis ranges
        return

    def get_x(self):
        x = [1.0]
        # point (1,0) is added
        metrics = self.metric_table.get_solver_metric(self.solver)
        best_solver_metrics = self.metric_table.get_column_minima()
        x.extend(sorted(metrics/best_solver_metrics))
        return x

    def get_y(self):
        nProb = self.get_problem_number()
        y = (numpy.arange(nProb + 1)) * (1.0 /nProb)
        # first point of any performance profile is (1,0)
        return y

    def get_name(self):
        if self.name is not None:
            return self.name
        return self.metric_table.get_solver_name(self.solver)
    

class DataProfile(Profile):
    
    def __init__( self, solvers=None, metricTable=None,**kwargs ): 
        self.metric_table = metricTable
        return

    def get_x(self,solverIndex):
        return self.metrics.solv_metrics(solverIndex)
    
    def get_name(self,solverIndex):
        return self.solverNames[solverIndex]
   

class ComparativeProfile(Profile):
    def __init__(self, metricTable=None,firstSolver=0, secondSolver=1,**kwargs):
        Profile.__init__(self,metricTable=metricTable,**kwargs)
        self.firstSolver = firstSolver
        self.secondSolver = secondSolver
        return

    def get_x(self):
        firstMetrics = self.metric_table.get_solver_metric(self.firstSolver)
        secondMetrics = self.metric_table.get_solver_metric(self.secondSolver)
        x = []
        for i in range(len(firstMetrics)):
            if (firstMetrics[i] + secondMetrics[i]) == 0:
                x.append(0.0)
            else:
                x.append((firstMetrics[i] - secondMetrics[i]) / (abs(firstMetrics[i]) + abs(secondMetrics[i])))
        return x
    
    def get_y(self):
        nProb = self.get_problem_number()
        y = (numpy.arange(nProb) + 1.0) * (1.0 /nProb)
        return y

    def get_name(self):
        if self.name is not None:
            return self.name
        return self.metric_table.get_solver_name(self.firstSolver) + '-' + self.metric_table.get_solver_name(self.secondSolver)

class ProfilesTickerFormatter(ticker.LogFormatterMathtext):
    def __init__(self,base=10.0,labelOnlyBase=True,
                 negativeScale=0,positiveScale=0,realZero=False,**kwargs):
        ticker.LogFormatterMathtext.__init__(self,base,labelOnlyBase)
        self._negative_scale = negativeScale + 0.0
        self._positive_scale = positiveScale + 0.0
        self._real_zero = realZero

    def __call__(self,x,pos=None):
        if x == 0:
            if self._real_zero:
                scaledValue = 0
            else:
                scaledValue = 1
        elif x > 0:
            scaledValue = pow(self._base, x - self._positive_scale)
        else:
            scaledValue = pow(self._base, -x - self._negative_scale)*(-1.0)
        return ticker.LogFormatterMathtext.__call__(self,scaledValue,pos)


class ProfilesGraph:
       
    def __init__( self,profiles=None,logscale=2,backend='pdf',xsymetric=True,title=None, **kwargs ):
        # Obtain options class with all default values
        self.profiles = None
        # print self.profile.metrics.table
        self.xMax = -1.000e+20
        self.xMin = 1.000e+20
        self.logscale = logscale
        self.backend = backend
        self.legendText = []
        self.x_symetric = xsymetric
        self.title_text = title
        if profiles is not None:
            #print profiles
            for profile in profiles:
                #print profile
                self.add_profile(profile)
       
        import matplotlib.pyplot as MM        

        self.params = {'axes.labelsize': 12,
                       'text.fontsize': 10,
                       'legend.fontsize': 14,
                       'xtick.labelsize': 14,
                       'xtick.major.size': 14,
                       'xtick.minor.size': 4,
                       'ytick.labelsize': 14,
                       'ytick.major.size': 6,
                       'ytick.minor.size': 4
                       #'text.usetex': True
                       }

        MM.rcParams.update(self.params)
        self.linestyles = [ '-', '.-', '+:','--',':', 'x:', '^:', 'v:', '<',
                            '>', 's', '+', 'x', 'D', 'd', '1', '2', '3', '4',
                            'h', 'H', 'p', '|', '_' ]
        
        self.colors = [ 'g', 'r', 'c', 'm', 'k', 'y', 'w' ]
        
        self.ax = MM.axes()
        self.mmplotcmd = self.ax.plot     
        self.show = MM.show
        self.savefig = MM.savefig
        self.title = MM.title
        return
       
    def add_profile(self,profile):
        if self.profiles is None:
            self.profiles = []
        #print profile.get_x()
        xMin = min(profile.get_x())
        xMax = max(profile.get_x())
        if xMin < self.xMin:
            self.xMin = xMin
        if xMax > self.xMax:
            self.xMax = xMax
        self.profiles.append(profile)
        
        return

    def log_scale(self,logBase,x):
        epsilon = pow(logBase + 0.00,-10.0)

        negative_scale = 0
        positive_scale = 0

        negative_x = [-log(-xe)/log(logBase) for xe in x if xe < 0]
        if len(negative_x) > 0 :
            negative_scale = floor(max(negative_x)) + 1 
            negative_x = [xe - negative_scale - epsilon for xe in negative_x]
        
        positive_x = [log(xe)/log(logBase) for xe in x if xe > 0]
        if len(positive_x) > 0 :
            positive_scale = floor(min(positive_x))
            positive_x = [xe - positive_scale + epsilon for xe in positive_x]

        zero_x = [0 for xe in x if xe == 0]

        scaled_x = negative_x  + zero_x + positive_x
        return scaled_x, -positive_scale, negative_scale 
    
    def const_scale(self,x,positiveOffset=0,negativeOffset=0): 
        negative_x = [xe - negativeOffset for xe in x if xe < 0]
        positive_x = [xe + positiveOffset for xe in x if xe > 0]
        zero_x = [0 for xe in x if xe == 0]
        return negative_x + zero_x + positive_x
        
    def plot(self,colors=None,linestyles=None,linewidth=None,**kwagrs):
   
        if colors is not None:
            self.colors = colors
        if linestyles is not None:
            self.linestyles = linestyles
        if linewidth is None:
            lineWidth = 1
        else:
            lineWidth = linewidth

        nColor = len(self.colors)
        nStyle = len(self.linestyles)
        
        legendText = []
        positive_scale = 0
        negative_scale = 0
        curves = {}
        for profile in self.profiles :
            xdata,pScale,nScale = self.log_scale(self.logscale,sorted(profile.get_x()))
            ydata = profile.get_y()
            ##print profile.get_name()
            curves[profile.get_name()] = (xdata,ydata,pScale,nScale)
            if pScale > positive_scale:
                positive_scale = pScale
            if nScale > negative_scale:
                negative_scale = nScale
            #print pScale, nScale
        
        scale = max([pScale,nScale])
        
        lscount = 0
        colcount = 0
        curveNames =  sorted(curves.keys())
        curveNames.reverse()
        #print curveNames
        for curveName in curveNames:
            if self.x_symetric :
                xdata = self.const_scale(curves[curveName][0],
                                         positiveOffset=scale - curves[curveName][2],
                                         negativeOffset=scale - curves[curveName][3])
            else:
                xdata = self.const_scale(curves[curveName][0],
                                         positiveOffset=positive_scale - curves[curveName][2],
                                         negativeOffset=negative_scale - curves[curveName][3])
            ydata = curves[curveName][1]
            #print xdata, ydata
            self.mmplotcmd( xdata,
                            ydata,
                            color=self.colors[(colcount % nColor )],
                            linestyle = self.linestyles[(lscount % nStyle)],
                            #color='black',
                            linewidth=lineWidth, drawstyle='steps-post') 
            lscount += 1
            colcount +=1 
            legendText.append(curveName)
 
        if negative_scale != 0:
            self.ax.xaxis.set_major_formatter(ProfilesTickerFormatter(base=self.logscale,
                                                                      labelOnlyBase=True,
                                                                      positiveScale=positive_scale,
                                                                      negativeScale=negative_scale,
                                                                      realZero=True))
        else:
            self.ax.xaxis.set_major_formatter(ProfilesTickerFormatter(base=self.logscale,
                                                                      labelOnlyBase=True,
                                                                      positiveScale=positive_scale,
                                                                      negativeScale=negative_scale,
                                                                      realZero=False))
        self.ax.legend( legendText, 'lower right' )
        if self.title_text is not None:
            self.title(self.title_text)
        self.ax.grid(True)
       
        
