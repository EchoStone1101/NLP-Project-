import os
import json
import math


with open("NormRectF.json","r") as f_obj:
	NormRectF = json.load(f_obj)
	f_obj.close()


Threshold = 5e-5
MyDict = []

for u in NormRectF:
	if(NormRectF[u] >= Threshold and len(u) <= 6):
		MyDict.append((u,0))
print(MyDict)
print(len(MyDict))

with open("XinDict.json","w") as f_obj:
	json.dump(MyDict,f_obj,indent = 4)
	f_obj.close()
