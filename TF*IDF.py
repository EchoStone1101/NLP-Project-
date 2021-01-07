import os
import json



with open("NanDict.json","r") as f_obj:
    Dict = json.load(f_obj)
    f_obj.close()
print(1)
MyDict = [u[0] for u in Dict]

with open("DocRawF.json","r") as f_obj:
    DocRawF = json.load(f_obj)
    f_obj.close()
print(1)
with open("DocCorpus.json","r") as f_obj:
    Corpus = json.load(f_obj)
    f_obj.close()
print(1)
with open("Att.json","r") as f_obj:
    Att = json.load(f_obj)
    f_obj.close()
print(1)

XinTopic = open("NanTopic.txt",'w')

for d in range(0,len(DocRawF)):
    Topic = []
    for u in DocRawF[d]:
        if(len(u) == 1):
            continue
        if(u in MyDict):
            Topic.append((u,DocRawF[d][u] / len(Corpus[d])*Att[u]['IDF']))
    if(len(Topic)):
        XinTopic.write(str(d)+" ")
    Topic = sorted(Topic,key = lambda d:d[1],reverse = True)
    for i in range(0,min(3,len(Topic))):
        XinTopic.write(Topic[i][0]+" ")
    XinTopic.write("\n")
    print(d/len(DocRawF)*100,"%")