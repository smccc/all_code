# coding:utf-8
import pdb
import math
import numpy

ref = {} # store the prerequisite relationship
df_c = {}
# 加载dbpedia元数据
cnt = 0
for line in open("/home/smc/LINE/linux/wiki_line.txt", 'r'):
    cnt += 1
    content = line.strip().split(' ')
    if len(content) < 2:
        print content
        continue
    A = content[0]
    B = content[1:]
    B = [float(item) for item in B]
    ref[A] = B
print cnt
print ("元素个数为: "+ str(len(ref)))

'''
# 计算得分
rlt_file = open('result/cs.line.txt', 'w')
for line in open("data/CS.edges", 'r'):
    content = line.strip().split('\t')
    A = '_'.join(content[0].split(' '))
    B = '_'.join(content[1].split(' '))
    if A not in ref or B not in ref:
        rlt_file.write('\t'.join([A, B, str(0)]) + '\n')
        continue
    vec1 = numpy.array(ref[A]).reshape(1, 100)
    vec2 = numpy.array(ref[B]).reshape(1, 100)
    num = float(numpy.dot(vec1, vec2.T))
    denom = numpy.linalg.norm(vec1) * numpy.linalg.norm(vec2)
    cos = num / denom 
    rlt = '\t'.join([A, B, str(cos)])  
    rlt_file.write(rlt + "\n")

rlt_file.close()
'''
