# Importing the necessary modules.
from pylab import *
import scipy.signal as sp

# Q.1
p11 = poly1d([1,0.5]) 					# setting numerator polynomial
p21 = polymul([1,1,2.5],[1,0,2.25])			# setting denominator polynomial
X1 = sp.lti(p11,p21)					# X1 in s domain
t1,x1 = sp.impulse(X1,None,linspace(0,50,500))	# x1 in time domain

# plot of x(t) vs t for Q.1
figure(0)
plot(t1,x1)
title("The solution x(t) for Q.1")
xlabel(r'$t\rightarrow$')
ylabel(r'$x(t)\rightarrow$')
grid(True)

# Q.2
p12 = poly1d([1,0.05])					# setting numerator polynomial
p22 = polymul([1,0.1,2.2525],[1,0,2.25])		# setting denominator polynomial
X2 = sp.lti(p12,p22)					# X2 in s domain
t2,x2 = sp.impulse(X2,None,linspace(0,50,500))	# x2 in time domain

# Plot of x(t) vs t for Q.2
figure(1)
plot(t2,x2)
title("The solution x(t) for Q.2")
xlabel(r'$t\rightarrow$')
ylabel(r'$x(t)\rightarrow$')
grid(True)

# Q.3
H = sp.lti([1],[1,0,2.25])				# Finding impulse response considering f(t) as input and x(t) as output
for w in arange(1.4,1.6,0.05):			# Taking various frequencies
	t = linspace(0,50,500)
	f = cos(w*t)*exp(-0.05*t)
	t,x,svec = sp.lsim(H,f,t)			# finding x(t) for respective frequency

# plot of x(t) for various frequencies vs time in Q.3
	figure(2)
	plot(t,x,label='w = ' + str(w))
	title("x(t) for different frequencies")
	xlabel(r'$t\rightarrow$')
	ylabel(r'$x(t)\rightarrow$')
	legend(loc = 'upper left', prop={'size':10})
	grid(True)

# Q.4
t4 = linspace(0,20,500)
X4 = sp.lti([1,0,2],[1,0,3,0])
Y4 = sp.lti([2],[1,0,3,0])	
t4,x4 = sp.impulse(X4,None,t4)
t4,y4 = sp.impulse(Y4,None,t4)

# plots of x(t) and y(t) vs t for Q.4 
figure(3)
plot(t4,x4,label='x(t)')
plot(t4,y4,label='y(t)')
title("x(t) and y(t)")
xlabel(r'$t\rightarrow$')
ylabel(r'$functions\rightarrow$')
legend(loc = 'upper right')
grid(True)

# Q.5
denom = poly1d([1e-12,1e-4,1])
H5 = sp.lti([1],denom)
w,S,phi = H5.bode()

# magnitude bode plot for Q.5 
figure(4)
subplot(2,1,1)
semilogx(w,S)
title("Magnitude plot")
ylabel(r'$20\log|H(j\omega)|\rightarrow$')
grid(True)
# phase bode plot for Q.5 
subplot(2,1,2)
semilogx(w,phi)
title("Phase plot")
xlabel(r'$\omega\rightarrow$')
ylabel(r'$\angle H(j\omega)\rightarrow$')
grid(True)

# Q.6
t6 = arange(0,25e-3,1e-7)
vin = cos(1e3*t6) - cos(1e6*t6)
t6,vo,svec = sp.lsim(H5,vin,t6)

# The plot of Vo(t) vs t for large time interval.
figure(5)
plot(t6,vo)
title("Long term response")
xlabel(r'$t\rightarrow$')
ylabel(r'$V_o(t)\rightarrow$')
grid(True)

# The plot of Vo(t) vs t for small time interval.
figure(6)
plot(t6[0:300],vo[0:300])
title("Short term response")
xlabel(r'$t\rightarrow$')
ylabel(r'$V_o(t)\rightarrow$')
grid(True)

show()
