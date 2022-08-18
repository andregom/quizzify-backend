from pathlib import Path
from fastT5 import export_and_get_onnx_model,generate_onnx_representation,quantize
from transformers import T5Config,AutoTokenizer

STORAGE_FOLDER_PATH = Path(__file__).resolve().parents[1].joinpath('storage')

trained_model_path = str(STORAGE_FOLDER_PATH.joinpath('model'))

optmization_export_path = STORAGE_FOLDER_PATH.joinpath('optimized')

# Step 1. convert huggingfaces t5 model to onnx
onnx_model_paths = generate_onnx_representation(trained_model_path, output_path=optmization_export_path)

# Step 2. (recommended) quantize the converted model for fast inference and to reduce model size.
quant_model_paths = quantize(onnx_model_paths)

tokenizer_onnx = AutoTokenizer.from_pretrained(trained_model_path)
config = T5Config.from_pretrained(trained_model_path)

tokenizer_onnx.save_pretrained(optmization_export_path)
config.save_pretrained(optmization_export_path)
