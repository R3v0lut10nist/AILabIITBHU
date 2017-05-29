from ailab import *

height_pcfg = 0

class PCFG(object):
	def __init__(self):
		self.root={}
	def make_tree(self,node,s):
		if len(s)==0:
			return
		j=1
		sk=''
		while s[j]!=':':
			sk=sk+s[j]
			j+=1
		j+=1
		coun=0
		for k in node.keys():
			if sk in k:
				coun+=1
		if coun>0:
			node[sk+str(coun)]={}
		else:
			node[sk]={}
		l=[]
		if s[j]=="{":
			c=0
			sv=''
			k=j
			while k<len(s):
				if s[k]=="{":
					c+=1
				if s[k]=="}":
					c-=1
				if c<0:
					l.append(sv+'}')
					break
				if c==0 and s[k]==',':
					l.append(sv+'}')
					sv=''
				if c>0:
					sv=sv+s[k]
				k+=1
			if coun==0:
				for sv in l:
					self.make_tree(node[sk],sv)
			else:
				for sv in l:
					self.make_tree(node[sk+str(coun)],sv)
		else:
			k=j
			sv=''
			while s[k]!="}":
				sv=sv+s[k]
				k+=1
			if coun==0:
				node[sk]=sv
			else:
				node[sk+str(coun)]=sv
	def pcfgfy(self,s):
		self.make_tree(self.root,s)

###########################################################################################

class Dependency(object):
	def __init__(self):
		self.root={}

	def reach_level(self,tree,pcfg,level):
		if level==1:
			if type(pcfg)==dict:
				tree[pcfg['#1']]={}
			else:
				tree[pcfg]={}
		else:
			if type(pcfg)==dict:
				for k in pcfg:
					if k!='#1':
						self.reach_level(tree[pcfg['#1']],pcfg[k],level-1)

	def traverse_tree(self,pcfg,height):
		for d in range(1,height+1):
			self.reach_level(self.root,pcfg,d)

	def make_dependency(self,pcfg,height):
		self.traverse_tree(pcfg['ROOT'],height)


#############################################################################

def init_head_null(d):
	for k in d:
		if type(d[k])==dict:
			d[k]['#1']=''
			init_head_null(d[k])

def head(k,tree):
	if tree[k]['#1']=='':
		if k=='S':
			tree[k]['#1']=head('VP',tree[k])
		elif k=='VP':
			for t in tree[k].keys():
				if 'VB' in t:
					tree[k]['#1']=tree[k][t]
		elif k=='NP':
			for t in tree[k].keys():
				if 'N' in t or 'CD' in t:
					if t=='NP':
						tree[k]['#1']=head('NP',tree[k])
					else:
						tree[k]['#1']=tree[k][t]
	return tree[k]['#1']

def find_head(tree):
	for k in tree:
		if type(tree)==dict and type(tree[k])==dict:
			if k=="ROOT" or k=="SBAR":
				tree[k]['#1']=head('S',tree[k])
			elif k=="S":
				tree[k]['#1']=head('VP',tree[k])
			elif k=="NP":
				for t in tree[k].keys():
					if 'N' in t or 'CD' in t:
						if t=='NP':
							tree[k]['#1']=head('NP',tree[k])
						else:
							tree[k]['#1']=tree[k][t]
			elif k=="VP":
				for t in tree[k].keys():
					if 'VB' in t:
						tree[k]['#1']=tree[k][t]
			elif 'PP' in k:
				tree[k]['#1']=head('NP',tree[k])
			find_head(tree[k])


################################################################################

def print_level(tree,level):
	if level==1:
		if type(tree)==dict:
			for k in tree.keys():
				if k!='#1':
					# print k,
					pass
			return "tree"
		else:
			if tree!='#1':
				# print tree,
				pass
			return "tree"
	else:
		if type(tree)==dict:
			s=""
			for k in tree:
				if k!='#1':
					s=s+print_level(tree[k],level-1)
			return s
		else:
			return ""



def print_tree(tree):
	global height_pcfg
	for d in range(1,20):
		a=print_level(tree,d)
		if a!="":
			height_pcfg=d
			# print

##########################################################################

s=''
f=open("output.txt")
for l in f:
	s=s+l.strip()

