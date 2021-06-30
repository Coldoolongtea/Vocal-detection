import utils as ut

ut.RuleBased();

'''
We have decided to only rely on the pitch to take the guess given that our formant values seem 
too tight. The system could do a better job if we had two pitch estimations and a more 
accurate formant estimation

An example of the output :
    
   
AveragePitchA   284.94287696415796
AverageFormantsA 3541.1141152813493
AveragePitchB   333.74103746754014
AverageFormantsB 3623.603287331265
Number A guesses  11
Number B guesses  19
the rule based system has made  26  right guesses and  4  wrong ones.
Thus accuracy is  86.66666666666667 



'''