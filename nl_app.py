import os
from google.cloud import language_v1
from google.cloud.language_v1 import enums

from google.cloud import language
from google.cloud.language import types

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

import streamlit as st

st.set_page_config(
    page_title='Entidades | Vocento',
    layout = 'wide',
)

import tempfile

import json

#creamos un dict con el contenido de las credenciales de json
contenido_json = {
  "type": st.secrets["type"],
  "project_id": st.secrets["project_id"],
  "private_key_id": st.secrets["private_key_id"],
  "private_key": st.secrets["private_key"],
  "client_email": st.secrets["client_email"],
  "client_id": st.secrets["client_id"],
  "auth_uri": st.secrets["auth_uri"],
  "token_uri": st.secrets["token_uri"],
  "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
  "client_x509_cert_url": st.secrets["auth_provider_x509_cert_url"]
}

#convertimos el dict en un JSON
uploaded_file = json.dumps(contenido_json)

#guardamos el JSON en un archivo temporal para poder llamar al path donde se encuentra el archivo JSON en GOOGLE_APPLICATION_CREDENTIALS
with tempfile.NamedTemporaryFile(mode='w', delete=False) as fp:
  #fp.write(uploaded_file.getvalue())
  fp.write(uploaded_file)
try:
  os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = fp.name
  #st.write('Found', fp.name)
  with open(fp.name) as a:
    #st.write(a.read())
    client = language_v1.LanguageServiceClient()
finally:
  os.unlink(fp.name)

import requests
from requests_html import HTMLSession

url_input = st.text_input('url para obtener Entidades, Sentimiento y Magnitud del sentimiento del texto')

if url_input == '':
 st.stop()

url = url_input

try:
    session = HTMLSession()
    response = session.get(url)
     
except requests.exceptions.RequestException as e:
    st.write(e)

#dominios objetivo
dominio_abc = 'abc.es'
dominio_voz = 'lavozdigital.es'
dominio_hoy = 'hoy.es'
dominio_rioja = 'larioja.com'
dominio_correo = 'elcorreo.com'
dominio_norteCastilla = 'elnortedecastilla.es'
dominio_diarioVasco = 'diariovasco.com'
dominio_comercio = 'elcomercio.es'
dominio_ideal = 'ideal.es'
dominio_sur = 'diariosur.es'
dominio_provincias = 'lasprovincias.es'
dominio_montanes = 'eldiariomontanes.es'
dominio_verdad = 'laverdad.es'
dominio_leon = 'leonoticias.com'
dominio_burgos = 'burgosconecta.es'

#dominios competencia
dominio_mundo = 'elmundo.es'
dominio_pais = 'elpais.com'
dominio_vanguardia = 'lavanguardia.com'

#elementos HTML para la extracci??n del texto de la noticia
elemento_abc = '.cuerpo-texto > p'
elemento_ppll = '.voc-detail > p'
elemento_mundo = '.ue-c-article__body > p'
elemento_pais = '.article_body > p'
elemento_vanguardia = '.article-modules > p'

#Realizamos un condicional para saber de qu?? dominio se trata la URL y extraer el elemento correspondiente a ese dominio.
if dominio_abc in url:
  p =  response.html.find(elemento_abc) #buscamos los elementos <p> de dentro de la clase cuerpo-texto.
  array = [] #creamos un array vacio.
  for i in range(len(p)): #recorremos todos los <p> de dentro de la clase cuerpo-texto para almacenarlos en el array vacio que acabamos de crear
    array.append(p[i].text)
  texto = " ".join(array) #concatenamos todos los textos (valores) del array para almacenar el texto completo de la noticia en una variable.
elif dominio_mundo in url:
  p =  response.html.find(elemento_mundo) #buscamos los elementos <p> de dentro de la clase cuerpo-texto.
  array = [] #creamos un array vacio.
  for i in range(len(p)): #recorremos todos los <p> de dentro de la clase cuerpo-texto para almacenarlos en el array vacio que acabamos de crear
    array.append(p[i].text)
  texto = " ".join(array) #concatenamos todos los textos (valores) del array para almacenar el texto completo de la noticia en una variable.
elif dominio_pais in url:
  p =  response.html.find(elemento_pais) #buscamos los elementos <p> de dentro de la clase cuerpo-texto.
  array = [] #creamos un array vacio.
  for i in range(len(p)): #recorremos todos los <p> de dentro de la clase cuerpo-texto para almacenarlos en el array vacio que acabamos de crear
    array.append(p[i].text)
  texto = " ".join(array) #concatenamos todos los textos (valores) del array para almacenar el texto completo de la noticia en una variable.
elif dominio_vanguardia in url:
  p =  response.html.find(elemento_vanguardia) #buscamos los elementos <p> de dentro de la clase cuerpo-texto.
  array = [] #creamos un array vacio.
  for i in range(len(p)): #recorremos todos los <p> de dentro de la clase cuerpo-texto para almacenarlos en el array vacio que acabamos de crear
    array.append(p[i].text)
  texto = " ".join(array) #concatenamos todos los textos (valores) del array para almacenar el texto completo de la noticia en una variable.
