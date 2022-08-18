import os
import zipfile
from pathlib import Path


COMMON_PARENT_FOLDER = Path(__file__).resolve().parents[2]

ROUTE_TO_BERTWSD_ZIP = [
    'models', 'bert_base-augmented-batch_size=128-lr=2e-5-max_gloss=6.zip']

BERTWSD_ZIP_FOLDER_PATH = COMMON_PARENT_FOLDER.joinpath(*ROUTE_TO_BERTWSD_ZIP)

SAVING_ROUTE = ['models']

ROUTE_TO_BERTWSD_MODEL = ['models', 'bert_base-augmented-batch_size=128-lr=2e-5-max_gloss=6']

PATH_TO_SAVE = COMMON_PARENT_FOLDER.joinpath(*SAVING_ROUTE)

PATH_TO_BERTWSD_MODEL = COMMON_PARENT_FOLDER.joinpath(*ROUTE_TO_BERTWSD_MODEL)

#  If unzipped folder exists don't unzip again.
if not os.path.isdir(PATH_TO_BERTWSD_MODEL):
    with zipfile.ZipFile(BERTWSD_ZIP_FOLDER_PATH, 'r') as zip_ref:
        zip_ref.extractall(PATH_TO_SAVE)
else:
    print(ROUTE_TO_BERTWSD_MODEL, " is extracted already")
