from transformers import pipeline
from transformers import AutoProcessor, AutoModelForTextToWaveform
import torch

device = 0 if torch.cuda.is_available() else -1

print("Device: ", device)

pipe = pipeline("text-to-speech", model="suno/bark", device=device)

processor = AutoProcessor.from_pretrained("suno/bark")
model = AutoModelForTextToWaveform.from_pretrained("suno/bark")

text = "Hello, this is a text-to-speech conversion using Hugging Face."

# Generate speech from text
waveform = pipe(text)

# Save the waveform to a file
with open("output.wav", "wb") as f:
    f.write(waveform["waveform"])