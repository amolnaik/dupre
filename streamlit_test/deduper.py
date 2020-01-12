import streamlit as st
from PIL import Image, ImageDraw
from pathlib import Path
import os
import imagededup
import numpy as np
from io import StringIO
import requests
import sys, io
from blinker import signal
from shutil import copy, move

st.title('Image Deduper')

# should come from user
    #image_dir = Path('/Users/amnaik/Documents/pprojects/pyfindimagedupes/imagededupml/test/')

st.sidebar.title("Setup")

folder_path = st.sidebar.text_input('folder', \
'/Users/amnaik/Documents/test/')

destination_path = Path('/Users/amnaik/Documents/to_delete/')

option = st.sidebar.selectbox('Choose algorithm', ('pHash', 'aHash', 'dHash', 'wHash', 'CNN'))

max_distance = st.sidebar.slider('distance threshold', 0, 64, 10)

search_method = st.sidebar.selectbox('Search', ('bktree','brute_force_cython'))

scores = st.sidebar.checkbox("show scores")

if st.sidebar.button("Start"):
    image_dir = folder_path



# -----------------------------------------------------------------------------#
status = st.empty()
status.text("Waiting...")
progress_bar = st.progress(0)

send_data = signal('send-data')
send_progress = signal('progress')


# -----------------------------------------------------------------------------#
from imagededup.methods import PHash, CNN, AHash, DHash, WHash

@send_data.connect
def receive_data(sender, **kw):
    #print("Caught signal from %r, data %r" % (sender, kw))
    status.text(kw['message'])
    return 'received!'

@send_progress.connect
def receive_progress(sender, **kw):
    #print("Caught signal from %r, data %r" % (sender, kw))
    progress_bar.progress(int(round(kw['percent'])))
    #status.text(kw['message'])
    return 'received!'

if option == "pHash":
    try:
        phasher = PHash()
        duplicates = phasher.find_duplicates(image_dir, max_distance_threshold=max_distance, \
                                         scores=True)
    except Exception as e:
        duplicates = {}
        st.write(str(e))
elif option == "CNN":
    try:
        cnn_encoder = CNN()
        duplicates = cnn_encoder.find_duplicates(image_dir=image_dir, scores=True)
    except Exception as e:
        duplicates = {}
        st.write(str(e))
elif option == "aHash":
    try:
        ahasher = AHash()
        duplicates = ahasher.find_duplicates(image_dir, max_distance_threshold=max_distance, \
                                         scores=True)
    except Exception as e:
        duplicates = {}
        st.write(str(e))
elif option == 'dHash':
    try:
        dhasher = DHash()
        duplicates = dhasher.find_duplicates(image_dir, max_distance_threshold=max_distance, \
                                         scores=True)
    except Exception as e:
        duplicates = {}
        st.write(str(e))
elif option == 'wHash':
    try:
        whasher = WHash()
        duplicates = whasher.find_duplicates(image_dir, max_distance_threshold=max_distance, \
                                         scores=True)
    except Exception as e:
        duplicates = {}
        st.write(str(e))
else:
    duplicates = {}
    st.write("Algorithm not chosen...")


# -----------------------------------------------------------------------------#

img_select = {}
for k, v in duplicates.items():
    if (v != []):
        img_select[k] = [x[0] for x in v]

st.write(img_select)



# -----------------------------------------------------------------------------#
st.subheader("Results")
i = 0
img_selected = []
to_delete = []
for k in img_select.keys():
    captions = []
    images = []
    # check if master image not in the similar image
    if k not in img_selected:
        i = i+1
        st.write("Record: %d" % (i))
        images.append(str(image_dir) + '/' + k)
        #copy for deletion
        copy(str(image_dir) + '/' + k, destination_path)
        to_delete.append(k)
        captions.append(k)
        for vi in img_select[k]:
            images.append(str(image_dir) + '/' + vi)
            captions.append(vi)
            img_selected.append(vi)
            #copy for deletion
            copy(str(image_dir) + '/' + vi, destination_path)
            to_delete.append(vi)

    st.image(images, caption=captions, width=300)

# -----------------------------------------------------------------------------#
num_files = len([f for f in os.listdir(folder_path) if f.endswith('.JPG') and os.path.isfile(os.path.join(folder_path, f))])

if len(img_select):
    summary = ("Found " + str(len(list(set(to_delete)))) + " similar images in total " + str(num_files) + " images")
    outcome = st.sidebar.text_area("Summary", summary)
else:
    outcome = st.sidebar.text_area("Summary", "")

st.subheader("For Deletion")
deletion_summary = st.write ("These files will be deleted from source folder", list(set(to_delete)))

for k in list(set(to_delete)):
    if os.path.isfile(str(image_dir) + '/' + k):
        os.remove(str(image_dir) + '/' + k)
    else:
        couldnt_delete = st.write("could not delete file", k)