sv=''
l=len(s)
for i in range(l):
	if s[i]==" " and s[i+1]=="(":
		continue
	sv=sv+s[i]
s=sv
s=s.replace("(","{")
s=s.replace(")","}")
l=len(s)
c=0
for i in range(l):
	if s[i]=="{":
		c+=1
	elif s[i]=="}":
		c-=1
		if c!=0 and s[i+1]!="}":
			s=s[:i+1]+","+s[i+1:]

i=0
while i<l:
	if i!=0 and s[i]=="{" and s[i-1]!="," and s[i-1]!=":":
		s=s[:i]+":"+s[i:]
		l+=1
		i+=1
	i+=1
s=':'.join(s.split(' '))

###################################################################################

pcfg = PCFG()
pcfg.pcfgfy(s)

pcfg_tree=pcfg.root
init_head_null(pcfg_tree)
find_head(pcfg_tree)
print_tree(pcfg_tree)

###################################################################################

def remove_child(tree):
	# print tree
	flag = False
	if type(tree)==dict:
		for k in tree:
			if type(tree[k])==dict and k in tree[k]:
				if len(tree[k])==1:
					tree[k]=tree[k][k]
				else:
					temp_dic={}
					# # print tree[k][k]
					if type(tree[k][k])==dict:
						for s in tree[k][k]:
							temp_dic[s]=tree[k][k][s]
					for k1 in tree[k]:
						# print tree[k], k1
						if k1!=k:
							temp_dic[k1]=tree[k][k1]
					tree[k]=temp_dic
				flag = True
		if flag:
			remove_child(tree)
		for k in tree:
			if type(tree[k])==dict:
				remove_child(tree[k])


def print_deptree(tree,level):
	if type(tree)==dict:
		for k in tree:
			print level*'\t'+k
			print_deptree(tree[k],level+1)
	else:
		if tree!='':
			print level*'\t'+tree

######################################################################################################

dep = Dependency()
dep.make_dependency(pcfg_tree,height_pcfg)
dep_tree = dep.root
# print dep_tree, '\n\n', pcfg_tree

remove_child(dep_tree)

# print dep_tree

for verb in dep_tree:
	for noun in dep_tree[verb]:
		if 'NP' in pcfg_tree['ROOT']['S'] and pcfg_tree['ROOT']['S']['NP']['#1']==noun:
			dep_tree[verb][noun+"(k1)"]=dep_tree[verb][noun]
			dep_tree[verb].pop(noun)
		elif 'NP' in pcfg_tree['ROOT']['S']['VP'] and pcfg_tree['ROOT']['S']['VP']['NP']['#1']==noun:
			dep_tree[verb][noun+"(k2)"]=dep_tree[verb][noun]
			dep_tree[verb].pop(noun)
		else:
			for k in pcfg_tree['ROOT']['S']['VP']:
				if 'PP' in k and pcfg_tree['ROOT']['S']['VP'][k]['#1']==noun:
					if 'TO' in pcfg_tree['ROOT']['S']['VP'][k]:
						dep_tree[verb][noun+"(k4)"]=dep_tree[verb][noun]
						dep_tree[verb].pop(noun)
					elif 'IN' in pcfg_tree['ROOT']['S']['VP'][k]:
						if pcfg_tree['ROOT']['S']['VP'][k]['IN']=="in":
							dep_tree[verb][noun+"(k7p)"]=dep_tree[verb][noun]
							dep_tree[verb].pop(noun)
						elif pcfg_tree['ROOT']['S']['VP'][k]['IN']=="at":
							dep_tree[verb][noun+"(k7t)"]=dep_tree[verb][noun]
							dep_tree[verb].pop(noun)
						elif pcfg_tree['ROOT']['S']['VP'][k]['IN']=="from":
							dep_tree[verb][noun+"(k5)"]=dep_tree[verb][noun]
							dep_tree[verb].pop(noun)
						elif pcfg_tree['ROOT']['S']['VP'][k]['IN']=="with":
							dep_tree[verb][noun+"(k3)"]=dep_tree[verb][noun]
							dep_tree[verb].pop(noun)
						elif pcfg_tree['ROOT']['S']['VP'][k]['IN']=="over":
							dep_tree[verb][noun+"(k2)"]=dep_tree[verb][noun]
							dep_tree[verb].pop(noun)
						elif pcfg_tree['ROOT']['S']['VP'][k]['IN']=="on":
							dep_tree[verb][noun+"(k7p)"]=dep_tree[verb][noun]
							dep_tree[verb].pop(noun)

