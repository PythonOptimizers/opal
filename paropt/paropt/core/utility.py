import os
import sys
import types
import string

def atoi(intStr):
    try :
        return string.atoi(intStr)
    except ValueError:
        return 1000000000

def atof(floatStr):
    try :
        return string.atof(floatStr)
    except ValueError:
        return 1e+50

class ColumnFileFormat:
    def __init__(self,fieldSeparator = ' ',recordSeparator = '\n',showFields = []):
        self.fieldSeparator = fieldSeparator
        self.recordSeparator = recordSeparator
        self.showFields = showFields
        pass
    
    def write(self,record,destFile):
        return
    
    def read(self,srcFile):
        lines = srcFile.read().split(self.recordSeparator)
        records = []
        for i in range(len(lines)):
            fields = lines[i].split(self.fieldSeparator,len(self.showFields))
            if len(fields) < len(self.showFields):
                continue
            record = {}
            for j in range(len(self.showFields)):
                if type(self.showFields[j]) == type((0,0)):
                    field = self.showFields[j][0]
                else:
                    field = self.showFields[j]
                record[field] = fields[j]
            records.append(record)
        return records

class FreeWidthColumnFileFormat(ColumnFileFormat):
    def __init__(self,fieldSeparator = ' ',recordSparator = '\n',showFields = []):
        ColumnFileFormat.__init__(self,fieldSeparator,recordSeparator,showFields)
    
    def write(self,record,destFile):
        if type(self.showFields[0]) == type((0,0)):
            field = self.showFields[0][0]
        else:
            field = self.showFields[0]
        fmtStr = '{' + field  + '}'
        for i in range(1,len(self.showFields)):
            if type(self.showFields[i]) == type((0,0)):
                field = self.showFields[i][0]
            else:
                field = self.showFields[i]
            fmtStr = fmtStr + self.fieldSeparator + '{' + field  + '}'
        fmtStr = fmtStr + self.recordSeparator
        #The function str.format() require Python 2.6 or later
        destFile.write(fmtStr.format(**record))
        return


class FixedWidthColumnFileFormat(ColumnFileFormat):
    def __init__(self,fieldSeparator = ' ',recordSeparator = '\n',
                 showFields = [],formatTemplate = {'int':'i','real':'.3e','category':'','const':''}):
        ColumnFileFormat.__init__(self,fieldSeparator,recordSeparator,showFields)
        self.formatTemplate = formatTemplate
        pass

    def write(self,record,destFile):
        fieldName = self.showFields[0][0]
        fieldWidth = self.showFields[0][1]
        if 'type' in record.keys() and len(self.showFields[0]) >= 3:
            fieldFormat = self.formatTemplate[record['type']]
        else:
            fieldFormat = ''
        fmtStr = '{' + fieldName  + ':' + str(fieldWidth) + fieldFormat + '}'
        for i in range(1,len(self.showFields)):
            fieldName = self.showFields[i][0]
            fieldWidth = self.showFields[i][1]
            if 'type' in record.keys() and len(self.showFields[i]) >= 3:
                fieldFormat = self.formatTemplate[record['type']]
            else:
                fieldFormat = ''
            fmtStr = fmtStr + self.fieldSeparator + '{' + fieldName  + ':' + str(fieldWidth) + fieldFormat + '}'
        fmtStr = fmtStr + self.recordSeparator
        #print "fmtStr",fmtStr,"here"
        #print >> destFile, fmtStr
        destFile.write(fmtStr.format(**record))
        return

        
def readwords(readFile):
    lines = readFile.readlines()
    words = []
    for i in range(len(lines)):
        wordInLine = lines[i].split(' ')
        if len(wordInLine) == 0:
            continue
        for j in range(len(wordInLine)):
            if len(wordInLine[j].strip()) != 0:
                words.append(wordInLine[j].strip())
    return words
