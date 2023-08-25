import logging

import azure.functions as func

import json
import pickle
from io import StringIO
import pandas as pd
import numpy as np
from scipy.spatial import distance

logging.info('Import OK.')

def main(req: func.HttpRequest, clicks, embdg) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    req_body = req.get_json()
    userId = req_body['userId']
    logging.info(f'Selected user ID is {userId}')
    articles_embeddings = pickle.loads(embdg.read())
    clicks_final = clicks.read()

    s=str(clicks_final,'utf-8')
    clicks_final = StringIO(s) 
    clicks_final=pd.read_csv(clicks_final)

    var = clicks_final.loc[clicks_final['user_id']==userId]['click_article_id'].tolist()
    value = var[-1]
    distances = distance.cdist([articles_embeddings[value]], articles_embeddings, "cosine")[0]
    result = np.argsort(distances)[1:6]
    result = result.tolist()

    recommandations = json.dumps(result)
    return func.HttpResponse(recommandations)