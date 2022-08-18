import torch
from transformers import BertModel, BertPreTrainedModel


class BertWSD(BertPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)

        self.bert = BertModel(config)
        self.dropout = torch.nn.Dropout(config.hidden_dropout_prob)

        self.ranking_linear = torch.nn.Linear(config.hidden_size, 1)

        self.init_weights()

