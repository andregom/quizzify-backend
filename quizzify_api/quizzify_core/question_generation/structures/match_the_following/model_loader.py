import torch
import math
from transformers import BertConfig, BertTokenizer
from pathlib import Path

from bert_wsd import BertWSD

COMMON_PARENT_FOLDER = Path(__file__).resolve().parents[2]

ROUTE_TO_BERTWSD_MODEL = ['models', 'bert_WSD', 'bert_base']

BERTWSD_FOLDER_PATH = COMMON_PARENT_FOLDER.joinpath(*ROUTE_TO_BERTWSD_MODEL)

DEVICE = torch.device('cpu') # 'cuda' if torch.cuda.is_available() else 'cpu')

model_dir = BERTWSD_FOLDER_PATH

model = BertWSD.from_pretrained(model_dir)
tokenizer = BertTokenizer.from_pretrained(model_dir)
# add new special token
if '[TGT]' not in tokenizer.additional_special_tokens:
    tokenizer.add_special_tokens({'additional_special_tokens': ['[TGT]']})
    assert '[TGT]' in tokenizer.additional_special_tokens
    model.resize_token_embeddings(len(tokenizer))
    
model.to(DEVICE)
model.eval()