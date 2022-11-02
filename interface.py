# srcs/streamlit_app/app.py
import sys,os
import streamlit as st
from elasticsearch import Elasticsearch
sys.path.append('srcs')
import utils, templates
import searchByImage
from PIL import Image
import requests
from io import BytesIO

hide_menu = """
    <style>

    footer{
        content:'Copyright @ 2022 : Jassem & Marwa;
        display:block;
        position:relative;
        color:tomato;
    }
    </style>
"""

INDEX = 'abc'
PAGE_SIZE = 20
DOMAIN = '127.0.0.1'
es = Elasticsearch("http://127.0.0.1:9200")

def main():
    st.title('Search engine based on images and text')
    st.markdown(hide_menu,unsafe_allow_html=True)
    indication1 = '<p style="font-family:Poppins; color: #3399ff; font-size: 25px">Search by word</p>'
    st.markdown(indication1, unsafe_allow_html=True)
    search = st.text_input('Enter search words:')
    indication2 = '<p style="font-family:Poppins; color: #3399ff; font-size: 25px">Search by image</p>'
    st.markdown(indication2, unsafe_allow_html=True)
    find = st.file_uploader('Select image')
    if search:
        results = utils.index_search(es, INDEX, search, PAGE_SIZE)
        # search results
        for i in range(len(results['hits']['hits'])):
            result = results['hits']['hits'][i]
            res = result['_source']
            res['url'] = result['_source']['url']
            st.write(templates.search_result(i, **res), unsafe_allow_html=True)

    elif find:

        def load_image(image_file):
            img = Image.open(image_file)
            return img

        if find is not None:
            # To See details
            file_details = {"filename": find.name, "filetype": find.type,
                        "filesize": find.size}
            st.write('Your image')
            # To View Uploaded Image
            st.image(load_image(find), width=250)
            # Saving upload
            with open(os.path.join("E:\\INDP3AIM\\indexation\\bdimage\\imgs\\", find.name), "wb") as f:
                f.write((find).getbuffer())

            path = "E:\\INDP3AIM\\indexation\\bdimage\\imgs\\"+find.name
            results = searchByImage.search_by_img(path)
            for i in range(len(results['hits']['hits'])):
                result = results['hits']['hits'][i]
                res = result['_source']
                res['url'] = result['_source']['url']
                res['tags'] = result['_source']['tags']

                st.write(templates.search_result(i, **res), unsafe_allow_html=True)




if __name__ == '__main__':
    main()
