class StatisticalMeasure:
    def average(measureName):
        return lambda p,m : m['CPU'].mean()
    average = staticmethod(average)


