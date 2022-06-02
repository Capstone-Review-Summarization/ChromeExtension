import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from keras.preprocessing.text import Tokenizer
from nltk.tokenize import word_tokenize
from keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import keras
import numpy as np
from rouge import Rouge
import random
from nltk.tokenize import sent_tokenize
from summarizer import Summarizer
import nltk


class SentimentAnalysis:
    def __init__(self, preprocess):
        self.preprocess = preprocess
        pass

    def predict_model(self):
        model = tf.keras.models.load_model('C:\\Users\\Divyang\\Desktop\\ChromeExtension\\Summarized Review Extension - Server\\summarization\\model12.hdf5')
        for i in range(len(self.preprocess.reviews_scraped_df['reviewCleaned'])):
            review = [self.preprocess.reviews_scraped_df['reviewCleaned'][i]]
            self.vectorize(review)
            sentiment = model.predict(self.review, batch_size=1, verbose=0)[0]
            if (np.argmax(sentiment) == 1):
                self.preprocess.temp_positive_reviews = pd.DataFrame({'reviewText': [self.preprocess.reviews_scraped_df['reviewText'][i]], 'reviewCleaned': [self.preprocess.reviews_scraped_df['reviewCleaned'][i]]})
                self.preprocess.positive_reviews = pd.concat([self.preprocess.positive_reviews, self.preprocess.temp_positive_reviews], ignore_index = True, axis = 0)
            elif (np.argmax(sentiment) == 0):
                # self.preprocess.negative_reviews = self.preprocess.negative_reviews.append(
                #     {'reviewText': self.preprocess.reviews_scraped_df['reviewText'][i],
                #      'reviewCleaned': self.preprocess.reviews_scraped_df['reviewCleaned'][i]
                #      }, ignore_index=True)
                self.preprocess.temp_negative_reviews = pd.DataFrame({'reviewText': [self.preprocess.reviews_scraped_df['reviewText'][i]], 'reviewCleaned': [self.preprocess.reviews_scraped_df['reviewCleaned'][i]]})
                self.preprocess.negative_reviews = pd.concat([self.preprocess.negative_reviews, self.preprocess.temp_negative_reviews], ignore_index = True, axis = 0)
        corpus_for_positive_clustering = self.preprocess.positive_reviews['reviewText'].tolist(
        )
        self.corpus_for_positive_clustering = corpus_for_positive_clustering
        print(self.corpus_for_positive_clustering)
        corpus_for_negative_clustering = self.preprocess.negative_reviews['reviewText'].tolist(
        )
        
        self.corpus_for_negative_clustering = corpus_for_negative_clustering
        print("Negative Cluster")
        print(self.corpus_for_negative_clustering)

    def vectorize(self, review):
        max_features = 2000
        tokenizer = Tokenizer(num_words=max_features, split=' ')
        tokenizer.fit_on_texts(
            self.preprocess.reviews_scraped_df['reviewCleaned'].values)
        X = tokenizer.texts_to_sequences(
            self.preprocess.reviews_scraped_df['reviewCleaned'].values)
        X = pad_sequences(X)
        self.tokenizer = tokenizer
        review = self.tokenizer.texts_to_sequences(review)
        # padding the review to have exactly the same shape as `embedding_2` input
        self.review = pad_sequences(review, maxlen=488, dtype='int32', value=0)
