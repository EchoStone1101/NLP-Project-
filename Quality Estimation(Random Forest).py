#Phase 4
#Estimated phrasal quality based on attributes and train set(via random forest)
import os
import json
import random
import math

random.seed(19260817)
FeedBack = True


def log(x):
	if(x <= 0):
		return 0
	return math.log(x)

Labeled = {}
Attributes = ['PMI','PKL','IDF']
if(FeedBack):
	Attributes = Attributes + ['SPMI','SPKL']

with open("Labeled.json","r") as f_obj:
	Labeled = json.load(f_obj)
	f_obj.close()

with open("Att.json","r") as f_obj:
	Att = json.load(f_obj)
	f_obj.close()

p1 = sum([Labeled[u] for u in Labeled])/len(Labeled)
p0 = 1-p1
Ent = -p0*log(p0) -p1*log(p1)

def GainGini(Index,A):
	temp = [(Att[u][A],Labeled[u],u) for u in Index]
	sort = sorted(temp,key = lambda d:d[0])
	Gain = []
	for i in range(1,len(sort)):
		left_p1 = sum([w[1] for w in sort[:i]])/i
		left_p0 = 1-left_p1
		right_p1 = sum([w[1] for w in sort[i:]])/(len(sort)-i)
		right_p0 = 1-right_p1
		Gain.append(Ent + i/len(sort)*(left_p0*log(left_p0)+left_p1*log(left_p1)) + (len(sort)-i)/len(sort)*(right_p0*log(right_p0)+right_p1*log(right_p1)))
	maximum = max(Gain)
	max_i = Gain.index(maximum)
	return((maximum,[x[2] for x in sort[:max_i+1]],[x[2] for x in sort[max_i+1:]],(sort[max_i][0]+sort[max_i+1][0])/2))

	
#1 CART Tree (m=2)

class CARTtreeNode:
	def __init__(self,data,left = None,right = None):
		self.data = data
		self.left = left
		self.right = right

	def GrowCARTtree(self,Index,A1,A2,error):
		CurGini = GainGini(Index,A1)
		self.data = CurGini[3]

		lnode = CARTtreeNode(0)
		self.left = lnode
		lAns = sum([Labeled[u] for u in CurGini[1]])/len(CurGini[1])
		est = 0
		for u in CurGini[1]:
			est = est + (Labeled[u]-lAns)**2
		est = est/len(CurGini[1])
		#print("L",lAns,est)
		if(est <= error):
			self.left.data = lAns
		else:
			self.left.GrowCARTtree(CurGini[1],A2,A1,error)

		rnode = CARTtreeNode(0)
		self.right = rnode
		rAns = sum([Labeled[u] for u in CurGini[2]])/len(CurGini[2])
		est = 0
		for u in CurGini[2]:
			est = est + (Labeled[u]-rAns)**2
		est = est/len(CurGini[2])
		#print("R",rAns,est)
		if(est <= error):
			self.right.data = rAns
		else:
			self.right.GrowCARTtree(CurGini[2],A2,A1,error)

class CARTtree:
	def __init__(self,A = []):
		node = CARTtreeNode(0)
		self.root = node
		self.A = A

	def Vote(self,A):
		cur = self.root
		count = 0
		while(cur.left != None and cur.right != None):
			if(A[count] <= cur.data):
				cur = cur.left
			else:
				cur = cur.right
			count = count^1
		return cur.data

#2 Random Forest

key = list(Labeled.keys())

def RandomSample(M):
	sample = []
	while(len(sample) < M):
		word = key[random.randint(0,len(key)-1)]
		sample.append(word)
			
	return sample


TreeCount = 128
T = []

if(FeedBack):
	ERR = 0.213
	while(len(T)<TreeCount):
		CHOICE = random.sample(range(0,len(Attributes)),2)
		A1 = Attributes[CHOICE[0]]
		A2 = Attributes[CHOICE[1]]
		if(A1 in ['SPMI','SPKL'] or A2 in ['SPMI','SPKL']):
			sample = RandomSample(len(key))
			if(GainGini(sample,A1)[0] > GainGini(sample,A2)[0]):
				T.append(CARTtree([A1,A2]))
				T[-1].root.GrowCARTtree(sample,A1,A2,ERR)
			else:
				T.append(CARTtree([A2,A1]))
				T[-1].root.GrowCARTtree(sample,A2,A1,ERR)
			print(len(T))
else:
	ERR = 0.21125
	while(len(T)<TreeCount):
		CHOICE = random.sample(range(0,len(Attributes)),2)
		A1 = Attributes[CHOICE[0]]
		A2 = Attributes[CHOICE[1]]
		sample = RandomSample(len(key))
		if(GainGini(sample,A1)[0] > GainGini(sample,A2)[0]):
			T.append(CARTtree([A1,A2]))
			T[-1].root.GrowCARTtree(sample,A1,A2,ERR)
		else:
			T.append(CARTtree([A2,A1]))
			T[-1].root.GrowCARTtree(sample,A2,A1,ERR)
		print(len(T))

print("Voting!")
Quality = {}

for WORD in Att:
	if(len(WORD) == 1):
		Quality[WORD] = 1
	else:
		ANS = 0
		for i in range(0,TreeCount):
			ANS = ANS + T[i].Vote([Att[WORD][T[i].A[0]],Att[WORD][T[i].A[1]]])
		Quality[WORD] = ANS/TreeCount

with open("Quality.json","w") as f_obj:
	json.dump(Quality,f_obj,indent = 4)
	f_obj.close()

