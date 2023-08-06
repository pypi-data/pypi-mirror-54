# AutoBUlidVocabulary
Auto BUlid Vocabulary

## 安装
```
pip install AutoBUlidVocabulary

```


## 直接使用google vocab

```
from AutoBUlidVocabulary import *

ids=GVocab(path='./test/').bulid(['哈'])
print(ids)

>>> [1506]

ids=GVocab(path='./test/').text_voc_ids("哈士奇手机")
print(ids)
```

# # 示例
```
from AutoBUlidVocabulary import Vocab

 word_list=["哈士奇","狗子"]
 vocab=Vocab()
 vocab_list=vocab.vocab_list(word_list)
 print(vocab_list)



```
