import utils as ut
import numpy as np




signal,energylist,fs=ut.speechSignalExtractor("SpeakerB", "arctic_a0001.wav");

Formants=ut.Formants(signal,30,20,fs);

print("The calculated formants are", Formants);

#We notice that our values are in the expected range as mentioned in the report
#We also notice that each formant is about 1000Hz greater than the previous one
#Which seems to be a good sign.



