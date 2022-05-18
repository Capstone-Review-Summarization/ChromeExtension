import imp
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .scrapper import Scrapper
from .Model.Preprocessing import Preprocess
from .Model.SentimentAnalysis import SentimentAnalysis
from .Model.Summarization import Summarization
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def summarize(request):
    print("done")
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)

    # replace hardcoded url with request.data.url
    url = body_data.get('page_url')
    #url = "https://www.amazon.in/Columbia-Mens-wind-resistant-Glove/dp/B0772WVHPS/?_encoding=UTF8&pd_rd_w=d9RS9&pf_rd_p=3d2ae0df-d986-4d1d-8c95-aa25d2ade606&pf_rd_r=7MP3ZDYBBV88PYJ7KEMJ&pd_rd_r=550bec4d-5268-41d5-87cb-8af40554a01e&pd_rd_wg=oy8v8&ref_=pd_gw_cr_cartx&th=1"
    print(body_data.get('page_url'))
    scrap = Scrapper(url)
    review_results = scrap.scrape_reviews()
    preprocess = Preprocess(review_results)
    preprocess.pre_process_data()
    sentiment = SentimentAnalysis(preprocess)
    summarize = Summarization()
    positive_review = summarize.summarize_reviews(
        sentiment.corpus_for_positive_clustering)
    negative_review = summarize.summarize_reviews(
        sentiment.corpus_for_negative_clustering)
    print(positive_review)
    print(negative_review)
    print(len(review_results))
    return JsonResponse({"review": review_results,
                         "positive_review": positive_review,
                         "negative_review": negative_review
                         })
