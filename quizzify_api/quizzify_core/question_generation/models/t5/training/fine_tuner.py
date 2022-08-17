from torch.utils.data import DataLoader

import preparation

# train_dataset, validation_dataset = preparation.train_dataset, preparation.validation_dataset

from transformers import (
    AdamW,
)

class T5FineTuner(preparation.pl.LightningModule):
    def __init__(self, hparams, t5model, t5tokenizer):
        super(T5FineTuner, self).__init__()
        self.save_hyperparameters(hparams)
        self.model = t5model
        self.tokenizer = t5tokenizer


    def forward( self, input_ids, attention_mask=None, decoder_input_ids=None, decoder_attention_mask=None, lm_labels=None):
         outputs = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            decoder_attention_mask=decoder_attention_mask,
            labels=lm_labels,
        )
         
         return outputs


    def training_step(self, batch, batch_idx):
        outputs = self.forward(
            input_ids=batch["source_ids"],
            attention_mask=batch["source_mask"],
            decoder_input_ids = batch["target_ids"],
            decoder_attention_mask=batch['target_mask'],
            lm_labels=batch['labels']
        )

        loss = outputs[0]
        self.log('train_loss', loss)
        return loss

    def validation_step(self, batch, batch_idx):
        outputs = self.forward(
            input_ids=batch["source_ids"],
            attention_mask=batch["source_mask"],
            decoder_input_ids = batch["target_ids"],
            decoder_attention_mask=batch['target_mask'],
            lm_labels=batch['labels']
        )

        loss = outputs[0]
        self.log("val_loss",loss)
        return loss

    def train_dataloader(self):
        return DataLoader(preparation.train_dataset, batch_size=self.hparams.batch_size,num_workers=4)

    def val_dataloader(self):
        return DataLoader(preparation.validation_dataset, batch_size=self.hparams.batch_size,num_workers=4)


    def configure_optimizers(self):
        optimizer = AdamW(self.parameters(), lr=3e-4, eps=1e-8)
        return optimizer

