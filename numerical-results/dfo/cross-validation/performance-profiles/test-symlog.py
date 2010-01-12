
from pylab import *
import matplotlib.ticker as tk
#dt = 0.01

class MyFormatter(tk.LogFormatterMathtext):
    def __init__(self,base=10.0,labelOnlyBase=True,scale=0):
        tk.LogFormatterMathtext.__init__(self,base,labelOnlyBase)
        self.base_value = base
        self._scale = scale + 0.0

    def __call__(self,x,pos=None):
        if x == 0:
            scaledValue = 0
        elif x > 0:
            scaledValue = pow(self._base, x - self._scale)
        else:
            scaledValue = pow(self._base, -x - self._scale)*(-1.0)
        return tk.LogFormatterMathtext.__call__(self,scaledValue,pos)


def formatter_function(x, pos):
    print 'Nho nha nho nhang'
    return str(x) + ' ho ho ' + str(pos)

x = np.array([-0.020221864382998663, -0.020221864382998663, -0.0010546743154031426, -0.0003411758288786893, -6.664250445151683e-05, -6.1677980871144303e-05, -3.0736722994657922e-05, -7.0899899811687805e-06, -3.8994709936684215e-06, -2.8361484678304802e-06, -4.6540895544102147e-07, -4.5009029463438372e-07, -4.4745741237602529e-07, -5.405405504037048e-09, -2.5957624790485806e-09, -1.8757554350448579e-12, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.2269611249082607e-11, 4.4647882956666309e-09, 7.92260378554199e-09, 3.0949528532961949e-08, 4.2113315957756326e-08, 1.146579044119741e-07, 1.9103976440981321e-07, 3.6856722602533059e-07, 9.0159333812105207e-07, 1.4682049105304978e-05, 2.5662375575403405e-05, 0.0050974254892412647, 0.0061754910500312968, 0.0065814885434537281, 0.007565328155152708, 0.089303422992453044, 0.99961671419192455])



#subplot(311)
#plot(x, y)
#xscale('symlog',basex=10)
#ylabel('symlogx')
#grid(True)
#gca().xaxis.grid(True, which='minor')  # minor grid on too

#from pylab import *

#dt = 0.01
#x = arange(-50.0, 50.0,
logbase = 10
epsilon = 0.1
x_neg = [-log(-xe)/log(logbase) for xe in x if xe < 0]
scale = max(x_neg) 
x_neg = [xe - scale - epsilon for xe in x_neg]
  
x_pos = [log(xe)/log(logbase) for xe in x if xe > 0]
scale = min(x_pos)
x_pos = [xe - scale + epsilon for xe in x_pos]
x_zero = [0 for xe in x if xe == 0]

xd = x_neg  + x_zero + x_pos
#print xd
y = (arange(len(xd)) + 1)*(1.0/len(xd))
#set_xlim([0,0.5])

currentAxes = gca()
#subplot(311)
#new_axes = axes()
#new_axes.semilogx(x, y)

currentAxes.plot(xd,y,drawstyle='steps-post')
#currentAxes.semilogx(x,y,basex=10)
#loglog(xd,y,basex=10,basey=10)
#new_axes.set_xscale('symlog',basex=10)
#gca().set_autoscale_on(False)
#currentAxes.xaxis.set_autoscale(False)
#currentAxes.set_xscale('symlog',basex=10,linthreshx=1.00e-11)

#xlim([-0.1,0.1])
#print gca().get_xlim()
#gca().xaxis.set_ticklocs([-0.1, -0.01, 0, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0])
#currentAxes.xaxis.set_major_locator(tk.FixedLocator(locs=[-7,-1,0,1,3,4,8,10]))
currentAxes.xaxis.set_major_formatter(MyFormatter(base=10,labelOnlyBase=False,scale=12))
#currentAxes.xaxis.set_major_formatter(tk.LogFormatterMathtext(base=10,labelOnlyBase=False))
#print tk.LogFormatterMathtext(base=10,labelOnlyBase=False).format_data(5)
#currentAxes.xaxis.set_major_formatter(tk.FuncFormatter(formatter_function))

#print MyFormatter(base=10,labelOnlyBase=False,scale=12).format_data(5)
print gca().xaxis.get_ticklocs()
print gca().xaxis.get_view_interval()
#ylabel('scalex-symlog')
#new_axes.grid(True)
grid(True)
gca().xaxis.grid(True, which='minor')  # minor grid on too

#subplot(312)
#plot(x, y)
#xscale('log')
#ylabel('scalex-log')


#subplot(313)
#plot(x, y)
#xscale('symlog')
#yscale('log')
#grid(True)
#ylabel('scalex-linear')

#show()


savefig('test.pdf')
