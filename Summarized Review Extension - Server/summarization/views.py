import imp
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .scrapper import Scrapper
from .Scrapper.scrape import Scrape
from .Model.Preprocessing import Preprocess
from .Model.SentimentAnalysis import SentimentAnalysis
from .Model.Summarization import Summarization
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def summarize(request):
    body_data = {}
    if(request.body):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)

    # replace hardcoded url with request.data.url
    url = body_data.get('page_url')
    print(url)
    # url = "https://www.amazon.in/American-Tourister-AMT-SCH-03/dp/B07CGSJNML/ref=zg-bs_luggage_1/262-9775886-1400609?pd_rd_w=dt4LC&pf_rd_p=56cde3ad-3235-46d2-8a20-4773248e8b83&pf_rd_r=3B78SYQ7YPC183YD8EEP&pd_rd_r=8d3779e1-f37c-4f4d-b302-bf32891e6438&pd_rd_wg=LngMr&pd_rd_i=B09M7P15CW&th=1"
    # url = "https://www.amazon.in/Apple-iPhone-13-128GB-Midnight/dp/B09G99CW2N/ref=sr_1_1_sspa?crid=38TS22ENECN6A&keywords=iphone%2B13&qid=1651472196&sprefix=%2Caps%2C221&sr=8-1-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUE4MjA2VktTUkNaM0cmZW5jcnlwdGVkSWQ9QTAxODU3NTU4SUtTTTJZUTVOM0cmZW5jcnlwdGVkQWRJZD1BMDg3Mjc2MDFIRFRQQjNSVFZJOTEmd2lkZ2V0TmFtZT1zcF9hdGYmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl&th=1"
    # url = "https://www.amazon.in/Ben-Martin-Classic-Collar-Cotton/dp/B09YMD4D6S/ref=sr_1_2_sspa?crid=2UZYRUA2Z8ZDQ&keywords=shirts+for+men&qid=1652949639&sprefix=shirts,aps,317&sr=8-2-spons&psc=1"
    # url = "https://www.amazon.in/Lenovo-Windows-Graphics-Phantom-82B500BHIN/dp/B08GG8WCW7/ref=lp_28207186031_1_2?th=1"
    # print(body_data.get('page_url'))
    scrape = Scrape(url)
    review_results = scrape.scrape()
    # print(review_results)
    print(len(review_results))
    print(review_results)
    # review_results = scrap.scrape_reviews()
    preprocess = Preprocess(review_results)
    preprocess.pre_process_data()
    sentiment = SentimentAnalysis(preprocess)
    sentiment.predict_model()
    summarize = Summarization()
    positive_review = summarize.summarize_reviews(
        sentiment.corpus_for_positive_clustering)
    negative_review = summarize.summarize_reviews(
        sentiment.corpus_for_negative_clustering)
    
    # print("Final result")
    # print(positive_review)
    # print(negative_review)
    print(len(review_results))
    return JsonResponse({"review": review_results,
                         "positive_review" : positive_review,
                         "negative_review" : negative_review
                         })
