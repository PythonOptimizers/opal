import sys
import re

import coopsort

if __name__ == '__main__':
    regExp = r'(.+\[\s*)(\d+)\.?\d*( , 0\s+\].*)'
    f = open(sys.argv[1])
    lines = f.readlines()
    f.close()
    for line in lines:
        beginPart = (re.sub(regExp, r'\1', line)).strip()
        midPart = (re.sub(regExp, r'\2', line)).strip()
        endPart = (re.sub(regExp, r'\3', line)).strip()
        #print midPart
        treeCode10 = int(re.sub(regExp, r'\2', line).strip())
        treeCode6 = coopsort.encode(treeCode10, 6)
        print beginPart, treeCode6, endPart
