from pylab import *									# importing pylab
import scipy.integrate as integrate							# importing scipy.integrate as integrate
def f(x):										# defining exp(x) as f(x)
	return exp(x)									
def g(x):										# defining cos(cos(x)) as g(x)
	return cos(cos(x))								
x = linspace(-2*pi,4*pi,1200)								# giving values for x
y_exp = f(x)										# defining y_exp as f(x)
y_cos = g(x)										# defining y_cos as g(x)
x1 = linspace(0,2*pi,400)								# giving values for x1
t = tile(x1,3)										# giving values for t from x1 using tile function
x2 = linspace(0,2*pi,401)								# giving values for x2
x2 = x2[:-1] # drop last term to have a proper periodic integral			# redefining x2 by removing last term
C_exp = zeros((51,1))									# initialising C_exp array for fourier coefficients of exp(x) by integration
C_cos = zeros((51,1))									# initialising C_cos array for fourier coefficients of cos(cos(x)) by integration
C_exp[0][0] = (1/(2*pi))*(integrate.quad(f,0,2*pi))[0]				# giving value for C_exp[0][0]
C_cos[0][0] = (1/(2*pi))*(integrate.quad(g,0,2*pi))[0]				# giving value for C_cos[0][0]
for k in range(1,26):									# iterating k from 1 to 25
	def u_exp(x,k):								# defining u_exp(x,k) as f(x)*cos(k*x)
		return f(x)*cos(k*x)
	def v_exp(x,k):								# defining v_exp(x,k) as f(x)*sin(k*x)
		return f(x)*sin(k*x)
	def u_cos(x,k):								# defining u_exp(x,k) as g(x)*cos(k*x)
		return g(x)*cos(k*x)
	def v_cos(x,k):								# defining v_exp(x,k) as g(x)*sin(k*x)
		return g(x)*sin(k*x)
# integrating u_exp,v_exp,u_cos,v_cos with respect to x by using quad funcction
	result_exp_a = integrate.quad(u_exp,0,2*pi,args=(k))
	result_exp_b = integrate.quad(v_exp,0,2*pi,args=(k))
	result_cos_a = integrate.quad(u_cos,0,2*pi,args=(k))
	result_cos_b = integrate.quad(v_cos,0,2*pi,args=(k))
# allotting fourier coefficients accordingly
	C_exp[2*k-1][0] = (1/pi)*result_exp_a[0]
	C_exp[2*k][0] = (1/pi)*result_exp_b[0]
	C_cos[2*k-1][0] = (1/pi)*result_cos_a[0]
	C_cos[2*k][0] = (1/pi)*result_cos_b[0]
# generating A matrix
b_exp=f(x2) 										# f has been written to take a vector
b_cos=g(x2)										# g has been written to take a vector
A = zeros((400,51)) 									# allocate space for A
A[:,0]=1										# col 1 is all ones
for k in range(1,26):									# iterating k from 1 to 25
	A[:,2*k-1]=cos(k*x2) 								# cos(kx) column
	A[:,2*k]=sin(k*x2) 								# sin(kx) column
c1=lstsq(A,b_exp,rcond=None)[0] 							# estimating fourier coefficients of exp(x) by lstsq function
c2=lstsq(A,b_cos,rcond=None)[0]							# estimating fourier coefficients of cos(cosx)  by lstsq function
Abs_exp = abs((c1)-transpose(C_exp))							# absolute difference between calculated and estimated fourier coefficients of exp(x)
Abs_cos = abs((c2)-transpose(C_cos))							# absolute difference between calculated and estimated fourier coefficients of cos(cosx)
B_exp = dot(A,c1)									# Estimated exp(x)
B_cos = dot(A,c2)									# Estimated cos(cosx)
largedev_exp = Abs_exp.max()								# largest deviation in fourier coefficients of exp(x)
largedev_cos = Abs_cos.max()								# largest deviation in fourier coefficients of cos(cos(x))
print("The largest deviation between coefficients for exp(x) is ",largedev_exp)	# printing largest deviation value for fourier coefficients of exp(x)
print("The largest deviation between coefficients for cos(cos(x)) is ",largedev_cos) # printing largest deviation value for fourier coefficients of cos(cos(x))
# plotting figure 1
figure(1)										# This is what you will be seeing on the folder of image
semilogy(x,y_exp,'b',label='Actual Value')						# plotting semilog for exp(x) 
semilogy(x,exp(t),'-r',label='Periodic Extension')					# plotting semilog for periodic extension of exp(x)
semilogy(x2,B_exp,'go',label='Estimated Value')					# plotting semilog for estimated exp(x)
title("Semilogy plot of exp(x), periodic extension,estimated exp(x)",size = 25)	# giving title to the plot
xlabel(r'$x\rightarrow$',size = 20)							# labelling x-axis
ylabel(r'$e^x\rightarrow$',size = 20)							# labellinf y-axis
grid(True)										# enabling grid
legend()										# enabling legend

