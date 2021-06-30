import utils as ut
import numpy as np
import matplotlib.pyplot as plt

f=600;
fe=10000;
N=200;
t=np.arange(N)/fe;

#We're here trying to test out normalization function
#To do so we start by creating a sin function which has an amplitude of 3
#After applying our function to the sin wave we notice on the graph that it
#Does normalize our signal as intended

y = 3*np.sin(2*np.pi*f*t);
plt.plot(t,y);


y=ut.Preprocessing(y);
plt.plot(t,y);