elif dominio_voz in url:
  p =  response.html.find(elemento_abc) #buscamos los elementos <p> de dentro de la clase cuerpo-texto.
  array = [] #creamos un array vacio.
  for i in range(len(p)): #recorremos todos los <p> de dentro de la clase cuerpo-texto para almacenarlos en el array vacio que acabamos de crear
    array.append(p[i].text)
  texto = " ".join(array) #concatenamos todos los textos (valores) del array para almacenar el texto completo de la noticia en una variable.
elif dominio_hoy in url or dominio_rioja in url or dominio_correo in url or dominio_norteCastilla in url or dominio_diarioVasco in url or dominio_comercio in url or dominio_ideal in url or dominio_sur in url or dominio_provincias in url or dominio_montanes in url or dominio_verdad in url or dominio_leon in url or dominio_burgos in url:
  p =  response.html.find(elemento_ppll) #buscamos los elementos <p> de dentro de la clase cuerpo-texto.
  array = [] #creamos un array vacio.
  for i in range(len(p)): #recorremos todos los <p> de dentro de la clase cuerpo-texto para almacenarlos en el array vacio que acabamos de crear
    array.append(p[i].text)
  texto = " ".join(array) #concatenamos todos los textos (valores) del array para almacenar el texto completo de la noticia en una variable. 
else:
  st.write('El dominio de la URL: ' + url + ' \nno se encuentra entre nuestros dominios objetivo o la competencia directa, y por lo tanto, no se puede extraer el texto. \nSi deseas incluir este dominio para su an??lisis, por favor, ponte en contacto con fvera@vocento.com')

st.header('Texto noticia')
st.write(texto)

#Available types: PLAIN_TEXT, HTML
type_ = enums.Document.Type.PLAIN_TEXT

# Optional. If not specified, the language is automatically detected.
language = "es"
document = {"content": texto, "type": type_, "language": language}

# Available values: NONE, UTF8, UTF16, UTF32
encoding_type = enums.EncodingType.UTF8

response = client.analyze_entities(document, encoding_type=encoding_type)

col1, col2 = st.beta_columns(2)

with col1:
    st.header('Entidades noticia')

    # Loop through entitites returned from the API
    for entity in response.entities:
        st.write(u"Entity Name: {}".format(entity.name))

        # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        st.write(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))

        # Get the salience score associated with the entity in the [0, 1.0] range
        st.write(u"Salience score: {}".format(round(entity.salience,3)))

        # Loop over the metadata associated with entity. For many known entities,
        for metadata_name, metadata_value in entity.metadata.items():
            st.write(u"{}: {}".format(metadata_name, metadata_value))


        # Loop over the mentions of this entity in the input document.
        #for mention in entity.mentions:
            #st.write(u"Mention text: {}".format(mention.text.content))

            # Get the mention type, e.g. PROPER for proper noun
            #st.write(
                #u"Mention type: {}".format(enums.EntityMention.Type(mention.type).name)
            #)'''
        st.write('\n')

with col2:
    ####################################### The text to analyze setiment
    st.header('Sentimiento')

    document = types.Document(
        content=texto,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    sscore = round(sentiment.score,4)
    smag = round(sentiment.magnitude,4)

    if sscore < 1 and sscore < -0.5:
      sent_label = "Muy Negativo"
    elif sscore < 0 and sscore > -0.5:
      sent_label = "Negativo"
    elif sscore == 0:
      sent_label = "Neutral"
    elif sscore > 1 and sscore > 1.5:
      sent_label = "Muy Positivo"
    elif sscore > 0 and sscore < 1.5:
      sent_label = "Positivo"

    st.write('Sentiment Score: {} es {}'.format(sscore,sent_label))

    predictedY =[sscore] 
    UnlabelledY=[0,1,0]

    if sscore < 0:
        plotcolor = 'red'
    else:
        plotcolor = 'green'

    plt.scatter(predictedY, np.zeros_like(predictedY),color=plotcolor,s=100)

    plt.yticks([])
    plt.subplots_adjust(top=0.9,bottom=0.8)
    plt.xlim(-1,1)
    plt.xlabel('Negativo                                                            Positivo')
    plt.title("Tipo de Sentimiento")
    plt.show()

    #title Ejecutar para calcular la magnitud del sentimiento { vertical-output: true }
    st.header('Magnitud Sentimiento')

    if smag >= 0 and smag < 1:
      sent_m_label = "Sin Emoci??n"
    elif smag > 2:
      sent_m_label = "Emoci??n Alta"
    elif smag > 1 and smag < 2:
      sent_m_label = "Emoci??n Baja"

    st.write('Sentiment Magnitude: {} es {}'.format(smag, sent_m_label))

    predictedY =[smag] 
    UnlabelledY=[0,1,0]

    if smag > 0 and smag < 2:
        plotcolor = 'red'
    else:
        plotcolor = 'green'

    plt.scatter(predictedY, np.zeros_like(predictedY),color=plotcolor,s=100)

    plt.yticks([])
    plt.subplots_adjust(top=0.9,bottom=0.8)
    plt.xlim(0,5)
    plt.xlabel('Emoci??n Baja                                                          Emoci??n Alta')
    plt.title("An??lisis Sentiment Magnitude")
    plt.show()
