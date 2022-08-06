from similarity.normalized_levenshtein import NormalizedLevenshtein

normalized_levenshtein = NormalizedLevenshtein()

def normalized_levenshtein_distanc_between(word1, word2):
    return normalized_levenshtein.distance(word1, word2)

def filter_by_nomralized_distanc(list, original_word, treshold=0.7):
    return [
        word 
        for word in list 
        if normalized_levenshtein_distanc_between(word, original_word) > treshold]


def test():
    print(normalized_levenshtein_distanc_between('USA', 'U.S.A'))
    print(normalized_levenshtein_distanc_between('USA', 'U.S'))
    print(normalized_levenshtein_distanc_between('USA', 'America'))
    print(normalized_levenshtein_distanc_between('USA', 'Canada'))
    print(normalized_levenshtein_distanc_between('USA', 'United States'))