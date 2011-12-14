from opal.TestProblemCollections import CUTEr
from opal.TestProblemCollections.cuterfactory import CUTErQuery

'''
Some notes on special problems:
- JUNKTURN is solved (ecode = 0) with surrogate whose tolerance is less strict.
  For the original blackbox, JUNKTURN return always exit code = 2. However
  the number of function evaluation and computing time of surrogate is
  so much higher. This means that the behavior on the surrogate is inverse
  from what we desire.
- DENCONVNE solved with surrogate but with blackbox, it returns ECODE=1
  or -1 and
  number of function evaluation is 1000 times much than surrogate
- CRESC132 sometimes returns code 2, sometimes return code -1. The behavior on
  blackbox and surrogate is similar
- A5NSSSSL: For p0, ECODE = 0, for almost other parameter values, ECODE=-1
  (30/32 parameter values) with computing time and FEVAL are so huge
  (10-30 miniutes in comparing to 17 seconds and, 36521 in comparing to 71).
  Two parameter values whose ECODE = 0 correspond to two special parameter sets.
  Initial parameter sets, and a better parameter set. This means, A5NSSSSL
  has huge impact on the similarity between original model (730 test problems)
  and reduced model (40 test problems). Actually, it has impact on the
  clustering, ATNSSSSL is not counted in reduced model. This make reduced model
  can be improved easily but it not the same behavior on original model.
  
'''
query = CUTErQuery(constraintType='BNLQO')
# Select tiny unconstrained HS problems.
CUTEr_constrained_problems = [prb for prb in CUTEr if query.match(prb)]

# Two few degree of freedom
too_few_freedom_problems = ['ARGAUSS', 'ARGLALE', 'ARGLBLE', 'ARGLCLE',
                            'ARWHDNE', 'CHNRSBNE','GROUPING','GROWTH',
                            'LEWISPOL','NYSTROM5','QR3DBD','SPMSQRT',
                            'SYNPOP24','YFITNE']

# Fixed variable, exit code = -3
fixed_variables_problems = ['RAYBENDS', 'RAYBENDL']

# Has difficulty with linear solver and CUTEr, CATENA can be solved by MUMPS
technical_difficulty_problems = ['CATENA', 'COSHFUN']


# Exit code =-1, Number of iteration exeeds 3000
hard_problems = ['A2NNDNSL', 'BLOCKQP1', 'BLOCKQP3', 'BLOCKQP5', 'BRAINPC0',
                 'BRAINPC2', 'BRAINPC4', 'BRAINPC6', 'BRITGAS', 'CATENARY',
                 'CRESC100', 'CRESC50', 'FLOSP2HH', 'GLIDER', 'HATFLDF',
                 'HS87', 'HVYCRASH', 'KTMODEL', 'LIPPERT2', 'LUKVLE11',
                 'LUKVLE15', 'LUKVLI1', 'MANNE', 'MSS3', 'NUFFIELD', 'ORTHREGE',
                 'PALMER5A', 'PALMER5E', 'PALMER7A', 'PALMER7E', 'POLAK3',
                 'SARO', 'SAROMM']

# Exit code = -2. Restoration failed
restoration_failed_problems = ['BRAINPC1', 'BRAINPC3', 'BRAINPC5', 'BRAINPC7',
                               'BRAINPC8', 'BRAINPC9', 'C-RELOAD', 'EQC',
                               'HIMMELBJ', 'LUKVLE17', 'LUKVLE2', 'LUKVLE4',
                               'LUKVLI2', 'LUKVLI4', 'NET2', 'NET3',
                               'ORTHRDS2', 'PFIT2', 'QCNEW', 'S365', 'S365MOD',
                               'SSEBNLN', 'VANDERM4']
# Runtime > 100 sec
long_problems = ['NCVXQP1', 'NCVXQP2', 'NCVXQP3', 'NCVXQP4', 'NCVXQP5',
                 'NCVXQP6', 'NCVXQP7', 'NCVXQP8', 'NCVXQP9', 'ODNAMUR']

