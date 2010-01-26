class StatisticalMeasure:
    def average(measureName):
        return lambda p,m : m[measureName].mean()
    average = staticmethod(average)


