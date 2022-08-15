import torch
from pathlib import Path
from transformers import T5ForConditionalGeneration, T5Tokenizer

STORAGE_FOLDER_PATH = Path(__file__).resolve().parents[1].joinpath('storage')

trained_model_path = STORAGE_FOLDER_PATH.joinpath('model')
tokenizer_path = STORAGE_FOLDER_PATH.joinpath('tokenizer')

model = T5ForConditionalGeneration.from_pretrained(trained_model_path)
tokenizer = T5Tokenizer.from_pretrained(tokenizer_path)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
model.eval()


def generate_question_from(context, answer):
    text = "context: " + context + " " + "answer: " + answer

    encoding = tokenizer.encode_plus(
        text, max_length=512, padding=True, return_tensors="pt")
    input_ids, attention_mask = encoding["input_ids"].to(
        device), encoding["attention_mask"].to(device)

    beam_outputs = model.generate(
        input_ids=input_ids, attention_mask=attention_mask,
        max_length=72,
        early_stopping=True,
        num_beams=5,
        num_return_sequences=3
    )

    questions = []
    for beam_output in beam_outputs:
        decoded_outputs = tokenizer.decode(
            beam_output, skip_special_tokens=True, clean_up_tokenization_spaces=True
        )
        questions.append(decoded_outputs)

    return questions
    

def test():
    context = "The Affordable Care Act, which is also referred to as ACA or Obamacare, was signed into law by President Barack Obama in 2010. The act was a major overhaul of the U.S. healthcare system, reducing the amount of uncompensated care the average family pays for. Obamacare originally required everyone to have health insurance and offered cost assistance to those who could not afford a plan on their own."
    answer = "Barack Obama"

    questions = generate_question_from(context, answer)

    print(*questions, sep="\n")
