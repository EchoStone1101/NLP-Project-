#Phase 1
#Raw Frequency Dictionary

import os
import json

def IsChinese(ch):
    if('\u4e00' <= ch <= '\u9fff'):
        return True
    return False

PUNC = ['。','，','：','；','“','”','‘','‘','！','？','、','《','》','（','）','(',')',',',':',';','"',"'",'!','?','.','・']
NUM = ['0','1','2','3','4','5','6','7','8','9']
f = {}
Corpus = []

index = {}
Cor = ""
count = 0
article = -1
Threshold = 50
#['X1','X2','X3','X4','X5','X6','X7','X8','X9','X10']
for path in ['Z1','Z2','Z3','Z4','Z5','Z6','Z7','Z8','Z9','Z10']:
	file = open(path)

	flag_num = False

	READ = False

	for line in file:
		line = line.strip('\n')
		if(line == '<HEADLINE>'):
			READ = True
			flag_num = False
			article = article+1
			Corpus.append("")
		if(line == '</HEADLINE>'):
			READ = False
			Cor = Cor + '。'
			count = count+1
			flag_num = False
		if(line == '<P>' or line == '<DATELINE>' or line == '<TEXT>'):
			READ = True
		if(line == '</P>' or line == '</DATELINE>' or line == '</TEXT>'):
			READ = False
			flag_num = False

		if(READ):
			for ch in line:
				if(ch in PUNC):
					if(flag_num):
						flag_num = False
						Cor = Cor + 'X'
						Corpus[article] = Corpus[article] + 'X'
						count = count+1
						if('X' in index):
							index['X'].append(count)
						else:
							index['X'] = [count]
					Cor = Cor + ch
					count = count+1
				if(ch in NUM):
					flag_num = True
				if(IsChinese(ch)):
					if(flag_num):
						flag_num = False
						Cor = Cor + 'X'
						Corpus[article] = Corpus[article] + 'X'
						count = count+1
						if('X' in index):
							index['X'].append(count)
						else:
							index['X'] = [count]
					Cor = Cor + ch
					Corpus[article] = Corpus[article] + ch
					count = count+1
					if(ch in index):
						index[ch].append(count)
					else:
						index[ch] = [count]
	file.close()

Cor = Cor + '。'

while(len(index)):
	print(len(index))
	_index = {}
	for u in index.keys():
		if((len(index[u]) >= Threshold or len(u) == 1) and len(u)<= 10):
			f[u] = len(index[u])
			for j in index[u]:
				if(Cor[j] not in PUNC):
					v = u + Cor[j]
					if(v in _index):
						_index[v].append(j+1)
					else:
						_index[v] = [j+1]
	index = _index

with open("RawF.json",'w') as f_obj:
	json.dump(f,f_obj,indent = 4)


with open("DocCorpus.json",'w') as f_obj:
	json.dump(Corpus,f_obj,indent = 4)