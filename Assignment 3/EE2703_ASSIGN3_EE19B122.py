from pylab import *						# importing pylab module						
from scipy.special import *					# importing special functions in scipy module
def g(t,A,B):							# defining a function g(t,A,B)
	return A*jv(2,t)+B*t					# returnining the value of g(t,A,B)
fitdata = loadtxt("fitting.dat")				# loading "fitting.dat" into the program as fitdata
t = fitdata[:,0]						# taking out time column(i.e 1st column) from fitdata
d = fitdata[:,1]						# taking out first column in data(i.e 2nd column in fitdata)
sigma = logspace(-1,-3,9)					# defining sigma(i.e standard deviation in probability distribution
y = g(t,1.05,-0.105)						# Finding the true value i.e f(t) without noise and assigning it to y
a,b = fitdata.shape						# finding how many rows and columns are there in fitdata; a corresponds to No. of rows and b corresponds to No. of columns
# generating M matrix in Q6
M = empty((a,2))						# Defining M as an empty array of dimension a*2 
for i in range(a):						# for loop in which i is iterating in the range(a)
	M[i] = (jv(2,t[i]),t[i])				# defining the terms in each row of M
p = array([1.05,-0.105])					# defining p array which contains values of A0,B0; i.e A0 = 1.05, B0 = -0.105
out = dot(M,p)							# multiplying arrays M,p and assigning the result to out
if array_equal(out,g(t,1.05,-0.105)) :			# checking whether out is equal to g(t,1.05,-0.105) or not
	 print("M.p is equal to true value")			# Printing "M.p is equal to true value" if out = g(t,1.05,-0.105)
else : print ("M.p is not equal to true value")		# printing "M.p is not equal to true value" if out != g(t,1.05,-0.105)

# plotting figure 0 in which we will plot truevalue, along with various amounts of noises
figure(0)							# this is the name what we will see on the folder of plot 
for i in range(1,10):						# iterating i from 1 to 9 so that we can plot 9 different noises corresponding to 9 data cloumns in fitdata
	plot(t,fitdata[:,i],label="σ=%.3f"%sigma[i-1])	# plotting t on x-axis and fitdata[:,i] on y axis and labelling the curve as σ=sigma[i-1] and upto 3 decimals for each iteration
plot(t,y,label="True Value",color='green',linewidth=3)	# plotting t on x-axis and y on y-axis in green colour and labelling the plot as "truevalue" 
title("Data to be fitted to theory",size = 25)		# givivng title to the plot as "Data to be fitted to theory"
xlabel(r'$t\rightarrow$',size = 20)				# labelling x-axxis
ylabel(r'$f(t)+n\rightarrow$',size = 20)			# labelling y-axis
grid(True)							# saying that i want plot in grid
legend()							# This is used to place legend on the axes

# calculating mean squared error in Q7
A = array([0.1*i for i in range(21)])				# Here A value is variable so I'm giving those values as array
B = array([-0.2+0.01*i for i in range(21)])			# Here E value is variable so I'm giving those values as array
E = zeros((21,21))						# This is our error array and we are initiating it by giving zeros to all elements in it
# This is all the process for calculation of MSerror
for i in range(21):
	for j in range(21):
		for k in range(a):
			E[i][j] += ((d[k] - (g(t[k],A[i],B[j])))**2)/a

# plotting contour of mean square error
figure(2)							# this is the name what we will see on the folder of plot 
X,Y = meshgrid(A,B)						# for plotting contour we have to define meshgrid
Contour=contour(X,Y,E,20)					# defining Contour as contour(X,Y,E,20)
clabel(Contour,Contour.levels[:5],inline=1)			# labelling
title("Q8:Contour Plot for Eij",size=20)			# giving title to the plot
xlabel(r'$A\rightarrow$',size=20)				# giving xlabel
ylabel(r'$B\rightarrow$',size=20)				# giving ylabel
grid(True)							# enabling grid so that we can get plot on a grid

# finding error in estimate of A,B
Ea = empty((9,1))						# defining Ea as empty array which corresponds to error in estimation of A
Eb = empty((9,1))						# defining Eb as empty array which corresponds to error in estimation of B
for j in range(9):
	
	AB = linalg.lstsq(M,fitdata[:,j+1],rcond=None)	# estimating A,B as elements in first row of AB
	Ea[j] = abs(AB[0][0]-p[0])				# calculation of error in estimation of A
	Eb[j] = abs(AB[0][1]-p[1])				# calculation of error in estimation of B
# plotting error in estimate of A,B
figure(3)									# this is the name what we will see on the folder of plot 
plot(sigma,Ea,label="A_error",color='red',marker='o',linestyle='dashed')	# plotting Ea Vs Sigma in red colour dots and a dashed line joining them
plot(sigma,Eb,label="B_error",color='green',marker='o',linestyle='dashed')	# plotting Eb Vs Sigma in green colour dots and a dashed line joining them
title("Q10: Variation of error with noise",size=25)				# giving the title to the plot
xlabel(r'$Noise Standard Deviation\rightarrow$',size=20)			# labelling x-axis
ylabel(r'$MS error\rightarrow$',size = 20)					# labelling y-axis
grid(True)									# enabling grid so that we can get plot on a grid
legend()									# This is used to place legend on the axes
# plot for first column of data with error bars
figure(1)									# this is the name what we will see on the folder of plot 
plot(t,y,label="True Value",color='blue',linewidth=3)			# plotting y Vs t curve in blue colour
errorbar(t[::5],d[::5],sigma[0],fmt='ro',label="Noise")			# plotting errorbars for every 5th term in 1st column
title("Q5: Data points for σ=0.10 along with exact function",size = 25)	# giving title to the plot
xlabel(r'$t\rightarrow$',size = 20)						# labelling x-axis
ylabel(r'$f(t)+n\rightarrow$',size = 20)					# labelling y-axis
grid(True)									# enabling grid so that we can get plot on a grid
legend()									# This is used to place legend on the axes
# plotting loglog. plot for plot in Q:10
figure(4)									# this is the name what we will see on the folder of plot 
loglog(sigma,Ea,'ro',label=" A_error")					# this will plot log(sigma) Vs log(Ea) in red colour dots(no dots joining) with label as A_error
errorbar(logspace(-1,-3,9),Ea,std(Ea),fmt='ro')				# this will plot the error bars
loglog(sigma,Eb,'go',label=" B_error")					# this will plot log(sigma) Vs log(Eb) in red colour dots(no dots joining) with label as B_error
errorbar(logspace(-1,-3,9),Eb,std(Eb),fmt='go')				# this will plot the error bars
title("Q11: Variation of error with noise",size=25)				# giving title to the plot
xlabel('Noise standard deviation',size=20)					# labelling x-axis
ylabel('MSerror',size=20)							# labelling y-axis
grid(True)									# enabling grid so that we can get plot on a grid
legend()									# This is used to place legend on the axes
show()										# this prints all the plots that were plotted till now
