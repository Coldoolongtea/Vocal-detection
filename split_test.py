import utils as ut


signal,energylist,fs=ut.speechSignalExtractor("SpeakerB", "arctic_a0001.wav");

print("The length of the original signal is : ", len(signal));


Frames=ut.split(signal,35,fs,35);

print("The original signal has been divided into :", len(Frames), " Frames");

#Unit conversion
widthOfFrame=(len(Frames[1])/fs)*1000

print("Width of frame in samples ", len(Frames[1]));

print("Each with a width of :", widthOfFrame, "ms");

#We notice that our function splits the signal into different frames
#The frames have the desired width in ms
#Some information is howerver discarted given that it doesn't fit in a frame the right size
    
