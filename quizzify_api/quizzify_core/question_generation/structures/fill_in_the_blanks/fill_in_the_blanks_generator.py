from pprint import pprint
import textwrap

from IPython.display import display, HTML
import xml.etree.ElementTree as et
import random

text = """There is a lot of volcanic activity at divergent plate boundaries in the oceans. For example, many undersea volcanoes are found along the Mid-Atlantic Ridge. This is a divergent plate boundary that runs north-south through the middle of the Atlantic Ocean. As tectonic plates pull away from each other at a divergent plate boundary, they create deep fissures, or cracks, in the crust. Molten rock, called magma, erupts through these cracks onto Earth’s surface. At the surface, the molten rock is called lava. It cools and hardens, forming rock. Divergent plate boundaries also occur in the continental crust. Volcanoes form at these boundaries, but less often than in ocean crust. That’s because continental crust is thicker than oceanic crust. This makes it more difficult for molten rock to push up through the crust. Many volcanoes form along convergent plate boundaries where one tectonic plate is pulled down beneath another at a subduction zone. The leading edge of the plate melts as it is pulled into the mantle, forming magma that erupts as volcanoes. When a line of volcanoes forms along a subduction zone, they make up a volcanic arc. The edges of the Pacific plate are long subduction zones lined with volcanoes. This is why the Pacific rim is called the “Pacific Ring of Fire.”"""

wrapper = textwrap.TextWrapper(width=150)
word_list = wrapper.wrap(text=text)
for element in word_list:
    print(element)

import string
import re
import nltk
import string
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
import pke
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import traceback
from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor
import spacy

nlp = spacy.load('en_core_web_sm')

def get_sentences_from(text):
    sentences = sent_tokenize(text)
    sentences = [sentence.strip() for sentence in sentences if len(sentence) > 20]
    return sentences

sentences = get_sentences_from(text)
print (sentences)

# nouns, adjectives and verbs
def get_main_parts_of_speech_from(text):
    key_words = []
    try:
        extractor = pke.unsupervised.MultipartiteRank()
        extractor.load_document(input=text, language='en')
        #    not contain punctuation marks or stopwords as candidates.
        pos = {'VERB', 'ADJ', 'NOUN'}
        stoplist = list(string.punctuation)
        stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
        stoplist += stopwords.words('english')
        # extractor.candidate_selection(pos=pos, stoplist=stoplist)
        extractor.candidate_selection(pos=pos)
        # 4. build the Multipartite graph and rank candidates using random walk,
        #    alpha controls the weight adjustment mechanism, see TopicRank for
        #    threshold/method parameters.
        extractor.candidate_weighting(alpha=1.1,
                                      threshold=0.75,
                                      method='average')
        keyphrases = extractor.get_n_best(n=30)
        

        for val in keyphrases:
            key_words.append(val[0])
    except:
        key_words = []
        traceback.print_exc()

    return key_words

main_parts_of_speech = get_main_parts_of_speech_from(text)
print("keywords: ", main_parts_of_speech)

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
        values = sorted(values, key=len, reverse=True)
        keyword_sentences[key] = values
    return keyword_sentences

keyword_sentence_mapping_noun_verbs_adj = get_sentences_for_keyword(main_parts_of_speech, sentences)
pprint (keyword_sentence_mapping_noun_verbs_adj)

def get_fill_in_the_blanks(sentence_mapping):
    out={"title":"Fill in the blank spaces by typing and matching them with the corresponding words at the top"}
    blank_sentences = []
    processed = []
    keys=[]
    for key in sentence_mapping:
        if len(sentence_mapping[key])>0:
            sent = sentence_mapping[key][0]
            # Compile a regular expression pattern into a regular expression object, which can be used for matching and other methods
            insensitive_sent = re.compile(re.escape(key), re.IGNORECASE)
            no_of_replacements =  len(re.findall(re.escape(key),sent,re.IGNORECASE))
            line = insensitive_sent.sub('<></>', sent)
            if (sentence_mapping[key][0] not in processed) and no_of_replacements<2:
                blank_sentences.append(line.split('<></>'))
                processed.append(sentence_mapping[key][0])
                keys.append(key)
    out["sentences"]=blank_sentences[:10]
    out["keys"]=keys[:10]
    return out


fill_in_the_blanks = get_fill_in_the_blanks(keyword_sentence_mapping_noun_verbs_adj)
pprint(fill_in_the_blanks)

root = et.Element("div")
root.set('style', 'display:flex-box;')

heading = et.Element("h2")
heading.text = fill_in_the_blanks['title']

keywords = et.Element("ul")
keywords.set('style', 'color:blue;')

all_keys = fill_in_the_blanks['keys']
random.shuffle(all_keys)
for blank in all_keys:
  child=et.Element("li")
  child.text = blank
  keywords.append(child)

sentences = et.Element("ol")
sentences.set('style', 'color:brown;')
for sentence in fill_in_the_blanks['sentences']:
  child=et.Element("li")
  quote = et.Element("div")
  quote.text = sentence[0]
  quote.append(et.Element("input"))
  quote.tail = sentence[1]
  quote.set('style', 'display:inline-block;')
  child.append(quote)
  sentences.append(child)
  sentences.append(et.Element("br"))

heading_content = et.Element("h4")

root.append(heading)
heading_content.append(keywords)
heading_content.append(sentences)
root.append(heading_content)

xmlstr = et.tostring(root)
xmlstr = xmlstr.decode("utf-8") 
display(HTML(xmlstr))

with open("html_output.html", "w") as file:
    file.write(xmlstr)