import sys
tra = open('cleanedTrain.txt', 'r')
t = open('cleanedCV.txt','r')
p = open('predCV.txt', 'r')
tr = []
pred = []
labels = []
for line in tra:
	if not line.startswith('#'):
		l = line.split('\t')
		if(l[0]!='\n' and (l[1][:-1] not in labels)):
			labels.append(l[1][:-1])

for line in t:
	if not line.startswith('#'):
		l = line.split('\t')
		if(l[0]!='\n'):
			tr.append(l[1][:-1])


for line in p:
	if not line.startswith('#'):
		l = line.split('\t')
		if(l[0]!='\n'):
			pred.append(l[1])

from sklearn.metrics import accuracy_score
print "Accuracy is: "+str(accuracy_score(tr, pred))

from sklearn.metrics import confusion_matrix
ans1 = confusion_matrix(tr, pred, labels=labels)

from sklearn.metrics import classification_report

for i in range(len(labels)):
	print str(labels[i])+": "+str(ans1[i])

print classification_report(tr, pred, target_names=labels)
tra.close()
t.close()
p.close()
