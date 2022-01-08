import logging
import json
import azure.functions as func


import os
from azure.core.exceptions import ResourceNotFoundError
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.formrecognizer import DocumentModelAdministrationClient
from azure.core.credentials import AzureKeyCredential
import subprocess

endpoint = "https://<your-form-recognizer-resource-name>.cognitiveservices.azure.com/"
key = "<your-form-recognizer-key>"

credential = AzureKeyCredential(key)

document_analysis_client = DocumentAnalysisClient(endpoint, credential)
model_id = "<your-model-id>"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        body = json.dumps(req.get_json())
    except ValueError:
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )
    
    if body:
        result = compose_response(body)
        return func.HttpResponse(result, mimetype="application/json")
    else:
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )

def compose_response(json_data):
    values = json.loads(json_data)['values']
    
    # Prepare the Output before the loop
    results = {}
    results["values"] = []
    
    for value in values:
        output_record = transform_value(value)
        if output_record != None:
            results["values"].append(output_record)
    return json.dumps(results, ensure_ascii=False)


def transform_value(value):
    try:
        recordId = value['recordId']
    except AssertionError  as error:
        return None

    # Validate the inputs
    try:         
        assert ('data' in value), "'data' field is required."
        data = value['data']        
        assert ('fileurl' in data), "'fileurl' field is required in 'data' object."
    except AssertionError  as error:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Error:" + error.args[0] }   ]       
            })

    try:                
        filename = value['data']['fileurl']
        docUrl = "https://<your-storage-account-name>.blob.core.windows.net/edited/"+filename+"?sp=racwdli&st=<>&se=<>&spr=https&sv=<>&sr=c&sig=<>"
        poller = document_analysis_client.begin_analyze_document_from_url(model=model_id, document_url=docUrl)
        result = poller.result()
        return_dict = {}
        for analyzed_document in result.documents:
            for name, field in analyzed_document.fields.items():
                return_dict.update({name: field.value})
        toplam = float(return_dict['toplam'])
        isim = return_dict['isim']
        firma = return_dict['firma']
        seri_no = return_dict['seri_no']
        date_time_str = return_dict['tarih']
        if "/" in date_time_str:
            s = ''.join(x for x in date_time_str if x.isdigit())
            modified_date="{}-{}-{}T00:00:00Z".format(s[4:8],s[2:4],s[0:2])
        else:
            splitted = date_time_str.split(".")
            modified_date="{}-{}-{}T00:00:00Z".format(splitted[2],splitted[1],splitted[0])
    except:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Could not complete operation for record." }   ]       
            })

    return ({
            "recordId": recordId,
            "data": {
                "toplam": toplam,
                "tarih": modified_date,
                "isim": isim,
                "seri_no": seri_no,
                "firma": firma     
                    },
            "errors": None,
            "warnings": None
            })

