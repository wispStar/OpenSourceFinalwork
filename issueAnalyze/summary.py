# coding=utf-8
import json
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords

def get_title_turns():
    with open('vacanza_python-holidays_issue.json', 'r',encoding='utf-8') as load_f:
        content = json.load(load_f)

    fp = open('vacanza_python-holidays_issue.txt', mode="w", encoding="utf-8")

    for data in content:
        title = data["title"]
        turns = data["turns"]
        data_str = str(title) + '\n'
        for turn in turns:
            data_str = data_str + turn + '\n'
        data_str += '\n'
        fp.write(data_str)
    fp.close()

def summary():
    with open('vacanza_python-holidays_issue.txt','r',encoding='utf-8') as f:
        t = f.read()
    stopwords_list = stopwords.words('english')

    # 分词
    w = word_tokenize(t)
    # 去除标点符号以及停止词
    w = [word for word in w if word.isalnum() and word not in stopwords_list]
    # 词性标注
    tw = pos_tag(w)
    # 提取名词
    nounwords = [name for name,value in tw if value in ['NN','NNS','NNP','NNPS']]
    # 词频统计
    d = {}
    for i in w:
        if i in d:
            d[i] += 1
        else:
            d[i] = 1
    freq_noun = {}
    for i in d.keys():
        if i in nounwords:
            freq_noun[i] = d[i]
    # 排序
    dict = sorted(freq_noun.items(),key = lambda d: d[1],reverse=True)
    with open('result.txt','w',encoding='utf-8') as f:
        [f.write(str(item)+'\n') for item in dict]
        f.close()