# Runtime approx 10h
extreme_long_problems = ['LUKVLE15']


# Exit code = 1: Solve to acceptable level
Solved_acceptable_level_problems = ['BLEACHNG', 'BRATU2DT', 'CATMIX', 'CSFI2',
                                    'DECONVNE', 'LCH', 'LUKVLE18', 'READING9',
                                    'ROBOT', 'SINROSNB', 'SOSQP1']

# Exit code = 2: Converged to a point of local infeasibility. Problem may be
# infeasible.
infeasible_problems = ['A2NNDNIL', 'A2NSDSIL', 'A5NNDNIL', 'A5NSDSIL', 'ARTIF',
                       'CONT6-QQ', 'CRESC132', 'CRESC4', 'DISCS', 'DRCAVTY2',
                       'DRCAVTY3', 'EG3', 'FLOSP2HL', 'FLOSP2HM', 'HIMMELBD',
                       'JUNKTURN', 'LINCONT', 'LIPPERT1', 'MODEL', 'NASH',
                       'OSCIPANE', 'PFIT3', 'PFIT4', 'POWELLSQ', 'WOODSNE']

# Exit code = 4: Iterates divering; problem might be unbounded.
unbounded_problems = ['ELATTAR', 'MESH', 'STATIC3']


# Exit code = 6: Feasible point for square problem found.
feasible_square_problems = ['VANDERM1', 'VANDERM2', 'VANDERM3']

# Unstable problems: Sometime return code = 0, sometime does not return code 0

unstable_problems = ['POWELLSQ', 'VANDERM3']

ipopt_solvable_problems = [prob for prob in CUTEr_constrained_problems if
                           (prob.name not in too_few_freedom_problems) and
                           (prob.name not in fixed_variables_problems) and
                           (prob.name not in technical_difficulty_problems) and
                           (prob.name not in hard_problems) and
                           (prob.name not in restoration_failed_problems)]

ipopt_opal_test_problems = [prob for prob in ipopt_solvable_problems if
                            prob.name not in long_problems]

ipopt_hard_problems =  [prob for prob in CUTEr_constrained_problems if
                        (prob.name in hard_problems) and
                        (prob.name not in extreme_long_problems)]

# Exit code = 0, and solving time <= 0.001 for parameterpardefault
ipopt_opal_surrogate_problems = [prob for prob in CUTEr_constrained_problems
                        if prob.name in ['AIRCRFTA', 'BOOTH', 'BT12', 'BT3',
                                         'CHACONN1', 'CHACONN2', 'CUBENE',
                                         'DIXCHLNG', 'EG1', 'EXTRASIM',
                                         'GENHS28', 'GOTTFR', 'HATFLDA',
                                         'HIMMELBA', 'HIMMELBC', 'HIMMELBE',
                                         'HS14', 'HS22', 'HS28', 'HS3', 'HS31',
                                         'HS35I', 'HS3MOD', 'HS4', 'HS40',
                                         'HS48', 'HS50', 'HS51', 'HS52',
                                         'HS55', 'HS60', 'HS78', 'HS79', 'HS8',
                                         'HS80', 'HS81', 'HS9', 'HS99',
                                         'HYPCIR', 'KIWCRESC', 'LSQFIT',
                                         'MAKELA2', 'MARATOS', 'MIFFLIN1',
                                         'MWRIGHT', 'ORTHREGB', 'PALMER5D',
                                         'SIMBQP', 'SINVALNE', 'SUPERSIM',
                                         'TAME', 'ZANGWIL3', 'ZECEVIC4']]

