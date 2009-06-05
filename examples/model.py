from paropt.Measures import cpuTime, funcEval, exitCode, funcVal


def sum_of_cpu_time(testResult):
    totalCpuTime = 0
    for prob in testResult.measureValueTable.keys():
        totalCpuTime = totalCpuTime + cpuTime(prob)
    return totalCpuTime

def sum_of_func_eval(testResult):
    neval = 0
    for prob in testResult.measureValueTable.keys():
        neval = neval + funcEval(prob)
    return neval

def solving_percent(testResult):
    unsolved = len(testResult.problems) - len(testResult.measureValueTable)
    for prob in testResult.measureValueTable.keys():
        if exitCode(prob) != 0:
            unsolved = unsolved + 1
    return 1.0e0  - float(len(testResult.problems) - unsolved)/float(len(testResult.problems))

def mean_of_cpu_time(testResult):
    totalCpuTime = 0.0e0
    for prob in testResult.measureValueTable.keys():
        totalCpuTime = totalCpuTime + cpuTime(prob)
    return totalCpuTime/len(testResult.measureValueTable)

def quality_asset(testResult):
    worseSolution = 0.0
    for prob in testResult.measureValueTable.keys():
        if funcVal(prob) - finalValues[prob] > 0.001:
            worseSolution = worseSolution + 1.0
    return worseSolution/len(testResult.measureValueTable.keys())

def p2(testResult):
    paramValues = [param.value for param in testResult.parameters if param.name == 'STPTHR']
    return paramValues[0]

measureValues = {'hse':[0.32,1254],
                 'hsi':[0.47,1876],
                 'uncons':[3.90,7993]
                 }
finalValues = {'HS100':675.0106,
               'HS102':97.5831,
               'HS104':1.0418,
               'HS106':2114.6230,
               'HS108':-0.8660,
               'HS11':-18.0361,
               'HS116':47.3284,
               'HS118':98.2927,
               'HS13':0.2099,
               'HS15':0.9819,
               'HS17':0.9964,
               'HS19':-7973.0000,
               'HS20':0.3204,
               'HS22':1.0000,
               'HS24':-1.0000,
               'HS268':0.0000,
               'HS30':1.0000,
               'HS34':-0.8337,
               'HS36':-3372.6460,
               'HS44':-26.4350,
               'HS59':-50.9293,
               'HS64':5936.6300,
               'HS66':0.5182,
               'HS70':0.0507,
               'HS72':7.7106,
               'HS76':-4.6818,
               'HS84':-12103450.0000,
               'HS86':-48.8468,
               'HS88':0.0000,
               'HS91':0.0000,
               'HS93':0.0000,
               'HS95':0.0156,
               'HS97':3.1358,
               'HS107':0.0000,
               'HS111':-1067.0210,
               'HS119':46.0000,
               'HS26':0.0000,
               'HS28':0.0000,
               'HS39':-1.0000,
               'HS40':-0.2500,
               'HS42':11.6679,
               'HS46':0.0000,
               'HS48':0.0000,
               'HS50':1.4094,
               'HS52':2.9623,
               'HS54':-0.0024,
               'HS56':0.0000,
               'HS6':0.0000,
               'HS60':0.0326,
               'HS62':-29375.3000,
               'HS68':-0.9379,
               'HS77':0.2416,
               'HS79':0.0788,
               'HS8':-1.0000,
               'HS81':-63.4675,
               'HS87':0.0000,
               'HS99':-1008050000.0000,
               'BIGGS6':0.2228,
               'BROWNAL':0.0033,
               'BROWNDEN':85822.2000,
               'BRYBND':0.0000,
               'CLIFF':0.1998,
               'CRAGGLVY':1.8882,
               'DIXMAANK':1.0000,
               'DQRTIC':0.0000,
               'EIGENALS':0.0004,
               'FMINSURF':1.0000,
               'GROWTHLS':1.0191,
               'GULF':6.9081,
               'HAIRY':20.0000,
               'HART6':-3.1954,
               'HATFLDE':0.0867,
               'HEART6LS':1.4190,
               'MANCINO':0.0001,
               'MOREBV':0.0000,
               'PFIT1LS':0.0382,
               'POWER':0.0000,
               'ROSENBR':0.0025,
               'SISSER':0.0000,
               'SNAIL':0.0000,
               'VARDIM':15.5981,
               'WATSON':0.0907
               }


probNames ={'hsi': ['HS11','HS13','HS15','HS17','HS19',
                    'HS20','HS22','HS24',
                    'HS30','HS34','HS36',
                    'HS44',
                    'HS59',
                    'HS64','HS66',
                    'HS70','HS72','HS76',
                    'HS84','HS86','HS88',
                    'HS91','HS93','HS95','HS97',
                    'HS100','HS102','HS104','HS106','HS108',
                    'HS116','HS118','HS268'],
            'hse':['HS6','HS8',
                   'HS26','HS28',
                   'HS39',
                   'HS40','HS42','HS46','HS48',
                   'HS50','HS52','HS54','HS56',
                   'HS60','HS62','HS68',
                   'HS77','HS79',
                   'HS81','HS87',
                   'HS99',
                   'HS107',
                   'HS111','HS119'],
            'hsei': ['HS14',
                     'HS32',
                     'HS71','HS73','HS74','HS75',
                     'HS109',
                     'HS114'],
            'hsu': ['HS1','HS2','HS3','HS4','HS5',
                    'HS25',
                    'HS38',
                    'HS45',
                    'HS110'],
            'uncons':['BIGGS6','BROWNAL','BROWNDEN','BRYBND',
                     'CLIFF','CRAGGLVY',
                     'DIXMAANK','DQRTIC',
                     'EIGENALS',
                     'FMINSURF',
                     'GROWTHLS','GULF',
                     'HAIRY','HART6','HATFLDE','HEART6LS',
                     'MANCINO','MOREBV',
                     'PFIT1LS','POWER',
                     'ROSENBR',
                     'SISSER','SNAIL',
                     'VARDIM','WATSON']}
