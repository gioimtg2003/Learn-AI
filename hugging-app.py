import os
from dotenv import load_dotenv 
import torch
import streamlit as st
from transformers import pipeline
from huggingface_hub import InferenceClient
from datetime import datetime
from transformers import VitsModel, AutoTokenizer
from functools import lru_cache
from scipy.io import wavfile 
import numpy as np

load_dotenv()

HUGGINGFACE_API_TOKEN=os.getenv("HUGGINGFACE_API_TOKEN")
client = InferenceClient(
    "mistralai/Mistral-7B-Instruct-v0.2",
    token=HUGGINGFACE_API_TOKEN,
)

# replace local model with huggingface inference client
# # image to text model
def image2text(url):
    # model="Salesforce/blip-image-captioning-base"
    model="nlpconnect/vit-gpt2-image-captioning"
    image_to_text = pipeline("image-to-text", model, max_new_tokens=10, device=0)
    caption = image_to_text(url)
    print(caption)
    text = caption[0]['generated_text']

    return text

@lru_cache(maxsize=100)
def caption2story(caption):
    template = """
        You are a storyteller;
        You can generate a story based on a simple narrative under 100 words with the following context:
        CONTEXT: {caption}
    """.format(caption=caption)
    model = "Qwen/Qwen2.5-0.5B"
    caption_to_story = pipeline("text-generation", model, max_new_tokens=100, device=0)
    story = caption_to_story(template)
    print(story)
    return story[0]['generated_text']

def text2speech_fb(text, filename):
    text_to_speech = pipeline("text-to-speech", model="facebook/mms-tts-eng")
    response = text_to_speech(text)
    filepath = 'output.flac' if filename is None else filename

    print(response)
    
    with open(filepath, "wb") as f:
        f.write(response['audio'])

    return filepath

def main():

    st.set_page_config(page_title="img 2 audio story", page_icon=None)
    st.header("Turn your image into Audio Story")
    uploaded_file = st.file_uploader("choose an image....", type=["jpg", "png", "jpeg", "JPG", "PNG", "JPEG", "bmp"])

    if uploaded_file is not None:
        print(uploaded_file)
        bytes_data = uploaded_file.getvalue()
        with open(uploaded_file.name, "wb") as file:
            file.write(bytes_data)
            st.image(uploaded_file, caption="Uploaded image..",
                use_column_width=True)
            scenerio = image2text(uploaded_file.name)
            story = caption2story(caption=scenerio)
            filename = f"{datetime.now()}-story.flac"
            filepath = text2speech_fb(story, filename=filename)

            with st.expander("scenerio"):
                st.write(scenerio)
            with st.expander("story"):
                st.write(story)

            if filepath is not None:
                st.audio(filepath)


if __name__ == "__main__":
     main()

