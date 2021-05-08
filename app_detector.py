### Exec Streamlit
# cd path/to/dir
# streamlit run app.py

### Install Azure Libraries
# !pip3 install --upgrade azure-cognitiveservices-vision-computervision
# !pip3 install pillow

### Import Packages following the Quick Start:
# Ref. https://docs.microsoft.com/en-us/azure/cognitive-services/Computer-vision/quickstarts-sdk/client-library?pivots=programming-language-python&tabs=visual-studio
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
from PIL import Image
import time
import sys
import os

### Read credentials from secret.json (cognitive vision)
import json
with open("secret-maz-srv-cv.json") as f:
    secret = json.load(f)

# Set KEY , ENDPOINT as constant from secret.json
KEY = secret["KEY"]
ENDPOINT = secret["ENDPOINT"]

# Authenticate & Instantiate the client
computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

### Function to detect objects' boundary coordinates
def detect_objects(local_image_path:str):
    # Convert image path to binary
    local_image = open(local_image_path, "rb")

    # Call API with URL
    detect_objects_results = computervision_client.detect_objects_in_stream(local_image)

    # Retrieve Objects
    objects = detect_objects_results.objects
    return objects

### Function to Get Tags
def get_tags(local_image_path:str):
    # Convert image path to binary
    local_image = open(local_image_path, "rb")

    # Call API with local image
    tags_result_local = computervision_client.tag_image_in_stream(local_image)

    # Print tag results with confidence score:
    # https://docs.microsoft.com/ja-jp/azure/cognitive-services/computer-vision/concept-tagging-images
    if (len(tags_result_local.tags) == 0):
        print("No tags detected.")
    else:
        tags_name=[]
        for tag in tags_result_local.tags:
             # print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
            tags_name.append(tag.name)

    return tags_name

### Build app with Steramlit
import streamlit as st

### Library for Drawing
from PIL import ImageDraw
from PIL import ImageFont

st.title("物体検出アプリ")

### Have user select their local picture and Process it
# file_uploader method return the file object (file path is not in there)
uploaded_file = st.file_uploader("Choose an image...", type=["jpg","png"])
if uploaded_file is not None:

    ### Prepare data
    # Prepare font data
    font = ImageFont.truetype(font="./img/Helvetica 400.ttf", size=50)

    # Prepare image obect (code comes from Example in streamlit image method)
    img = Image.open(uploaded_file)

    # Set image_pat and Save image in it (code comes from doc about Image library)
    img_path = f"img/{uploaded_file.name}"
    img.save(img_path)

    # Set image as a subject of ImageDraw
    draw = ImageDraw.Draw(img)

    # Detect objects' boundary coordinates
    objects = detect_objects(img_path)

    ### Draw Rectangular above(z)
    for object in objects:
        # object coodinate
        x = object.rectangle.x
        y = object.rectangle.y
        w = object.rectangle.w
        h = object.rectangle.h

        # Object boundary baseline
        draw.rectangle([(x, y), (x+w, y+h)], fill=None, outline="green", width=5)

        # object name *object is changed to object_property
        # 違う→:https://docs.microsoft.com/ja-jp/azure/cognitive-services/computer-vision/concept-object-detection
        caption = object.object_property

        # Measure the caption size with use of font
        text_w, text_h = draw.textsize(caption, font=font)

        # Object caption area
        draw.rectangle([(x, y), (x+text_w, y+text_h)], fill="green", outline=None, width=5)

        # Object caption
        draw.text((x, y), caption, fill="white", font=font)

    ### Set Image below(z)
    st.image(img)

    ### Display tags
    tags_name = get_tags(img_path)
    # print(", ".join(tags_name))       # Terminal Check
    tags_name = ", ".join(tags_name)

    st.markdown("**認識されたコンテンツタグ**")
    st.markdown(f"> {tags_name}")
