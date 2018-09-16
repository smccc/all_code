# coding:utf-8
import pdb
import math
import numpy

ref = {}  # 存储依赖关系
line_v = {}  # 存储line的100维向量
# 加载dbpedia元数据
cnt = 0
for line in open("wiki_rels.txt", 'r'):
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
print cnt
print ("元素个数为: "+ str(len(ref)))

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
    line_v[A] = B
print cnt
print ("元素个数为: "+ str(len(line_v)))

# 计算得分 line & refd方法结合
rlt_file = open('result_line/cs.edges.txt', 'w')
for line in open("data/CS.edges", 'r'):
    content = line.strip().split('\t')
    A = '_'.join(content[0].split(' '))
    B = '_'.join(content[1].split(' '))
    A2B = 0
    B2A = 0
    refd_a = 0
    refd_b = 0
    if A not in ref:
        rlt_file.write(str(A) + '\t' + str(B) + '\t' + str(0) + '\n')
        continue
    for item in ref[A]:
        # 计算和A关联的每个词与B的LINE条件概率
        if item not in line_v or B not in line_v:
            continue
        vec1 = numpy.array(line_v[item]).reshape(1, 100)
        vec2 = numpy.array(line_v[B]).reshape(1, 100)
        num = numpy.e ** float(numpy.dot(vec1, vec2.T))
        den = 0
        if item in ref:
            for item_c in ref[item]:
                if item_c not in line_v:
                    continue
                vec3 = numpy.array(line_v[item_c]).reshape(1, 100)
                den += numpy.e ** float(numpy.dot(vec3, vec1.T))
        if den != 0:
            refd_a += float(num/den)
    if refd_a == 0:
        rlt_file.write(str(A) + '\t' + str(B) + '\t' + str(0) + '\n')
        continue
        

    if B not in ref:
        rlt_file.write(str(A) + '\t' + str(B) + '\t' + str(0) + '\n')
        continue
    for item in ref[B]:
        # 计算和B关联的每个词与A的LINE条件概率
        if item not in line_v or A not in line_v:
            continue
        vec1 = numpy.array(line_v[item]).reshape(1, 100)
        vec2 = numpy.array(line_v[A]).reshape(1, 100)
        num = numpy.e ** float(numpy.dot(vec1, vec2.T))
        den = 0
        if item in ref:
            for item_c in ref[item]:
                if item_c not in line_v:
                    continue
                vec3 = numpy.array(line_v[item_c]).reshape(1, 100)
                den += numpy.e ** float(numpy.dot(vec3, vec1.T))
        if den != 0:
            refd_b += float(num/den)
    if refd_b == 0:
        rlt_file.write(str(A) + '\t' + str(B) + '\t' + str(0) + '\n')
        continue

    refD = refd_a/len(ref[A]) - refd_b/len(ref[B])
    rlt_file.write(str(A) + '\t' + str(B) + '\t' + str(refD) + '\n')

rlt_file.close()





# 计算得分 refd方法
# rlt_file = open('result/math.edges.txt', 'w')
# for line in open("data/MATH.edges", 'r'):
#     content = line.strip().split('\t')
#     A = '_'.join(content[0].split(' '))
#     B = '_'.join(content[1].split(' '))
#     A2B = 0
#     B2A = 0
#     A2B_total = 0
#     B2A_total = 0
#     if (A not in ref) or (B not in ref):
#         rlt_file.write(str(A) + '\t' + str(B) + '\t' + str(0) + '\n')
#         continue
#     for item in ref[A]:
#         A2B_total += 1
#         if (item in ref) and (B in ref[item]):
#             print ("A: "+A+' item: '+item+' B: '+B)
#         A2B += 1
#     for item in ref[B]:
#         B2A_total += 1
#         if (item in ref) and (A in ref[item]):
#             print ("B: "+B+' item: '+item+' A: '+A)
#             B2A += 1
#     print(A2B_total)
#     print(B2A_total)
#     # pdb.set_trace()
#     # refD = float(A2B)/A2B_total - float(B2A)/B2A_total
#     print A
#     print B
#     refD = float(A2B)/len(ref[A]) - float(B2A)/len(ref[B])
#     rlt_file.write(str(A) + '\t' + str(B) + '\t' + str(refD) + '\n')
#
# rlt_file.close()
