from .models.t5.execution.prediction import generate_question_from

def generate_question(context, answer):
    return generate_question_from(context, answer)


generate_question('', '')