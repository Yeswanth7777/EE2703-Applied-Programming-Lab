import sys
import numpy as np
import math

if len(sys.argv) == 2:
	if sys.argv[1].split(".")[1] != "netlist":
		print("ERROR:Incorrect input file type")
	else:
		start = -1 						# initialising start eqaul to -1.
		end = -2						# initialising end is eqaul to -2.
		GND = 0 						# setting GND to zero
		n = 0 							# initialising n to 0 (corresponds to number of nodes except ground node)
		flist = []						# definining flist as an empty list
		CIRCUIT = ".circuit"					# Assigning CIRCUIT as circuit\n.
		END = ".end"						# Assigning End as end\n.
		acckt = ".ac"						# Assigning acckt as ac\n.
		AC = 0							# initialising AC to 0
		s = 0							# initialising s to 0 (s corresponds to number of voltage sources)
		x=0							# initialising x to zero(this is useful when writing nodal analysis equation for voltage sources
				
		with open(sys.argv[1]) as f: 				# opening the input file as f
			lines = f.readlines()				# defining a list as lines and place each line in input file as an element in lines
			
			for i in range(0,len(lines)):			# for loop 
				if lines[i][:len(CIRCUIT)]==CIRCUIT:
				   start = i   			# giving the index of .circuit line in lines as start
				elif lines[i][:len(END)]==END:
				   end = i			   	# giving the index of .end line in lines as end
				elif lines[i][:len(acckt)]==acckt:
					ac = lines[i].split()		# splitting lines[i] and storing them in a list defined as ac(we are doing this to access frequency in ac signal) 
					AC+=i				# giving the index of .ac line in lines as AC
					w=2*math.pi*float(ac[-1])	# calculating angular frequency

			if AC<end:
				AC = 0					# setting AC to 0 if AC<end
			if start >= end: 				# checking whether ckt is valid or not
			    print("INVALID CIRCUIT")			# printing invalid circuit if start>= end
			else:
				for i in range(start+1,end):
					yeswanth = (lines[i].split("#")[0]).split()	# removing comment and splitting the remaining line and storing them in a list called as yeswanth	
					flist.append(yeswanth)				# adding elements of yeswanth in flist
				print(*flist,sep = "\n")				# printing the netlist in tabulated form
						#Perfect upto here tokens were saved 
		# for finding number of nodes and number of voltage sources :
				for i in range(0,len(flist)):
					
					
						if flist[i][1] == "GND": a = 0	
						else: a = int(flist[i][1])							
						if flist[i][2] == "GND": b = 0							
						else: b = int(flist[i][2]) 
						
						if n <= a:
							n = a
						if n <= b:
							n = b
						if flist[i][0][0] == "V" : s+=1		#No. of voltage sources
				print("number of nodes(including ground) = %d" %(n+1)) 	# printing number of nodes		
				print("number of voltage sources = %d" %(s))		 	# printing number of voltage sources		
				
				A = [ [ 0 for i in range(n+s) ] for j in range(n+s) ]	# initialising A
				B = [ [ 0 for i in range(n+s) ] for j in range(1) ]		# initialising B
					
				for i in range(0,len(flist)):										
		# Nodal analysis for Resistors:	
					if flist[i][0][0] == "R":
						r = float(flist[i][3])
						
						if flist[i][1] == "GND":
							a = 0
						else:
							a = int(flist[i][1])
						if flist[i][2] == "GND":
							b = 0
						else:
							b = int(flist[i][2])

						if a*b != 0:
							A[a-1][a-1] += 1/r
							A[a-1][b-1] += -1/r
							A[b-1][a-1] += -1/r
							A[b-1][b-1] += 1/r
						if a == 0:
							A[b-1][b-1] += 1/r
						if b == 0:
							A[a-1][a-1] +=1/r
		# Nodal analysis for Capacitors:
					if flist[i][0][0] == "C" and AC !=0:
						z = complex(0,-1/(w*float(flist[i][3])))	# giving impedence for capacitor
						
						if flist[i][1] == "GND":
							a = 0
						else:
							a = int(flist[i][1])
						if flist[i][2] == "GND":
							b = 0
						else:
							b = int(flist[i][2])

						if a*b != 0:
							A[a-1][a-1] += 1/z
							A[a-1][b-1] += -1/z
							A[b-1][a-1] += -1/z
							A[b-1][b-1] += 1/z
						if a == 0:
							A[b-1][b-1] += 1/z
						if b == 0:
							A[a-1][a-1] +=1/z

		# Nodal analysis for Inductors:
					if flist[i][0][0] == "L" and AC !=0:
						z = complex(0,(w*float(flist[i][3])))		# giving impedence for inductor
						
						if flist[i][1] == "GND":
							a = 0
						else:
							a = int(flist[i][1])
						if flist[i][2] == "GND":
							b = 0
						else:
							b = int(flist[i][2])

						if a*b != 0:
							A[a-1][a-1] += 1/z
							A[a-1][b-1] += -1/z
							A[b-1][a-1] += -1/z
							A[b-1][b-1] += 1/z
						if a == 0:
							A[b-1][b-1] += 1/z
						if b == 0:
							A[a-1][a-1] +=1/z
		# nodal analysis for voltage sources:
					if flist[i][0][0] == "V":
						x+=1
						if flist[i][1] == "GND":
							a = 0
						else:
							a = int(flist[i][1])
							A[int(n+x-1)][a-1] = 1
							A[a-1][int(n+x-1)] = -1
							if flist[i][3] =="ac":								
								B[0][int(n+x-1)] = complex(float(flist[i][-2])*math.cos(float(flist[i][-1])),float(flist[i][-2])*math.sin(float(flist[i][-1])))
							else:								
								B[0][int(n+x-1)] = float(flist[i][-1])
						if flist[i][2] == "GND":
							b = 0
						else:
							b = int(flist[i][2])
							A[int(n+x-1)][b-1] = -1
							A[b-1][int(n+x-1)] = -1
							if flist[i][3] == "ac":
								B[0][n+x-1] = -complex(float(flist[i][-2])*math.cos(float(flist[i][-1])),float(flist[i][-2])*math.sin(float(flist[i][-1])))
							else:
								B[0][n+x-1] = -float(flist[i][-1])	
				
				out = np.linalg.solve(A,B[0]) 			# using linalg to solve nodal analysis matrix

						
						
				#print("Voltages at nodes are")
				for i in range(0,n+s):
					if AC==0:
						if i<n:print("Voltage at node %d is :"%(i+1))
						if i>=n:print("Current through V%d source is :"%(i-n+1))
						print(float("%.2f"%out[i]))
					else:
						if i<n:print("Voltage at node %d is : "%(i+1))
						if i>=n:print("Current through V%d source is : "%(i-n+1))
						print(out[i])  
				
				
elif len(sys.argv) ==1 : print("Usage: %s \nError: No Input Found \nExpected:FileName.py FileName.netlist" % sys.argv[0])
else: print("Usage: %s \nError:Too Many Inputs Found \nExpected:FileName.py FileName.netlist" % sys.argv)
