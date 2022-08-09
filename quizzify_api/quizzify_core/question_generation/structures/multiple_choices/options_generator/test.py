import engines

# engines.utils.permutations.test()

# engines.sense2vec_options_generator.test()

# engines.utils.levenshtein.test()

Word = engines.utils.word.Word

# def test_sentence_transformers(lexeme):
#     word = Word(lexeme)

    
# test_sentence_transformers('Rihanna')


def test_filters(lexical_unity):
    
    word = Word(lexical_unity)

    s2v = engines.sense2vec_options_generator


    distracters = s2v.get_similar_options_to(word.on_search_term_format)

    permutations = engines.utils.permutations

    words_filtrd_by_edit_distance = permutations.filter_by_edit_distance(
        distracters,
        word.original_graphy
    )

    words_filtrd_by_edit_distance = permutations.filter_all_by_edit_distance(
        distracters
    )

    levenshtein = engines.utils.levenshtein

    filtered_distracters = levenshtein.filter_by_nomralized_distanc(
        words_filtrd_by_edit_distance,
        word.original_graphy,
        0.8
    )

    sentence_transformers = engines.sentence_transformers_options_generator

    sentence_transformers.test('Barack Obama')
    sentence_transformers.test('Will Smith')

    # distracters = sentence_transformers.get_annswer_and_distracters_embeddings(
    #     word.original_graphy,
    #     distracters
    # )

    print(filtered_distracters)


test_filters('USA')
print()
test_filters('Donald Trump')
print()
test_filters('Barack Obama')
