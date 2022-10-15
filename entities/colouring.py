# Colouring
from termcolor import colored
import re

import warnings, operator, html
from IPython.core.display import display, HTML 

def colour(story, who, when, where, what, new_add):
    text = story
    ls_who = set(who)
    #print("who {}:".format(ls_who))
    ls_when = set(when)
    #print("when {}:".format(ls_when))
    ls_where = set(where)
    print("where: {}".format(ls_where))
    ls_what = set(what)
    #print("what: {}".format(ls_what))
    for t in ls_who:
        text = re.sub(r'\b{}\b'.format(t),colored(t,'white','on_blue'),text)   
    for t in ls_when:
        text = re.sub(r'\b{}\b'.format(t),colored(t,'white','on_green'),text)
    for t in new_add:
        text = re.sub(t,colored(t,'white','on_red'),text)
    for t in ls_where:
        text = re.sub(r'\b{}\b'.format(t),colored(t,'white','on_red'),text)
    for t in ls_what:
        text = re.sub(r'\b{}\b'.format(t),colored(t,'white','on_magenta'),text)

    return print(text)


def colouring2(story, who, when, where, what, new_add):
    text = story
    ls_who = set(who)
    print("who {}:".format(ls_who))
    ls_when = set(when)
    print("when {}:".format(ls_when))
    ls_where = set(where)
    print("where: {}".format(ls_where))
    ls_what = set(what)
    print("what: {}".format(ls_what))
    new_add = new_add

    for t in ls_who:
        text = re.sub(r'\b{}\b'.format(t),'<span style="background-color:rgb(174, 212, 255);">' + html.escape(t) + '<span style="font-size: 60%; font-weight:bold"> WHO</span>' + '</span>',text)
    for t in ls_when:
        text = re.sub(r'\b{}\b'.format(t),'<span style="background-color:rgba(123,239,178,0.5);">' + html.escape(t) + '<span style="font-size: 60%; font-weight:bold"> WHEN</span>' + '</span>',text)
    for t in ls_where:
        text = re.sub(r'\b{}\b'.format(t),'<span style="background-color:rgb(255, 204, 204);">' + html.escape(t) + '<span style="font-size: 60%; font-weight:bold"> WHERE</span>' + '</span>',text)
    for t in new_add:
        text = re.sub(r'\b{}\b'.format(t),'<span style="background-color:rgb(255, 204, 204);">' + html.escape(t) + '<span style="font-size: 60%; font-weight:bold"> WHERE</span>' + '</span>',text)
    for t in ls_what:
        text = re.sub(r'\b{}\b'.format(t),'<span style="background-color:rgb(255, 255, 179);">' + html.escape(t) + '<span style="font-size: 60%; font-weight:bold"> WHAT</span>' + '</span>',text)

    print(text)
    
    #return display(HTML(text))
    return text