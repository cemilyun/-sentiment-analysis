import streamlit as st
import pandas as pd
import os
import json
import sys
import plotly.graph_objects as go
from tensorflow import keras
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.preprocessing.text import Tokenizer
import tensorflow as tf
import numpy as np
import pickle
import itertools
from tensorflow.keras.models import load_model
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
def loadModel(aList):
    model = load_model('model.h5')
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    statement = aList.copy()
    statement = pad_sequences(tokenizer.texts_to_sequences(statement), maxlen=model.input_shape[1])
    statement.shape
    predd = model.predict(statement)
    predd = np.where(predd > 0.6, 1, 0)
    i = 0
    return_list=[]
    olumlu = []
    olumsuz = []
    while i < len(predd):
        if predd[i] == 1:
            olumlu.append(aList[i])
            return_list.append(predd[i])
        else:
            olumsuz.append(aList[i])
            return_list.append(predd[i])
        i += 1
    return return_list, olumlu, olumsuz


st.title("Sentiment Analysis")
files = [f for f in os.listdir('.') if os.path.isfile(f)]
dosyalar = []
for f in files:
    if f.endswith(".json"):
        f = f.replace(".json", "").replace("_"," ")
        dosyalar.append(f)

tweet = st.selectbox("Görüntülemek istediğiniz tweeti seçiniz",dosyalar)
tweet = tweet.replace(" ","_")
if st.button('Çalıştır') and tweet != "":
    try:
        tweetJson = [json.loads(line) for line in open(tweet + ".json", 'r', encoding="utf-8")]
        expander = st.expander("Tweetler")
        for i in range(len(tweetJson)):
            expander.write(str(i)+". "+ tweetJson[i]['tweet'])
            st.write()
    except FileNotFoundError as err:
        st.error("Böyle bir dosya bulunamadı.")

elif tweet == "":
    st.error("Lütfen bir tweet giriniz.")


analysis = st.selectbox("Analizi yapılacak tweeti seçiniz",dosyalar)
analysis = analysis.replace(" ", "_")
pozCount = 0
negCount = 0


if st.button('Analiz Yap') and analysis != "":
    analysisJson = [json.loads(line) for line in open(analysis + ".json", 'r', encoding="utf-8")]
    tweetler = []
    for i in range(len(analysisJson)):
        tweetler.append(analysisJson[i]['tweet'])
    st.success(f"Analiz başarıyla tamamlandı. Analiz edilen tweet sayısı: {len(tweetler)}")
    yeni, olumlu, olumsuz = loadModel(tweetler)
    for i in yeni:
        if i == 1:
            pozCount += 1
        elif i == 0:
            negCount += 1

    countList = ['Pozitif','Negatif']
    values = [pozCount, negCount]
    fig = go.Figure(go.Pie(labels=countList, values=values, hoverinfo="label+percent",textinfo="value"))
    st.header("Analiz:")
    st.plotly_chart(fig)
    olumluTweets = st.expander("Olumlu Tweetler")
    for i in range(len(olumlu)):
        olumluTweets.write(str(i) + ". " + olumlu[i])
        st.write()
    olumsuzTweets = st.expander("Olumsuz Tweetler")
    for i in range(len(olumsuz)):
        olumsuzTweets.write(str(i) + ". " + olumsuz[i])
        st.write()
elif analysis == "":
    st.error("Lütfen analiz yapılacak tweet giriniz.")


