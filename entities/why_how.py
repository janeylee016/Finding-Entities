from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import torch
import numpy as np

def qa(questions, context):
    model_name = "deepset/bert-large-uncased-whole-word-masking-squad2"

    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    result = []

    for question in questions:
        # a) Get predictions
        nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
        QA_input = {
            'question': question,
            'context': context
        }
        res = nlp(QA_input)

        print(res['answer'])

        result.append(res['answer'])

        # return res['answer'], res['score']
    return result