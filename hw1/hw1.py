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
def stdin():
	
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

	return nfa

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
			
		
def problem1():
	nfa = stdin()
	
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
	finalNfa = set()
	for i in range(len(nfa)):
		if nfa[i]['final'] == 1:
			finalNfa.add(i)
	
	for p in qd:
		# set final value 1 only if	
		# intersection of p['states'] and finalNfa is not empty
		if len(p['states'].intersection(finalNfa)) == 0:
			p['final'] = 0
		else:
			p['final'] = 1
	
	return qd


# print dfa into appropriate standard output format
def printDfa(dfa):
	print (len(dfa))
	index = 0
	for p in dfa:
		print index, p['final'], p['0'], p['1'] 
		index += 1

if __name__ == "__main__":
	
	dfa = problem1()
	printDfa(dfa)
