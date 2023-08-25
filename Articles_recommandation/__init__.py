import logging
import pandas as pd
from scipy.spatial import distance
#from .Recommandation import top5
import pickle
import azure.functions as func
import json
import numpy as np

with open("C:\\Users\\pcasaux\\OneDrive - Castelis\\Documents\\OCR\\P9\\dataset\\news-portal-user-interactions-by-globocom\\articles_embeddings.pickle", 'rb') as file_pi:
    #Documents\\articles_embeddings.pickle", 'rb') as file_pi:
  #  C:\Users\pcasaux\OneDrive - Castelis\Documents\OCR\P9\dataset\news-portal-user-interactions-by-globocom
    articles_embeddings = pickle.load(file_pi)
        
clicks = pd.read_csv('C:\\Users\\pcasaux\\OneDrive - Castelis\\Documents\\OCR\\P9\\dataset\\news-portal-user-interactions-by-globocom\\clicks_tot.csv')
old_clicks = pd.read_csv('C:\\Users\\pcasaux\\Documents\\clicks_tot.csv')
var = clicks.loc[clicks['user_id']==1234]['click_article_id'].tolist()
value=var[-1]
print(value)

def top5(articles_embeddings, userId, clicks_final):
    # get all articles read by user
    var = clicks_final.loc[clicks_final['user_id']==userId]['click_article_id'].tolist()
    
#     #chose randomly one
#     value = randint(0, len(var))
#     print(value)
    
    # chose last one --> le plus proche en terme de préférence
    value = var[-1]
    print(value)

    # get 5 articles the most similar to the selected one
    distances = distance.cdist([articles_embeddings[value]], articles_embeddings, "cosine")[0]
    
    # find indexes except the one selected
    result = np.argsort(distances)[1:6]
    

    # similarity value between selected article and 5 top proposed articles (the smaller the better!)
    similarite = distance.cdist([articles_embeddings[value]], articles_embeddings[result], "cosine")[0]
    return result, similarite


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    userID = req.params.get('userID')
    
    if not userID:
        return func.HttpResponse(
             "Vous n'avez pas rentré de userID das l'URL, exemple : ?userID=1234",
             status_code=404
        )
    
    if not userID.isdigit():
        return func.HttpResponse(
             "Vous avez rentré un userID qui n'est pas une suite de chiffres, exemple : ?userID=1234",
             status_code=404
        )
        
        
    result, similarite=top5(articles_embeddings,int(userID),clicks)
    
    return func.HttpResponse(json.dumps(result.tolist()), mimetype="application/json")
"""
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
"""