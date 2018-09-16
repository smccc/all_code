# coding:utf-8
import math
ref = {} # store the prerequisite relationship
df_c = {}
# 加载dbpedia元数据
cnt = 0
for line in open("newresult.txt", 'r'):
    cnt += 1
    content = line.strip().split('\t')
    if len(content) < 2:
        continue
    A = content[0]
    B = content[1]
    if A in ref:
        ref[A].add(B)
    else:
        ref.setdefault(A,set(B))
    if A in df_c:
        df_c[A] += 1
    else:
        df_c[A] = 1
    if B in df_c:
        df_c[B] += 1
    else:
        df_c[B] = 1
print cnt
print ("元素个数为: "+ str(len(ref)))

# 计算得分
rlt_file = open('result/cs.edges_neg_tfidf.txt', 'w')
for line in open("data/CS.edges_neg", 'r'):
    content = line.strip().split('\t')
    A = '_'.join(content[0].split(' '))
    B = '_'.join(content[1].split(' '))
    A2B = 0
    B2A = 0
    A2B_total = 0
    B2A_total = 0
    if (A not in ref) or (B not in ref):
	rlt_file.write(str(A) + '\t' + str(B) + '\t' + str(0) + '\n')
        continue 
    for item in ref[A]:
        if(item in df_c ):
	    A2B_total += float(math.log(float(cnt/df_c[item]))/math.log(2))
        if (item in ref) and (B in ref[item]):
            print ("A: "+A+' item: '+item+' B: '+B)
	    A2B += float(math.log(float(cnt/df_c[item]))/math.log(2))
    for item in ref[B]:
        print(item)
	if(item in df_c ):
	    B2A_total += float(math.log(float(cnt/df_c[item]))/math.log(2))
        if (item in ref) and (A in ref[item]):
            print ("B: "+B+' item: '+item+' A: '+A)
	    print(item+'???'+str(df_c[item]))
	    B2A += float(math.log(float(cnt/df_c[item]))/math.log(2))
    print(A2B)
    print(B2A)
    refD = float(A2B)/A2B_total - float(B2A)/B2A_total
    rlt_file.write(str(A) + '\t' + str(B) + '\t' + str(refD) + '\n')

rlt_file.close()

