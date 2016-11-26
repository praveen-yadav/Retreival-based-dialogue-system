from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from collections import Counter
import re, math
from difflib import SequenceMatcher

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


def remove(fname, c):
	global systemSet
	global systemSet1
	fh=open(fname,'r')
	count=0
	systemSet1 = set()
	
	tempList=[]	
	cnt =0
	prev=""
	prevprev=""
	for line in fh:
		line=line.strip()						
		temp=line.strip().split(':')
		cnt+=1
		if cnt%1000==0:
			print cnt, len(systemSet)
		if count<=c or 1:		
			if len(temp)>1:
				temp=line[9:]	
				similar=[]			
				if line.startswith("System"):
					#systemList.append(temp)
					vector1 = text_to_vector(temp)
					#print vector1
					maxcosine = -2
					sent = ""
					#print temp
					for sent2 in systemSet:
						vector2 = text_to_vector(sent2)
						cosine = get_cosine(vector1, vector2)
						#print cosine
						if cosine > 0.92 and cosine<1:
							#print sent2, cosine
							similar.append(sent2)
				
						if cosine > maxcosine:
							maxcosine = cosine
							sent = sent2
				#	print sent
					
					if maxcosine==1:
						for word in similar:
							systemSet.remove(word)
				
		if line.startswith("----"):
			count=count+1
			continue
	




def getData(fname,c):
	global systemList
	global userList
	global testData	
	global trigram_SUS
	global trigram_dict
	global bigram_dict
	fh=open(fname,'r')
	count=0
	
	
	tempList=[]	
	cnt =0
	prev=""
	prevprev=""
	for line in fh:
		line=line.strip()						
		temp=line.strip().split(':')

		if count<=c or 1:		
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
			continue
	
		cnt +=1
		if len(temp)==0:
			continue
		temp = str(temp)
		if cnt==1:
			prevprev = temp
		elif cnt==2:
			prev = str(temp)
			tempbidict = {}
			tempbidict[prev] = 1
			bigram_dict[prevprev] = tempbidict
				
		else:
			if prev in bigram_dict:
				tempbidict = bigram_dict[prev]
				if temp in tempbidict:
					tempbidict[temp] +=1
					bigram_dict[prev] = tempdict
				else:
					tempbidict[temp] = 1
					bigram_dict[prev] = tempdict
			else:
				tempdict={}
				tempdict[temp] = 1
				bigram_dict[prev] = tempdict
			

			key = prevprev+"|"+prev
			if key in trigram_dict:
				tempdict = trigram_dict[key]
				if temp in tempdict:
					tempdict[temp] +=1
					trigram_dict[key] = tempdict
				else:
					tempdict[temp] = 1
					trigram_dict[key] = tempdict
			else:
				tempdict={}
				tempdict[temp] = 1
				trigram_dict[key] = tempdict
					
			prevprev=prev
			prev = temp
					
		


	
	
					
#fnames=["DSTC1.txt","DSTC2.txt","DSTC3.txt"]
fnames = ["DSTC3.txt"]
systemList=[]
userList=[]
testData=[]
trigram_dict = {}
bigram_dict = {}

c=[2200]
#c=[900,2000,2200]
for i in range(len(fnames)):
	getData(fnames[i],c[i])
systemList = set(systemList)
#remove(fnames[0],c[0])

userList = set(userList)
print len(systemList)

# for sys in systemList:
# 	print sys

# print "customer:\n"
# for sys in userList:
# 	print sys	

# print len(systemList),len(userList)
prevprev = "Thank you for calling the Cambridge Information system. Your call will be recorded for research purposes. You may ask for information about a place to eat, such as a restaurant, a pub, or a cafe. How may I help you?"
print prevprev
while 1:
	user_text = raw_input("User : ")
#user_text = "im looking for a moderately priced restaurant in the girton area";
	vector1 = text_to_vector(prevprev)
	

	sysoptions=[]
	maxcosine = -2
	sent = ""
	for sent2 in systemList:
		vector2 = text_to_vector(sent2)
		cosine = get_cosine(vector1, vector2)
		#print cosine
