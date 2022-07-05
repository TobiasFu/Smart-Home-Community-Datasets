#Creating n-grams, sort and group them 
import pandas as pd 
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.pipeline import make_pipeline
nltk.download('stopwords')


##How to access the data
with open("automation_posts_12_06.csv", 'r', encoding='utf-8') as f:
    # deserialize file to Python object
    my_data = pd.read_csv(f)


##list of texts 
texts = []
for val in my_data.values():
    for post in val["posts"]:
        texts.append(post['text'])

#list to pandas data frame 
df = pd.DataFrame(texts)
df.columns = ['post'] 

#data frame for all titles 
titles = []
for val in my_data.values():
    titles.append(val['topicname'])

title = pd.DataFrame(titles)
title.columns = ['title']

#n-grams
from nltk.corpus import stopwords
stoplist = stopwords.words('english') + ['though','00','000','0000','2021','20','21','19','18','17','16']
print(stoplist)

##Creation and counting of n-grams 
from sklearn.feature_extraction.text import CountVectorizer
c_vec = CountVectorizer(stop_words=stoplist, ngram_range=(3,3)) #size of n-grams
# matrix of ngrams
ngrams = c_vec.fit_transform(df['post']) #which data
# count frequency of ngrams
# count_values = ngrams.toarray().sum(axis=0)
count_values = ngrams.sum(axis=0).tolist()[0]
# list of ngrams
vocab = c_vec.vocabulary_
df_ngram = pd.DataFrame(sorted([(count_values[i],k) for k,i in vocab.items()], reverse=True)
            ).rename(columns={0: 'frequency', 1:'bigram/trigram'})
print(df_ngram[0:60]) #print (how many?)

##Create topic groups and print them
#NMF Model
tfidf_vectorizer = TfidfVectorizer(stop_words=stoplist, ngram_range=(3,3)) #size of the n-grams
nmf = NMF(n_components=20) #number of groups 
pipe = make_pipeline(tfidf_vectorizer, nmf)
pipe.fit(title['title']) #which dataset
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += ", ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()
print_top_words(nmf, tfidf_vectorizer.get_feature_names(), n_top_words=10) #print

'''
#LDA model (alternative to NMF Model)
from sklearn.decomposition import LatentDirichletAllocation
tfidf_vectorizer = TfidfVectorizer(stop_words=stoplist, ngram_range=(2,3))
lda = LatentDirichletAllocation(n_components=10)
pipe = make_pipeline(tfidf_vectorizer, lda)
pipe.fit(df['post'])
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += ", ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()
print_top_words(lda, tfidf_vectorizer.get_feature_names(), n_top_words=10)
'''