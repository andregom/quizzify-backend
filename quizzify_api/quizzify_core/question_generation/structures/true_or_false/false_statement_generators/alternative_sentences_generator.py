import tensorflow as tf
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer

import nltk
nltk.download('punkt')
from nltk import tokenize

from utils.sentence import Sentence


# print(tf.reduce_sum(tf.random.normal([1000, 1000])))

# print(tf.config.list_physical_devices('GPU'))

GPT2tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
GPT2model = TFGPT2LMHeadModel.from_pretrained("gpt2",pad_token_id=GPT2tokenizer.eos_token_id)

def get_alternative_sentences(original_sentence):
    sentence = Sentence(original_sentence)

    partial_sentence = sentence.partial_sentence
    input_ids = GPT2tokenizer.encode(partial_sentence,return_tensors='tf')
    maximum_length = len(partial_sentence.split())+40

    sample_outputs = GPT2model.generate(
        input_ids, 
        do_sample=True, 
        max_length=maximum_length, 
        top_p=0.80, # 0.85 
        top_k=30,   #30
        repetition_penalty  = 10.0,
        num_return_sequences=10
    )

    generated_sentences=[]

    for i, sample_output in enumerate(sample_outputs):
        decoded_sentence = GPT2tokenizer.decode(sample_output, skip_special_tokens=True)
        final_sentence = tokenize.sent_tokenize(decoded_sentence)[0]
        generated_sentences.append(final_sentence)
        print (i,": ",final_sentence)

    return generated_sentences

    
def test():
    
    original_sentence = 'The old woman was sitting under a tree and sipping coffee.'

    get_alternative_sentences(original_sentence)