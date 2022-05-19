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


class Preprocess:
    def __init__(self, reviews_scraped):
        self.reviews_scraped = reviews_scraped

    def pre_process_data(self):
        reviews_scraped_df = pd.DataFrame(
            self.reviews_scraped, columns=['reviewText'])
        reviews_scraped_df['reviewCleaned'] = ''
        reviews_scraped_df['reviewText'] = reviews_scraped_df['reviewText'].str.replace(
            '\n', ' ')
        reviews_scraped_df["reviewCleaned"] = reviews_scraped_df["reviewText"].apply(
            lambda x: self.clean_reviews(str(x)))
        reviews_scraped_df.reviewCleaned = reviews_scraped_df.reviewCleaned.astype(
            str)
        self.reviews_scraped_df = reviews_scraped_df
        self.positive_reviews = pd.DataFrame(
            columns=['reviewText', 'reviewCleaned'])
        # print(reviews_scraped_df.head())
        self.negative_reviews = pd.DataFrame(
            columns=['reviewText', 'reviewCleaned'])

    def clean_reviews(self, text):
        # this function performs following
        # 1. stripping the text from any leading or trailing whitespaces
        # 2. convert text to lowercase
        # 3. tokenize and remove punctuation
        # 4. remove words that contain numbers
        # 5. remove duplicates
        # 6. remove empty tokens
        # 7. pos tag text
        # 8. lemmatize text
        # 9. remove words with only one letter

        text.strip()
        text = text.lower()
        text = [word.strip(string.punctuation) for word in text.split(" ")]
        text = [word for word in text if not any(c.isdigit() for c in word)]
        text = list(set(text))
        text = [t for t in text if len(t) > 0]
        pos_tags = pos_tag(text)
        text = [WordNetLemmatizer().lemmatize(t[0], self.get_wordnet_pos(t[1]))
                for t in pos_tags]
        text = [t for t in text if len(t) > 1]
        text = " ".join(text)
        return text

    def get_wordnet_pos(self, pos_tag):
        if pos_tag.startswith('J'):
            return wordnet.ADJ
        elif pos_tag.startswith('V'):
            return wordnet.VERB
        elif pos_tag.startswith('N'):
            return wordnet.NOUN
        elif pos_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN
