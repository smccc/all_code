# coding:utf-8
import pdb
import math
import numpy

ref = {} # store the prerequisite relationship
df_c = {}
# 加载dbpedia元数据
cnt = 0
for line in open("result_out.txt", 'r'):
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

# 计算得分
rlt_file = open('result/math.nn_1.txt', 'w')
for line in open("data/MATH.edges", 'r'):
    content = line.strip().split('\t')
    A = '_'.join(content[0].split(' '))
    B = '_'.join(content[1].split(' '))
    if A not in ref or B not in ref:
        continue
    xxx = ref[A]
    xxx.extend(ref[B])
    rlt = '\t'.join([str(xxx), str(1)])  
    rlt_file.write(rlt + "\n")

rlt_file.close()
