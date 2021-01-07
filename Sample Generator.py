#Phase 3
#Generate sample based on raw dictionary and good dictionary
import os
import json
import random
import sys

SIZE = {2:300,3:150,4:50}
length = [2,3,4]
PSample = {2:{},3:{},4:{}}
NSample = {2:{},3:{},4:{}}

random.seed(19260817)

with open("Att.json","r") as f_obj:
    Att = json.load(f_obj)
    f_obj.close()

GoodDict = []
with open("中文词表.txt","r") as f_obj:
    for line in f_obj:
    	line = line.strip('\n')
    	GoodDict.append(line)
    f_obj.close()


for l in length:
    while(len(PSample[l]) < SIZE[l]):
      i = random.randint(0,len(GoodDict))
      if(len(GoodDict[i]) == l and GoodDict[i] in Att):
            PSample[l][GoodDict[i]] = 1

key = list(Att.keys())
for l in length:
    while(len(NSample[l]) < SIZE[l]):
      i = random.randint(0,len(key))
      if(len(key[i]) == l and Att[key[i]] not in GoodDict):
            NSample[l][key[i]] = 0

Sample = {}
for l in length:
    for u in PSample[l]:
        Sample[u] = PSample[l][u]
    for u in NSample[l]:
        Sample[u] = NSample[l][u]

print(Sample)
with open("Labeled.json","w") as f_obj:
    json.dump(Sample,f_obj,indent = 4)
    f_obj.close()

