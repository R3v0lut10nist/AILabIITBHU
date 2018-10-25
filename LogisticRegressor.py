from sys import *
from math import *
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

def sigmoid(z):
	'''
	returns sigmoid value
	'''
	return 1.0/(1+exp(-1*z))

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
				arguements["LOW"].append(eval(li[0]))
				arguements["AGE"].append(eval(li[1]))
				arguements["LWT"].append(eval(li[2]))
				arguements["RACE"].append(eval(li[3]))
				arguements["SMOKE"].append(eval(li[4]))
				arguements["PTL"].append(eval(li[5]))
				arguements["HT"].append(eval(li[6]))
				arguements["UI"].append(eval(li[7]))
				arguements["FTV"].append(eval(li[8]))
	X = [arguements["AGE"],arguements['LWT'],arguements["RACE"],arguements["SMOKE"],arguements["PTL"],arguements["HT"],arguements["UI"],arguements["FTV"]]
	y = arguements["LOW"]
	m = len(y)
	X.append([1 for i in range(m)])
	alpha = 0.0005
	theta = [0,0,0,0,0,0,0,0,0]
	print "Training the data..."
	for i in range(num_of_iters):
		th = [j for j in theta]
		for k in range(9):
			th[k]=theta[k]-(alpha*1.0/m)*sum([( sigmoid(theta[0]*X[0][j] + theta[1]*X[1][j] + theta[2]*X[2][j] + theta[3]*X[3][j] + theta[4]*X[4][j] + theta[5]*X[5][j] + theta[6]*X[6][j] + theta[7]*X[7][j] + theta[8]*X[8][j]) - y[j] )*X[k][j] for j in range(m)])
		theta = [j for j in th]
	pred = [int(sigmoid(theta[0]*X[0][j] + theta[1]*X[1][j] + theta[2]*X[2][j] + theta[3]*X[3][j] + theta[4]*X[4][j] + theta[5]*X[5][j] + theta[6]*X[6][j] + theta[7]*X[7][j] + theta[8]*X[8][j])>=0.5) for j in range(m)]
	print sqrt(-1*sum([y[j]*log(sigmoid(theta[0]*X[0][j] + theta[1]*X[1][j] + theta[2]*X[2][j] + theta[3]*X[3][j] + theta[4]*X[4][j] + theta[5]*X[5][j] + theta[6]*X[6][j] + theta[7]*X[7][j] + theta[8]*X[8][j])) + (1-y[j])*log(1-sigmoid(theta[0]*X[0][j] + theta[1]*X[1][j] + theta[2]*X[2][j] + theta[3]*X[3][j] + theta[4]*X[4][j] + theta[5]*X[5][j] + theta[6]*X[6][j] + theta[7]*X[7][j] + theta[8]*X[8][j])) for j in range(m)])/m)
	model_file = open('theta2.txt','wb')
	model_file.write(str(theta))
	model_file.close()
	print ""
	print theta
	print confusion_matrix(y,pred,labels=[0,1])
	print classification_report(y,pred,labels=[0,1])

def test(a,b,c,d,e,f,g,h):
	theta = eval(open('theta2.txt','rb').readline())
	t = sigmoid(a*theta[0] + b*theta[1] + c*theta[2] + d*theta[3] + e*theta[4] + f*theta[5] + g*theta[6] + h*theta[7] + theta[8])
	if t>=0.5:
		print "Low weight!"
	if t<0.5:
		print "Not Low weight!"
	print t

if argv[1]=="--train":
	train(eval(argv[2]))
if argv[1]=="--test":
	test(eval(argv[2]),eval(argv[3]),eval(argv[4]),eval(argv[5]),eval(argv[6]),eval(argv[7]),eval(argv[8]),eval(argv[9]))
