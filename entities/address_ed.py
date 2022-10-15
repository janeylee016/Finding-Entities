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
pretrained_model_folder_path = './bert-ner-main/bert-ner-main/bert_ner_address/'

hyperparameter_set = {}
ner = BertNER(**hyperparameter_set)

model = BertNERModel.from_pretrained(os.path.join(pretrained_model_folder_path, 'trained_model'))
tok_name = './bert-ner-main/bert-ner-main/bert_ner_address/'
tokenizer = AutoTokenizer.from_pretrained(os.path.join(pretrained_model_folder_path, 'tok'))

with open(os.path.join(pretrained_model_folder_path, 'label_encoder.pkl'), 'rb') as f:
    label_encoder = pickle.load(f)

ner.load(model, tokenizer, label_encoder)

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
