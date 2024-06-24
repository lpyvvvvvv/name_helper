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


# 2024年iia辰年，木龙年，天干木，地支土，纳音覆灯火。因为龙喜行于天空，而与曰、月、星、辰为伍。如:星、云、霖、霈、辰、晨、腾、农、浓、侬、振。起名宜用星，云，辰的字根。
# 因为龙喜水、雨，取龙为雨神，江河之水为水龙王掌管，龙得水，也使得其所。如:水、冰、江、沈、汪、注、沛、泳、淳、海、涵、清、洁、潮、浏、瀚。起名宜用“氵”、“水”之字根。
# 因龙在中国人心中的地位z大，宜称大，发号施令，不宜称小。如:大、王、君、玲、琴、五、珍、珠、琳、琪、瑷、瑜、瑶、璞、璋、环、琼。起名宜用:“王、大、君、帝、令、 主、长”之字根。

# 一、避免采用有“山”、“丘”“寅”的字根，会“良”、犯上“龙”“虎”斗。因山为老虎之乡，艮qua意也为山。如:山、岑、岸、岩、岳、峰、岛、峻、峡、岗、崔、崧、岚、嵩、岭、艮、良、艰、虎、寅、演。
# 二、避免采用有“戌”、“犭”“犬”之字根，因辰与成正冲，犯了正冲，是生肖姓名中z大的禁忌。如:戌、成、诚、茂、晟、狄、猛、猷、犹、获、献、威。
# 三、避免采用有小“口”之字根，会形成困龙之意。如:台、古、可、名、同、合、味、品、哈、唐、哥、哲、员、商、束、喜、器、嘉。
# 四、避免“文”有“辶”“曰”、“川”、“几”“邑”、的字根，会有龙降格为蛇之“巳”、感，由大变小，地位降低之意。如:元、允、尤、弘、弟、强、巷、先、选、迪、逢、通、连、造、进、运、迁、迈、还、郭、邓、邝、郑、
# 郎、郁、都、乡、延、建。
# 五、避免才用有“宀”的字根，龙也不喜欢洞穴，有龙见龙、王见王之意。如:字、守、宏宋、家、容、密、寅、宁、宝。

# “龙”在十二生肖排行第五位,地支为“辰”,五行属“土”。龙为吉祥神圣的象征,能吸收日月星辰之精华,腾云驾雾、翱翔天际、不食人间烟火是它的特性。
# 以姓名学的角度来解析,龙为神化之瑞兽、帝王之象征,喜用“王格”、掌印”字根,也喜“披彩衣”、“戴冠冕”,都能增添肖龙者的权势与江山。
# 喜用“日、月、星”,代表有定见、善计划、前途光明。但是“月”也代表“肉”字根与玉兔,“肉字根”与龙的食性不符,龙与兔又是刑克关系,故使用“月”字根时需特别谨慎搭配。
# 马的地支为午,肖龙者喜用“午”字根,象征“龙马精神”,有干劲能开拓未来。
# 龙为天上之物,故不喜“住家”、栅栏”、“洞穴”字根,会有“龙困浅滩”有志难伸的困境。龙喜水,能腾云驾雾,故喜用“云”、“雨”、“水”字根。代表有助力,能善用环境、资源,一飞冲天。“三合”、“三会”为有助益。“申子辰”三合、“寅卯辰”三会,故喜“申、子”字根。
# 虽然
# “三会”为有助益,但是“寅卯”龙虎斗,“卯辰”为刑克,故禁用“卯、辰”字根。
# 龙不食人间烟火,不论“肉”字根与“五谷”字根皆无助益,故不喜用。
# 蛇的俗称为“小龙”,“巳”字根会让龙降格。龙为天上物,落入凡间变成人也是降格,也不喜“人”字根。“巳、人”字根会让肖龙者个性会过于胆小保守畏缩。
# 辰与戌正冲,辰与卯刑克,故肖龙者不喜用“戌”字根与“卯”字根,为破格。
# 肖龙者忌用“寅”字根,会形成“龙争虎斗”“两雄争霸”“两败俱伤”的局面。


