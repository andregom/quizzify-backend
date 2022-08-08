import scipy
from sentence_transformers import SentenceTransformer, util

import alternative_sentences_generator


def sort_sentences_by_terms_proximity(
    original_sentence, list_of_falsified_sentences, reverse=True
):
    BERT_model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

    original_sentence_embedding = BERT_model.encode([original_sentence])
    false_sentences_embeddings = BERT_model.encode(list_of_falsified_sentences)

    distances = scipy.spatial.distance.cdist(
        original_sentence_embedding, false_sentences_embeddings, "cosine")[0]

    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])
    print(results)

    differing_sentences = []
    for idx, distance in results:
        differing_sentences.append(list_of_falsified_sentences[idx])
        print(list_of_falsified_sentences[idx])

    if reverse:
        differing_sentences = reversed(differing_sentences)

    return differing_sentences


def test():
    original_sentence = "The old woman was sitting under a tree and sipping coffee."

    list_of_falsified_sentences = alternative_sentences_generator.get_alternative_sentences(
        original_sentence
    )

    sort_sentences_by_terms_proximity(
        original_sentence, list_of_falsified_sentences)


# test()
