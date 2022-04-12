import string
import nltk
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer

nltk.download('stopwords')
words_pack = stopwords.words("russian")
morph = MorphAnalyzer(lang='ru')


def pymorphy_preproc(line):
    return [morph.parse(word)[0].normal_form for word in line]


def del_stopwords(line, words_pack):
    filtered_line = []
    for word in line.split(' '):
        if word not in words_pack:
            filtered_line.append(word)
    return filtered_line


def preproc_line(line, stop_words=words_pack):
    line = ''.join(i for i in line if not i.isdigit())
    line = ' '.join(line.split())
    line = line.translate(str.maketrans('', '', string.punctuation))
    line = line.lower()
    if len(stop_words):
        line = del_stopwords(line, stop_words)
    line = pymorphy_preproc(line)
    #line = ' '.join(line)
    return line
