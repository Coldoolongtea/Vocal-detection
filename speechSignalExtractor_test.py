import utils as ut

signal,energy,fs=ut.speechSignalExtractor("SpeakerB", "arctic_a0001.wav");

print("The sampling frequency is equal to", fs,"Hz");

if(fs==16000):
    print("The sampling frequency is the right one");


#With the use of the program Audacity we were able to check our fs and 
#The representation of our signal we have notices that the signal we plot here
#Resembles the signal which the we get with audacity 
#(the pictures are inserted in the report)
#and so does the sampling frequency (16000)
ut.visualize(signal, energy, fs);
