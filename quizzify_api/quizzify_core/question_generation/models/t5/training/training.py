import argparse
import pytorch_lightning as pl

import preparation
from fine_tuner import T5FineTuner

import torch
import gc

gc.collect()

torch.cuda.empty_cache()

preparation.load_datasets()

STORAGE_FOLDER_PATH = preparation.STORAGE_FOLDER_PATH

args_dict = dict(
    batch_size=1,
)

args = argparse.Namespace(**args_dict)


model = T5FineTuner(args, preparation.t5_model, preparation.t5_tokenizer)

del(preparation.t5_model)
del(preparation.t5_tokenizer)
gc.collect()

trainer = pl.Trainer(max_epochs = 1, accelerator='gpu', devices=1)

trainer.fit(model)

print ("Saving model")
save_path_model = STORAGE_FOLDER_PATH.joinpath('model')
save_path_tokenizer = STORAGE_FOLDER_PATH.joinpath('tokenizer')
model.model.save_pretrained(save_path_model)
preparation.t5_tokenizer.save_pretrained(save_path_tokenizer)