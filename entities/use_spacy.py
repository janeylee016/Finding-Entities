# SPACY NER

import spacy
from spacy import displacy

def use_spacy(story):
    '''
    story: text used
    '''
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(story)

    loc_sp = []
    when_sp = []
    person_sp = []

    for X in doc.ents:
        if X.label_ == "ORG" or X.label_ == "GPE" or X.label_ == "LOC" or X.label_ == "FAC":
            loc_sp.append(X.text.lower())
        elif X.label_ == "PERSON":
            person_sp.append(X.text.lower())
        elif X.label_ == "DATE" or X.label_=="TIME":
            when_sp.append(X.text.lower())
        else:
            #print(X.text, X.label_)
            continue

    return doc, loc_sp, when_sp, person_sp 

