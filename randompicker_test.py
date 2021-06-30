import utils as ut



#The result gives us n different file names from the SpeakerA directory 
#After trying the test a few times we do notice that it allows to randomly get
#the names of various audio files in the desired directory

vocals = ut.randompicker("SpeakerA",n=3);

for L in vocals:
    print("The vocal ", L," has been selected");



