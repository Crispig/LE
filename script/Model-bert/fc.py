import numpy as np
f_v=open('./bert-base-uncased/vocab.txt')
f=f_v.readline()
vo=[]
while f is not None and f !='':
    vo.append(f.split('\n')[0])
    f=f_v.readline()
def search(n):
    return vo[n]
# print(search(10))
# print(search(15))
f_v.close
