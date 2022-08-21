def generate_question(context, answer, optmize=True):
    if optmize:
        from .models.t5.execution.optim_prediction import optim_model_generate_question
        return optim_model_generate_question(context, answer)

    from .models.t5.execution.prediction import generate_question_from
    return generate_question_from(context, answer)