# plotting figure 2
figure(2)										# This is what you will be seeing on the folder of image
plot(x,y_cos,'b',label='Actual VAlue')						# plotting cos(cos(x))
plot(x,g(t),'r',label='fourier function')						# plotting fourier function for cos(cos(x))
plot(x2,B_cos,'go',label='Estimated value')						# plotting estimated cos(cos(x))
title("plot of cos(cos(x)) and it's Fourier function",size = 25)			# giving title to the plot
xlabel(r'$x\rightarrow$',size = 20)							# labelling x-axis
ylabel(r'$cos(cos(x))\rightarrow$',size = 20)						# labellinf y-axis
grid(True)										# enabling grid
legend()										# enabling legend

# plotting figure 3
figure(3)										# This is what you will be seeing on the folder of image
n = linspace(0,50,51)									# giving values for n
semilogy(n,abs(C_exp),'ro',label='integrated coefficients')				# semilog plot of magnitude of integrated fourier coefficients for exp(x)
semilogy(n,abs(c1),'go',label='Estimated Coefficients')				# semilog plot of magnitude of estimated fourier coefficients for exp(x)
title('Semilog plot of fourier coefficients of $exp(x)$',size=25)			# giving title to the plot
xlabel(r'$n\rightarrow$',size = 20)							# labelling x-axis
ylabel(r'magnitude of fourier coefficients$\rightarrow$',size = 20)			# labellinf y-axis
grid(True)										# enabling grid
legend()										# enabling legend

# plotting figure 4
figure(4)										# This is what you will be seeing on the folder of image
loglog(n,abs(C_exp),'ro',label='integrated coefficients')				# loglog plot of magnitude of integrated fourier coefficients for exp(x)
loglog(n,abs(c1),'go',label='Estimated Coefficients')				# loglog plot of magnitude of estimated fourier coefficients for exp(x)
title('loglog plot of fourier coefficients of $exp(x)$',size=25)			# giving title to the plot
xlabel(r'$n\rightarrow$',size = 20)							# labelling x-axis
ylabel(r'magnitude of fourier coefficients$\rightarrow$',size = 20)			# labellinf y-axis
grid(True)										# enabling grid
legend()										# enabling legend

# plotting figure 5
figure(5)										# This is what you will be seeing on the folder of image
semilogy(n,abs(C_cos),'ro',label='integrated coefficients')				# semilog plot of magnitude of integrated fourier coefficients for cos(cos(x))
semilogy(n,abs(c2),'go',label='Estimated Coefficients')				# semilog plot of magnitude of estimated fourier coefficients for cos(cos(x))
title('semilog plot of fourier coefficients of $cos(cos(x))$',size=25)		# giving title to the plot
xlabel(r'$n\rightarrow$',size = 20)							# labeling x-axis
ylabel(r'magnitude of fourier coefficients$\rightarrow$',size = 20)			# labellinf y-axis
grid(True)										# enabling grid
legend()										# enabling legend

# plotting figure 6
figure(6)										# This is what you will be seeing on the folder of image
loglog(n,abs(C_cos),'ro',label='integrated coefficients')				# loglog plot of magnitude of integrated fourier coefficients for cos(cos(x))
loglog(n,abs(c2),'go',label='Estimated Coefficients')				# loglog plot of magnitude of estimated fourier coefficients for cos(cos(x))
title('loglog plot of fourier coefficients of $cos(cos(x))$',size=25)		# giving title to the plot
xlabel(r'$n\rightarrow$',size = 20)							# labelling x-axis
ylabel(r'magnitude of fourier coefficients$\rightarrow$',size = 20)			# labellinf y-axis
grid(True)										# enabling grid
legend()										# enabling legend
show()											# this shows all the plots that were plotted till now
