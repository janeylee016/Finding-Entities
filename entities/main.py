from flask import Blueprint, render_template, request, session, redirect, url_for, flash, make_response, jsonify
import re

from werkzeug.utils import secure_filename

import spacy
import warnings, operator, html
from IPython.core.display import display, HTML 

# from entities.location import rule3
# from entities.address import pred
from entities.address import address
from entities.use_spacy import use_spacy
from entities.who import wiki_who, professions
from entities.where import where_rule, sparql
from entities.colouring import colour, colouring2
from entities.why_how import qa


#main = Blueprint("main", __name__, static_folder="static/css", template_folder="templates")
main = Blueprint("main", __name__, static_folder="static/imgs", template_folder="templates")


@main.route('/home')
@main.route("/", methods=["POST", "GET"])
def home():
    print(request.base_url)
    if request.method == "POST" and ("input-submit" in request.form):
        session.permanent = True
        text = request.form['input']
        #session['text'] = text
        story = text.lower()
        cap_story = text
        doc, loc_sp, when_sp, person_sp = use_spacy(cap_story)

        nouns = []
        for token in doc:
            #print(token.text, token.pos_, token.tag_, token.dep_)
            if (token.pos_ == 'NOUN') == True:
                nouns.append(token.text)

        termlist = set(nouns)
    
        # # STEP 6 WHO - get people nouns
        who_container = wiki_who(termlist)

        # WHO - Get professions
        who_prof = []
        for val in termlist:
            value = professions(val)
            if value != "NA":
                who_prof.append(value)

        # WHO
        who = person_sp + who_container + who_prof
        print('WHO {}'.format(who))

        # STEP 7 (nouns - who)
        remaining_nouns = set(nouns) - set(who)

        # WHEN (step 8) 
        when_list = []
        for item in set(when_sp):
            i = item.split(" ")
            for token in i:
                when_list.append(token)

        when = set(when_sp)
        when_token = set(when_list)
        print("WHEN: {}".format(when))
        #print("WHEN_token: {}".format(when_token))

        # WHERE - locations using patterns (step 9)
        sent = list(where_rule(story.lower()))
        nlp = spacy.load('en_core_web_sm')

        where_nouns_sp = []
        for item in sent:
            item = nlp(item)
            for token in item:
                #print(token.text, token.pos_, token.tag_, token.dep_)
                if token.pos_ == "PROPN" or token.pos_ == "NOUN":
                    where_nouns_sp.append(str(token))
        
        # WHERE - locations using SPARQL
        res = sparql()
        where_nouns_db = []
        for noun in remaining_nouns:
            if noun in list(res):
                #print("noun: {}".format(noun))
            
                where_nouns_db.append(noun)

        where_nouns = where_nouns_sp + where_nouns_db + loc_sp
        where = set(where_nouns) - set([x.lower() for x in who]) - set([x.lower() for x in when])
        print(where)

        # Where - locations using GovTech Address Model (step 10)
        new_add = address(story)
        where_sum = list(where) + list(new_add)

        # What (step 11)
        what = set(nouns) - set(who) -set(where) -set(when_token) 

        result = colouring2(story, who, when, where, what, new_add)
        #print(result)
        test = result

        # WHY. HOW 
        questions = ["how was the crime committed", "how long was the sentence", "how old was the victim", "how much was the fine", "Why was the person arrested"]
        print(questions)
        context = story
        why_how = qa(questions, context)
        print(why_how)
        qn1 = why_how[0]
        qn2 = why_how[1]
        qn3 = why_how[2]
        qn4 = why_how[3]
        qn5 = why_how[4]


        return render_template('home.html', who=list(set(who)), when=list(when), where_sum=where_sum, new_add=list(new_add), what=list(what), qn1=qn1, qn2=qn2, qn3=qn3, qn4=qn4, qn5=qn5, test=test)
    return render_template('home.html')

        # if input:
        #     return redirect(url_for('main.results', input=input))
        # else:
        #     flash("No inputs given. Please give your inputs in the text box below.")
    

    
    # # WHERE - locations using patterns (step 9)
    # sent = list(where_rule(story.lower()))
    # nlp = spacy.load('en_core_web_sm')

    # where_nouns_sp = []
    # for item in sent:
    #     item = nlp(item)
    #     for token in item:
    #         #print(token.text, token.pos_, token.tag_, token.dep_)
    #         if token.pos_ == "PROPN" or token.pos_ == "NOUN":
    #             where_nouns_sp.append(str(token))

    # # WHERE - locations using SPARQL
    # res = sparql()
    # where_nouns_db = []
    # for noun in remaining_nouns:
    #     if noun in list(res):
    #         print("noun: {}".format(noun))
            
    #         where_nouns_db.append(noun)

    # where_nouns = where_nouns_sp + where_nouns_db + loc_sp
    # where = set(where_nouns) - set([x.lower() for x in who])
    # print(where)

    # # Where - locations using GovTech Address Model (step 10)
    # new_add = address(story)

    # # What (step 11)
    # what = set(nouns) - set(who) -set(where) -set(when_token) 

    # result = colouring2(story, who, when, where, what)
  

    ####################
    # if (request.method == "POST") and ("file-submit" in request.form):    
    #     file = request.files['filename']
    #     if file:
    #         file = request.files['filename']
    #         data = []
    #         filename = secure_filename(file.filename)
    #         for line in file:
    #             data.append(line) 
    #         text = ''.join(map(bytes.decode,data))
  
    #         return redirect(url_for('main.results', text=text))
    #     else:
    #         flash("Please upload a file")
    
    #return render_template("home.html")




# @main.route('/results', methods=["POST", "GET"])
# def results():
#     input = request.args.get('input') #input text
#     loc, response = rule3(input)
#     locations = pred(input)
#     text = request.args.get('text') # file upload text
#     res = {}
#     res['loc'] = locations
#     res['text'] = input
#     resp = jsonify(res)
#     for item in resp.loc:
#         i = re.search(item, input)

#     return render_template('results_file.html', input = input)

# @main.route('/results', methods=["POST", "GET"])
# def results():
#     input = request.args.get('input') #input text
#     text = request.args.get('text') # file upload text
#     # if request.args.get('input') != None:
#     #     input = request.args.get('input')
#     # else:
#     #     input = request.args.get('text')
#     # if input != None:
#     #     input = input
#     # else:
#     #     input = text
#     loc, response = rule3(input)
#     locations = pred(input)
#     print(response, type(response))
#     for i in response:
#         replace = "<span style='color:blue;font-weight:bold'>" + str(i) + "</span>"
        
#         input = re.sub(str(i), replace, input)
#         print(input, type(input))
       
#     print(input)
#     return render_template('results_file.html', input = input)

