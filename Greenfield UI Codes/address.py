# Libraries for govtech's model
import os
# os.listdir()
# os.chdir('C:/Users/user/Downloads/bert-ner-main/bert-ner-main')

from bert_ner.model.bert_ner import BertNER, BertNERModel
import pandas as pd
import pickle
import os
import argparse
from transformers import AutoTokenizer
import torch

import logging
import os
import random
import re

import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
from torch.nn import CrossEntropyLoss
from torch.utils.data import (DataLoader, RandomSampler, SequentialSampler,
                              TensorDataset)
from tqdm import tqdm, trange
from sklearn.preprocessing import LabelEncoder
import math
from datasets import load_metric


from transformers import (                           
                            AutoConfig, 
                            AutoTokenizer,
                            BertForTokenClassification,
                        )

from transformers import AdamW, get_linear_schedule_with_warmup

import pickle

## GOVTECH NER MODEL
pretrained_model_folder_path = 'C:/Users/Kokul/Desktop/FAKE/venv/bert-ner-main/bert-ner-main/bert_ner_address/'

hyperparameter_set = {}
ner = BertNER(**hyperparameter_set)

model = BertNERModel.from_pretrained(os.path.join(pretrained_model_folder_path, 'trained_model'))
tok_name = 'C:/Users/Kokul/Desktop/FAKE/venv/bert-ner-main/bert-ner-main/bert_ner_address/'
tokenizer = AutoTokenizer.from_pretrained(os.path.join(pretrained_model_folder_path, 'tok'))

with open(os.path.join(pretrained_model_folder_path, 'label_encoder.pkl'), 'rb') as f:
    label_encoder = pickle.load(f)

ner.load(model, tokenizer, label_encoder)

def address(story):
    def pred(query):
        predictions = ner.predict([query.split()], collapse_tokens=True)

        add = []
        word = []
        for i in range(len(predictions[0])):
            if predictions[0][i][1] == 'Address of Incident' and i != len(predictions[0])-1:
                w = predictions[0][i][0]
                word.append(w)
                if predictions[0][i+1][1] == 'O':
                    add.append(" ".join(word))
                    word = []
            elif predictions[0][i][1] == 'Address of Incident':
                add.append(" ".join(word))
            else:
                continue

        return add

    address = pred(story)

    new_add = []
    for add in address:
        if '#' in add:
            print(add)
            # find the '#' in address; is a list
            str1 = re.findall(r'\#\s\d{1,5}\s-\s\d{1,5}',add)
            for i in range(len(str1)):
                if i != (len(str1) - 1):
                    # split the space and then join without space
                    str2 = "".join(str1[i].split(" "))
                    # update the address
                    add = re.sub(str1[i],str2, add)
                else:
                    str2 = "".join(str1[i].split(" "))
                    add = re.sub(str1[i],str2, add)
                    new_add.append(add)
        else:
            new_add.append(add)  

    return new_add
