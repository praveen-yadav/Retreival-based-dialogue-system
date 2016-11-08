from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from collections import Counter
import re, math

WORD = re.compile(r'\w+')
def text_to_vector(text):
     text=text.lower()
     words = WORD.findall(text)
   
     return Counter(words)

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def getData(fname,c):
	global systemList
	global userList
	global testData	
	fh=open(fname,'r')
	count=0
	
	
	tempList=[]
		
	for line in fh:
		line=line.strip()
							
		temp=line.strip().split(':')
		if count<=c:		
			if len(temp)>1:
				temp=line[9:]	
				if line.startswith("System"):
					systemList.append(temp)
				else:
					userList.append(temp)
		else:		
			temp=line[9:]
			if line.startswith("----"):
				if len(tempList)>2:				
					testData.append(tempList)
				tempList=[]
			else:
				tempList.append(temp)
		if line.startswith("----"):
			count=count+1
					
#fnames=["DSTC1.txt","DSTC2.txt","DSTC3.txt"]
fnames = ["DSTC3.txt"]
systemList=[]
userList=[]
testData=[]

c=[2200]
#c=[900,2000,2200]
for i in range(len(fnames)):
	getData(fnames[i],c[i])
systemList = set(systemList)
userList = set(userList)
count = 0
for sys in systemList:
	print sys
	count += 1
	if count == 5:
		break
print len(systemList),len(userList)

user_text = "I want to eat chinese";
vector1 = text_to_vector(user_text)
print vector1
maxcosine = -2
sent = ""
for sent2 in userList:
	vector2 = text_to_vector(sent2)
	cosine = get_cosine(vector1, vector2)
	if cosine > maxcosine:
		maxcosine = cosine
		sent = sent2
print sent

exit()



vectorizer_system = CountVectorizer(analyzer = "word", tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000)
vec_system=vectorizer_system.fit(systemList)
vectorized_system=vec_system.transform(systemList)
print vectorized_system[1]



	


vectorizer_user = CountVectorizer(analyzer = "word", tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000)
vec_user=vectorizer_user.fit(userList)
vectorized_user=vec_user.transform(userList)

km_system = KMeans(n_clusters=10, init='k-means++', max_iter=100, n_init=1)
km_system.fit(vectorized_system)

km_user = KMeans(n_clusters=10, init='k-means++', max_iter=100, n_init=1)
km_user.fit(vectorized_user)

#labels = km.predict(train_data_features)
#print len(labels)

for i in range(len(testData)):
	print "\n\n******************************"
	curList=testData[i]
	curList=curList[1:-1]
	userConv=curList[1::2]
	systemConv=curList[0: :2]

	print systemConv
	print
	print userConv
	print 

	#test_data_features = vec.transform(curList)
	#labels = km.predict(test_data_features)
	system_features=vec_system.transform(systemConv)
	system_labels=km_system.predict(system_features)
	print system_labels
	
	user_features=vec_user.transform(userConv)
	user_labels=km_user.predict(user_features)
	print user_labels
	j=0
	k=0
	while j<len(system_labels) and k<len(user_labels):
		print system_labels[j],user_labels[k],
		j=j+1
		k=k+1
	if j<len(system_labels):
	 	print system_labels[j],
	print 
	
	
	
