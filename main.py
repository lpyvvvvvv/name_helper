#!/usr/bin/env python
# -*- coding: utf-8 -*-
import full_wuxing_dict as w
from urllib import parse
from pyppeteer import launch
import asyncio
import random
import time
import traceback

g_full_dict = {
    '水': w.shui_dict,
    '火': w.huo_dict,
    '木': w.mu_dict,
    '金': w.jin_dict,
    '土': w.tu_dict
}


#木生火，火生土，土生金，金生水，水生木
#木克土，土克水，水克火、火克金、金克木

#指定笔画
g_assign_num = [[8,8],[8,10],[8,16],[8,17],[9,2],[9,15],[9,16],[10,6],[10,7],[10,15],[11,6],[11,7],[11,14],[18,6],[18,7],[20,5],[22,10],
                [14,5],[14,6],[14,7],[14,8],[14,9],[14,10],[14,11],[14,12]
                ]

#指定五行
g_assign_wuxing = []
# g_assign_wuxing = ["水","木"]

#排除文字
g_exclude_word = []
# g_exclude_word = ["迎","沛","雯","瑜","池","祯","焕","连","莲","洪","志","颖","乐","潮","彦","玩","贤","要","哈","旺","朋","添","强","亮","晴","朗","锋","峰","辉","文","杰","聪","汪"]

#指定文字
g_assign_word = ["睿"]

# [(8, 10, '金土金', '大吉'), (8, 16, '金土火', '大吉'), (8, 17, '金土土', '大吉'), (9, 2, '金土木', '中吉'), (9, 15, '金土火', '大吉'), (9, 16, '金土土', '大吉'), (10, 7, '金金金', '中吉'), (10, 15, '金金土', '大吉'), (11, 6, '金金金', '中吉'), 
# (11, 7, '金金金', '中吉'), (11, 14, '金金土', '大吉'), (18, 6, '金土火', '大吉'), (18, 7, '金土土', '大吉'), (20, 5, '金金土', '大吉'), (20, 10, '金金水', '中吉')]


WORD_FILE_PATH = "data/word_meta.txt"

WORD_EXCLUDE_PATH = "data/word_exclude.txt"

g_word_with_num = {}   # 笔画：字
g_word_with_wuxing_num = {}   # 五行：{笔画：字}
g_word_detail = {}   # 字：(字，五行，笔画)

#读取配置
def readFile():
    global g_word_with_num
    global g_word_with_wuxing_num
    global g_word_detail
    global g_exclude_word

    with open(WORD_EXCLUDE_PATH, 'r', encoding='utf8') as f:
         lines = f.readlines()
         for line in lines:
            if not line:
                continue
            w = line.strip()
            g_exclude_word.append(w)
    
    with open(WORD_FILE_PATH, 'r', encoding='utf8') as f:
            lines = f.readlines()
            for line in lines:
                if not line:
                     continue
                l = line.split(',')
                if not l:
                    continue

                wuxing, num, w = l[0],int(l[1]),l[2]
                w = w.strip()

                g_word_detail[w] = (w, wuxing, num)

                if not g_word_with_wuxing_num.get(wuxing, None):
                     g_word_with_wuxing_num[wuxing] = {}
                n_dict = g_word_with_wuxing_num.get(wuxing, {})
                if not n_dict.get(num, None):
                     n_dict[num] = []
                l2 = n_dict.get(num, [])
                l2.append(w)

                if not g_word_with_num.get(num, None):
                     g_word_with_num[num] = []
                l3 = g_word_with_num.get(num, [])
                l3.append(w)



def main():

    readFile()
    

    result = ""
    name_list = []

    has_assign_word = False
    if len(g_assign_word) > 0:
         has_assign_word = True
    for i in range(2):
            
        j = 1
        for num in g_assign_num:
            first = num[0]
            second = num[1]
            
            if has_assign_word:
                if i == 0:
                    fist_list = g_assign_word
                    second_list = g_word_with_num.get(second, [])
                else:
                    fist_list = g_word_with_num.get(first, [])
                    second_list = g_assign_word
            else:
                if i > 0:
                     break
                fist_list = g_word_with_num.get(first, [])
                second_list = g_word_with_num.get(second, [])

            # if len(g_assign_word) > 0:
            #     x = random.randint(0, 1)
            #     if x == 0:
            #         fist_list = g_assign_word
            #         second_list = g_word_with_num.get(second, [])
            #     else:
            #         fist_list = g_word_with_num.get(first, [])
            #         second_list = g_assign_word
            # else:
            #     fist_list = g_word_with_num.get(first, [])
            #     second_list = g_word_with_num.get(second, [])

            for w1 in fist_list:
                if w1 in g_exclude_word:
                    continue
                
                t1 = g_word_detail.get(w1)
                num1 = t1[2]

                if num1 != first:
                    continue

                
                if g_assign_wuxing:
                    wu1 = g_assign_wuxing[0]
                    tt1 = g_word_detail.get(w1)
                    if tt1[1] != wu1:
                            continue

                    
                for w2 in second_list:
                        if w2 in g_exclude_word:
                            continue

                        t2 = g_word_detail.get(w2)
                        num2 = t2[2]

                        if num2 != second:
                            continue
                    
                        # if g_assign_word and (w1 not in g_assign_word and w2 not in g_assign_word):
                        #     continue

                        if g_assign_wuxing:
                            wu2 = g_assign_wuxing[1]
                            tt2 = g_word_detail.get(w2)
                            if tt2[1] != wu2:
                                continue

                        

                        wu1 = t1[1]
                        wu2 = t2[1]

                        
                        

                        name = "李%s%s, %s %s, %s %s"%(w1, w2, num1, num2, wu1, wu2)
                        name_list.append(name)
                        result += name
                        result += "\n"



    lll = len(name_list)
    print("-------------------------------------total = ", lll)
    

    if lll <= 0:
         print("no name suit")
         return

    tt = int(time.time())
    fname = "result/name_list.txt"
    f = open(fname, 'a', encoding='utf8')


    lastIndex = []
    while True:
         try:
            print("press any key to continue:")
            s = input()

            if s == "q":
                 break;
            
            f.write("--------------------------\n")
            f.flush()
            for i in range(10):
                index = random.randint(0, lll - 1)
                if index in lastIndex:
                        continue
                lastIndex.append(index)
                ss = name_list[index]
                print(ss)

                f.write(ss)
                f.write("\n")
                f.flush()


            
         except Exception as e:
             traceback.print_exc()
             print('Have a rest, then continue...')
         
    
    f.close()

                




if __name__ == '__main__':
    main()