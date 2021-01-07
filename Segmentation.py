#Phase 5
#Segment the corpus and calculate feedback attributes
import os
import json
import math

with open("RawF.json","r") as f_obj:
	RawF = json.load(f_obj)
	f_obj.close()

with open("Quality.json","r") as f_obj:
	DicQ = json.load(f_obj)
	f_obj.close()

with open("DocCorpus.json","r") as f_obj:
	Corpus = json.load(f_obj)
	f_obj.close()

with open("Labeled.json","r") as f_obj:
	Labeled = json.load(f_obj)
	f_obj.close()

with open("Att.json","r") as f_obj:
	Att = json.load(f_obj)
	f_obj.close()

def log(x):
	if(x >= 0):
		return math.log(x)
	else:
		return 0


DicNormF = {}
MAX_LEN = 10
LEN_COUNT = [0 for i in range(0,MAX_LEN+1)]
for u in RawF:
	LEN_COUNT[len(u)] = LEN_COUNT[len(u)]+RawF[u]
for u in RawF:
	DicNormF[u] = RawF[u]/LEN_COUNT[len(u)]

def NormF(word):
	if(word in DicNormF):
		return DicNormF[word]
	else:
		return 0

def Q(word):
	if(word in DicQ):
		return DicQ[word]
	else:
		return 0


#Dynamic Programming
def DP(C,len_penalty,Div = False):
	n = len(C)
	H = [0 for i in range(0,n+1)]
	Bool = [False for i in range(0,n+1)]
	Bool[0] = True
	G = [0 for i in range(0,n+1)]

	for i in range(0,n):
		if(Bool[i] == False):
			continue
		word = ''
		flag = False
		if(Div):
			index = range(1,min(n,MAX_LEN+1))
		else:
			index = range(1,MAX_LEN+1)
		for d in index:
			if(i+d > n):
				break
			word = word + C[i+d-1]
			if(NormF(word) > 0 and (Bool[i+d] == False or (H[i] + log((len_penalty**(1-d)) * NormF(word) * Q(word))) > H[i+d])):
				#print(i,d,word)
				H[i+d] = H[i] + log(len_penalty**(1-d) * NormF(word) * Q(word))
				G[i+d] = i
				Bool[i+d] = True
				flag = True
	i = n
	m = 0
	Seg = []
	#print(G)
	while(i>0):
		phrase = ""
		if(G[i] < 0):
			G[i] = 0
		for j in range(G[i],i):
			phrase = phrase + C[j]
		Seg.append(phrase)
		#print(G[i],i)
		i = G[i]
	#print(Seg)
	Seg.reverse()
	return (Seg,H[n])

#Viterbi Training

def VT(C,len_penalty):
	converge = False
	S = [[] for d in range(0,len(C))]
	_S = [[] for d in range(0,len(C))]
	count = 0
	while(not converge):
		_DicNormF = {}
		count = count + 1
		print(count)
		converge = True
		for d in range(0,len(C)):
			S[d] = DP(C[d],len_penalty)[0]
			if(d % 100 == 0):
				print(count,d)
			if(S[d] != _S[d]):
				converge = False;
			for word in S[d]:
				if(word in _DicNormF):
					_DicNormF[word] = _DicNormF[word] + 1
				else:
					_DicNormF[word] = 1
		_S = S
		SLEN_COUNT = [0 for i in range(0,MAX_LEN+1)]
		for d in range(0,len(C)):
			for s in S[d]:
				SLEN_COUNT[len(s)] = SLEN_COUNT[len(s)]+1
		for u in _DicNormF:
			_DicNormF[u] = _DicNormF[u]/SLEN_COUNT[len(u)]
		for u in DicNormF:
			if(u in _DicNormF):
				DicNormF[u] = _DicNormF[u]
			else:
				DicNormF[u] = 0
				


#Penalty Learning
def PL(C,r0):
	up = 2
	low = 0
	convergeTarget = 2
	while(up - low >= convergeTarget):
		len_penalty = (up+low)/2
		VT(C,len_penalty)
		r = r0 * len(Labeled)/2
		count = 0
		for u in Labeled:
			if(Labeled[u]):
				S = DP(u,len_penalty)[0]
				if(len(S) == 1):
					r = r-1
					count = count + 1
		print(len_penalty,(r0 * len(Labeled)/2 - r)/len(Labeled)*2,count)
		if(r>=0):
			up = len_penalty
		else:
			low = len_penalty
	return len_penalty


'''
len_penalty = PL(Corpus[:1001],0.90)
print(len_penalty)
'''

len_penalty = 15
VT(Corpus,len_penalty)

with open("NormRectF.json","w") as f_obj:
	_DicNormF = {}
	for u in DicNormF:
		if(DicNormF[u] > 0):
			_DicNormF[u] = DicNormF[u]
	json.dump(_DicNormF,f_obj)
	print("DicLen:",len(_DicNormF))
	f_obj.close()


_Labeled = {}
for l in Labeled:
	if((Labeled[l] == 1 and DicNormF[l]>0) or Labeled[l] == 0):
		_Labeled[l] = Labeled[l]

with open("Labeled.json","w") as f_obj:
	Labeled = json.dump(_Labeled,f_obj,indent = 4)
	print("LabelLen:",len(_Labeled))
	f_obj.close()

for u in Att:
	if(len(u)>1 and DicNormF[u]>0):
		Att[u]['SPMI'] = log((NormF(u) * Q(u) *(len_penalty**(1-len(u))))) - DP(u,len_penalty,Div = True)[1]
		Att[u]['SPKL'] = Att[u]['SPMI']* (NormF(u) * Q(u) *(len_penalty**(1-len(u))))

with open("Att.json","w") as f_obj:
	json.dump(Att,f_obj,indent = 4)
	f_obj.close()
