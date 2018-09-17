out_file = open("result.txt",'w')

for line in open("D:/2017Graduatework/page_links.ttl", 'r'):
    content = line.strip().split(' ')
    entity1 = content[0][:-1].split('/')[-1]
    entity2 = content[-2][:-1].split('/')[-1]
    out_file.write("\t".join([entity1, entity2]) + '\n')
    print('entity1: ' + entity1 + ' entity2: ' + entity2)

out_file.close()