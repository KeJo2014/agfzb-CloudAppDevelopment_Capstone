import sys 
import json
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict): 
    authenticator = IAMAuthenticator("oBTB7py***********************FR9gX3XPfG3")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://fc2b57ff-6ef4-******************tnosqldb.appdomain.cloud")
    
    try:
        test = dict["review"]
        request = "post"
    except:
        request = "get"
    
    if(request == "get"):
        print("GET")
        # HANDLE GET REQUEST
        response = service.post_find(
                    db='reviews',
                    selector={'dealership': {'$eq': int(dict['dealerId'])}},
                ).get_result()
        try: 
            result= {
                'headers': {'Content-Type':'application/json'}, 
                'body': {'data':response} 
                }        
            return result
        except:  
            return { 
                'statusCode': 404, 
                'message': 'Something went wrong!'
                }
    else:
        print("POST")
        # HANDLE POST REQUEST
        data = dict["review"]
        new_entry = json.loads(data)
        print(new_entry)
        new_review = service.post_document(db='reviews', document=new_entry["payload"]).get_result()
        if new_review["ok"]:
            result = {
                "headers": {"Content-Type": "application/json"},
                "body": {"message": "Review posted successfully."}
            }
    
            print(new_review)
            return result
        
        else: 
            error_json = {
                "statusCode": 500,
                "message": "Could not post review due to server error."
            }
            return error_json
        error_json = {
            "statusCode": 500,
            "message": "Could not post review due to server error."
        }
        return error_json
