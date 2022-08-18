import re
import nltk
import torch
import statistics


from statistics import mode
from torch.nn.functional import softmax
from nltk.corpus import wordnet as wn

nltk.download('omw-1.4')

import model_loader as model_loader

from model_loader import DEVICE, tokenizer

from keywords_extract import keyword_sentence_mapping

from preparation import (
    MAX_SEQ_LENGTH,
    GlossSelectionRecord,
    _create_features_from_records
)



def get_sense(sent):
    re_result = re.search(r"\[tgt\](.*)\[tgt\]", sent)
    if re_result is None:
        print("\nIncorrect input format. Please try again.")

    ambiguous_word = re_result.group(1).strip()
    results = dict()

    for i, synset in enumerate(set(wn.synsets(ambiguous_word))):
        results[synset] = synset.definition()

    if len(results) == 0:
        return None

    sense_keys = []
    definitions = []
    for sense_key, definition in results.items():
        sense_keys.append(sense_key)
        definitions.append(definition)

    record = GlossSelectionRecord("test", sent, sense_keys, definitions, [-1])

    features = _create_features_from_records([record], MAX_SEQ_LENGTH, tokenizer,
                                             cls_token=tokenizer.cls_token,
                                             sep_token=tokenizer.sep_token,
                                             cls_token_segment_id=1,
                                             pad_token_segment_id=0,
                                             disable_progress_bar=True)[0]

    print('Features: ', features)

    with torch.no_grad():
        logits = torch.zeros(len(definitions), dtype=torch.double).to(DEVICE)
        for i, bert_input in list(enumerate(features)):
            logits[i] = model_loader.model.ranking_linear(
                model_loader.model.bert(
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

    sense = preds[0][0]
    meaning = preds[0][1]
    return sense


def get_synsets_for_word(word):
    return set(wn.synsets(word))


keyword_best_sense = {}

for keyword in keyword_sentence_mapping:
    print("\n\n")
    print("Original word: ", keyword)
    try:
        identified_synsets = get_synsets_for_word(keyword)
    except:
        continue
    for synset in identified_synsets:
        print(synset, "   ", synset.definition())
    top_3_sentences = keyword_sentence_mapping[keyword][:3]
    best_senses = []
    for sent in top_3_sentences:
        insensitive_keyword = re.compile(re.escape(keyword), re.IGNORECASE)
        modified_sentence = insensitive_keyword.sub(
            " [tgt] "+keyword+" [tgt] ", sent, count=1)
        modified_sentence = " ".join(modified_sentence.split())
        print("modified sentence ", modified_sentence)
        best_sense = get_sense(modified_sentence)
        best_senses.append(best_sense)
    best_sense = mode(best_senses)
    print("Best sense: ", best_sense)
    defn = best_sense.definition()
    print(defn)
    keyword_best_sense[keyword] = defn
