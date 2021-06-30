import utils as ut


signal,energylist,fs=ut.speechSignalExtractor("SpeakerB", "arctic_a0001.wav");

MFCC=ut.MFCC(signal,30,fs,20);

print("The length of our MFCC is ", len(MFCC));
print("We get the following MFCC :", MFCC);




#We notice that the output is an array of 13 values
#The first value in the array s the energy as for the other values they are the MFCCs
#Unfortunately we are unable to truly tell if these values are the right ones given that despite 
#An internet search we were unable to find examples in order to compare our answers