import utils as ut

a=[1,2,3,6,20,-5]

energy=ut.energyCalc(a);
#We manually calculated the energy of our signal a and found a value of 475
#By ensuring that our energy function returns an equivilent value we can say that
#The function does the desired job
if (energy == 475):
    print("Test succeded")