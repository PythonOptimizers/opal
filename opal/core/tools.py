# Miscellaneous tools.
import re

def extract_measure(content, description, name, valueType = 'int'):
    numberPattern = {'int':'\d+',
                     'real':'-?\d*\.\d+',
                     'float':'-?\d*\.\d+E(\+|-)\d+'}
    converters = {'int':int,
                  'real': float,
                  'float': float}

    matches = re.finditer(description + '\s+:\s+(?P<' +
                          name + '>' +
                          numberPattern[valueType] + ')',
                          content)
    value = None
    for m in matches:
        if name not in m.groupdict().keys():
            raise Exception('Could not to extract measure ' + name)
            continue
        value = converters[valueType](m.groupdict()[name])
    return value

