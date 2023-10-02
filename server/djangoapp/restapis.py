import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
    #     if api_key:
    #         # Basic authentication GET
    #             response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
    #                                 auth=HTTPBasicAuth('apikey', api_key))
    #     else:
    #         # no authentication GET
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# def get_dealers_by_id_from_cf(url,id, **kwargs):
#     # Call get_request with a URL parameter
#     json_result = get_request(url+"?id="+str(id))
#     if json_result:
#         # Get the row list in JSON as dealers
#         dealer_doc = json_result[0]
#         print(dealer_doc)
#         # For each dealer object
#         # Create a CarDealer object with values in `doc` object
#         dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
#                                 id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
#                                 short_name=dealer_doc["short_name"],
#                                 st=dealer_doc["st"], zip=dealer_doc["zip"])
#         return [dealer_obj]
#     else:
#         return

def get_dealers_by_id_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,id=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealer_doc = json_result["body"][0]
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                short_name=dealer_doc["short_name"],
                                st=dealer_doc["st"], zip=dealer_doc["zip"])
        return dealer_obj
    return False

def get_dealer_reviews_from_cf(url, dealer_id, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url+'?dealerId='+str(dealer_id))
    if json_result:
        # Get the row list in JSON as dealers
        print(json_result)
        dealers = json_result["data"]["docs"]
        # Get its content in `doc` object
        for dealer_doc in dealers:
            review_obj = DealerReview(
                dealership=dealer_doc["dealership"],
                name=dealer_doc["name"],
                purchase=dealer_doc["purchase"],
                review=dealer_doc["review"],
                purchase_date=dealer_doc["purchase_date"], car_make=dealer_doc["car_make"],
                car_model=dealer_doc["car_model"],
                car_year=dealer_doc["car_year"],sentiment="", id=dealer_id)
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text_to_analyse):
    url = 'https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict'
    header = {"grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"}
    myobj = { "raw_document": { "text": text_to_analyse } }
    response = requests.post(url, json = myobj, headers=header)
    formatted_response = json.loads(response.text)
    try:
        if(formatted_response['documentSentiment']['label'] == "SENT_POSITIVE"):
            return "positive"
        elif(formatted_response['documentSentiment']['label'] == "SENT_NEGATIVE"):
            return "negative"
        else:
            return "neutral"
    except:
        return "error"

def post_request(url, json_payload, **kwargs):
    print(json_payload)
    response = requests.post(url, params=kwargs, json=json_payload)
    print(response.text)
    return response.text