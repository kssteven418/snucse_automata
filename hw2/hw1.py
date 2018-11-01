#!/usr/bin/python

import sys
from pprint import pprint

# read NFA from standard input
def stdin(terminals):
	
	# mode can be either 1 or 2 and stands for the problem number
	num_states = int(sys.stdin.readline())
	prod = []
	nonterminals = []

	#read line by line 
	for i in range(num_states):
		line = sys.stdin.readline()
		temp = []
		for i in range(len(line)):
			if line[i].isalpha() or line[i] in terminals:
				temp.append(line[i])
				if line[i].isalpha() and line[i] not in nonterminals:
					nonterminals.append(line[i])

		prod.append(temp)
	
	# parsed input as a list of productions
	# each production is a list
	# where the 1st elmt is the LHS nonterminal variable
	# ex) S:A*B -> [S, A, *, B]
	
	return prod, nonterminals


def removeSingleProd(in_prod, nt):

	#first, separate productions into single productions and multi-productions
	#and arrange into directory having key = LHS nonterminals
	singleprod = {}
	multiprod = {}

	#init directories
	for x in nt:
		singleprod[x] = []
		multiprod[x] = []

	#separate and arrange productions
	for prod in in_prod:
		#if single production and RHS is nonterminal
		if len(prod)==2 and prod[1] in nt: 
			singleprod[prod[0]].append(prod)
		else:
			multiprod[prod[0]].append(prod)
	
	# then, for every A in nonterminal,
	# find all nonterminal B's such that A->*B
	
	#init connections (with direct transition)
	connected = {}
	for x in nt:
		connected[x] = set()
		prods = singleprod[x] # single productions whose LHS are x
		for p in prods: # for every sigle
			connected[x].add(p[1])
	
	
	#then add indirect connections through iteration
	keepIter = True
	while keepIter:
		keepIter = False
		for x in connected:
			# old connection of nonterminal x
			old_connection = set(connected[x]) 
			# new connection of nonterminal x
			new_connection = set(connected[x])

			# add all nonterminals connected with y in the old_connection
			# into the new_terminal
			for y in old_connection:
				new_connection = new_connection.union(connected[y])
			
			#if the new_connection and the old_connection are different,
			#continue the interation
			if len(new_connection-old_connection)!=0:
				keepIter=True
			connected[x] = new_connection
	
	#finally, we can build a new set of productions w/o single productions
	
	final_prod = []
	for x in nt:
		#first, add the non-single productions
		for p in multiprod[x]:
			final_prod.append(p)
		#then, add new productions for the single production
		x_connected = connected[x] # all nonterminals that are connected to x
		#x->*y
		for y in x_connected:
			y_prod = multiprod[y]
			for yp in y_prod:
				# new production is x to yp[1:]
				final_prod.append([x]+yp[1:])
	
	"""
	pprint(singleprod)
	print("")
	pprint(multiprod)
	print("")
	pprint(connected)
	print("")
	pprint(final_prod)
	"""
	return final_prod


#helper function
# rename opeator terminals
# if terminal is not operator (num), then return itself
def renameTerminal(t):
	if t=='+':
		return 'a'
	if t=='-':
		return 'b'
	if t=='*':
		return 'c'
	if t=='/':
		return 'd'
	if t=='(':
		return 'e'
	if t==')':
		return 'f'
	return t

#helper function
#divide a given production into multiple productions 
#having at most two terminals
#and return them as a list
def divideProd(prod, num_dict):
	if len(prod)==3:
		return [prod]
	new_name = '<'+prod[0]+num_dict[prod[0]]+'>'
	num_dict[prod[0]] += 1
	new_prod = [prod[0], new_name, prod[-1]]
	rec_prod = [new_name] + prod[2:]
	print(new_name)
	return [new_prod]+divideProd(rec_prod, num_dict)

# build final Chomsky standard form
# productions : list productions with no single productions
# nt : list of nonterminals
# t : list of terminals
def buildStandard(productions, nt, t) :
	
	# copy productions
	new_prod = []
	for p in productions:
		new_prod.append(list(p))

	# for keeping new terminal-producing productiosn, such as <a>->+
	terminals = []
	terminal_prods = []
	
	# additional number to rename new nonterminals
	num = 0

	final_prod = []

	#first of all, rename terminals and nonterminals
	for p in new_prod:
		
		#rename the LHS
		p[0] = '<'+p[0]+'>'
		
		#rename RHS
		#if the length is 1, then the RHS is a single terminal
		if len(p)==2 :
			final_prod.append(p)
			continue

		# otherwise, RHS is composed of multiple terminals and nonterminals
		for i in range(len(p))[1:]:
			if p[i] in t: # if terminal
				# if the terminal is shown first time
				# make additional terminal-producing production
				if p[i] not in terminals: 
					terminals.append(p[i])
					temp = ['<'+renameTerminal(p[i])+'>', p[i]]
					terminal_prods.append(temp)
				p[i] = '<'+renameTerminal(p[i])+'>'

			else : # if nonterminal, simple rename it into <NT> format
				p[i] = '<'+p[i]+'>'
		
		# then divide the RHS so that RHS has only two nonterminals
		divided = []
		test = 0
		while True:
			if len(p)==3:
				divided.append(p)
				break
			new_name = "<C"+str(num)+">"
			num += 1
			# group front n-1 productions into new_name
			divided.append([p[0], new_name, p[-1]])
			# new production that expand new_name into n-1 productions
			p = [new_name] + p[1:-1]
		
		final_prod = final_prod + divided	
	
	# merge the terminal-producing productions
	final_prod = final_prod + terminal_prods
	
	return final_prod 


#print function
def printResult(prod):
	print(len(prod))
	for p in prod:
		temp = ""
		for i in range(len(p)):
			temp = temp + p[i]
			if i==0: 
				temp = temp+":"
		print(temp)

if __name__ == "__main__":
	terminals = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '(', ')']
	in_prod, nonterminals = stdin(terminals)
#print(in_prod)
#print(nonterminals)

	noSingleProd = removeSingleProd(in_prod, nonterminals)
#pprint(noSingleProd)
	
	finalProd = buildStandard(noSingleProd, nonterminals, terminals)
#pprint(finalProd)

	printResult(finalProd)
