f1 = None
f2 = None
f3 = None
f4 = None
f5 = None
with open('../result/t5-large-1.txt',mode='r') as f:
    f1 = f.readlines()
with open('../result/t5-large-2.txt',mode='r') as f:
    f2 = f.readlines()
with open('../result/t5-large-3.txt',mode='r') as f:
    f3 = f.readlines()
with open('../result/t5-large-4.txt',mode='r') as f:
    f4 = f.readlines()
with open('../result/t5-large-all.txt',mode='r') as f:
    f5 = f.readlines()

result1_list = []
result2_list = []
result3_list = []
result4_list = []
result5_list = []
resultt_list = []

old_head = None
with open('../result/t5-large-tgt.txt',mode='r') as f:
    ft = f.readlines()
    old_head = [int(ft[0].split('/')[-1].split('.')[0].split('v')[-1])]
    recent1_line = f1[0].split('[[')[1].split(']]')[0].split("], [")
    recent2_line = f2[0].split('[[')[1].split(']]')[0].split("], [")
    recent3_line = f3[0].split('[[')[1].split(']]')[0].split("], [")
    recent4_line = f4[0].split('[[')[1].split(']]')[0].split("], [")
    recent5_line = f5[0].split('[[')[1].split(']]')[0].split("], [")
    recentt_line = ft[0].split('[')[1].split(']')[0].split()
    for id, line in enumerate(ft[1:]):
        if int(line.split('/')[-1].split('.')[0].split('v')[-1]) != old_head[-1]:
            old_head.append(int(line.split('/')[-1].split('.')[0].split('v')[-1]))
            result1_list.append(recent1_line)
            result2_list.append(recent2_line)
            result3_list.append(recent3_line)
            result4_list.append(recent4_line)
            result5_list.append(recent5_line)
            resultt_list.append(recentt_line)
            recent1_line = f1[id + 1].split('[[')[1].split(']]')[0].split("], [")
            recent2_line = f2[id + 1].split('[[')[1].split(']]')[0].split("], [")
            recent3_line = f3[id + 1].split('[[')[1].split(']]')[0].split("], [")
            recent4_line = f4[id + 1].split('[[')[1].split(']]')[0].split("], [")
            recent5_line = f5[id + 1].split('[[')[1].split(']]')[0].split("], [")
            recentt_line = ft[id + 1].split('[')[1].split(']')[0].split()
        else:
            recent1_line += f1[id + 1].split('[[')[1].split(']]')[0].split("], [")
            recent2_line += f2[id + 1].split('[[')[1].split(']]')[0].split("], [")
            recent3_line += f3[id + 1].split('[[')[1].split(']]')[0].split("], [")
            recent4_line += f4[id + 1].split('[[')[1].split(']]')[0].split("], [")
            recent5_line += f5[id + 1].split('[[')[1].split(']]')[0].split("], [")
            recentt_line += ft[id + 1].split('[')[1].split(']')[0].split()
        
    result1_list.append(recent1_line)
    result2_list.append(recent2_line)
    result3_list.append(recent3_line)
    result4_list.append(recent4_line)
    result5_list.append(recent5_line)
    resultt_list.append(recentt_line)

for i in range(1,len(old_head)):
    for j in range(len(old_head)):
        if old_head[j] == i:
            t_h = old_head[i - 1]
            t_1 = result1_list[i - 1]
            t_2 = result2_list[i - 1]
            t_3 = result3_list[i - 1]
            t_4 = result4_list[i - 1]
            t_5 = result5_list[i - 1]
            t_t = resultt_list[i - 1]
            old_head[i - 1] = old_head[j]
            result1_list[i - 1] = result1_list[j]
            result2_list[i - 1] = result2_list[j]
            result3_list[i - 1] = result3_list[j]
            result4_list[i - 1] = result4_list[j]
            result5_list[i - 1] = result5_list[j]
            resultt_list[i - 1] = resultt_list[j]
            old_head[j] = t_h
            result1_list[j] = t_1
            result2_list[j] = t_2
            result3_list[j] = t_3
            result4_list[j] = t_4
            result5_list[j] = t_5
            resultt_list[j] = t_t



with open('../combination/t5-large-1_final.txt',mode='w') as f:
    for i in range(len(old_head)):
        f.write(str(result1_list[i]) + '\n')
with open('../combination/t5-large-2_final.txt',mode='w') as f:
    for i in range(len(old_head)):
        f.write(str(result2_list[i]) + '\n')
with open('../combination/t5-large-3_final.txt',mode='w') as f:
    for i in range(len(old_head)):
        f.write(str(result3_list[i]) + '\n')
with open('../combination/t5-large-4_final.txt',mode='w') as f:
    for i in range(len(old_head)):
        f.write(str(result4_list[i]) + '\n')
with open('../combination/t5-large-all_final.txt',mode='w') as f:
    for i in range(len(old_head)):
        f.write(str(result5_list[i]) + '\n')
with open('../combination/t5-large-tgt_final.txt',mode='w') as f:
    for i in range(len(old_head)):
        f.write(str(old_head[i]) + ":" + str(resultt_list[i]) + '\n')