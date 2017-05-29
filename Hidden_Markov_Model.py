import sys

def train():
	training_database_file = open(sys.argv[2],'rb')
	words = []
	tags = []

	print "Finding unique words and tags..."
	for line in training_database_file.readlines():
		l = line.split('\t')
		if l[0]!='\n':
			if l[0] not in words:
				words.append(l[0])
			if l[1][:-1] not in tags:
				tags.append(l[1][:-1])

	print "Making dictionary of words..."
	dict_words = {}
	i = 0
	for word in words:
		dict_words[word]=i
		i+=1

	dict_tags = {}
	i=0
	for tag in tags:
		dict_tags[tag]=i
		i+=1

	print "Setting up pi, A and B..."
	pi = [0 for i in range(len(tags))]
	A = [[0 for i in range(len(tags))] for i in range(len(tags))]
	B = [[0 for i in range(len(tags))] for i in range(len(words))]
	tag_count = [0 for i in range(len(tags))]

	training_database_file.close()
	training_database_file = open(sys.argv[2],'rb')
	flag = 1
	number_of_sentences = 0
	prev_tag = ''

	print "Modelling..."
	print "Finding counts..."
	for line in training_database_file.readlines():
		l = line.split('\t')
		if l[0]!='\n':
			if flag:
				pi[dict_tags[l[1][:-1]]]+=1
				B[dict_words[l[0]]][dict_tags[l[1][:-1]]]+=1
				tag_count[dict_tags[l[1][:-1]]]+=1
				prev_tag = l[1][:-1]
				number_of_sentences+=1
				flag = 0
			else:
				A[dict_tags[l[1][:-1]]][dict_tags[prev_tag]]+=1
				B[dict_words[l[0]]][dict_tags[l[1][:-1]]]+=1
				tag_count[dict_tags[l[1][:-1]]]+=1
				prev_tag = l[1][:-1]
		else:
			flag = 1

	print "Finalizing matrix..."

	for i in range(len(pi)):
		pi[i]=pi[i]*1.0/number_of_sentences

	for i in range(len(tags)):
		for j in range(len(tags)):
			A[i][j]=A[i][j]*1.0/tag_count[j]

	for i in range(len(words)):
		for j in range(len(tags)):
			B[i][j]=B[i][j]*1.0/tag_count[j]

	training_database_file.close()

	print "Writing learned model..."
	final_model_pi = open("pi.txt",'wb')
	final_model_pi.write(str(pi))
	final_model_pi.close()

	final_model_A = open("A.txt",'wb')
	final_model_A.write(str(A))
	final_model_A.close()

	final_model_B = open("B.txt",'wb')
	final_model_B.write(str(B))
	final_model_B.close()

	final_model_words = open("words.txt",'wb')
	for word in words:
		final_model_words.write(word+"\n")
	final_model_words.close()

	final_model_tags = open("tags.txt","wb")
	for tag in tags:
		final_model_tags.write(tag+"\n")
	final_model_tags.close()

def test():
	testing_file = open(sys.argv[2], 'rb')
	test_data = []

	print "Reading test data..."
	sentence=[]

	for line in testing_file.readlines():
		if line!='\n':
			sentence.append(line[:-1])
		else:
			test_data.append(sentence)
			sentence=[]
	if sentence:
		test_data.append(sentence)
	testing_file.close()

	words = []
	tags = []

	print "Finding unique words and tags..."
	word_data = open("words.txt","rb")
	tag_data = open("tags.txt","rb")
	for line in word_data.readlines():
		if line not in words:
			words.append(line[:-1])

	for line in tag_data.readlines():
		if line not in tags:
			tags.append(line[:-1])
	word_data.close()
	tag_data.close()

	print "Making dictionary of words..."
	dict_words = {}
	i = 0
	for word in words:
		dict_words[word]=i
		i+=1

	dict_tags = {}
	i=0
	for tag in tags:
		dict_tags[tag]=i
		i+=1

	print "using models..."
	pi = eval(open("pi.txt","rb").readline())
	A = eval(open("A.txt","rb").readline())
	B = eval(open("B.txt","rb").readline())

	print "Running Viterbi..."
	prediction = open(sys.argv[3],"wb")
	T1 = [[0 for i in range(len(words))] for j  in range(len(tags))]
	T2 = [[0 for i in range(len(words))] for j  in range(len(tags))]

	for y in test_data:
		for tag in tags:
			T1[dict_tags[tag]][dict_words[y[0]]]=pi[dict_tags[tag]]*B[dict_words[y[0]]][dict_tags[tag]]
			T2[dict_tags[tag]][dict_words[y[0]]]=0
		i=1

		while i<len(y):
			for tag in tags:
				T1[dict_tags[tag]][dict_words[y[i]]]=B[dict_words[y[i]]][dict_tags[tag]]*max([T1[dict_tags[tag_iters]][dict_words[y[i-1]]]*A[dict_tags[tag]][dict_tags[tag_iters]] for tag_iters in tags])
				T2[dict_tags[tag]][dict_words[y[i]]]=[T1[dict_tags[tag_iters]][dict_words[y[i-1]]]*A[dict_tags[tag]][dict_tags[tag_iters]] for tag_iters in tags].index(max([T1[dict_tags[tag_iters]][dict_words[y[i-1]]]*A[dict_tags[tag]][dict_tags[tag_iters]] for tag_iters in tags]))
			i+=1

		z=[T1[dict_tags[tag_iters]][dict_words[y[i-1]]] for tag_iters in tags].index(max([T1[dict_tags[tag_iters]][dict_words[y[i-1]]] for tag_iters in tags]))
		x=[tags[z]]

		i=len(y)-1
		while i>0:
			z=T2[z][dict_words[y[i]]]
			x.append(tags[z])
			i-=1
		x.reverse()

		for i in range(len(y)):
			prediction.write(y[i]+"\t"+x[i]+"\n")
		prediction.write("\n")
	prediction.close()


inp = sys.argv[1]
if inp=="--train":
	train()
if inp=="--test":
	test()

