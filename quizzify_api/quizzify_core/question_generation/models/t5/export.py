import torch
from pathlib import Path
from transformers import T5ForConditionalGeneration, T5Tokenizer

STORAGE_FOLDER_PATH = Path(__file__).parent.joinpath('storage')

trained_model_path = STORAGE_FOLDER_PATH.joinpath('model')
tokenizer_path = STORAGE_FOLDER_PATH.joinpath('tokenizer')

model = T5ForConditionalGeneration.from_pretrained(trained_model_path)
tokenizer = T5Tokenizer.from_pretrained(tokenizer_path)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
model.eval()

def get_model():
    return model

def get_tokeninzer():
    return tokenizer