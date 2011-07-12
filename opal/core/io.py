# Simple helper functions for input and output.

def read_params_from_file(filename):

    converters = {'categorical':int, 'binary':int, 'integer':int, 'real':float}
    fp = open(filename, 'rb')
    params = {}
    for line in fp:
        words = line.strip('\n').split(':')
        params[words[0]] = converters[words[1]](words[2])
    fp.close()
    return params



def write_measures_to_file(filename, measures):

    fp = open(filename, 'w')
    for measure in measures:
        print >> fp, measure, measures[measure]
    fp.close()
    return
