from sys import *
from math import *

def train(num_of_iters):
	arguements = {}
	training_database = open('lowbwt.arff','r')
	lines = training_database.readlines()
	print "Reading training data..."
	for line in lines:
		if line[0]!='%' and line[0]!='\n':
			if line[0]=='@':
				li = line.split(" ")
				if li[0]=="@attribute":
					arguements[li[1]]=[]
			else:
				li=line.split(",")
				arguements["AGE"].append(eval(li[1]))
				arguements["LWT"].append(eval(li[2]))
				arguements["RACE"].append(eval(li[3]))
				arguements["SMOKE"].append(eval(li[4]))
				arguements["PTL"].append(eval(li[5]))
				arguements["HT"].append(eval(li[6]))
				arguements["UI"].append(eval(li[7]))
				arguements["FTV"].append(eval(li[8]))
				arguements["class"].append(eval(li[9].strip()))
	X = [arguements["AGE"],arguements['LWT'],arguements["RACE"],arguements["SMOKE"],arguements["PTL"],arguements["HT"],arguements["UI"],arguements["FTV"]]
	y = arguements["class"]
	m = len(y)
	X.append([1 for i in range(m)])
	alpha = 0.000001
	theta = [0,0,0,0,0,0,0,0,0]
	print "Training the data..."
	for i in range(num_of_iters):
		th = [j for j in theta]
		for k in range(9):
			th[k]=theta[k]-(alpha*1.0/m)*sum([(theta[0]*X[0][j] + theta[1]*X[1][j] + theta[2]*X[2][j] + theta[3]*X[3][j] - y[j])*X[k][j] for j in range(m)])
		theta = [j for j in th]
	print sqrt(sum([(theta[0]*X[0][j] + theta[1]*X[1][j] + theta[2]*X[2][j] + theta[3]*X[3][j] + theta[4]*X[4][j] + theta[5]*X[5][j] + theta[6]*X[6][j] + theta[7]*X[7][j] + theta[8]*X[8][j] - y[j])**2 for j in range(m)])/(2*m))
	model_file = open('theta.txt','wb')
	model_file.write(str(theta))
	model_file.close()
	print ""
	print theta

def test(a,b,c,d,e,f,g,h):
	theta = eval(open('theta.txt','rb').readline())
	print a*theta[0] + b*theta[1] + c*theta[2] + d*theta[3] + e*theta[4] + f*theta[5] + g*theta[6] + h*theta[7] + theta[8]

if argv[1]=="--train":
	train(eval(argv[2]))
if argv[1]=="--test":
	test(eval(argv[2]),eval(argv[3]),eval(argv[4]),eval(argv[5]),eval(argv[6]),eval(argv[7]),eval(argv[8]),eval(argv[9]))
