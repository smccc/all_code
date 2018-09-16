# coding:utf-8
import pdb
import math

ref = {} # store the prerequisite relationship
df_c = {}
# 加载dbpedia元数据
cnt = 0
for line in open("../wiki_rels.txt", 'r'):
    cnt += 1
    content = line.strip().split('\t')
    if len(content) < 2:
        continue
    A = content[0]
    B = content[1]
    # ref[A]的元素个数是出度
    if A in ref:
        ref[A].add(B)
    else:
        ref.setdefault(A,set(B))
    '''
    if A in df_c:
        df_c[A] += 1
    else:
        df_c[A] = 0
    '''
    # df_c是入度
    if B in df_c:
        df_c[B] += 1
    else:
        df_c[B] = 0
print cnt
print ("元素个数为: "+ str(len(ref)))

# 计算得分
cnt = 0
rlt_file = open('features_wiki_result.txt', 'w')
for line in open("../wiki_rels.txt", 'r'):
    #cnt += 1
    #if cnt >= 10000:
    #    break
    content = line.strip().split('\t')
    if len(content) != 2:
        continue
    A = '_'.join(content[0].split(' '))
    B = '_'.join(content[1].split(' '))
    A2B = 0
    B2A = 0
    if (A not in ref) or (B not in ref):
    	# rlt_file.write(str(A) + '\t' + str(B) + '\t' + str(0) + '\n')	
	    continue
    for item in ref[A]:
        if (item in ref) and (B in ref[item]):
            print ("A: "+A+' item: '+item+' B: '+B)
            A2B += 1
    for item in ref[B]:
        if (item in ref) and (A in ref[item]):
            print ("B: "+B+' item: '+item+' A: '+A)
            B2A += 1
    # pdb.set_trace()
    # refD = float(A2B)/A2B_total - float(B2A)/B2A_total
    print A
    print B
    refD = float(A2B)/len(ref[A]) - float(B2A)/len(ref[B])
    # numbers of common neighbors
    unions = len(ref[A] & ref[B])
    # A or B may not have indegree
    if A not in df_c:
        df_c[A] = 0
    if B not in df_c:
        df_c[B] = 0
    
    output = [A, B, str(len(ref[A])), str(df_c[A]), str(len(ref[B])), str(df_c[B]), str(unions), str(refD)]
    rlt_file.write('\t'.join(output) + '\n')
    #rlt_file.write(str(A) + '\t' + str(B) + '\t' + str(refD) + '\n')

rlt_file.close()
