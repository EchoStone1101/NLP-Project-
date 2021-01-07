#Phase 2
#Calculate PMI,PKL and IDF based on RawFrequency

import os
import json
import math
from collections import defaultdict

class TrieNode(object):
    def __init__(self, value=None):
        self.value = value
        self.fail = None
        self.tail = 0
        self.children = {}


class Trie(object):
    def __init__(self, words):
        self.root = TrieNode()
        self.count = 0
        self.words = words
        for word in words:
            self.insert(word)
        self.ac_automation()

    def insert(self, sequence):
        self.count += 1
        cur_node = self.root
        for item in sequence:
            if item not in cur_node.children:
                child = TrieNode(value=item)
                cur_node.children[item] = child
                cur_node = child
            else:
                cur_node = cur_node.children[item]
        cur_node.tail = self.count

    def ac_automation(self):
        queue = [self.root]
        while len(queue):
            temp_node = queue[0]
            queue.remove(temp_node)
            for value in temp_node.children.values():
                if temp_node == self.root:
                    value.fail = self.root
                else:
                    p = temp_node.fail
                    while p:
                        if value.value in p.children:
                            value.fail = p.children[value.value]
                            break
                        p = p.fail
                    if not p:
                        value.fail = self.root
                queue.append(value)

    def search(self, text):
        p = self.root
        start_index = 0
        rst = defaultdict(list)
        for i in range(len(text)):
            single_char = text[i]
            while single_char not in p.children and p is not self.root:
                p = p.fail
            if single_char in p.children and p is self.root:
                start_index = i
            if single_char in p.children:
                p = p.children[single_char]
            else:
                start_index = i
                p = self.root
            temp = p
            while temp is not self.root:
                if temp.tail:
                    rst[self.words[temp.tail - 1]].append((start_index, i))
                temp = temp.fail
        return rst



with open("RawF.json","r") as f_obj:
    RawF = json.load(f_obj)
    f_obj.close()

with open("DocCorpus.json","r") as f_obj:
    Corpus = json.load(f_obj)
    f_obj.close()


Att = {}

def log(x):
    return math.log(x)

def P(u):
    if(u in Att):
        return Att[u]['P']
    else:
        return 0

def PMI(v):
    if(v in Att):
        return Att[v]['PMI']
    else:
        return 0

def PKL(v):
    if(v in Att):
        return Att[v]['PKL']
    else:
        return 0

def IDF(u):
    return Att[u]['IDF']

tot = 0

for u in RawF:
    tot = tot+RawF[u]
    Att[u] = {'P':0, 'PMI':0, 'PKL':0, 'IDF':0, 'SPMI':0, 'SPKL':0}

print("Initialized")
for u in RawF:
    Att[u]['P'] = RawF[u] / tot
print("P Calculated!")

for v in RawF:
    if(len(v)>1):
        Att[v]['PMI'] = min([ log(P(v) / P(v[:i]) / P(v[i:]))  for i in range(1,len(v))])
        Att[v]['PKL'] = PMI(v) * P(v)
print("PMI/PKL Calculated!")


print("TrieTree Building Started")
ACTree = Trie(list(RawF.keys()))
print("TrieTree Built")


f = []
for i in range(0,len(Corpus)):
    index = dict(ACTree.search(Corpus[i]))
    f.append({})
    for u in index:
        f[i][u] = len(index[u])
    if(i%100 == 0):
        print(i)

with open("DocRawF.json","w") as f_obj:
    json.dump(f,f_obj,indent = 4)
    f_obj.close()
print("DocRawF Calculated!")


for u in RawF:
    if(len(u) == 1):
        count = 0
        for d in range(0,len(Corpus)):
            if(u in Corpus[d]):
                count = count + 1
        Att[u]['IDF'] = log(len(Corpus)/count)

for u in RawF:
    if(len(u) > 1):
        for word in u:
            Att[u]['IDF'] = Att[u]['IDF'] + IDF(word)
        Att[u]['IDF'] = Att[u]['IDF'] / len(u)
print("IDF Calculated!")

with open("Att.json","w") as f_obj:
    json.dump(Att,f_obj,indent = 4)
    f_obj.close()

