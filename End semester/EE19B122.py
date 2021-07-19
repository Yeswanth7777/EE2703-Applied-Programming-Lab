# Tadigoppala Yeswanth
# EE19B122
# EE2703 Final code

from numpy import *
from pylab import *						# importing everything that is there in pylab. Here in this code we will use numpy and matplotlib modules.

N=100								# loop is divided into N parts and here N is given as 100.
a=10								# a is radius of the loop and it is equal to 10 cm.
# Q1,Q11 are discussed in report pdf

# Q2

x=linspace(-1,1,3)						# giving values to x using linspace so that x will have 3 values seperated by 1cm
y=linspace(-1,1,3)						# giving values to y using linspace so that y will have 3 values seperated by 1cm
z=arange(1,1001,1)						# giving values to z using linspace so that z will have 1000 values seperated by 1cm
X,Y,Z=meshgrid(x,y,z)						# dividing the volume into 3*3*1000 using meshgrid
rijk =zeros((3,3,1000,3))					# this is the one which will have all 9000 points in space
rijk[:,:,:,0]=X						# X values are stored
rijk[:,:,:,1]=Y						# Y values are stored
rijk[:,:,:,2]=Z						# Z values are stored

# Q3

phi_l=linspace(0,2*pi,101)					# phi_l is the angle made by lth part of loop with x-axis
phi_l=phi_l[:-1]
I=zeros((2,N))							# initialising I array which consists of 2 rows and N columns In which first column corresponds to Ix and 
								# second column corresponds to Iy
i1=zeros((2,N))
r=zeros((2,N))							# initialising r array which consists of 2 rows and N columns In which first column is x component of r and
								#  second row is y component of r
#if we consider the current as given in question								
I[0]=-1e7*((cos(phi_l)))*(sin(phi_l))				# giving values of x component of current for each element
I[1]=1e7*((cos(phi_l)))*(cos(phi_l))				# giving values of y component of current for each element
r[0]=a*(cos(phi_l))						# finding x position of each current element
r[1]=a*(sin(phi_l))						# finding y position of each current element

#if we consider absolute value of current								
i1[0]=-1e7*(abs(cos(phi_l)))*(sin(phi_l))				# giving values of x component of current for each element
i1[1]=1e7*(abs(cos(phi_l)))*(cos(phi_l))				# giving values of y component of current for each element
rxy = zeros((2,N))						# defining x,y coordinates of midpoints of current elements as an array rxy
rxy[0] = a*(cos((phi_l)+(pi/N)))				# defining x coordinate of midpoint of current element in rxy[0]
rxy[1] = a*(sin((phi_l)+(pi/N)))				# defining y coordinate of midpoint of current element in rxy[1]
# plotting current elements in x-y plane
figure(0)							# figure 0 is the name we will see on the folder of current elements plot
plot(rxy[0],rxy[1],'ro')					# plotting current elements 
xlabel('X $\longrightarrow$ ',size=10)			# giving x label to the plot
ylabel('Y $\longrightarrow$ ',size=10)	 		# giving Y label to the plot
title('plot of current elements in x-y plane')		# giving title to the plot
axis('square')							# making the coordinate axis to look like a square
grid('True')

# plotting current using quiver
figure(1)					 		# figure 1 is the name we will see on the folder of current elements plot
quiver(r[0],r[1],I[0],I[1],scale=1e8)				# this is the function we will use for vector plotting
axis('square')			 				# making the axis to look like square
xlabel('X $\longrightarrow$ ',size=10)			# giving x label to the plot
ylabel('Y $\longrightarrow$ ',size=10)	 		# giving Y label to the plot
title('Current Flow in The Loop using quiver',size=12) 	# giving title of the plot
axis('Square') 
grid('True')							# command to enable the grid in the plot 

figure(2)					
quiver(r[0],r[1],i1[0],i1[1],label="current flow")			 	#plotting the current vectors using quiver function
xlabel('X $\longrightarrow$ ',size=10)	 				#giving x-label to the plot
ylabel('Y $\longrightarrow$ ',size=10)	 				#giving y-label to the plot
title('Current Through The Loop if we consider absolute value of I',size=12) #giving title to the plot
grid('True')									#enabling grid to the plot
axis('Square')
legend()									#adding legend to the plot

# Q4

dl = zeros((2,N))						# initialising the dl vector as an array with all zeros
r_l=c_[a*(cos(phi_l)),a*(sin(phi_l)),zeros(N)]		# defining r_l vector using an array
dl[0] = -(2*pi*a/N)*sin(phi_l)				# defining x coordinate of dl vector
dl[1] = (2*pi*a/N)*cos(phi_l)					# defining y coordinate of dl vector


