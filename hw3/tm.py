#!/usr/bin/python

import sys
from pprint import pprint

# read productions from standard input
def stdin():
	
	num_vars = int(sys.stdin.readline()) # k
	var = ['0', '1', '#']

	# list of k+3 variables
	# 0, 1, #, a, b, c, ...
	for i in range(num_vars):
		var.append(chr(ord('a')+i))

	num_states = int(sys.stdin.readline())

	stop_line = sys.stdin.readline()
	stop_state = []
	
	# stop state as a list
	# ith element : is ith state a stop state?
	for i in range(num_states):
		stop_state.append(int(stop_line[i]))

	# transition rule
	# ith element of the transition list : transition rule for current state i
	# each transition rule as a dictionary, key is a variable(0, 1, #, a, b, c ...)
	# i.e. transition[0]['0'] is a dictionary,
	# with a key ns(next state), w(write), and mv(move)
	transition = []
	for b in range(num_states):
		temp = {}
		for l in range(num_vars+3):
			temp[var[l]] = {}
			trans_line = sys.stdin.readline()
			trans_line = trans_line.split()
			temp[var[l]]['ns'] = trans_line[0]
			temp[var[l]]['w'] = trans_line[1]
			temp[var[l]]['mv'] = trans_line[2]
		transition.append(temp)
	
	# input string
	temp = sys.stdin.readline()
	instrings = []

	# debugging mode
	if temp[0]=='D':
		n_in = int(sys.stdin.readline())	
		
		print(n_in)
		for k in range(n_in):
				
			temp = sys.stdin.readline()
			instring = '#'
			# remove unnecessary tokens (such as \n)
			for i in temp:
				if i in var:
					instring = instring+i
			instring = instring + '#'
			instrings.append(instring)

	#normal input
	else:
		instring = '#'
	
		# remove unnecessary tokens (such as \n)
		for i in temp:
			if i in var:
				instring = instring+i
		instring = instring + '#'
		instrings.append(instring)
	return var, num_states, stop_state, transition, instrings

def tm(stop_state, transition, instring):
	cur_pos = 0
	cur_state = 0
	cnt = 0
	while(True):
		cnt = cnt+1
		cur_var = instring[cur_pos] # read tape input
		rule = transition[cur_state] # rule
		rule = rule[cur_var]
		#print (cur_state)
		#print (cur_var)
		#print (instring)
		
		# at stop position
		if stop_state[cur_state] == 1 :
			break

		if rule['ns'] != '-' : # exists state transition
			# if not, then no state transition -> infinite loop

			# 1) write output
			temp = list(instring)
			temp[cur_pos] = rule['w']
			instring = ''.join(temp)

			# 2) state transition
			cur_state = int(rule['ns'])

			# 3) move position
			if rule['mv'] == 'L':
				if cur_pos == 0: # error
					print("left side out of bound")
					break
				cur_pos = cur_pos-1 # move left

			elif rule['mv'] == 'R':
				if cur_pos == len(instring)-1: # at the rightmost end
					instring = instring+"#" # append one more '#'
				cur_pos = cur_pos+1 # move right
		
	return instring
		

# remove #
def outputstring(string):
	outstring = ""
	for i in range(len(string)):
		if string[i] != '#':
			outstring = outstring + string[i]
	
	return outstring


# for debugging
def unary_conv(u, op):
	if op==1:
		return len(u)
	elif op==2:
		x = 0
		y = 0
		sw = 0
		for i in range (len(u)):
			if u[i]=='1' and sw==0:
				x = x+1
			elif u[i]=='1' and sw==1:
				y = y+1
			elif u[i]=='0':
				sw = 1
		return x, y
				




if __name__ == "__main__":

	var, num_states, stop_state, transition, instrings = stdin()
	for instring in instrings:
		outstring = outputstring(tm(stop_state, transition, instring))
		i1, i2 = unary_conv(instring, 2)
	#	print(i1, i2)
		print(i1)
#		print(outstring)
		print(unary_conv(outstring, 1))
