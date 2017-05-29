def AND(a,b):
	return a and b

def OR(a,b):
	return a or b

def NOT(a):
	return not a

def Implies(a,b):
	return OR(NOT(a),b)

def Iff(a,b):
	return OR(AND(a,b),AND(NOT(a),NOT(b)))

operators = ['(','!','&','|','>','=',')']

precedence = ['!','&','|','>','=','(']

def to_postfix(statement):
	stack = []
	postfix = ''
	for ch in statement:
		if ch not in '(!&|>=)':
			postfix=postfix+ch
		if ch == '(':
			stack.append(ch)
		if ch in '!&|>=':
			if len(stack)==0:
				stack.append(ch)
			else:
				while len(stack)!=0 and precedence.index(stack[-1])<=precedence.index(ch):
					postfix=postfix+stack.pop()
				stack.append(ch)
		if ch==")":
			while stack[-1]!='(':
				postfix=postfix+stack.pop()
			stack.pop()
	while len(stack)!=0:
		postfix=postfix+stack.pop()
	return postfix


def evaluate_postfix(statement):
	stack=[]
	for ch in statement:
		if ch=='1' or ch=='0':
			stack.append(ch)
		else:
			if ch=='!':
				a=eval(stack.pop())
				stack.append(str(NOT(a)))
			if ch=='&':
				b=eval(stack.pop())
				a=eval(stack.pop())
				stack.append(str(AND(a,b)))
			if ch=='|':
				b=eval(stack.pop())
				a=eval(stack.pop())
				stack.append(str(OR(a,b)))
			if ch=='>':
				b=eval(stack.pop())
				a=eval(stack.pop())
				stack.append(str(Implies(a,b)))
			if ch=='=':
				b=eval(stack.pop())
				a=eval(stack.pop())
				stack.append(str(Iff(a,b)))
	return bool(eval(stack[0]))

def evaluate(table1,i,statement):
	postfix_statement=to_postfix(statement)
	for v in table1:
		if v in postfix_statement:
			postfix_statement=postfix_statement.replace(v,str(table1[v][i]))
	return evaluate_postfix(postfix_statement)		


m=input("number of statements : ")
statements = [raw_input() for i in range(m)]
variables = []


for state in statements:
	i=0
	while i < len(state):
		if state[i]==' ':
			state=state[:i]+state[i+1:]
			i-=1
		i+=1
	v=''
	for ch in state:
		if ch not in operators:
			v=v+ch
		if ch in operators:
			if v!='' and v not in variables:
				variables.append(v)
			v=''
	if v!='' and v not in variables:
		variables.append(v)

print variables

n = len(variables)
table1 = {v:[0 for i in range(2**n)] for v in variables}
table2 = {s:[False for i in range(2**n)] for s in statements}

i=1
j=n-1
while j>=0:
	for t in range(2**(i-1)):
		k=2**i-1-t
		while k<2**n:
			table1[variables[j]][k]=1
			k=k+2**i
	i=i+1
	j=j-1

for s in statements:
	for i in range(2**n):
		table2[s][i]=evaluate(table1,i,s)

table = [[0 for j in range(n+m)] for i in range(2**n)]
tablehead = []
for v in variables:
	tablehead.append(v)
for s in statements:
	tablehead.append(s)

for i in range(2**n):
	for j in range(n):
		table[i][j]=str(int(table1[variables[j]][i]))
	for j in range(n,n+m):
		table[i][j]=str(int(table2[statements[j-n]][i]))

import csv
with open('finalresult.csv','w') as csvfile:
	writer=csv.writer(csvfile,delimiter=',')
	writer.writerow(tablehead)
	writer.writerows(table)

taut_contr_cont = {s:'' for s in statements}

for j in range(n,n+m):
	x=table[0][j]
	c=0
	for i in range(2**n):
		if table[i][j]!=x:
			break
		c=c+1
	if c==2**n:
		if x=='0':
			taut_contr_cont[statements[j-n]]='Self-Contradiction'
		elif x=='1':
			taut_contr_cont[statements[j-n]]='Tautology'
	else:
		taut_contr_cont[statements[j-n]]='Contingency'

for s in statements:
	print s, "  ", taut_contr_cont[s]

flag=False
for j in range(m):
	for i in range(j+1,m):
		if table2[statements[i]]==table2[statements[j]]:
			flag=True
			print "Equivalence in ("+statements[i]+") and ("+statements[j]+")"
if not flag:
	print "No Equivalent statements found"

for i in range(2**n):
	c=0
	for j in range(n,n+m):
		if table[i][j]!='1':
			break
		c=c+1
	if c==m:
		print "Set of statements are Logically consistent"
		break
if c!=m:
	print "Set of statements are not logically consistent"

impl_statements=[]
impl_index = []
for i in range(m):
	for j in range(m):
		if i!=j:
			impl_statements.append("("+statements[i]+")>("+statements[j]+")")
			impl_index.append((i,j))

m=len(impl_statements)
table_new = [[0 for j in range(n+m)] for i in range(2**n)]
table2 = {s:[False for i in range(2**n)] for s in impl_statements}
for s in impl_statements:
	for i in range(2**n):
		table2[s][i]=evaluate(table1,i,s)

for i in range(2**n):
	for j in range(n):
		table_new[i][j]=str(int(table1[variables[j]][i]))
	for j in range(n,n+m):
		table_new[i][j]=str(int(table2[impl_statements[j-n]][i]))


for j in range(n,n+m):
	c=0
	for i in range(2**n):
		if table_new[i][j]!='1':
			break
		c=c+1
	if c==2**n:
		a=impl_index[j-n]
		print statements[a[0]] + " logically entails " + statements[a[1]]
