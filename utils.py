import numpy as np;
import os;
import random;
from scipy.io import wavfile
import math
import matplotlib.pyplot as plt
import xcorr as xr
import scipy.signal as sig
import scipy as sc
import LPC as lp
import cmath
import filterbanks as FB




def Preprocessing(array):
    #This function provides us with a normalised signal
    #We start by taking the maximum value of our signal
    
    
    #We divide each value in our signal by the maximum value
    Normalized=array/np.max(abs(array));
    #This way we end up with a normailzed signal   
    
    return Normalized;


def split(signal,width,fs,step):
    #This is a function that will split the signal into frames  
    
    #N is the number samples
    N = len(signal);
    #fs is the sampling frequency, which is the number of samples per seconds
    #the width is here supplied to the function is ms
    #therefore by multiplying it by fs and dividing by a thousand in order to
    #get the width in samples
    width = (width*fs)/1000;
    step = (step*fs)/1000; 
    frames=[]; 
    currentWindow=[]; 
    
    #if the wlength of the signal is smaller or equal in size to the desired width
    #we'll only have one frame in total
    if N <= width:
        framecount = 1;
    #If not the number of frames we'll have is given by the following formula
    else:
        framecount = 1 + int((N - width) / step);
        
    transition = int((framecount - 1) * step + width);
    zeros=np.zeros(np.abs(transition-N));
    #In order to harmonize the legth of the different signals we add zeros towards the end
    signal=np.concatenate((signal,zeros)) 
    
    First=0; 
    Last=0; 
    #The limit is the value which allows us to ensure that we remain inside of the array
    limit=int(N/step)-1;
    
    for i in range (0, limit): 
        #We start moving the frame by saying that our new last position is our fist one 
        #to which we have added the desired width
        Last=First+width;
        #In this line we define our current window
        currentWindow=np.asarray(signal[int(First):int(Last)]); 
        #we add our current window to our frame list
        frames.append(currentWindow);         
        First=First+step;
        
    frames=np.asarray(frames);
    return frames;    



    
def energyCalc(signal):
    #the following function helps us get the energy of our signal
    #It is a simple implementation of the energy definition
    energy=0;
    for x in signal:        
        energy+=np.square(abs(x));
    return energy;

#ABPES stands for Autocorrelation-Based Pitch Estimation System
def ABPES(signal,width,step,fs):  
    #We start by normalizing the signal
    normalizedSignal=Preprocessing(signal); 
    #then we split the signal into frames
    Frames = split(normalizedSignal,width,fs,step);      
    pitch=[];
    threshold = 7;
    # For each frame we're going to compute the energy and 
    # compare it to a threshold if the energy is greater
    # than the threshold we consider the frame to be voiced and thus
    # compute the autocorrelation in order to get the pitch of the frame
    for F in Frames:
        NRJ=energyCalc(F);
        #In order to get the Tmaxlag we need to divide the sampling         
        #frequency by the minimum frequency which in this case is 50
        maxl=math.floor(fs*0.02);
        if(NRJ>threshold):
          lags, corr=xr.xcorr(F,F,'none',maxl);           
          #We look for the position of the different peaks keeping in mind
          #that our values should have a maximum frequency of 500
          peaks, prop=sig.find_peaks(corr, distance=int(fs/500));
          #plt.plot(lags,corr);
          #If the length of the peak array is greater than one
          # we consider the max to be at the center of the array
          # given that the biggest correlation is always at lag 0
          # and then we get the second position by getting a neighbouring
          # peak
          #The distance between the two peaks is the fundemental period
          Max=lags[peaks];
          
          if(len(Max)>1):              
                    
              center=int(len(Max)/2);
              T0=Max[center+1]-Max[center];
                
              F0=1/T0;
              #Given that earlier we the distance in frames
              #we multiply by the sampling frequency
              #To get the frequency in Hz
              F0=F0*fs;
              pitch.append(F0);
              
        
        
    return pitch





def randompicker(directoryname,n):
    #This is a finction which selects 5 random audio files 
    #from a given directory
    selectedVocals = []
    #We start by making a list which has the different file names
    files = os.listdir(directoryname);
    #We pick 5 random file names from the list created previously
    for x in range(0,n):
      tmp=random.choice(files);
      selectedVocals.append(tmp);
      #We return the five selected vocals
    return selectedVocals

def speechSignalExtractor(directoryname, Vocal):   
    #This function allows us to extract the signal,fs, and energy of 
    #a given wave file
    
    fs, signal=wavfile.read(directoryname+ "/" +Vocal)
    
    energylist=[];
    #we normalise the signal
    normalizedSignal=Preprocessing(signal);   
    
    #and split it into differrent frames
    
    Frames=split(normalizedSignal,30,fs,20);
    #before computing the energy on each frame
    # for F in Frames :
    #energylist.append(energyCalc(F));      
    energylist=[energyCalc(i) for i in Frames];
    
    return signal,energylist,fs;



 


