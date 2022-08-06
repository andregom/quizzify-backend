import engines

# engines.utils.permutations.test()

# engines.sense2vec_options_generator.test()

# engines.utils.levenshtein.test()


def test_filters():
    Word = engines.utils.word.Word

    s2v = engines.sense2vec_options_generator

    word = Word('USA')

    distracters = s2v.get_similar_options_to(word.on_search_term_format)

    permutations = engines.utils.permutations

    words_filtrd_by_edit_distance = permutations.filter_by_edit_distance(
        distracters,
        word.original_graphy
    )

    levenshtein = engines.utils.levenshtein

    filtered_distracters = levenshtein.filter_by_nomralized_distanc(
        words_filtrd_by_edit_distance,
        word.original_graphy
    )

    print(filtered_distracters)


test_filters()
