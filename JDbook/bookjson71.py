# coding:utf-8

import chardet
import re
import json
import unicodedata
import codecs

def run():
    cnt = 1
    flag = False
    flag1 = False
    output_dict = {"books": []}
    out_file = codecs.open("bookjson_out.txt", "w", "utf-8")
    for line in open("bookjd.json", "r"):
        book_dict = {}
        cnt += 1
        if cnt <= 20:
            # 提取并拆分目录
            mulu = []
            content = line.split(" ")
            str_ = ""
            # print content
            for item in content:
                # print item
                if '<h3>目录</h3>' in item:
                    flag = True
                elif '</div>' in item:
                    if flag1:
                        str_ += item
                        break
                    elif flag:
                        str_ += item
                        flag1 = True
                elif flag:
                    str_ += item

            flag = False
            flag1 = False
            categories = process(str_)

            cnt_cat = 0
            for item in categories:
                if item in ["><", "> <", ">……<", ">  <", ">    <"]:
                    # 会有一些目录,中间没有内容,过滤掉
                    continue
                cat_whole = item[1:-1]
                cat_uni = cat_whole.strip().decode("utf-8")
                # cat_uni = cat_whole.decode("gbk")
                cat_eng = unicodedata.normalize("NFKC", cat_uni)
                regex = re.compile('\s+')
                cat_lst = regex.split(cat_eng)
                print cat_lst
                # 设置目录等级
                if len(cat_lst) >= 2:
                    level = len(cat_lst[0].split("."))
                    if cat_lst[-1].isdigit():
                        cat_name = cat_lst[-2]
                    else:
                        cat_name = cat_lst[-1]
                else:
                    level = 1
                    cat_name = cat_whole

                cnt_cat += 1
                mulu.append({"label":cat_name, "orderid":cnt_cat, "level":level})

            # 构建json
            params = json.loads(line)
            url = params['result']['url']
            books_info = params['result']['parameter']
            title = params['result']['title']
            book_dict.setdefault("书名", title)
            book_dict.setdefault("目录", mulu)
            book_dict.setdefault("url", url)
            for item in books_info:
                new_item = unicodedata.normalize("NFKC", item)
                info_pair = new_item.split(":")
                book_dict.setdefault(info_pair[0].strip(), info_pair[1].strip())

            book_out = json.dumps(book_dict, ensure_ascii=False, encoding='UTF-8')
            print book_out
            output_dict["books"].append(book_dict)
        else:
            break
    dict_out = json.dumps(output_dict, ensure_ascii=False, encoding='UTF-8')
    out_file.write(dict_out)
    out_file.close()

def process(str):
    # print str
    str_new = str.replace("\\n", ' ')
    str = str_new.replace("\\", ' ')
    # print str
    pattern_js = re.compile(r'>.*?<')
    categories = pattern_js.findall(str)
    return categories
    # for item in categories:
    #     print item[1:-1]

if __name__ == "__main__":
    run()