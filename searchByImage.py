import numpy as np
import keras
import streamlit as st
from numpy import array
from tensorflow.keras.utils import load_img
from keras.applications.vgg16 import VGG16
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.preprocessing import image
from keras import Model, Sequential
from keras.layers import Dense, Flatten
from PIL import Image
import requests
from io import BytesIO
import pickle
from keras.applications.vgg16 import preprocess_input
import pickle as pkl
from interface import es, INDEX
from sklearn.preprocessing import MinMaxScaler

# vgg16_model = VGG16()
#
# model = Sequential()
#
# for layer in vgg16_model.layers[:-1]:
#     model.add(layer)
#
# model.layers.pop()

base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)


# Freeze the layers
for layer in model.layers:
    layer.trainable = False

pca_reload = pkl.load(open('pca.pkl','rb'))
from sklearn.decomposition import PCA

def search_by_img(path):
    img = image.load_img(path, target_size=(224, 224))
    img = image.img_to_array(img)
    st.write(img.shape)
    #img = img.reshape((1, img.shape[0], img.shape[1], img.shape[2]))
    x = np.expand_dims(img, axis=0)
    img = preprocess_input(x)
    feature = model.predict(img)[0]
    #img = preprocess_input(img)
    # Pass image into model to get encoded features
    #feature = model.predict(img, verbose=0)
    # faire la reduction des features
    # Standardizing the features
    #feature = MinMaxScaler().fit_transform(np.reshape(feature,(1,4096)))
    feature = feature / np.linalg.norm(feature)
    vector = pca_reload.transform(feature.reshape(1,-1))[0].tolist()




    body = {
        "query": {
            "elastiknn_nearest_neighbors": {
                "field": "feature_vector",
                "vec": {
                    "values": vector
                },
                "model": "lsh",
                "similarity": "l2",
                "candidates": 100
            }
        }
    }


    return (es.search(index=INDEX, body=body))