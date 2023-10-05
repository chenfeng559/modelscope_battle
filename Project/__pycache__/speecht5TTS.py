# Following pip packages need to be installed:
# !pip install git+https://github.com/huggingface/transformers sentencepiece datasets

from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
from datasets import load_dataset

processor = SpeechT5Processor.from_pretrained("./models--microsoft--speecht5_tts/snapshots/47ef28aada010fa307bb8d956e46bd4d908b1514")
model = SpeechT5ForTextToSpeech.from_pretrained("./models--microsoft--speecht5_tts/snapshots/47ef28aada010fa307bb8d956e46bd4d908b1514")
vocoder = SpeechT5HifiGan.from_pretrained("./models--microsoft--speecht5_hifigan/snapshots/bb6f429406e86a9992357a972c0698b22043307d/")
embeddings_dataset = load_dataset("./Matthijs___cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
def generateTextAudio(text):
    global processor, model, vocoder, speaker_embeddings
    inputs = processor(text=text, return_tensors="pt")
    # load xvector containing speaker's voice characteristics from a dataset
    speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

    sf.write("./output/output.wav", speech.numpy(), samplerate=16000)
    return "./output/output.wav"

# _=generateTextAudio('hello nice to meet you, Mr. President," he says as the phone rings in a loud ringing tone and his secretary answers it: "Yes! It is me!" The president looks up from answering that call but does not answer again because')
# print(_)