import re
import nltk
import torch
from pprint import pprint
from torch.nn.functional import softmax
from collections import namedtuple
from nltk.corpus import wordnet as wn

from transformers import logging
logging.set_verbosity_error()

import preparation
from model_loader import model, tokenizer, DEVICE
from preparation import MAX_SEQ_LENGTH

nltk.download('omw-1.4')
sentence = "Mark's favourite game is **Cricket**."


sentence_for_bert = sentence.replace("**", " [tgt] ")
sentence_for_bert = " ".join(sentence_for_bert.split())

print(sentence_for_bert)

re_result = re.search(r"\[tgt\](.*)\[tgt\]", sentence_for_bert)
if re_result is None:
    print("\nIncorrect input format. Please try again.")

ambiguous_word = re_result.group(1).strip()

print("Word: ", ambiguous_word)


results = dict()

# wn_pos = wn.NOUN
# for i, synset in enumerate(set(wn.synsets(ambiguous_word, pos=wn_pos))):
for i, synset in enumerate(set(wn.synsets(ambiguous_word))):
    results[synset] = synset.definition()

pprint(results)

sense_keys = []
definitions = []
for sense_key, definition in results.items():
    sense_keys.append(sense_key)
    definitions.append(definition)


print(sense_keys)
print(definitions)


record = preparation.GlossSelectionRecord(
    "test", sentence_for_bert, sense_keys, definitions, [-1])

print('Record: ', [record])

features = preparation._create_features_from_records([record], MAX_SEQ_LENGTH, tokenizer,
                                                     cls_token=tokenizer.cls_token,
                                                     sep_token=tokenizer.sep_token,
                                                     cls_token_segment_id=1,
                                                     pad_token_segment_id=0)[0]

print(len(features))

for ftr in features:
    converted = tokenizer.convert_ids_to_tokens(ftr.input_ids)
    print(converted, len(converted))

with torch.no_grad():
    logits = torch.zeros(len(definitions), dtype=torch.double).to(DEVICE)
    for i, bert_input in list(enumerate(features)):
        print(bert_input)
        logits[i] = model.ranking_linear(
            model.bert(
                input_ids=torch.tensor(
                    bert_input.input_ids, dtype=torch.long).unsqueeze(0).to(DEVICE),
                attention_mask=torch.tensor(
                    bert_input.input_mask, dtype=torch.long).unsqueeze(0).to(DEVICE),
                token_type_ids=torch.tensor(
                    bert_input.segment_ids, dtype=torch.long).unsqueeze(0).to(DEVICE)
            )[1]
        )
    scores = softmax(logits, dim=0)

    preds = (sorted(zip(sense_keys, definitions, scores),
             key=lambda x: x[-1], reverse=True))

print("\n")
for pred in preds:
    print(pred)
sense = preds[0][0]
meaning = preds[0][1]

print("\nMost appropriate sense: ", sense)
print("Most appropriate meaning: ", meaning)
