import torchaudio
from datasets import load_dataset, load_metric
from transformers import (
    Wav2Vec2ForCTC,
    Wav2Vec2Processor,
)
import torch
import re
import sys

model_name = "facebook/wav2vec2-large-xlsr-53-portuguese"
device = "cuda"

chars_to_ignore_regex = '[\,\?\.\!\-\;\:\"]'  # noqa: W605

model = Wav2Vec2ForCTC.from_pretrained(model_name).to()
processor = Wav2Vec2Processor.from_pretrained(model_name)

resampler = torchaudio.transforms.Resample(orig_freq=48_000, new_freq=16_000)

#load the corpus
#ds = load_dataset("common_voice", "pt", split="test", data_dir="./cv-corpus-6.1-2020-12-11")
# because it comes in mp3, it is necessary to convert it to wav

from os import path
from pydub import AudioSegment

import pdb
def map_to_array(batch):
    mp3 = False
    stereo = True
    if mp3:
        sound = AudioSegment.from_mp3(batch["path"])
        dst = batch["path"][:-4] + '.wav'
        batch["path"] = dst
        sound.export(dst, format="wav")
    speech, _ = torchaudio.load(batch["path"])
    if stereo:
        batch["speech"] = resampler.forward(speech.squeeze(0)).numpy()[0]
    else:
        batch["speech"] = resampler.forward(speech.squeeze(0)).numpy()
    batch["sampling_rate"] = resampler.new_freq
    batch["sentence"] = re.sub(chars_to_ignore_regex, '', batch["sentence"]).lower().replace("’", "'")
    return batch

#select a small portion of the whole dataset
#ds_small = ds.select([0, 1, 2, 3])
#ds_small = ds_small.map(map_to_array)

def map_to_pred(batch):
    features = processor(batch["speech"], sampling_rate=batch["sampling_rate"][0], padding=True, return_tensors="pt")
    input_values = features.input_values.to()
    attention_mask = features.attention_mask.to()
    with torch.no_grad():
        logits = model(input_values, attention_mask=attention_mask).logits
    pred_ids = torch.argmax(logits, dim=-1)
    batch["predicted"] = processor.batch_decode(pred_ids)
    batch["target"] = batch["sentence"]
    return batch

# creates a dataset using the audio bellow
reference_dict = {'client_id':['teste'], 'path':['rednose1.wav'], 'sentence':[''], 
                  'up_votes':['2'], 
                  'down_votes':[0], 'age': [23], 'gender': [''], 'accent': [''], 
                  'locale':['pt'], 'segment':["''"]}

from datasets import Dataset
data = Dataset.from_dict(reference_dict)

data = data.map(map_to_array)
result = data.map(map_to_pred, batched=True, batch_size=32, remove_columns=list(data.features.keys()))

# name = result[0].replace()
# print(result[0])
import os
os.system('cls' if os.name == 'nt' else 'clear')
patientName = str(result[0]).replace("{'predicted': '", "")
patientName = patientName.replace("', 'target': ''}", "")
print(patientName)


