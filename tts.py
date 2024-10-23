import requests 
from playsound import playsound 
import os
from typing import Union 
import sys
import time
import threading
from dotenv import load_dotenv 

load_dotenv()

API_TEXT_TO_SPEECH=os.getenv("API_URL_TEXT_TO_SPEECH")
ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
AUTH_TOKEN = os.getenv("CLOUDFLARE_AUTH_TOKEN")
def generate_audio(message: str, voice: str = "Matthew", folder: str = "", extension: str = ".mp3") -> Union[None, str]:
    url: str = f"{API_TEXT_TO_SPEECH}?voice={voice}&text={{{message}}}"

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    
    try:
        result = requests.get(url=url, headers=headers)
        file_path = os.path.join(folder, f"{voice}{extension}")
        with open(file_path, "wb") as file:
            file.write(result.content)
        playsound(file_path)
        time.sleep(0.5)
        os.remove(file_path)
        return None
    except Exception as e:
        print(e)
        return None

def print_animated_message(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.050)  # Adjust the sleep duration for the animation speed
    print()

def co_speak(message: str, voice: str = "Matthew", folder: str = "", extension: str = ".mp3") -> Union[None, str]:
    try:
        generate_audio(message, voice, folder, extension)
        return None
    except Exception as e:
        print(e)

def speak(text):
    t1 = threading.Thread(target=co_speak, args=(text,))
    t2 = threading.Thread(target=print_animated_message, args=(text,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    
def generative(question) -> str:

    prompt = f'''
    Your are G-AI, a friendly assistant. You are asked to provide a step-by-step guide to the user's question.
   Please answer the user question below and then follow this format to give us feedback if you have some answers on this format otherwise please answer in normal format. Example of format when there is a result returned in the form:
        1. Visit the abcxyz website
        2. Click the register button to register an account
        3. Enter information.

        Instead of numbering each step, you should change it to:
        First Visit the abcxyz website
        Second Click the register button to register an account
        Third Enter information.
        User: {question}

        Assistant:
    '''
    response = requests.post(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/meta/llama-3-8b-instruct",
        headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
        json={
        "messages": [
            {"role": "system", "content": "You are a friendly assistant"},
            {"role": "user", "content": prompt}
        ]
        }
    )
    result = response.json()
    print(result["result"]["response"])
    
    return result["result"]["response"]

co_speak(generative("What your name?"))
