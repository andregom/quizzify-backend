import itertools
from typing import List, Tuple
import itertools
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


from sentence_transformers import SentenceTransformer

from . import sense2vec_options_generator

model = SentenceTransformer('all-MiniLM-L12-v2')

def get_annswer_and_distracters_embeddings(answer, candidate_distracters):
    answer_embedding = model.encode([answer])
    distracter_embeddings = model.encode(candidate_distracters)
    return answer_embedding, distracter_embeddings


def max_marginal_relevance(
    doc_embedding: np.ndarray,
    word_embeddings: np.ndarray,
    words: List[str],
    top_n: int = 5,
    diversity: float = 0.9
) -> List[Tuple[str, float]]:
    # Extract similarity within words, and between words and the document
    word_doc_similarity =cosine_similarity(word_embeddings, doc_embedding)
    word_similarity = cosine_similarity(word_embeddings)

    # initialize cadidates and already chooses best keywrod/keyphrase
    keywords_idx = [np.argmax(word_doc_similarity)]
    candidates_idx = [i for i in range(len(words)) if i != keywords_idx[0]]

    for _ in range(top_n - 1):
        # Extract similarities within cadidates and
        # between cadidates and selected keywords/phrases
        candidate_similarities = word_doc_similarity[candidates_idx, :]
        target_similarities = np.max(word_similarity[candidates_idx][:, keywords_idx], axis=1)

        # Calculate MMR
        mmr = (1 - diversity) * candidate_similarities - diversity * target_similarities.reshape(-1, 1)
        mmr_idx = candidates_idx[np.argmax(mmr)]

        # Update keywrods & candidates
        keywords_idx.append(mmr_idx)
        candidates_idx.remove(mmr_idx)


    return [(words[idx], round(float(word_doc_similarity.reshape(1, -1)[0][idx]), 4)) for idx in keywords_idx]


def test(lexeme):

    original_word = lexeme

    s2v_distracters = sense2vec_options_generator.get_similar_options_to(
        original_word)

    s2v_distracters.insert(0, original_word)

    # print(s2v_distracters)

    
    answer_embed, distracter_embed = get_annswer_and_distracters_embeddings(
        original_word, s2v_distracters)

    # print(answer_embed, distracter_embed)


    final_distracters = max_marginal_relevance(answer_embed, distracter_embed, s2v_distracters, 5)
    filtered_distracters = []
    for dist in final_distracters:
        filtered_distracters.append(dist[0])

    answer = filtered_distracters[0]
    FilteredDistracters = filtered_distracters[1:]

    print(answer)
    print('-'*20)
    print(*FilteredDistracters, sep='\n')

    return filtered_distracters
