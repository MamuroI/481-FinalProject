from zipfile import ZipFile
import fnmatch
import pandas as pd
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import words as Word
import nltk
from nltk.stem import PorterStemmer
import rarfile
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from scipy import sparse
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def preProcess(s):
    s = word_tokenize(s)
    stopwords_set = set(stopwords.words())
    stop_dict = {s: 1 for s in stopwords_set}
    s = [w for w in s if w not in stop_dict]
    s = ' '.join(s)
    return s

def tf(text,info):
    test = text
    print(test)
    cleaned_description = info
    vectorizer = CountVectorizer(preprocessor=preProcess, ngram_range=(1, 3))
    cleaned_description_cv = vectorizer.fit_transform(cleaned_description)
    cleaned_description_cv.data = np.log10(cleaned_description_cv.data+1)
    X = pd.DataFrame(cleaned_description_cv.toarray(), columns=vectorizer.get_feature_names_out())
    extracted_word = vectorizer.fit_transform([test])
    specific_col = vectorizer.inverse_transform(extracted_word)
    result_col = X.columns.intersection(set(specific_col[0]))
    result_dataframe = X[result_col]
    sum_x_axis = result_dataframe.sum(axis=1)
    last_result = sum_x_axis.sort_values(ascending=False)
    last_last_result = last_result.iloc[:10]
    return last_last_result.index[0]

def tf_idf(text,info):
    cleaned_description = info
    vectorizer = CountVectorizer(preprocessor=preProcess, ngram_range=(1, 3))
    X = vectorizer.fit_transform(cleaned_description)
    idf = len(info) / (X.tocoo() > 0).sum(0)
    X.data = np.log10(X.data + 1)
    X = X.multiply(np.log10(idf))
    input_tv = vectorizer.transform([text])
    cosine_sim = cosine_similarity(X, input_tv).flatten()
    result1 = pd.DataFrame(cosine_sim)
    result2 = result1.sort_values([0], ascending=False)
    result3 = result2.iloc[:5]
    return result3.index[0]

class BM25(object):
    def __init__(self, b=0.75, k1=1.6):
        self.vectorizer = TfidfVectorizer(preprocessor=preProcess, norm=None, smooth_idf=False, ngram_range=(1, 3))
        self.b = b
        self.k1 = k1

    def fit(self, X):
        self.vectorizer.fit(X)
        y = super(TfidfVectorizer, self.vectorizer).transform(X)
        self.avdl = y.sum(1).mean()

    def transform(self, q, X):

        b, k1, avdl = self.b, self.k1, self.avdl

        # apply CountVectorizer
        X = super(TfidfVectorizer, self.vectorizer).transform(X)
        len_X = X.sum(1).A1
        q, = super(TfidfVectorizer, self.vectorizer).transform([q])
        assert sparse.isspmatrix_csr(q)

        # convert to csc for better column slicing
        X = X.tocsc()[:, q.indices]
        denom = X + (k1 * (1 - b + b * len_X / avdl))[:, None]
        # idf(t) = log [ n / df(t) ] + 1 in sklearn, so it need to be coneverted
        # to idf(t) = log [ n / df(t) ] with minus 1
        idf = self.vectorizer._tfidf.idf_[None, q.indices] - 1.
        numer = X.multiply(np.broadcast_to(idf, X.shape)) * (k1 + 1)
        return (numer / denom).sum(1).A1