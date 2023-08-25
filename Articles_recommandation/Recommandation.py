import numpy as np
from scipy.spatial import distance

def top5(articles_embeddings, userId, clicks_final):
    # get all articles read by user
    var = clicks_final.loc[clicks_final['user_id']==userId]['click_article_id'].tolist()
    
#     #chose randomly one
#     value = randint(0, len(var))
#     print(value)
    
    # chose last one --> le plus proche en terme de préférence
    value = var[-1]
#     print(value)

    # get 5 articles the most similar to the selected one
    distances = distance.cdist([articles_embeddings[value]], articles_embeddings, "cosine")[0]
    
    # find indexes except the one selected
    result = np.argsort(distances)[1:6]
    
"""
    # similarity value between selected article and 5 top proposed articles (the smaller the better!)
    similarite = distance.cdist([articles_embeddings[value]], articles_embeddings[result], "cosine")[0]
    return result, similarite
"""