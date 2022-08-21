from .models.t5.execution.prediction import generate_question_from
from .models.t5.execution.optim_prediction import optim_model_generate_question


def generate_question(context, answer, optmize=True):
    if optmize:
        return optim_model_generate_question(context, answer)

    return generate_question_from(context, answer)
