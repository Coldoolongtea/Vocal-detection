import utils as ut

signal,energylist,fs=ut.speechSignalExtractor("SpeakerB", "arctic_a0001.wav");

condition=0;


#The ABPES function is our autocorelation function
#In order to insure its functionment we make sure that 
#all the valuse we get for the pitch are in the correct range
#We also realise that the pitch variable here will contain different values
#One for each voiced frame
pitch=ut.ABPES(signal,30,20,fs);

for p in pitch:
    if (60<p<500):
        condition=1;
    else:
        condition=0;
        
if(condition==1):
    print("All our pitch values are in the expected range of 60 to 500Hz");

print("Here is our pitch list: ", pitch);