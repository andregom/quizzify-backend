import os
import torch
from pathlib import Path
from transformers import AutoTokenizer
from fastT5 import get_onnx_model, get_onnx_runtime_sessions, OnnxT5

STORAGE_FOLDER_PATH = Path(__file__).resolve().parents[1].joinpath('storage')

optim_trained_model_path = STORAGE_FOLDER_PATH.joinpath('optimized')
tokenizer_path = STORAGE_FOLDER_PATH.joinpath('optimized')

encoder_path = optim_trained_model_path.joinpath('model-encoder-quantized.onnx')
decoder_path = optim_trained_model_path.joinpath('model-decoder-quantized.onnx')
init_decoder_path = optim_trained_model_path.joinpath('model-init-decoder-quantized.onnx')

optim_model_paths = encoder_path, decoder_path, init_decoder_path
model_sessions = get_onnx_runtime_sessions(optim_model_paths)
model = OnnxT5(optim_trained_model_path, model_sessions)
device = torch.device("cpu")
model = model.to(device)

tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

def optim_model_generate_question(context, answer):
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