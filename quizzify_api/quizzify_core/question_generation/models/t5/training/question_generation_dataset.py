import copy
import pandas as pd
from torch.utils.data import Dataset

class QuestionGenerationDataset(Dataset):
    def __init__(self, tokenizer, filepath, max_len_inp=128,max_len_out=96,truncate=True):
        self.path = filepath

        self.passage_column = "context"
        self.answer = "answer"
        self.question = "question"

        # self.data = pd.read_csv(self.path)
        self.data = pd.read_csv(self.path, nrows=550)

        self.truncate = truncate
        self.max_len_input = max_len_inp
        self.max_len_output = max_len_out
        self.tokenizer = tokenizer
        self.inputs = []
        self.targets = []
        self.skippedcount = 0
        self._build()

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, index):
        source_ids = self.inputs[index]["input_ids"].squeeze()
        target_ids = self.targets[index]["input_ids"].squeeze()

        src_mask = self.inputs[index]["attention_mask"].squeeze()  # might need to squeeze
        target_mask = self.targets[index]["attention_mask"].squeeze()  # might need to squeeze

        labels = copy.deepcopy(target_ids)
        labels [labels==0] = -100

        return {"source_ids": source_ids, "source_mask": src_mask, "target_ids": target_ids, "target_mask": target_mask,"labels":labels}

    def _build(self):
        for idx in range(len(self.data)):
            passage,answer,target = self.data.loc[idx, self.passage_column],self.data.loc[idx, self.answer], self.data.loc[idx, self.question]

            input_ = "context: %s  answer: %s </s>" % (passage, answer)
            target = "question: %s </s>" % (str(target))

            # get encoding length of input. If it is greater than self.max_len skip it
            test_input_encoding = self.tokenizer.encode_plus(input_,
                                        truncation=self.truncate,
                                        return_tensors="pt")
            
            length_of_input_encoding = len(test_input_encoding['input_ids'][0])


            if length_of_input_encoding > self.max_len_input:
              self.skippedcount = self.skippedcount + 1
              continue

            # tokenize inputs
            tokenized_inputs = self.tokenizer.batch_encode_plus(
                [input_], max_length=self.max_len_input, pad_to_max_length=True, return_tensors="pt"
            )
            # tokenize targets
            tokenized_targets = self.tokenizer.batch_encode_plus(
                [target], max_length=self.max_len_output, pad_to_max_length=True, return_tensors="pt"
            )

            self.inputs.append(tokenized_inputs)
            self.targets.append(tokenized_targets)

