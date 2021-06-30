import utils as ut
import numpy as np
import matplotlib.pyplot as plt

f=600;
fe=10000;
N=200;
t=np.arange(N)/fe;



y = 3*np.sin(2*np.pi*f*t);

plt.plot(t,y);

y=ut.Preamplaises(y ,0.67)

plt.plot(t,y);

#We notice that the signal we get after applying the filter is modified
#After doing some reshearch online we have found similar graphs to the one we get
#Which leads us to think that the filter is well applied on our sine wave