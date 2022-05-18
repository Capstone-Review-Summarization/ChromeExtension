from this import d
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


class Summarization:
    def __init__(self):
        self.rouge = Rouge()

    def summarize_reviews(self, content_list):
        if (len(content_list) <= 1):
            return content_list
        while (len(content_list) > 1):
            text_clusters = self.clustering(content_list)
            for i in range(len(text_clusters[0])):
                text_clusters[0][i].strip()
            wre_clusters = self.weak_ref_ext(text_clusters)
            wre_text_clusters = self.clustering(wre_clusters)
            final_summary = self.summarizer(wre_text_clusters)
            content_list = final_summary
        return final_summary

    def clustering(self, corpus_for_clustering):
        cluster = []
        clusters = []
        token_len = 0

        if(len(corpus_for_clustering) <= 2):
            clusters = [review for review in corpus_for_clustering]

        while len(corpus_for_clustering) > 2:
            pivot_data = random.choice(corpus_for_clustering)
            token_len = len(sent_tokenize(pivot_data))
            cluster = [pivot_data]
            df_cluster = pd.DataFrame(columns=['text', 'rouge-1 score'])
            # getting rouge-1 f1 score for all data wrt to pivot_data
            for j in range(len(corpus_for_clustering)):
                if (pivot_data != corpus_for_clustering[j]):
                    scores = rouge.get_scores(
                        pivot_data, corpus_for_clustering[j])
                    df_cluster = df_cluster.append(
                        {'text': corpus_for_clustering[j], 'rouge-1 score': scores[0].get('rouge-1').get('f')}, ignore_index=True)
            df_cluster.sort_values("rouge-1 score", axis=0,
                                   ascending=False, inplace=True, na_position='last')
            token_len = token_len + \
                len(sent_tokenize(df_cluster['text'][0])) + \
                len(sent_tokenize(df_cluster['text'][1]))
            already_in_cluster = [pivot_data,
                                  df_cluster['text'][0], df_cluster['text'][1]]
            for k in range(2, len(df_cluster)):
                if(len(sent_tokenize(corpus_for_clustering[k])) + token_len < 512):
                    token_len = token_len + \
                        len(sent_tokenize(corpus_for_clustering[k]))
                    cluster.append(corpus_for_clustering[k])
                    df_cluster.drop(k, inplace=True)
                    already_in_cluster.append(corpus_for_clustering[k])
                else:
                    break
            corpus_for_clustering = [
                review for review in corpus_for_clustering if review not in already_in_cluster]
            del df_cluster
            clusters.append(cluster)
            cluster = []
        return clusters

    def weak_ref_ext(self, content_list):
        total_score = 0
        review_f1score_pair = {}
        wre = []
        for cluster in content_list:
            review_list = cluster
            review_list = list(set(review_list))
            for review in review_list:
                if(review != '\n'):
                    for other_review in review_list:
                        if(other_review != review):
                            score = rouge.get_scores(review, other_review)
                            total_score = total_score + \
                                score[0].get('rouge-1').get('f') / \
                                (len(review_list) - 1)
                    review_f1score_pair[review] = total_score
                    total_score = 0
            {k: v for k, v in sorted(
                review_f1score_pair.items(), key=lambda item: item[1])}
            wre.append(list(review_f1score_pair.keys())[-1])
            review_f1score_pair = {}
        return wre

    def summarizer(self, content_list):
        summaries = []
        bert_model = Summarizer()
        for i in range(len(content_list)):
            body = content_list[i]
            bert_summary = ''.join(bert_model(body, min_length=60))
            summaries.append(bert_summary)
        return summaries
