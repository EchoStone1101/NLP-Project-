import os
import json



with open("NanDict.json","r") as f_obj:
    MyDict = json.load(f_obj)
    f_obj.close()

with open("RawF.json","r") as f_obj:
    RawF = json.load(f_obj)
    f_obj.close()

for u in MyDict:
    u[1] = RawF[u[0]]

MyDict = sorted(MyDict,key = lambda d:d[1],reverse = True)

with open("NanDict.json","w") as f_obj:
    json.dump(MyDict,f_obj,indent = 4)
    f_obj.close()