#Ceptrum-Based Pitch Estimation Sytem
def CBPES(signal,width,step,fs,threshold):
    #We start by normalizing the signal
    normalizedSignal=Preprocessing(signal); 
    #then we split the signal into frames
    Frames = split(normalizedSignal,width,fs,step);
    pitch=[];
    for F in Frames:
        
        N=len(F);
        NRJ=energyCalc(F);
        if(NRJ>threshold):
            #Application of the hamming window
            
            h= np.hamming(N)*F;            
            #h=sig.boxcar(N)*F
            
           
           #we start by computing the frequency response of the signal
           #We then calculate the logarithmic value          
          
            logValue=20*np.log10(abs(h));
            
           #In order to get the Cepstrum we take the inverse 
           #fourier transform of the signal's log spectrum
           
            cepstrum = abs(np.fft.ifft(logValue));
            print(cepstrum)
            admittedValues=[];
            # As mentioned in the protocole our algorithm should 
            # now look for the peak value in the part of the cepstrum where
            # the fundemental frequency is (between 60 and 500Hz);
            for F in cepstrum:
                if (F>1/60 and F<1/500):
                    admittedValues.append(F);                    
                    pitch.append(fs*F);
                    
        
    
    return pitch
            
def Preamplaises(x ,a):
    
    #Using the formula mentioned in the protocol
    #y(t) = x(t) - ax(t-1)
    y=np.zeros(len(x));
    
    
    for i in range(0,len(x)):
        y[i]=x[i] - a * x[i-1];   
   
    return y
  
def ConjRemover (Racines):
    #This is a function which removes the negative complexe conjugate vales,
    #From a given array
    CleanRoots=[]
    for i in Racines:
        if (np.imag(i) >= 0):
            CleanRoots.append(i);
        
    return CleanRoots
            
def Formants(signal,width,step,fs):
    
    
    #We start by splitting the signal into frames
      Frames = split(signal,width,fs,step);
      Formants=[];
      for F in Frames:
          #We apply a filter on each frame
          filtered=Preamplaises(F,0.67);    
          #We then apply a hamming window on each filtered frame
          windowed = sig.hamming(len(filtered))*filtered;
          #The LPC function allows us to get the LPC coefficients
          coef=lp.lpc_ref(windowed, 12);            
          roots = np.roots (coef);
          #After retrieving the roots of our coefficients
          #we make sure to only keep one of the two complexe conjugate values
          
          cleanRoot= ConjRemover(roots);
         
          anglelist =[];  
         
          for R in cleanRoot:
              #we get the phase of each of our roots
             a = cmath.phase(R) ;
             anglelist.append(a);
             
          #Sorted allows us to ensure that the angles are stored in increasing values
          Form = sorted(anglelist);
          #We convert from rad per sec to hertz
          converted=[];
          for i in Form:
                 converted.append((i*fs)/(2*np.pi));   
                
          Formants.append(converted);  
          
      return Formants

def Power(signal):
    #This function computes the power spectrum of an array by following the formula
    #Given in the instructions
   NTFD=512;
   
   FFT = np.absolute(np.fft.rfft(signal, NTFD))  ;
   powerSpectrum = ((1.0 / NTFD) * ((FFT) ** 2))   ;     

   return powerSpectrum ;
    
    
def loopSpeechSignalExtractor(directoryname):  
    #this is a function which loops 5 signals
    #allowing us to visualise the signal and energy of each
    #This function was useful in order to determine the threshold
    #Based on the different graphs we got
    selectedVocals=randompicker(directoryname,5);
    for file in selectedVocals:
        signal,energylist,fs=speechSignalExtractor(directoryname, file);
        # ABPES(signal,30,20,fs);
        visualize(signal, energylist, fs);



def MFCC(signal,width,fs,step):
    #Step number one is here the pre-emphasize of the signal as seen previously
    #a=0.97 given by the teacher
      filtered=Preamplaises(signal,0.97);
      #Next we split into frames
      Frames = split(filtered,width,fs,step);
      
      for F in Frames:
          #For each frame we apply a hamming window
          windowed = sig.hamming(len(F))*F;
          #we can now compute the power sprectrum of the signal periodogram
          pow_frames=Power(windowed);
          #We pass our power spectrum into our melfilter
          filter_banks=FB.filter_banks(pow_frames, fs, nfilt = 40, NFFT=512);
          #Here we use a discrete cosine transform given the strong correlation
          #between the coefficients
          #Here we have a problem when using 1 for the axis value so we have 
          #used -1 as mentioned on the scipy documentation
          dc=sc.fft.dct(filter_banks,type=2,axis=-1,norm='ortho');          
          #We only keep the first 13 elements, the first being the energy equivilent,
          #and the 12 others the MFCC
          dc=dc[:13];
          
      return dc
      

