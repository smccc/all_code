fwrite = open("wiki_nets.txt", "w")

cnt = 0
for line in open("wiki_rels.txt", "r"):
    cnt += 1
    if cnt % 10000000 == 0:
        print cnt
    content = line.strip() + "\t" + "1" + "\n"
    fwrite.write(content)

fwrite.close()
