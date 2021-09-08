import numpy as np
f_tt=open('./model_ensembles/test-tgt.txt')
f_v1=open('./model_ensembles/test-albert-xxlarge-v2.txt')
f_v2=open('./model_ensembles/test-bert-base-uncased.txt')
f_v3=open('./model_ensembles/test-t5-large.txt')

out=open('../test/temp.json','w')

f_t=f_tt.readline()
f_1=f_v1.readlines()
f_2=f_v2.readlines()
f_3=f_v3.readlines()

num=0
al=0
index=0

print('{',end='',file=out)
while f_t is not None and f_t != '':
    list_t=f_t.split('[\'')[1].split('\']')[0].split('\', \'')
    num+=1
    print('\"test{}\":['.format(str(num).zfill(4)),end='',file=out)
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
            temp = 15*float(s1[j])+2*float(s2[j])+6*float(s3[j])
            # temp = float(s3[j])
            y.append(temp)

        yt=np.array(y)
        # print(yt)
        k=np.argmax(yt)
        # print(k)
        if i==num_line-1:
            if num == 400:
                print('\"{}\"]'.format(chr(ord('A')+k)),end='',file=out)
            else:
                print('\"{}\"],'.format(chr(ord('A')+k)),file=out)
        else:
            print('\"{}\",'.format(chr(ord('A')+k)),end='',file=out)

    # print(']')
    f_t = f_tt.readline()
    index=index+1

print('}',file=out)

f_tt.close()
f_v1.close()
f_v2.close()
f_v3.close()
out.close()