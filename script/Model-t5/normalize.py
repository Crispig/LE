import numpy as np

path1 = "../combination/t5-large-1_final.txt"
path2 = "../combination/t5-large-2_final.txt"
path3 = "../combination/t5-large-3_final.txt"
path4 = "../combination/t5-large-4_final.txt"
path5 = "../combination/t5-large-all_final.txt"

str1_list = []
str2_list = []
str3_list = []
str4_list = []
str5_list = []

result1_list = []
result2_list = []
result3_list = []
result4_list = []
result5_list = []

with open(path1, mode='r') as f:
    str1_list = f.readlines()

with open(path2, mode='r') as f:
    str2_list = f.readlines()

with open(path3, mode='r') as f:
    str3_list = f.readlines()

with open(path4, mode='r') as f:
    str4_list = f.readlines()

with open(path5, mode='r') as f:
    str5_list = f.readlines()

for i in range(400):
    result1_list.append([])
    result2_list.append([])
    result3_list.append([])
    result4_list.append([])
    result5_list.append([])
    line1 = str1_list[i].split('[\'')[-1].split('\']')[0]
    line2 = str2_list[i].split('[\'')[-1].split('\']')[0]
    line3 = str3_list[i].split('[\'')[-1].split('\']')[0]
    line4 = str4_list[i].split('[\'')[-1].split('\']')[0]
    line5 = str5_list[i].split('[\'')[-1].split('\']')[0]
    for j in range(len(line1.split('\', \''))):
        result1_list[-1].append([float(k) for k in line1.split('\', \'')[j].split(', ')])
        result2_list[-1].append([float(k) for k in line2.split('\', \'')[j].split(', ')])
        result3_list[-1].append([float(k) for k in line3.split('\', \'')[j].split(', ')])
        result4_list[-1].append([float(k) for k in line4.split('\', \'')[j].split(', ')])
        result5_list[-1].append([float(k) for k in line5.split('\', \'')[j].split(', ')])

result_list = []

a = 5
b = 8
c = 5
d = 8
e = 9

for i in range(400):
    result_list.append([])
    for j in range(len(result1_list[i])):
        sample = np.sum([np.array([a * i for i in result1_list[i][j]]), np.array([b * i for i in result2_list[i][j]]), np.array([c * i for i in result3_list[i][j]]), np.array([d * i for i in result4_list[i][j]]), np.array([e * i for i in result5_list[i][j]])],axis=0)
        # sample = np.array([a * i for i in result1_list[i][j]])
        # print(sample)
        norm = [sample[i] / max(abs(sample)) for i in range(len(sample))]
        result_list[-1].append(norm)
# np.save("./albert-xxlarge-v2.npy", np.array(result_list, dtype=object),allow_pickle=True)

with open("../model_ensembles/t5-large.txt",mode='w') as f:
    for i in result_list:
        f.write(str(i) + '\n')