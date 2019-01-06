from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .secret import SECRET_CLARIFAI_API_KEY
import base64
import os

# pull key from env or secret.py as fallback
CLARIFAI_API_KEY = os.environ.get('CLARIFAI_API_KEY', SECRET_CLARIFAI_API_KEY)

# import python ClarifaiApp
from clarifai.rest import ClarifaiApp
cf_app = ClarifaiApp(api_key=CLARIFAI_API_KEY)

# View Functions for /image routes

# csrf added to handle POST request not related to FE Form
@csrf_exempt
def images(request):
    """
    Handles all requests for /image route, methods: GET, POST
    """
    if request.method == 'POST':

        # do stuff to return JSON response to clarifai
        #body_unicode = request.body.decode('utf-8')

        # get encoded base64 pic from post request
        encodedpic = request.POST.get('encodedpic')


        #encodedpic = body["encodedpic"]

        # # set clarifai model to use
        model = cf_app.public_models.general_model

        # import pdb
        # pdb.set_trace()

        # base64_bytes = base64.b64encode(bytes(encodedpic))
        # # send request to clarifai
        
        # get dict from clarifai
        raw_response = model.predict_by_base64(bytes(encodedpic, 'UTF-8'))

        # get list of dicts representing relations
        response = raw_response['outputs'][0]['data']['concepts']

        relations = [{ "association": concept['name'], "value": concept['value'] } for concept in response]


        # response = json.loads(raw_response)

        # { relations: [{ association: name, confidence: value }] };

        return JsonResponse({
            "relations": relations
        })

    # otherwise return get request JSON
    elif request.method == 'GET':
        # raw_response is a generator
        raw_response = cf_app.models.get_all();

        # list of model objects from generator
        response_list = list(raw_response);

        # create list of models dicts
        response_models = [model.dict() for model in response_list]

        # extract just name and id from model
        models = [{ "name" : model_dict['model']['name'], "id" : model_dict['model']['id'] } for model_dict in response_models]

        return JsonResponse({'message': 'Clarifai Models', 'models': models})

    else:
        return JsonResponse({'message': 'Nothing to do!'})