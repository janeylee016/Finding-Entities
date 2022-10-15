import spacy

nlp = spacy.load('en_core_web_sm',disable=['ner','textcat'])

# rule 3 function - preposition
def rule3(text):
    loc_prep = ['above', 'across', 'after','against', 'along', 'among', 'around', 'at', 'behind', 'below', 'beside',
           'between', 'by', 'close to', 'down', 'from', 'in front of', 'inside', 'in', 'into',
           'near', 'next to', 'off', 'on', 'onto', 'opposite', 'out of', 'outside', 'over', 'past', 'round', 'through',
           'to', 'towards', 'under', 'up']

    doc = nlp(text)
    sent = []
    sent1 = []
    # for sent in doc.sents:
    #     for token in sent:
    #         print(token.text, token.i - sent.start)
    for token in doc:
        # look for prepositions
        if token.pos_ == 'ADP' and token.text in loc_prep:
            phrase = ''
            #print(token, token.pos_, token.head, token.head.pos_)
            # for child in token.children:
            #     print('token: {}, child:{}'.format(token,child))
            #print(token.sent)
            #print(token.i, token)
            #print('edge:', token.right_edge, token.right_edge.i)
            #print('leftedge:',token.left_edge.i)

            # for tree in token.subtree:
            #     print('token: {}, tree:{}'.format(token,tree))
            #     print(token.i, tree.i)

            # if its head word is a noun or aux
            if token.head.pos_ in ['NOUN', 'AUX', 'VERB']:

                # append noun and preposition to phrase
                phrase += token.head.text
                phrase += ' ' + token.text
                #print("token head:", token.head.i)
                

                # check the nodes to the right of the prepositions
                for right_tok in token.rights:
                    print(token, right_tok, right_tok.pos_)
                    # append if it is a noun or proper noun
                    if (right_tok.pos_ in ['NOUN','PROPN']) or right_tok.dep_.endswith("obj") == True:
                        #print("right tok:", right_tok, right_tok.pos_, right_tok.i)
                        phrase += ' '+right_tok.text
                        #print('phrase:', phrase)
                        
                        try:
                            # s = token.sent
                            # print(s)
                            # a = doc
                            # print(a)
                            #print("i",token.head.i, right_tok.i)
                            s1 = doc[token.head.i:token.right_edge.i+1]
                            #print(s1)
                            #print('==================')
                        except:
                            print('error', right_tok)
                            #print('!!!!!!!!!!!!!!!!!!')
                    else:
                        print('NOO', right_tok, right_tok.pos_)
            



                    if len(phrase)>2:
                        sent.append(phrase)
                        sent1.append(s1)

    # for i in sent:
    #     #print("hello")
    #     tok = i.split(" ")
    #     print(tok)
    #     #print(tok[0], tok[-1])


    return sent, sent1