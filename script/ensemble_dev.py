import numpy as np
f_tt=open('./model_ensembles/tgt.txt')
f_v1=open('./model_ensembles/albert-xxlarge-v2.txt')
f_v2=open('./model_ensembles/bert-base-uncased.txt')
f_v3=open('./model_ensembles/t5-large.txt')

# out=open('./out/temp.txt','w')

f_t=f_tt.readline()
f_1=f_v1.readlines()
f_2=f_v2.readlines()
f_3=f_v3.readlines()

num=0
al=0
index=0
while f_t is not None and f_t != '':
    list_t=f_t.split('[\'')[1].split('\']')[0].split('\', \'')
    num_line=len(list_t)
    al+=num_line
    for i in range(num_line):
        y = []
        an1=f_1[index].split('[[')[1].split(']]')[0].split("], [")[i]
        an2=f_2[index].split('[[')[1].split(']]')[0].split("], [")[i]
        an3=f_3[index].split('[[')[1].split(']]')[0].split("], [")[i]
        s1 = an1.split(',')
        s2 = an2.split(',')
        s3 = an3.split(',')

        for j in range(4):
            temp = 16*float(s1[j])+2*float(s2[j])+7*float(s3[j])
            # temp = float(s3[j])
            y.append(temp)

        yt=np.array(y)
        # print(yt)
        k=np.argmax(yt)
        # print(k)
        # if i==num_line-1:
        #     print('{}]'.format(k),file=out)
        # else:
        #     print('{}, '.format(k),end='',file=out)

        if k==int(list_t[i]):
            num=num+1
    # print(']')
    f_t = f_tt.readline()
    index=index+1

# f_target.close()
print("-----------Result-----------")
print("Accuracy:"+str(num/al))
f_tt.close()
f_v1.close()
f_v2.close()
f_v3.close()