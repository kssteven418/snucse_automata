#!/usr/bin/python

import sys
from pprint import pprint

#problem 1

# help function for the stdin fuction
# make appropriate NFA transition list with the given input string
#'0, 1' -> [0, 1]
#'-' -> None
def transList(string):
	temp = string.split(',')
	if temp[0] == '-': # no transition
		return None
	for i in range(len(temp)):
		temp[i] = int(temp[i]) # make string into integer
	temp.sort()
	return temp


# read NFA from standard input
def stdin(mode):
	
	# mode can be either 1 or 2 and stands for the problem number
	num_states = int(sys.stdin.readline())
	nfa = []
	
	#read line by line 
	for i in range(num_states):
		line = sys.stdin.readline()
		#then, parse to make each state into a dictionary
		temp = {}
		parseLine = line.split()
		temp['final'] = int(parseLine[1]) # final state
		temp['0'] = transList(parseLine[2]) 
		temp['1'] = transList(parseLine[3])
		temp['e'] = transList(parseLine[4])
		nfa.append(temp)

	# for problem 2, should also make input lists
	inputs = []
	
	if mode == 2:
		num_inputs = int(sys.stdin.readline())
		for i in range(num_inputs):
			line = sys.stdin.readline()
			line = line[:-2] # remove \r\n
			inputs.append(line)
	
	return nfa, inputs


#returns a set of final states of a given NFA
def getNfaFinalStates(nfa):
	finalNfa = set()
	for i in range(len(nfa)):
		if nfa[i]['final'] == 1:
			finalNfa.add(i)
	return finalNfa


# E function
# reachable states starting from 'states'
# through epsilon edges
def E(nfa, states):
	final = set(states)
	states = list(states)

	for q in states:
		if nfa[q]['e']!=None:
			#states that can reach from the state q
			#by reading epsilon
			temp = set(nfa[q]['e'])
			
			for p in temp:
				if p not in final:
					states.append(p)
			
			final = final.union(temp)

	return final


# Delta function
# reachable states starting from 'states'
# by reading alphabet 'alp'
def delta(nfa, states, alp):
	final = set()
	for q in states:
		if nfa[q][alp] != None:
			temp = set(nfa[q][alp])
			final = final.union(temp)
	return final


# find index of the marked state in qd
# return -1 if all unmarked
def indexMarked(qd):
	for i in range(len(qd)):
		if qd[i]['mark'] == True:
			return i
	return -1
	

# return index of the states if already in qd
# return -1 if not in qd
# states is given as a set
def matchStates(qd, states):
	for i in range(len(qd)):
		if qd[i]['states'] == states:
			return i
	return -1
			
def getDfa(nfa):
	
	qd = [] # Q_D
	temp = {}
	temp['mark'] = True
	temp['states'] = E(nfa, [0])
	qd.append(temp)

	# Build DFA according to the textbook algorithm (p.21-22)
	while True:
		index = indexMarked(qd) # get index of marked state
		if index < 0:
			break # break if all states are unmarked
		
		p = qd[index]
		p['mark'] = False # unmark the state
		
		for alp in ['0', '1']:
			r = E(nfa, delta(nfa, p['states'], alp))
			matchIndex = matchStates(qd, r)
			if matchIndex<0:
				# if not in qd, append new entry at qd
				temp = {}
				temp['mark'] = True
				temp['states'] = r
				qd.append(temp)
				p[alp] = len(qd)-1

			else:
				p[alp] = matchIndex
	
	# Then, mark the final state
	finalNfa = getNfaFinalStates(nfa)

	for p in qd:
		# set final value 1 only if	
		# intersection of p['states'] and finalNfa is not empty
		if len(p['states'].intersection(finalNfa)) == 0:
			p['final'] = 0
		else:
			p['final'] = 1
	
	return qd

def runDfa(x, dfa):
	p = dfa[0]

	for i in range(len(x)):
		ns = p[x[i]]
		p = dfa[ns]
	
	if p['final'] == 0:
		return False
	else:
		return True


def runNfa(x, nfa):
	# list of the final states of the given NFA
	finalNfa = getNfaFinalStates(nfa)
	
	# algorithm given at the pdf
	states = E(nfa, [0])
	for i in range(len(x)):
		 states = delta(nfa, states, x[i])
		 states = E(nfa, states)
	
	# check whether the states contain the final states of NFA
	if len(states.intersection(finalNfa)) == 0:
		return False
	else:
		return True


######################### PROBLEM SOLVER FUNCTIONS ####################	

def problem1():
	nfa, _ = stdin(1)
	
	dfa = getDfa(nfa)

	return dfa


def problem2():
	nfa, inputs = stdin(2)
	
	nfaResult = []
	for x in inputs:
		nfaResult.append(runNfa(x, nfa))
	
	return nfaResult


def compareDfaNfa():
	nfa, inputs = stdin(2)
	dfa = getDfa(nfa) 
	
	dfaResult = []
	nfaResult = []

	for x in inputs:
		d_temp = runDfa(x, dfa)
		n_temp = runNfa(x, nfa)
		dfaResult.append(d_temp)
		nfaResult.append(n_temp)
	
	return dfa, dfaResult, nfaResult
		
	

################ FORMAT PRINT FUNCTIONS ################

# print dfa into appropriate standard output format
def printDfa(dfa):
	print (len(dfa))
	index = 0
	for p in dfa:
		print index, p['final'], p['0'], p['1'] 
		index += 1


# print True/False into YesNo format
def printYesNo(tf):
	for i in tf:
		if i:
			print("Yes")
		else:
			print("No")


if __name__ == "__main__":
	
	# get mode from the commandline argument
	
	if len(sys.argv) != 2 :
		print "Wrong Input Format"
		exit(0)

	if sys.argv[1] not in ['1', '2', '3']:
		print "Wrong Input Format"
		exit(0)

	mode = sys.argv[1]

	#problem 1
	if mode == '1':
		dfa = problem1()
		printDfa(dfa)
	
	#problem 2
	elif mode == '2':
		tf = problem2()
		printYesNo(tf)
	
	#problem 3
	elif mode == '3':
		dfa, dr, nr = compareDfaNfa()
		print "Result : ", dr==nr
		print "DFA : "
		printDfa(dfa)
