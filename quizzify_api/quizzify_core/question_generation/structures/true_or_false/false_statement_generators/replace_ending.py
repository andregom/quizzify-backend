import string
import spacy
from allennlp.predictors.predictor import Predictor

predictor = Predictor.from_path(
    "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo-constituency-parser-2018.03.14.tar.gz",
    predictor_name="elmo-constituency-parser",
)

def predict_sentence():
    
    nlp = spacy.load('en_core_web_sm')

    sentence = "The old woman was sitting under a tree and sipping coffe."

    sentence = sentence.rstrip(string.punctuation)

    print(sentence)

    parser_output = predictor.predict(sentence=sentence)

    print(parser_output)


predict_sentence()