#		cosine = SequenceMatcher(None, user_text, sent2).ratio()
		if cosine > 0:
#			print sent2, cosine
			sysoptions.append((sent2,cosine))
		if cosine > maxcosine:
			maxcosine = cosine
			sent = sent2
	sysoptions = sorted(sysoptions, key=lambda x:x[1], reverse=1)
#	print sysoptions[0]
	reply=""
	for prevprev,val1 in sysoptions:
	#	print "PREV - ", prevprev
		

		#print vector1
		vector1 = text_to_vector(user_text)
		maxcosine = -2
		sent = ""
		options=[]	
		for sent2 in userList:
			vector2 = text_to_vector(sent2)
			cosine = get_cosine(vector1, vector2)
			#print cosine
#			cosine = SequenceMatcher(None, user_text, sent2).ratio()
			if cosine > 0:
#				print sent2, cosine
				options.append((sent2,cosine))
			if cosine > maxcosine:
				maxcosine = cosine
				sent = sent2
	#	print sent
	
		prev = sent
		if prev.startswith("goodbye"):
			exit()
#		print trigram_dict[prevprev+'|'+prev]
		#print len(trigram_dict)
		freq = 0
		reply=""
		key = prevprev+'|'+prev
		if key in trigram_dict: 
			for i in trigram_dict[prevprev+'|'+prev].keys():
				if trigram_dict[prevprev+'|'+prev][i] > freq:
					freq = trigram_dict[prevprev+'|'+prev][i]
					reply = i
		else:
			options = sorted(options, key=lambda x:x[1], reverse=1)
	#		print options[0]
			for (i,j) in options:
				key = prevprev+'|'+i
				if key in trigram_dict:
					break
			if key in trigram_dict: 
				for i in trigram_dict[key].keys():
					if trigram_dict[key][i] > freq:
						freq = trigram_dict[key][i]
						reply = i
	
		if len(reply)>1:
			break
	#	for i in bigram_dict[prev].keys():
	#		if bigram_dict[prev][i] > freq:
	#			freq = bigram_dict[prev][i]
	#			reply = i
	#	print "BIGRAM"

	#print prevprev
	print reply
	prevprev=reply
#	prev=reply
exit()



# vectorizer_system = CountVectorizer(analyzer = "word", tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000)
# vec_system=vectorizer_system.fit(systemList)
# vectorized_system=vec_system.transform(systemList)
# print vectorized_system[1]



	


# vectorizer_user = CountVectorizer(analyzer = "word", tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000)
# vec_user=vectorizer_user.fit(userList)
# vectorized_user=vec_user.transform(userList)

# km_system = KMeans(n_clusters=10, init='k-means++', max_iter=100, n_init=1)
# km_system.fit(vectorized_system)

# km_user = KMeans(n_clusters=10, init='k-means++', max_iter=100, n_init=1)
# km_user.fit(vectorized_user)

# #labels = km.predict(train_data_features)
# #print len(labels)

# for i in range(len(testData)):
# 	print "\n\n******************************"
# 	curList=testData[i]
# 	curList=curList[1:-1]
# 	userConv=curList[1::2]
# 	systemConv=curList[0: :2]

# 	print systemConv
# 	print
# 	print userConv
# 	print 

# 	#test_data_features = vec.transform(curList)
# 	#labels = km.predict(test_data_features)
# 	system_features=vec_system.transform(systemConv)
# 	system_labels=km_system.predict(system_features)
# 	print system_labels
	
# 	user_features=vec_user.transform(userConv)
# 	user_labels=km_user.predict(user_features)
# 	print user_labels
# 	j=0
# 	k=0
# 	while j<len(system_labels) and k<len(user_labels):
# 		print system_labels[j],user_labels[k],
# 		j=j+1
# 		k=k+1
# 	if j<len(system_labels):
# 	 	print system_labels[j],
# 	print 

