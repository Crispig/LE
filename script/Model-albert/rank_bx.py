import numpy as np
from multiprocessing import Pool
# f_target=open('tar.txt')
f_target=open('./result_1_6_final_3600/tgt.txt')
f_v1=open('./result_1_6_final_3600/model1.txt')
f_v2=open('./result_1_6_final_3600/model2.txt')
f_v3=open('./result_1_6_final_3600/model3.txt')
f_v4=open('./result_1_6_final_3600/model4.txt')
# f_v5=open('./result_12_8/model5.txt')
# f_v6=open('./result_12_8/model6.txt')

f_1=f_v1.readlines()
f_2=f_v2.readlines()
f_3=f_v3.readlines()
f_4=f_v4.readlines()
# f_5=f_v5.readlines()
# f_6=f_v6.readlines()
f_t=f_target.readlines()
num=0
all=0
alll=0
maxx=0
ar=0
br=0
cr=0
dr=0
# er=0
# fr=0
numr=0
def ccc(args):
    return cl(*args)


def cl(a,b,c,d):
    global num
    global alll
    # index=0
    global maxx
    global ar
    global br
    global cr
    global dr
    global all
    # global er
    # global fr
    global numr
    # TODO  需要修改总共有多少行和txt中tgt的行数一样！！！
    for index in range(422):
        list_t=f_t[index].split(':')[1].split('[[')[1].split(']]')[0].split(',')
        l=len(list_t)
        all+=l
        for i in range(l):
            y = []
            an1=f_1[index].split('[[')[1].split(']]')[0].split("], [")[i]
            an2=f_2[index].split('[[')[1].split(']]')[0].split("], [")[i]
            an3=f_3[index].split('[[')[1].split(']]')[0].split("], [")[i]
            an4=f_4[index].split('[[')[1].split(']]')[0].split("], [")[i]
            # an5=f_5[index].split('[[')[1].split(']]')[0].split("], [")[i]
            # an6=f_6[index].split('[[')[1].split(']]')[0].split("], [")[i]
            s1=an1.split(',')
            s2=an2.split(',')
            s3=an3.split(',')
            s4=an4.split(',')
            # s5=an5.split(',')
            # s6=an6.split(',')
            for j in range(4):
                temp = a * float(s1[j]) + b * float(s2[j]) + c * float(s3[j]) + d * float(s4[j]) 
                y.append(temp)
            yt=np.array(y)
            k=np.argmax(yt)
            if k==int(list_t[i].strip()):
                num+=1
        # f_t = f_target.readline()
    # print(all)
    
    # print(num,'----',7758)
    # TODO 修改分母（总题数）和
    if  num/ 7798*100> maxx:
        maxx= num/ 7798*100
        if maxx > 90.8: 
            print(maxx,'---',a,' ',b,' ',c,' ',d)
        ar=a
        br=b
        cr=c
        dr=d
        # er=e
        # fr=f
        numr= num
        # alllr= alll
    num = 0

a=range(20)
b=range(20)
c=range(20)
d=range(20)
# e=range(20)
# f=range(20)


args_list=[]
for aa in a:
    for bb in b:
        for cc in c:
            for dd in d:
                # for ee in e:
                #     for ff in f:
                args_list.append([aa,bb,cc,dd])


pool=Pool(56)
pool.map(ccc,args_list)
print("Datasets*4_重叠")
print("valid_eval_accuracy:"+str(num/alll*100))
# print("valid_eval_accuracy:"+str(maxx))
print(ar)
print(br)
print(cr)
print(dr)

print(numr)
# print(alllr)
f_target.close()
f_v1.close()
f_v2.close()
f_v3.close()
f_v4.close()
