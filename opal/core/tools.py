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


class TableFormatter:

    def __init__(self, fieldDelimiter=' ', recordDelimiter='\n'):

        self.field_delimiter = fieldDelimiter
        self.record_delimiter = recordDelimiter
        self.row_template = None
        return

    def set_header(self, headers=None, *args):

        cols = []
        if headers is not None:
            cols.extend(headers)
        cols.extend(args)
        if len(cols) == 0:
            return None
        self.row_template = '{0:<}'
        headerStr = 'PROB'
        for col in cols:
            self.row_template = self.row_template + self.field_delimiter + \
                '{1['+ col + ']:>}'
            headerStr = headerStr + self.field_delimiter + col
        self.row_template = self.row_template + self.record_delimiter
        headerStr = headerStr + self.record_delimiter
        return headerStr


    def format(self, problem, record, **kwargs):

        record.update(kwargs)
        if len(record) == 0:
            return None
        try:
            return self.row_template.format(problem, record)
        except KeyError:
            return None
