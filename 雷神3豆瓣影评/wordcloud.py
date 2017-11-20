import codecs
import numpy as np
import pandas as pd
import jieba.analyse
import matplotlib.pyplot as plt
from PIL import Image
import os
from wordcloud import WordCloud,ImageColorGenerator

os.chdir("C:\\Users\\nasna\\PycharmProjects\\untitled1\\spider\\test")

f = open('content.txt','r',encoding = 'gb18030')
content = f.read()
f.close()

Thor_img =np.array(Image.open('timg2.jpg'))

jieba.analyse.set_stop_words('stopword2')
jieba.load_userdict('dict.txt')
tags = jieba.analyse.extract_tags(content, topK=120, withWeight=True)

word_frenquence = dict()
for i in tags:
    word_frenquence[i[0]] = i[1]


wc = WordCloud(background_color = 'white',mask = Thor_img,
               font_path = 'msyh.ttc')
wc.generate_from_frequencies(word_frenquence)

img_colors = ImageColorGenerator(Thor_img)
plt.imshow(wc.recolor(color_func = img_colors),interpolation = 'bilinear')
plt.axis("off")
plt.show()