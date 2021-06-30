import utils as ut


#This is a test for our ConjRemover function
#Which removes the negative complex conjugate
a=[1+3j,1-3j,5+4j,5-4j,6+6j,5+3j,-3j+5];
print("before :",a);
a=ut.ConjRemover(a);
print("After :",a);
#By printing the results we can see that the negative complex conjugates are removes

"""
The results of the code are:
    before : [(1+3j), (1-3j), (5+4j), (5-4j), (6+6j), (5+3j), (5-3j)]
    After : [(1+3j), (5+4j), (6+6j), (5+3j)]
    
    """