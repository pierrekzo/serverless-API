"""

import streamlit as st
import pandas as pd
import requests
import pickle
import Recommandation as reco

# App title
st.title("Application de recommandation d'articles")

frame = pd.read_csv('')

# On créé une liste des 100 premiers utilisateurs pour y choisir un ID
users = frame['user_id'][:100].unique

st.write("""
# Application de recommandation d'aticles
""")
st.write("""
## Dans cette application, vous pouvez rentrer un ID d'utilisateur et elle vous retournera une recommandation de 5 articles selon les lectures passées de cet utilisateur
""")

userId = st.selectbox('Choisissez un utilisateur', options=users)

url='http://localhost:7071/api/Articles_recommandation'

with open('C:\Users\pcasaux\Documents\articles_embeddings.pickle', 'rb') as file_pi:
    articles_embeddings = pickle.load(file_pi)
    
clicks = pd.read_csv('C:\Users\pcasaux\Documents\clicks_tot.csv')

if st.button('Connect'):
    obj = {'name' : userId}
    a = requests.get(url, params = obj)
    st.write("## Nous vous recommandons de lire les articles aux Id suivants :")
    reco.top5(articles_embeddings, userId, clicks)
    st.write(a.text)
    
"""