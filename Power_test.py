import utils as ut
import numpy as np
import matplotlib.pyplot as plt


fs = 30.0

t = np.arange(0, 10, 1/fs)

y = np.sin(2*np.pi*6*t) + np.random.randn(len(t))


powerSpectrum = ut.Power(y)

frequency = np.linspace(0, fs/2, len(powerSpectrum))

plt.plot(frequency, powerSpectrum)
