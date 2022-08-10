from pathlib import Path
from pydoc import resolve
import pandas as pd
from sklearn.utils import shuffle
from datasets import load_dataset
from pprint import pprint



STORAGE_FOLDER_PATH = Path(__file__).resolve().parents[1].joinpath('storage')

DATASETS_FOLDER_PATH = STORAGE_FOLDER_PATH.joinpath('datasets')

train_dataset = load_dataset('squad', split='train')
valid_dataset = load_dataset('squad', split='validation')

sample_validation_dataset = next(iter(valid_dataset))
pprint(sample_validation_dataset)

context = sample_validation_dataset['context']
question = sample_validation_dataset['question']
answer = sample_validation_dataset['answers']['text'][0]

print("context: ", context)
print("question: ", question)
print("answer: ", answer)

pd.set_option('display.max_colwidth', None)
df_train = pd.DataFrame(columns = ['context','answer','question'])
df_validation = pd.DataFrame(columns = ['context','answer','question'])

print(df_validation)
print(df_train)


def count_short_and_long_answers_on(dataset, dataframe):
    long_answrs_number = 0
    short_answrs_number = 0
    
    for index, value in enumerate(dataset):
        text_passage = value['context']
        question = value['question']
        answer = value['answers']['text'][0]
        number_of_words = len(answer.split())
        if number_of_words >= 7:
            long_answrs_number = long_answrs_number + 1
            continue
        else:
            dataframe.loc[short_answrs_number] = [text_passage] + [answer] + [question]
            short_answrs_number = short_answrs_number + 1

    return dataframe, long_answrs_number, short_answrs_number



df_train, long, short = count_short_and_long_answers_on(train_dataset, df_train)

print('long answers in tran dataset: ', long)
print('short answers in train dataset: ', short)

df_validation, long, short = count_short_and_long_answers_on(valid_dataset, df_validation)

print('long answers in tran dataset: ', long)
print('short answers in train dataset: ', short)

df_train = shuffle(df_train)
df_validation = shuffle(df_validation)

print(df_train)
print(df_validation)

df_train.head()
df_validation.head()

train_storage_path = DATASETS_FOLDER_PATH.joinpath('squad_t5_train.csv')
validation_storage_path = DATASETS_FOLDER_PATH.joinpath('squad_t5_validation.csv')
df_train.to_csv(train_storage_path, index=False)
df_validation.to_csv(validation_storage_path, index=False)

