"""
         Name: Yeswanth.T
         Roll Number: EE19B122
          EE2703  Assignment-1
"""

from sys import argv, exit	#taking arguments for the program from the commandlines

"""
We use constants for some repetedly used comomands to make our code easier.
For example, if you decide to change the command from '.circuit' to '.start' later,
    we only need to change the constant
"""
CIRCUIT = '.circuit'
END = '.end'

if len(argv) != 2:	#checking whether number of command line arguments is equal to 2 or not. 
    print('\nUsage: %s <inputfile>' % argv[0])  #if the user doesn't give required inputfile and only the required inputs, this command asks the user to input a file
    exit()   # if len(argv) !=2 print the statement and exit.

"""
The user might input a wrong file name by mistake.
In this case, the open function will throw an IOError.
we do this using try-catch.whenever the code crashes,it will automatically goes to except and prints error
"""
try:
    with open(argv[1]) as f:				#openimg the inputfile and alloting it to the file pointer f 
        lines = f.readlines()				#reading the lines of inputfile and lists it to lines
        start = -1; end = -2
        for line in lines:              		# extracting circuit definition start and end lines
            if CIRCUIT == line[:len(CIRCUIT)]:
                start = lines.index(line)
            elif END == line[:len(END)]:
                end = lines.index(line)
                break
        if start >= end:                		# validating circuit block
            print('Invalid circuit definition')
            exit(0)

        for line in reversed(lines[start+1:end]):	
       	    words=line.split("#")[0].split()		#splitting the words of line seperated by space and by not considering the text after # i.e Removing the comments
       	    output =' '.join(reversed(words))		#joining the words of the line in reverse order and storing it as data
            print(output)                 		# print output

except IOError:
    print('Invalid file')				#printing error in case user didn't input the correct file
    exit()