# 忌用字
# 1、辰戌冲，戌”字根-戌、犬、犬。例如-成、威、器、状、狄。
# 2、刑克-玉兔见龙云里去，“卯”字根-卯、兔。例如-卿、柳、逸、勉。
# 3、龙虎斗，“寅”字根-寅、虎。例如-演、彪、卢、号、处。
# 4、天罗地网，丑字根-牲、物、妞、浩、纽、生、牟，未字根-妹、善、义、美、群、翔。
# 5、五行，土-培、垚、均、里、坚。金-钧、鑫、铜、铨、锋、铭。
# 6、不得食，五谷杂粮-豆、米、田、麦、梁、禾、甫字根。例如-丰、菊、咪、麴、梁、和、禀、秉、秧、秦、圃，肉类-月、心、忄、肉，例如-胜、肯、思、志、惠、恕、恒恒、忱、性、怡。
# 7、不得地，洞穴、屋檐、栅栏-口、宀、冖、门、册、聿、户字根，例如-台、乔、单、嘉、宙、安、宜、同、闳、栅、肇、扉、戽。山字根-山、丘、艮字根，例如-崇、峰、嵋、峨、巖、岳、良。平原字根-平、原、田、例如-萍、愿、叠。
# 8、降格一士、卿、臣、亚、相。例如-志、颐、亚、想、壮。
# 9、降格-大龙变小龙，“巳”字根-虫、廴、辶、毛、弓、巳。例如-虹、建、迎、迪、连、张、巽。
# 10、降格，“人”字根-人、亻、彳。例如:仙、任、仲、杰、复、介、信、伦、徐。


# 喜用字
# 3划：子、上、大、巾
# 4划：水、太、日、天、丹、孔、日、午、五、王
# 5划：永、玉、主、立、申、北、市、令、巨、旦
# 6划：存、旭、字、汀、好、衣、羽、求、早、光、朱
# 7划：汝、彤、君、孝、言、李、江
# 8划：明、承、旺、昆、升、昊、昌、孟、坤、长、宗、易、雨、采、青、沛、昀、昕、朋、朔、沂、汪、函
# 9划：泰、昶、彦、泉、昱、厚、皇、泊、是、勃、春、映、泳、珏、音、南、玥、星、奕、宣、昭、冠、姵、纪
# 10划：晃、晋、时、洧、素、玲、纯、洛、晏、津、书、洵、珂、育、纮、神、珅马、袁、洪
# 11划：绅、将、绍、朗、紫、婕、珮、凰、彩、珠、涓、翎、浩、常、浮、海、晞、珪、晨、婧、康
# 12划：清、淼、、朝、翔、淦、胜、焜、媛、媚、丝、晶、晴、景、绚、咏、涵、淳、球、晰、智、云、淀、絜、絮、雅、捷、期、注、淋、涪、珺、渊、络、曾
# 13划：诠、煌、扬、琨、禄、会、旸、驰、鼎、琮、湘、湄、琳、绢、暄、焕、靖、湖、盟、暖、晖、诗、圣、漆、煊、睛、驯、湜、汤、雷、詹
# 14划：绪、彰、睿、畅、綦、誓、凤、祯、瑀、綵、绵、绮、菁、纶、裳、维、绰、绿、察、滋、細、瑗、瑄、瑜、瑚、温
# 15划：影、漳、震、赐、霆、论、谅、娟、缇、满、莹、致、绿、靓、缃、霈、玛、谊、谆
# 16划：潮、璋、翰、勋、缙、洁、静、萦、学、晓、昙、谕、谚、霖、锦、澐、润、霑、澔、谛、霍
# 17划：鸿、骏、绩、谦、誊、璟、孺、阳、蔡
# 18划：濬、曜、绣、鹃、潍、濡、璨、织、濶
# 19划：玺、鹏、璇、滢、丽、韵、宠
# 20划：瀚、腾、骞、飘、缤、潆、耀
# 21划：籐、藤
# 22划：蔼
# 24划：灵、雳




#木生火，火生土，土生金，金生水，水生木
#木克土，土克水，水克火、火克金、金克木

#指定笔画
g_assign_num = [[8,8],[8,10],[8,16],[8,17],[9,2],[9,15],[9,16],[10,6],[10,7],[10,15],[11,6],[11,7],[11,14],[18,6],[18,7],[20,5],[22,10],
                ]

#指定五行
g_assign_wuxing = []
# g_assign_wuxing = ["水","木"]
# g_assign_wuxing = ["金","水"]

#排除文字
g_exclude_word = []

#指定文字
g_assign_word = ["南"]

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


    while True:
         try:
            print("press any key to continue:")
            s = input()

            if s == "q":
                 break;
            
            f.write("--------------------------\n")
            f.flush()
            for i in range(10):

                lll = len(name_list)
                if lll <= 0:
                    print("no result any more")
                    break;

                index = random.randint(0, lll - 1)

                

                ss = name_list[index]
                print(ss)

                f.write(ss)
                f.write("\n")
                f.flush()

                del name_list[index]


            
         except Exception as e:
             traceback.print_exc()
             print('Have a rest, then continue...')
         
    
    f.close()

                




if __name__ == '__main__':
    main()