# Radomly representative
ipopt_opal_p0_clustered_problems_0 = [prob for prob in CUTEr_constrained_problems
                                    if prob.name in ['PALMER1E', 'HS28',
                                                     'CUBENE', 'HS63', 'BT4',
                                                     'A0ESDNDL', 'EIGMINB',
                                                     'HS79', 'BROWNALE',
                                                     'HS77', 'BT2', 'DTOC1ND',
                                                     'LUKVLE7', 'BT7',
                                                     'LUKVLE10', 'BT6',
                                                     'DUAL4', 'QR3D', 'GASOIL',
                                                     'SPANHYD', 'GRIDNETF',
                                                     'HS100LNP', 'JANNSON3',
                                                     'OPTCNTRL', 'TRAINF',
                                                     'HELSBY', 'QPCBLEND',
                                                     'ZAMB2', 'LCH',
                                                     'FLETCHER', 'HS109',
                                                     'FLOSP2HL', 'DISC2',
                                                     'CORE1', 'QPCBOEI2',
                                                     'HYDROELL', 'ORBIT2',
                                                     'OET2', 'QPNBOEI2']]



# Most represetatvie
ipopt_opal_p0_clustered_problems_1 = [prob
                                      for prob in CUTEr_constrained_problems
                                      if prob.name in['ROBOTARM', 'GENHS28',
                                                      'ORTHREGB', 'ORTHRDM2',
                                                      'HS41', 'PORTFL3',
                                                      'LUKVLE3', 'HS9', 'HS62',
                                                      'OPTCTRL6', 'HS69',
                                                      'HAGER4', 'HATFLDG',
                                                      'TRIGGER', 'GRIDNETG',
                                                      'PINENE', 'BDVALUES',
                                                      'HEART8', 'GASOIL',
                                                      'ALLINITC', 'ORTHRGDS',
                                                      'SREADIN3', 'SAWPATH',
                                                      'DEGENLPB', 'TRAINF',
                                                      'HELSBY', 'QPCBLEND',
                                                      'A5NSDSDM', 'LCH',
                                                      'PRODPL1', 'OPTMASS',
                                                      'A0NNSNSL', 'ERRINBAR',
                                                      'CORE1', 'HADAMARD',
                                                      'QPNSTAIR', 'ORBIT2',
                                                      'AGG', 'CORKSCRW']]
# Most representative, clustered by measure map (multiple soms)
ipopt_opal_p0_clustered_problems_2 = [prob
                                      for prob in CUTEr_constrained_problems
                                      if prob.name in ['POWELL20', 'BLOWEYB',
                                                       'BLEACHNG', 'CSFI2',
                                                       'CLNLBEAM', 'PALMER1',
                                                       'CORKSCRW', 'DRUGDISE',
                                                       'ORTHREGA', 'SSNLBEAM',
                                                       'A5NNDNSL', 'STEENBRG',
                                                       'SIPOW1', 'SIPOW2M',
                                                       'MODEL', 'PFIT4',
                                                       'VANDERM3', 'YFIT',
                                                       'DISCS', 'HIMMELP5',
                                                       'PALMER3A', 'DUALC8',
                                                       'HYDROELS', 'OPTMASS',
                                                       'FLETCHER', 'FLOSP2HL',
                                                       'CRESC4', 'QR3DLS',
                                                       'ELATTAR', 'MESH',
                                                       'A2NNDNDL', 'CHEBYQAD',
                                                       'QPCSTAIR', 'GAUSSELM',
                                                       'READING9', 'LUKVLI12',
                                                       'SOSQP1', 'LCH',
                                                       'VANDERM1', 'ROBOT',
                                                       'A0NNSNSL', 'HS99EXP',
                                                       'A5ENSNDL', 'SMMPSF',
                                                       'CORE2', 'A4X12',
                                                       'STATIC3', 'MAXLIKA',
                                                       'HS38', 'HS13',
                                                       'PALMER4', 'EG3',
                                                       'PALMER1B', 'DEMBO7',
                                                       'POWELLSQ', 'PALMER6A',
                                                       'PALMER3', 'OET7',
                                                       'TWIRISM1', 'NET1',
                                                       'ROTDISC', 'CONT6-QQ',
                                                       'BIGGSC4', 'ERRINBAR']]


test_problems = [prob for prob in CUTEr_constrained_problems if
                 prob.name in ['3PK','A0ENDNDL','A0ENINDL']]


