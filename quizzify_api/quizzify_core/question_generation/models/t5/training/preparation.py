from pathlib import Path

import pytorch_lightning as pl
from termcolor import colored
from question_generation_dataset import QuestionGenerationDataset

from transformers import (
    T5ForConditionalGeneration,
    T5Tokenizer,
    get_linear_schedule_with_warmup
)


STORAGE_FOLDER_PATH = Path(__file__).resolve().parents[1].joinpath('storage')

train_dataset = validation_dataset = t5_tokenizer = t5_model = None

def load_datasets():

    global train_dataset, validation_dataset, t5_tokenizer, t5_model

    DATASETS_FOLDER_PATH = STORAGE_FOLDER_PATH.joinpath('datasets')

    train_file_path = DATASETS_FOLDER_PATH.joinpath('squad_t5_train.csv')
    validation_file_path = DATASETS_FOLDER_PATH.joinpath('squad_t5_validation.csv')

    pl.seed_everything(42)

    t5_tokenizer = T5Tokenizer.from_pretrained('t5-base')
    t5_model = T5ForConditionalGeneration.from_pretrained('t5-base')

    train_dataset = QuestionGenerationDataset(t5_tokenizer,train_file_path)

    train_sample = train_dataset[100]

    decoded_train_input = t5_tokenizer.decode(train_sample['source_ids'])
    decoded_train_output = t5_tokenizer.decode(train_sample['target_ids'])

    print (decoded_train_input)
    print (decoded_train_output)

    validation_dataset = QuestionGenerationDataset(t5_tokenizer,validation_file_path)
