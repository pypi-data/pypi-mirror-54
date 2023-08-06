import pickle
import os,re
class Vocab:
    def __init__(self,file='vectorizer.pk'):
        self.vocab_file = file
        pass
    def remove(self):
        if os.path.exists(self.vocab_file):
        #删除文件，可使用以下两种方法。
            os.remove(self.vocab_file)
        #os.unlink(my_file)
        else:
            print ('no such file:%s'%self.vocab_file)

    def bulid_vectorizer(self,sentences):
        """
        sentences=['生 的 小猫 也 爱吃 鸡蛋', '真是 好有爱 的 一对']
        word_dict  
        """

        word_list = " ".join(sentences).split()
        word_dict=self.add_vectorizer( word_list)
        # self.save(word_dict)
        return word_dict
    def save(self, word_dict):
        """
        保存词典
        """
        with open(self.vocab_file, 'wb') as fin:
        # pickle.dump(cv, fin)
            pickle.dump(word_dict, fin)
    def load(self):
        """
        加载词典
        """
        if os.path.exists(self.vocab_file):
        # 加载模型
            word_dict=pickle.load(open(self.vocab_file, "rb"))
            
        else:
            word_dict= {}
        return word_dict
    def add_vectorizer(self, text_arr):
        """
        添加新的字典元素
        """
        word_dict=self.load()
        word_arr=list(word_dict.keys())
        # print(word_arr)
        # word_arr=word_arr+text_arr
        for word in text_arr:
            word_arr.append(word)

        # word_list = list(set(word_arr))
        # word_list=word_arr
        # print(word_list)
        word_dict = {w: i for i, w in enumerate(word_arr)}
        self.save(word_dict)

        return word_dict

        

    def get_vectorizer(self, text_arr):
        """
        text_arr=['哈士奇','柯基犬']

        text_ids=[0, 8, 7, 4, 6, 1, 5, 6, 9, 2, 3]
        """
        if os.path.exists(self.vocab_file):
        # 加载模型
            word_dict=self.load()
        # print(vocabulary) 
        else:
            word_dict=self.bulid_vectorizer(text_arr)
        text_ids=[]
        for word in text_arr:
            try:
                text_ids.append(word_dict[word])
            except :
                word_dict=self.add_vectorizer([word])
                
                text_ids.append(word_dict[word]) 
        # print(word_dict)
        # print(text_ids)
        return text_ids
    def text_voc_ids(self,text):
        """
        逐字获取voc值
        """
        # print(list(a))
        word_list=list(text)
        vocab_list=self.get_vectorizer(word_list)
        # print(vocab_list)
        return vocab_list

# #测试代码
# text = "哈士奇 dam cat he 柯基犬"
# word_list = text.split()
# print('word_list',word_list)

# t = Vocab()
# ids = t.get_vectorizer(word_list)
# print(ids)



# sentences=['生 的 小猫 也 爱吃 鸡蛋', '真是 好有爱 的 一对']
# word_dict=t.bulid_vectorizer(sentences)
# print("word_dict",word_dict)

#  add_vectorizer(self, text_arr)

import requests
import os
class GVocab:
    """   这个是自动 获取 
    """
    def __init__(self,path="./"):
        self.vocab_file = path+"vocab.txt"
        #自动加载
        self.vocab=self.load()
        pass
    def download(self):
        print( "downloading with requests")
        url = 'https://raw.githubusercontent.com/napoler/AutoBUlidVocabulary/master/vocab.txt' 
        r = requests.get(url) 
        with open( self.vocab_file, "wb") as code:
            code.write(r.content)

    def load(self):
        """
        这里加载
        """
        if os.path.exists( self.vocab_file):
            pass
        else:
            self.download()

        f = open( self.vocab_file,"r")  
        lines = f.readlines()#读取全部内容  
        vocab={}
        for i,line in enumerate(lines): 
            # print( line  )
            vocab[line[:-1]]=i
        return vocab
    def get(self,word_list):
        """
        获取词的向量
        """
        ids=[]
        # print(self.vocab)
        for word in word_list:
            try:
                ids.append(self.vocab[word])
            except:
                ids.append(self.vocab['[UNK]'])   
        return ids
    def bulid(self,word_list):
        return   self.get(word_list)
    def text_voc_ids(self,text):
        # import jieba
        # jieba.load_userdict( self.vocab_file)
        """
        逐字获取voc值
        """
        # # print(list(a))

        # word_list=list(text)
        # # word_list=[]
        # # for word in jieba.cut(text):
        # #     word_list.append(word)
        # print(word_list)
        # while ' ' in word_list:
        #     word_list.remove(' ')
        word_list=self.text_list(text)
        vocab_list=self.bulid(word_list)
        return vocab_list
    def text_list(self, text):
        """
        文本转化成数组
        """
        # text = re.sub(r'[^\w\s]','',text)
        word_list=list(text)
        # word_list=[]
        # for word in jieba.cut(text):
        #     word_list.append(word)
        # print(word_list)
        while ' ' in word_list:
            word_list.remove(' ')
        return word_list
    
    def sentence_ids(self,text,text_len=0):
        #"""自动对句子标记开始结束  自动修剪和添加""""
        #text 文字
        #text_len 数字长度
        text_list=   self.text_list(text)
        if text_len == 0:
            text_list=['[CLS]']+text_list+['[SEP]']   
        elif text_len > len(text_list):
           text_list=['[CLS]']+text_list+['[SEP]']+['[PAD]']*(text_len-len(text_list))
        elif text_len < len(text_list):
            text_list=['[CLS]']+text_list[:text_len]+['[SEP]']
        else:
            text_list=['[CLS]']+text_list+['[SEP]']
        ids_list=self.get(text_list)  
        return ids_list
    def sentence_ids_list(self,text_list=[],text_len=0):
        #"""自动对句子标记开始结束  自动修剪和添加""""
        #text 文字
        #text_len 数字长度
        if text_len == 0:
            text_list=['[CLS]']+text_list+['[SEP]']   
        elif text_len > len(text_list):
           text_list=['[CLS]']+text_list+['[SEP]']+['[PAD]']*(text_len-len(text_list))
        elif text_len < len(text_list):
            text_list=['[CLS]']+text_list[:text_len]+['[SEP]']
        else:
            text_list=['[CLS]']+text_list+['[SEP]']
        ids_list=self.get(text_list)  
        return ids_list