print 'Dependency tree:\n----------------'
print_deptree(dep_tree,0)
print "_________________________________________________\n\n PCFG Tree:"
print " ---------"

##################################################################################

c=2


def traverse(graph, tree, parent):
	global c
	i=0
	if type(tree)==dict:
		for k in tree:
			if k!='#1':
				temp_node = GraphNode(c,k)
				c+=1
				if type(tree[k])==dict and '#1' in tree[k]:
					temp_node.head = tree[k]['#1']
				graph.add_edge(temp_node, parent)
				traverse(graph, tree[k], c-1)
	else:
		if tree!='#1':
			temp_node = GraphNode(c,tree)
			c+=1
			graph.add_edge(temp_node, parent)

pcfg_graph_root = GraphNode(1,"ROOT")
pcfg_graph_root.head = pcfg_tree['ROOT']['#1']
pcfg_graph = Graph(pcfg_graph_root)
traverse(pcfg_graph, pcfg_tree['ROOT'], 1)

pcfg_graph.print_preorder(1,'')

#################################################################################

c=0
for verb in dep_tree:
	for noun in dep_tree[verb]:
		if 'nn' not in noun:
			c=1
			a=noun+',nn'
			dep_tree[verb][a]=dep_tree[verb][noun]
			dep_tree[verb].pop(noun)
			noun=a
			for adj in dep_tree[verb][noun]:
				for ch in pcfg_tree['ROOT']['S']['VP']['NP']['NP']:
					if 'JJ' in ch and pcfg_tree['ROOT']['S']['VP']['NP']['NP'][ch]==adj:
						a=adj+',adj'
						dep_tree[verb][noun][a]=dep_tree[verb][noun][adj]
						dep_tree[verb][noun].pop(adj)
			if 'PP' in pcfg_tree['ROOT']['S']['VP']['NP']:
				for noun2 in dep_tree[verb][noun]:
					# for ch in pcfg_tree['ROOT']['S']['VP']['NP']['PP']:
					try:
						if pcfg_tree['ROOT']['S']['VP']['NP']['PP']['NP']['NN']==noun2:
							c=2
							if 'IN' in pcfg_tree['ROOT']['S']['VP']['NP']['PP']:
								a=noun2+'('+pcfg_tree['ROOT']['S']['VP']['NP']['PP']['IN']+'),nn'
								dep_tree[verb][noun][a]=dep_tree[verb][noun][noun2]
								dep_tree[verb][noun].pop(noun2)
							elif 'TO' in pcfg_tree['ROOT']['S']['VP']['NP']['PP']:
								a=noun2+'('+pcfg_tree['ROOT']['S']['VP']['NP']['PP']['TO']+'),nn'
								dep_tree[verb][noun][a]=dep_tree[verb][noun][noun2]
								dep_tree[verb][noun].pop(noun2)
							noun2=a
							for adj in dep_tree[verb][noun][noun2]:
								for ch in pcfg_tree['ROOT']['S']['VP']['NP']['PP']['NP']:
									if 'JJ' in ch and pcfg_tree['ROOT']['S']['VP']['NP']['PP']['NP'][ch]==adj:
										a=adj+',adj'
										dep_tree[verb][noun][noun2][a]=dep_tree[verb][noun][noun2][adj]
										dep_tree[verb][noun][noun2].pop(adj)
					except:
						if pcfg_tree['ROOT']['S']['VP']['NP']['PP']['NP']['NP']['NN']==noun2:
							c=2
							if 'IN' in pcfg_tree['ROOT']['S']['VP']['NP']['PP']:
								a=noun2+'('+pcfg_tree['ROOT']['S']['VP']['NP']['PP']['IN']+'),nn'
								dep_tree[verb][noun][a]=dep_tree[verb][noun][noun2]
								dep_tree[verb][noun].pop(noun2)
							elif 'TO' in pcfg_tree['ROOT']['S']['VP']['NP']['PP']:
								a=noun2+'('+pcfg_tree['ROOT']['S']['VP']['NP']['PP']['TO']+'),nn'
								dep_tree[verb][noun][a]=dep_tree[verb][noun][noun2]
								dep_tree[verb][noun].pop(noun2)
							noun2=a
							for adj in dep_tree[verb][noun][noun2]:
								for ch in pcfg_tree['ROOT']['S']['VP']['NP']['PP']['NP']:
									if 'JJ' in ch and pcfg_tree['ROOT']['S']['VP']['NP']['PP']['NP'][ch]==adj:
										a=adj+',adj'
										dep_tree[verb][noun][noun2][a]=dep_tree[verb][noun][noun2][adj]
										dep_tree[verb][noun][noun2].pop(adj)
						for noun3 in dep_tree[verb][noun][noun2]:
							if pcfg_tree['ROOT']['S']['VP']['NP']['PP']['NP']['PP']['NP']['NN']==noun3:
								c=3
								if 'IN' in pcfg_tree['ROOT']['S']['VP']['NP']['PP']['NP']['PP']:
									a=noun3+'('+pcfg_tree['ROOT']['S']['VP']['NP']['PP']['NP']['PP']['IN']+'),nn'
									dep_tree[verb][noun][noun2][a]=dep_tree[verb][noun][noun2][noun3]
									dep_tree[verb][noun][noun2].pop(noun3)
								elif 'TO' in pcfg_tree['ROOT']['S']['VP']['NP']['PP']['NP']['NP']['PP']:
									a=noun3+'('+pcfg_tree['ROOT']['S']['VP']['NP']['PP']['NP']['NP']['PP']['TO']+'),nn'
									dep_tree[verb][noun][noun2][a]=dep_tree[verb][noun][noun2][noun3]
									dep_tree[verb][noun][noun2].pop(noun3)
								noun3=a
								for adj in dep_tree[verb][noun][noun2][noun3]:
									for ch in pcfg_tree['ROOT']['S']['VP']['NP']['PP']['NP']['PP']['NP']:
										if 'JJ' in ch and pcfg_tree['ROOT']['S']['VP']['NP']['PP']['NP']['PP']['NP'][ch]==adj:
											a=adj+',adj'
											dep_tree[verb][noun][noun2][noun3][a]=dep_tree[verb][noun][noun2][noun3][adj]
											dep_tree[verb][noun][noun2][noun3].pop(adj)