k=0.1								# defining k which is already given in the assignment

# Q5 and Q6

# defining calc function if we consider current as given in the question
def calc(l):
    Rijkl=linalg.norm(rijk-r_l[l],axis=-1)					# defining norm using the inbuilt norm function
    Axl=((cos(phi_l[l]))*exp((-1j)*k*(Rijkl))*(dl[0][l]))/Rijkl		# defining x component of magnetic potential(A) using the formula given in 
    										# assignment 
    Ayl=((cos(phi_l[l]))*exp((-1j)*k*(Rijkl))*((dl[1][l])))/Rijkl		# defining y component of magnetic potential(A) using the formula given in 
    										# assignment 
    return Rijkl,Axl,Ayl							# these are the values that are returned when we call this function
Axl=Ayl=0									# setting both initial values of x and y components of magnetic potential to zero

# Q7

for i in range(N):								# updating both x and y components of A using for loop
    R,dxl,dyl=calc(i)								# calling calc() function for each value of i
    Axl+=dxl									# incrementing Axl
    Ayl+=dyl									# incrementing Ayl
    
# Q8
Bz=(Ayl[1,2,:]-Ayl[1,0,:]-(Axl[2,1,:]-Axl[0,1,:]))/4				# giving values to Bz using vectorized operation and formula given in assignment

# Q9

# plotting magnetic field versus z
figure(3)									# figure 2 is the name we will see on the folder of current elements plot
loglog(z,abs(Bz),'b')								# plotting Bz Vs z in loglog in blue colour
xlabel('z(cm) $\longrightarrow$ ',size=10)					# giving x label to the plot
ylabel('Bz $\longrightarrow$ ',size=10)					# giving y label to the plot
title('Magnetic Field Vs z')							# giving title to the plot
grid('True')									# command to enable the grid in the plot 
# defining cal function if we consider current as given in the question
def cal(l):
    Rijkl=linalg.norm(rijk-r_l[l],axis=-1)					# defining norm using the inbuilt norm function
    Axl=(abs((cos(phi_l[l])))*exp((-1j)*k*(Rijkl))*(dl[0][l]))/Rijkl		# defining x component of magnetic potential(A) using the formula given in 
    										# assignment 
    Ayl=(abs((cos(phi_l[l])))*exp((-1j)*k*(Rijkl))*((dl[1][l])))/Rijkl		# defining y component of magnetic potential(A) using the formula given in 
    										# assignment 
    return Rijkl,Axl,Ayl							# these are the values that are returned when we call this function
Axl=Ayl=0									# setting both initial values of x and y components of magnetic potential to zero

# Q7

for i in range(N):								# updating both x and y components of A using for loop
    R,dxl,dyl=cal(i)								# calling calc() function for each value of i
    Axl+=dxl									# incrementing Axl
    Ayl+=dyl									# incrementing Ayl
    
# Q8
Bz1=(Ayl[1,2,:]-Ayl[1,0,:]-(Axl[2,1,:]-Axl[0,1,:]))/4			# giving values to Bz using vectorized operation and formula given in assignment

# Q9

# plotting magnetic field versus z
figure(4)									# figure 2 is the name we will see on the folder of current elements plot
loglog(z,abs(Bz1),'b')								# plotting Bz Vs z in loglog in blue colour
xlabel('z(cm) $\longrightarrow$ ',size=10)					# giving x label to the plot
ylabel('Bz $\longrightarrow$ ',size=10)					# giving y label to the plot
title('Magnetic Field Vs z if we consider absolute value of I')		# giving title to the plot
grid('True')									

# Q10

# Fitting the field to a fit of the type Bz=cz^b.
def lstsqfit(data):								# defining lstsqfit function to find best fit values of c,b
    #input arguments:- data
    M=c_[ones(len(data)),log(arange(1001-len(data),1001,1))]			# Matrix by adding columns
    est=linalg.lstsq(M,log(data),rcond=None)[0]				# using linalg.lstsq for obtaining best fit values
    return exp(est[0]),est[1]							# returning the required quantities i.e c,b
c,b = lstsqfit(abs(Bz))
d,e = lstsqfit(abs(Bz1))							# calling lstsqfit function to find best fit values of c,b
print('if we consider I expression in the question:')
print('best fit value of c is :',c)						# printing the best fit value of c 
print('best fit value of b is :',b)						# printing the best fit value of b
print('if we consider absolute value of I:')
print('value of c is:',d)							#printing the value of c
print('value of b is:',e)							#printing the value of b

show()										# this will show all the plots those were plotted till now
