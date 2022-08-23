from .keywords_extractor import get_keywords
from ..question_generation.question_generator import generate_question
from ..question_generation.structures.multiple_choices.options_generator.options_generator import get_filtered_similar_options_to


def get_questions_and_alternatives(context, keywords):
    questions = generate_question
    alternatives = get_filtered_similar_options_to
    return {
        answer: {
            'questions': questions(context, answer),
            'alternatives': alternatives(answer)
        }
        for answer
        in keywords
    }


def mount_quiz_from(text, quick=False):
    context = text

    if quick or len(text) > 2000:
        from .summarizer import summarize_text
        summarized_text = summarize_text(text)
        context = summarized_text

    if quick:
        main_keywords = get_keywords(text, summarized_text)
        keywords = main_keywords
    else:
        keywords = main_keywords = get_keywords(text)

    multiple_choice_quest = get_questions_and_alternatives(context, keywords)

    print(len(text))
    return multiple_choice_quest


def test(text):
    print(mount_quiz_from(text))
    print(len(text))