print "_________________________________________________\n"
print_deptree(dep_tree,0)
print "\n"

if c==1:
	print "x, (",
if c==2:
	print "x, y, (",
if c==3:
	print "x, y, z, (",
for verb in dep_tree:
	for noun in dep_tree[verb]:
		if 'nn' in noun:
			for adj in dep_tree[verb][noun]:
				if 'adj' in adj:
					print "color( x,",adj[:-4],") ^",
			for noun2 in dep_tree[verb][noun]:
				if 'nn' in noun2:
					for adj in dep_tree[verb][noun][noun2]:
						if 'adj' in adj:
							print "color( y,",adj[:-4],") ^",
					for noun3 in dep_tree[verb][noun][noun2]:
						if 'nn' in noun3:
							for adj in dep_tree[verb][noun][noun2][noun3]:
								if 'adj' in adj:
									print "color( z,",adj[:-4],") ^",
							c=''
							for ch in noun3:
								if ch!='(':
									c=c+ch
								else:
									break
							print "shape( z,",c,") ^",
							l=len(c)
							c=''
							for ch in noun3[l+1:]:
								if ch!=')':
									c=c+ch
								else:
									break
							print c+"( y, z ) ^",
					c=''
					for ch in noun2:
						if ch!='(':
							c=c+ch
						else:
							break
					print "shape( y,",c,") ^",
					l=len(c)
					c=''
					for ch in noun2[l+1:]:
						if ch!=')':
							c=c+ch
						else:
							break
					print c+"( x, y ) ^",
			c=''
			for ch in noun:
				if ch!='(':
					c=c+ch
				else:
					break
			print "shape( x,",c,")",

print ")"