def RuleBased():
    #We start by picking 15 random vocals from each Speaker
    #We have decided to focux on the average values, some precision will be sacrificed 
    #For the sake of ease
    SpeakerB=randompicker("SpeakerB",15);
    SpeakerA=randompicker("SpeakerA",15);    
    MeanpitchListA=[];
    MeanpitchListB=[];
    MeanFormantListA=[];
    MeanFormantListB=[];
    #A is meant to be the number of times our system guesses A
    A=0;
    #B is the number of times our system guesses B
    B=0;
    #The I am wrong integer is used to give us an idea of the number of times we failes to get
    #The right results
    IamWrong=0;
    for vocalA in SpeakerA :
     #We start by extracting the information from each of our randomly selected vocals
       signal,energylist,fs=speechSignalExtractor("SpeakerA", vocalA);
       #We then use our autocorrelation function in order to compute the pitch
       pitch=ABPES(signal,30,20,fs);     
       #After many observations we have decided that the pitch value of 300 seems to
       #Be a good threshold for seperating Speaker A from Speaker B
       if(np.mean(pitch)<300):
          A=A+1; 
       else:
           IamWrong=IamWrong+1;
           B=B+1;
       #MeanpitchListA is a variable which contains the mean value of the pitch for a given vocal
       MeanpitchListA.append(np.mean(pitch));
       formants=Formants(signal,30,20,fs);
       for i in formants:
           MeanFormantListA.append(np.mean(i));
    MeanFormantListA=np.mean(MeanFormantListA);
    #AveragePitchA has the average pitch for the 15 different vocals from speaker A
    AveragePitchA=np.mean(MeanpitchListA);
    AverageFormantsA=np.mean(MeanFormantListA);
    print("AveragePitchA  ",AveragePitchA);
    print("AverageFormantsA", AverageFormantsA);
    #The same thought process is repeated for speaker B
    for vocalB in SpeakerB :
        signal,energylist,fs=speechSignalExtractor("SpeakerB", vocalB);
        pitch=ABPES(signal,30,20,fs);
        if(np.mean(pitch)<300):
          A=A+1; 
          IamWrong=IamWrong+1;
        else:
           B=B+1;
        MeanpitchListB.append(np.mean(pitch));
        formants=Formants(signal,30,20,fs);
        for x in formants:
           MeanFormantListB.append(np.mean(x));
          
    MeanFormantListB=np.mean(MeanFormantListB);
    AveragePitchB=np.mean(MeanpitchListB);
    AverageFormantsB=np.mean(MeanFormantListB);
    
    #We decided to visualize the pitch and the formants
    #This was done in order to pick thresholds for allowing for the decision making
    #Of out function
    print("AveragePitchB  ",AveragePitchB);
    print("AverageFormantsB", AverageFormantsB);
    print("Number A guesses ", A );
    print("Number B guesses ", B );
    print("the rule based system has made ",30-IamWrong," right guesses", "and ",IamWrong," wrong ones."  );
    print("Thus accuracy is ", (30-IamWrong)*100/30, "%");
    
    #This bit of code is an experiment, we were hoping to get a threshold in order to use it in
    #Later on function RuleBased3 in order to see how well it could preform, this way we hoped we could give
    #Future versions of the code more autonomy;
    difference=abs(AveragePitchB-AveragePitchA)/2;
    minimun=min(AveragePitchB,AveragePitchA);
    threshold= minimun+difference;
    
    return threshold;
     
    
