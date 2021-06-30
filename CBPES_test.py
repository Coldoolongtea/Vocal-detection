import utils as ut

signal,energylist,fs=ut.speechSignalExtractor("SpeakerB", "arctic_a0001.wav");

condition=0;


#The CBPES function is Cepstrum-based pitch estimation
#When printing the pitch estimation we get an empty array
#And we also regularily get warnings because applying the hamming window
#To our voiced frames seems to leave us with a minute value which when
#Insearted into the logarithm triggers an error
#This function is not reliable and needs more work

pitch=ut.CBPES(signal,30,20,fs,7);

for p in pitch:
    if (60<p<500):
        condition=1;
    else:
        condition=0;
        
if(condition==1):
    print("All our pitch values are in the expected range of 60 to 500Hz");

print("Here is our pitch list: ", pitch);