- Try to create a new measure relating the solution quality. We define a measure elementary by FVAL - FZERO
  + For the unconstrained test problems, the new elementary measure works well. However for the constrained problems, the FZERO may
    be less than the FEVAL because X0 is not a feasible point.
- 2009-10-07: Try to penalty the infeasiblity of initial point by a const. This const is considered as a parameter of the 
  Algorithmic Parameter Optimization.
- 2009-10-07: Define the elementary measure of number of function evaluation. We count the evaluations of the constraints.
- 2009-10-09: Suspect the instabilty of DFO in different machine basing on the 
  different IPOPT-FORTRAN installation is caused by the different dependencies 
  like HSL, TRON, ... See detail in the dependencies libraries of IPOPT-FORTRAN
- 2009-11-02: Change the parameter optimization problem
  + For the unconstrained test problem, we consider CNSTOL parameter as a 
    variable. In this case, CNSTOL has signification in evaluating the solution of 
    trust 
region sub-problem and evaluating the predicted reduction
  + For the constrained test problem, we will fix the CNSTOL because CNSTOL is 
    used to relax the constrained of the origin problem. In the case that 
    CNSTOL is set so large, the constrained problem may become a unconstrained 
    problem
- 2009-11-02 Change the measure varphi_EVAL
    varphi_EVAL(p_1,p_2) = (mu_EVAL(p_1) - mu_EVAL(p_2)/(mu_EVAL(p_1) + mu_EVAL(p_2))
- 2009-11-02 Verify the CUTEr driver for DFO to check if we provide correct 
  information under sssumption that we pass all constrains as free-derivative to 
  DFO
- 2009-11-03 There are differences in some test problems between old platform (queue 
  suse) and new platform (queue redhat). To test always in old platform, specify 
  the execution queue redhat in LSF command
- 2009-11-04 Change the PP by default is 1000. This has so much influence on the 
  constrained test problems. The PP has not any affect to the unconstrained test 
  problem, so we can fix it to reduce the dimension of parameter tuning problem 
