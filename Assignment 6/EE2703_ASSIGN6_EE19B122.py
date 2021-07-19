#importing required modules
from sys import argv
from pylab import *
from numpy import *
#importing pandas module for data extraction
import pandas as pd

#default input arguments
n=100 # spatial grid size.
M=5 # number of electrons injected per turn.
nk=500 # number of turns to simulate.
u0=10 # threshold velocity.
p=0.25 # probability that ionization will occur
sigma=2 # standard deviation of electrons injected
#checking if correct number of input arguments are given or not
#if not given,exiting the program
try:
	len(argv)==1 and len(argv)==6
except ioerror:
	print('no enough argumnets')
	exit(0)

#if correct number of arguments given,then updating the constants using sys.argv
if len(argv)==6:
	n=int(argv[1])	#initialising the constants to a new value specified by user
	M=int(argv[2])	#Initialising data type(to float,int upon convinience) of given argument by user
	nk=int(argv[3])
	u0=float(argv[4])
	p=float(argv[5])
	sigma=float(argv[6])

#initialising three vector(1-D arrays) as zeroes for storing electron information
xx=zeros((n*M),dtype='float')	#postion
u=zeros((n*M),dtype='float')	#velocity
dx=zeros((n*M),dtype='float')	#displacement

#initialising lists for Intensity,Pelectron positions,velocity
#lists are used as we dont know the exact length
I=[]	#intensity
X=[]	#position
V=[]	#velocity

#performing the algorithm for nk tuns
for i in range(1,nk):
	#identifying the indices where elctron is available/ejected
	if i==1:
		ii=where(xx>0)	#using where function
	#where returns data type-tuple and first element of the tuple is an array containing indices
	dx[ii]=u[ii]+0.5	#updating displacemet of elctrons which are in tubelight only
	u[ii]=u[ii]+1		#increasing velocity of electrons which are in tubelight only
	xx[ii]=xx[ii]+dx[ii]	#updating position of each electron
	
	#identifying the electrons which reaches anode i.e., x=L or x=n
	iin=where(xx>=n)	#using where function
	#updating the information of electrons which reached anode
	xx[iin]=0	#position updated to zero,as they are not available
	u[iin]=0	#velocity will be zero
	dx[iin]=0	#displacement will be also zero for electrons that reached anode
		
	#finding electrons which has veocity greater than threshold
	kk=where(u>=u0)
	#now performing a random distribuition to find which electrons have probability p to collide with atoms
	#using rand() to get normalised distribuition
	ll=where(rand(len(kk[0]))<=p)	#getting indices of available elctron postions which can be collided
	#now finding elctron indices which are collided
	kl=kk[0][ll]
	#updating the collided elctron velcity to zero
	u[kl]=0
	#as collision may occur between i and i+dx,we are subtracting a random variable between 0 and dx
	xx[kl]=xx[kl]-rand(len(kl))*dx[kl]
	#as electrons are collided there is a photon which contributes to intensity
	#so adding the information of collidee elctrons using extend function
	I.extend(xx[kl].tolist())
	
	#finding position of zero for filling new electrons
	i0=where(xx==0)[0]
	#getting number of new elctrons by normal distribuition of mean and sigma specified
	m=int(sigma*rand()+M)	#integer part is taken,as number of elctrons is an integer
	#now the newly injected electrons should go into array of length n*M(xx array)
	#there can be a case where there is no enough free positions in array
	#then injecting only electrons which has space in array
	nv=min(len(i0),m)	#finding minimum of free spaces and injected elctrons
	
	#updating the position array(xx) to 1 where electrons are injected
	xx[i0[0:nv]]=1
	u[i0[0:nv]]=0	#velocity should be zero of newly injected electrons
	dx[i0[0:nv]]=0	#dispacement of new electrons are zero
	#identifying electron positions where x>0
	ii=where(xx>0)[0]
	#extending the X and V lists 
	X.extend(xx[ii].tolist())
	V.extend(u[ii].tolist())

#plotting electron density in histogram
figure(0)
hist(X,bins=arange(0,101,1),rwidth=0.8,ec='black')
title('electron density histogram')
xlabel('position')

#plotting intensity in histgram
figure(1)
a,bins,c=hist(I,arange(0,101,1),rwidth=0.8,ec='black')
#hist returns three arrays/arguments that contains information of histogram
title('intensity histogram')
xlabel('position')

#as hist returns the information of histogram,we find the electron intensity which are present between succesive postions
xpos=0.5*(bins[0:-1]+bins[1:]) #performing average value
d={'position':xpos,'count':a}  #column labelling
#pandas dataframe retuns data in tabulated form
p=pd.DataFrame(data=d)
#not restriction the number of rows and columns so taht every data is printed
pd.set_option("display.max_rows", None, "display.max_columns", None)
#printing data table
print(p)

#plotting phase space
figure(2)
plot(X,V,'or')
xlabel('position')
ylabel('velocity')
title('electron phase space')
show()