def RuleBased2():    
    #This function is similar to the previous one, the only change is the 
    #Pitch threshold which allows us to tell if it's speaker A or B
    SpeakerB=randompicker("SpeakerB",15);
    SpeakerA=randompicker("SpeakerA",15);    
    MeanpitchListA=[];
    MeanpitchListB=[];
    MeanFormantListA=[];
    MeanFormantListB=[];
    
    A=0;
    
    B=0;
 
    IamWrong=0;
    for vocalA in SpeakerA :
    
       signal,energylist,fs=speechSignalExtractor("SpeakerA", vocalA);
       
       pitch=ABPES(signal,30,20,fs);     
       #After many observations we have decided that the pitch value of 300 seems to
       #Be a good threshold for seperating Speaker A from Speaker B, however this time we consider 
       #the equation the other way around
       if(np.mean(pitch)>300):
          B=B+1;
          IamWrong=IamWrong+1;
       else:
           
           A=A+1;
       
       MeanpitchListA.append(np.mean(pitch));
       formants=Formants(signal,30,20,fs);
       for i in formants:
           MeanFormantListA.append(np.mean(i));
    MeanFormantListA=np.mean(MeanFormantListA);
    
    AveragePitchA=np.mean(MeanpitchListA);
    AverageFormantsA=np.mean(MeanFormantListA);
    print("AveragePitchA  ",AveragePitchA);
    print("AverageFormantsA", AverageFormantsA);
    
    for vocalB in SpeakerB :
        signal,energylist,fs=speechSignalExtractor("SpeakerB", vocalB);
        pitch=ABPES(signal,30,20,fs);
        if(np.mean(pitch)>300):
          B=B+1; 
         
        else:
           A=A+1; 
           IamWrong=IamWrong+1;
        MeanpitchListB.append(np.mean(pitch));
        formants=Formants(signal,30,20,fs);
        for x in formants:
           MeanFormantListB.append(np.mean(x));
          
    MeanFormantListB=np.mean(MeanFormantListB);
    AveragePitchB=np.mean(MeanpitchListB);
    AverageFormantsB=np.mean(MeanFormantListB);
    
    
    
    print("AveragePitchB  ",AveragePitchB);
    print("AverageFormantsB", AverageFormantsB);
    print("Number A guesses ", A );
    print("Number B guesses ", B );
    print("the rule based system has made ",30-IamWrong," right guesses", "and ",IamWrong," wrong ones."  );
    print("Thus accuracy is ", (30-IamWrong)*100/30, "%");
    
    
    
    
def RuleBased3():    
    #This function is similar to the previous one, the only change is the 
    #Pitch threshold which allows us to tell if it's speaker A or B
    SpeakerB=randompicker("SpeakerB",15);
    SpeakerA=randompicker("SpeakerA",15);    
    MeanpitchListA=[];
    MeanpitchListB=[];
    MeanFormantListA=[];
    MeanFormantListB=[];
    #We have decided to use a threshold which is given to us by our previous RuleBased and which results  
    pitchThreshold=RuleBased();
    A=0;
    
    B=0;
 
    IamWrong=0;
    for vocalA in SpeakerA :
    
       signal,energylist,fs=speechSignalExtractor("SpeakerA", vocalA);
       
       pitch=ABPES(signal,30,20,fs);     
       if(np.mean(pitch)>pitchThreshold):
          B=B+1;
          IamWrong=IamWrong+1;
       else:
           
           A=A+1;
       
       MeanpitchListA.append(np.mean(pitch));
       formants=Formants(signal,30,20,fs);
       for i in formants:
           MeanFormantListA.append(np.mean(i));
    MeanFormantListA=np.mean(MeanFormantListA);
    
    AveragePitchA=np.mean(MeanpitchListA);
    AverageFormantsA=np.mean(MeanFormantListA);
    print("AveragePitchA  ",AveragePitchA);
    print("AverageFormantsA", AverageFormantsA);
    
    for vocalB in SpeakerB :
        signal,energylist,fs=speechSignalExtractor("SpeakerB", vocalB);
        pitch=ABPES(signal,30,20,fs);
        if(np.mean(pitch)>pitchThreshold):
          B=B+1; 
         
        else:
           A=A+1; 
           IamWrong=IamWrong+1;
        MeanpitchListB.append(np.mean(pitch));
        formants=Formants(signal,30,20,fs);
        for x in formants:
           MeanFormantListB.append(np.mean(x));
          
    MeanFormantListB=np.mean(MeanFormantListB);
    AveragePitchB=np.mean(MeanpitchListB);
    AverageFormantsB=np.mean(MeanFormantListB);
    
    
    print("AveragePitchB  ",AveragePitchB);
    print("AverageFormantsB", AverageFormantsB);
    print("Number A guesses ", A );
    print("Number B guesses ", B );
    print("the rule based system has made ",30-IamWrong," right guesses", "and ",IamWrong," wrong ones."  );
    print("Thus accuracy is ", (30-IamWrong)*100/30, "%");
     
     
         
     

def visualize(signal, energy, fs): 
    #This is a function which is used to get a visual representation of
    #the signal and it's energy in the form of two subplots
    #We start by getting the length of the signal
    N=len(signal);
    #we use the legth if the signal divided by the sampling
    #frequency in order to get the time in seconds which will here be 
    #plotted on the x-asis
    t = np.arange(N)/fs;
    #Given that the energy is an array which contains the different energies
    #For each frame, dividing the length of the signal
    #will gives us an idea of the different frames in the signal
    step = int(len(signal)/len(energy));
    #we will this way find the corresponding values for the x-axis 
    #which we'll need in order to plot the energy graph
    tf = np.arange(step, len(signal), step)/fs;
    #ax will allow us to get out two subplots
    fig, ax = plt.subplots(2,sharex='col', sharey='row');
    
    ax[0].plot(t,signal, 'b') ;    
    ax[0].set(title='The Signal');

    ax[1].plot(tf,energy, 'r');
    ax[1].set(title='The energy');
    
    plt.show();
    
    

