import textwrap
from pprint import pprint
from flashtext import KeywordProcessor
from nltk.tokenize import sent_tokenize
import traceback
# from nltk.corpus import wordnet
# from nltk.corpus import stopwords
import pke
import re
import nltk
import string
import itertools
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')


def tokenize_sentences(text):
    sentences = sent_tokenize(text)
    sentences = [sentence.strip()
                 for sentence in sentences if len(sentence) > 20]
    return sentences


text = """ Once upon a time, there lived a lion in the dense Amazon rainforest. While he was sleeping by resting his big head on his paws, a tiny little mouse unexpectedly crossed by and ran across the lion’s nose in haste. This woke up the lion and he laid his huge paw angrily on the tiny mouse to kill her.

The poor mouse begged the lion to spare her this time and she would pay him back on some other day. Hearing this, the lion was amused and wondered how could such a tiny creature ever help him. But he was in a good mood and in his generosity he finally let the mouse go.

A few days later, a hunter set a trap for the lion while the big animal was stalking for prey in the forest. Caught in the toils of a hunter’s net, the lion found it difficult to free himself and roared loudly in anger.

As the mouse was passing by, she heard the roar and found the lion struggling hard to free himself from the hunter’s net. The little creature quickly ran towards the lion’s trap that bound him and she gnawed the net with her sharp teeth until the net tore apart. Slowly she made a big hole in the net and soon the lion was able to free himself from the hunter’s trap.

The lion thanked the little mouse for her help and the mouse reminded him that she had finally repaid the lion for sparing her life before. Thereafter, the lion and the mouse became good friends and lived happily in the forest. """

wrapper = textwrap.TextWrapper(width=150)
word_list = wrapper.wrap(text=text)
for element in word_list:
    print(element)


def get_keywords(text):
    out=[]
    try:
        # extractor = pke.unsupervised.MultipartiteRank()
        extractor = pke.unsupervised.YAKE()
        extractor.load_document(input=text)
        grammar = r"""
                NP:
                    {<NOUN|PROPN>+}
            """
        extractor.ngram_selection(n=1)
        extractor.grammar_selection(grammar=grammar)
        # pos = {'VERB', 'ADJ', 'NOUN'}
        # pos ={'NOUN'}
        # stoplist = list(string.punctuation)
        # stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
        # stoplist += stopwords.words('english')
        # extractor.candidate_selection(n=1,pos=pos, stoplist=stoplist)
        extractor.candidate_selection(n=1)

        extractor.candidate_weighting(window=3,
                                      use_stems=False)

        keyphrases = extractor.get_n_best(n=30)
        

        for val in keyphrases:
            out.append(val[0])
    except:
        out = []
        traceback.print_exc()

    return out

keywords = get_keywords(text)[:8]
print ("keywords: ", keywords)

sentences = tokenize_sentences(text)
print (sentences)

def get_sentences_for_keyword(keywords, sentences):
    keyword_processor = KeywordProcessor()
    keyword_sentences = {}
    for word in keywords:
        keyword_sentences[word] = []
        keyword_processor.add_keyword(word)
    for sentence in sentences:
        keywords_found = keyword_processor.extract_keywords(sentence)
        for key in keywords_found:
            keyword_sentences[key].append(sentence)

    for key in keyword_sentences.keys():
        values = keyword_sentences[key]
        values = sorted(values, key=len, reverse=False)
        keyword_sentences[key] = values
    return keyword_sentences

keyword_sentence_mapping = get_sentences_for_keyword(keywords, sentences)
pprint (keyword_sentence_mapping)

