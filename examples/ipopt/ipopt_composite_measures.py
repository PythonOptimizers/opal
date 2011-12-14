def avg_time(parameters, measures):
    n = len(measures['CPU']) 
    if n == 0:
        return 0.0
    return (sum(measures["CPU"]) + 0.0)/(n + 0.0)

def sum_eval(parameters, measures):
    return sum(measures['FEVAL']) + sum(measures['GEVAL']) +\
           sum(measures['EQCVAL']) + sum(measures['EQJVAL']) +\
           sum(measures['INCVAL']) + sum(measures['INJVAL'])

def weighted_sum_eval(parameters, measures):
    result = 0.0
    for (feval, geval, eqcval, eqjval, incval, injval, weight) in \
        zip(measures['FEVAL'], measures['GEVAL'], measures['EQCVAL'], \
            measures['EQJVAL'], measures['INCVAL'], measures['INJVAL'], \
            measures['WEIGHT']):
        result = result + weight*(feval + geval + eqcval + eqjval + incval + \
                                  injval)
    return result

def sum_ecode_square(parameters, measures):
    result = 0.0
    for val in measures['ECODE']:
        result = result + val*val
    return result


def sum_ecode(parameters, measures):
    return sum(measures['ECODE'])

def sum_unsolvability(parameters, measures):
    unsolvabilities = 0
    for eCode in measures['ECODE']:
        if eCode < 0:
            unsolvabilities = unsolvabilities + 1
    return unsolvabilities

def sum_iteration(parameters, measures):
    return sum(measures['NITER'])
               
