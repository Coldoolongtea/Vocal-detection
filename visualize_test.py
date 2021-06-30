import utils as ut

signal,energy,fs=ut.speechSignalExtractor("SpeakerB", "arctic_a0001.wav");

ut.visualize(signal, energy, fs);

#given that the main goal of this function is to output a graph holding two subplots
#one for the energy one for the temporal representaion of the signal on two subplots
#We can say that the visualize function does the job needed.