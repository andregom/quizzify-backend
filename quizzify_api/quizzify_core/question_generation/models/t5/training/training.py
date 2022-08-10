import argparse
import glob
import os
from pathlib import Path
import json
import time
import logging
import random
import re
from itertools import chain
from string import punctuation
from pprint import pprint

import numpy as np
import torch
import pytorch_lightning as pl
from termcolor import colored
import textwrap

from question_generation_dataset import QuestionGenerationDataset
from fine_tuner import T5FineTuner

from transformers import (
    T5ForConditionalGeneration,
    T5Tokenizer,
    get_linear_schedule_with_warmup
)

import gc

gc.collect()

torch.cuda.empty_cache()
torch.cuda.set_enabled_lms(True)

STORAGE_FOLDER_PATH = Path(__file__).resolve().parents[1].joinpath('storage')

DATASETS_FOLDER_PATH = STORAGE_FOLDER_PATH.joinpath('datasets')

train_file_path = DATASETS_FOLDER_PATH.joinpath('squad_t5_train.csv')
validation_file_path = DATASETS_FOLDER_PATH.joinpath('squad_t5_validation.csv')

pl.seed_everything(42)

t5_tokenizer = T5Tokenizer.from_pretrained('t5-base')
t5_model = T5ForConditionalGeneration.from_pretrained('t5-base')

train_dataset = QuestionGenerationDataset(t5_tokenizer,train_file_path)

train_sample = train_dataset[50]
decoded_train_input = t5_tokenizer.decode(train_sample['source_ids'])
decoded_train_output = t5_tokenizer.decode(train_sample['target_ids'])

# print (decoded_train_input)
print (decoded_train_output)

validation_dataset = QuestionGenerationDataset(t5_tokenizer,validation_file_path)

args_dict = dict(
    train_dataset = train_dataset,
    validation_dataset = validation_dataset,
    batch_size=4,
)

args = argparse.Namespace(**args_dict)


model = T5FineTuner(args, t5_model, t5_tokenizer)

trainer = pl.Trainer(max_epochs = 1, accelerator='gpu', devices=1)

trainer.fit(model)

print ("Saving model")
save_path_model = STORAGE_FOLDER_PATH.joinpath('model')
save_path_tokenizer = STORAGE_FOLDER_PATH.joinpath('tokenizer')
model.model.save_pretrained(save_path_model)
t5_tokenizer.save_pretrained(save_path_tokenizer)