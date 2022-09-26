import datetime
import glob

import pandas as pd
import twint
import streamlit as st
#Configure

Tweets_df = pd.DataFrame()

c = twint.Config()
st.set_page_config(
    page_title="Twitter Sentiment Analysis",
    page_icon= "🕊"
)

st.title("Twitter Sentiment Analysis")

kelime = st.text_input('Aranacak kelimeyi giriniz')


sayi = st.number_input('Kaç adet tweet listelemek istersiniz: (20nin katlarını gir)', min_value=1)
c.Limit = sayi

sincee = st.date_input("Tarih Aralığı (since)")
c.Since = str(sincee)

untill = st.date_input("Tarih Aralığı (until)")
c.Until = str(untill)

c.Pandas = True

langg = st.selectbox('Hangi dildeki tweetleri arayacaksınız ?',('Türkçe','İngilizce','Fransızca'))
if langg == "Türkçe":
    c.Search = "lang:tr " +'"'+ kelime +'"'
elif langg == "İngilizce":
    c.Search = "lang:en " + '"'+ kelime +'"'
elif langg == "Fransızca":
    c.Search = "lang:fr " +'"'+ kelime +'"'

kayitsecenek = st.radio("Tabloyu kaydetmek ister misiniz?",('Evet', 'Hayır'))

kelime = kelime.replace(" ","_").replace("#","")

if kayitsecenek == 'Evet':
    if glob.glob((kelime + ".json"), recursive=True):
      st.error("Böyle bir dosya var")
    else:
        c.Output = kelime + ".json"
        c.Store_json = True
elif kayitsecenek == "Hayır":
    print()
if st.button('Çalıştır'):
    twint.run.Search(c)
    Tweets_df = twint.storage.panda.Tweets_df
    st.dataframe(Tweets_df)
