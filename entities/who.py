# GET PEOPLE NOUNS USING WIKIPEDIA
##https://stackoverflow.com/questions/54625493/how-to-group-wikipedia-categories-in-python (USE THIS)
#https://wikipedia.readthedocs.io/en/latest/code.html#api

import re 
import random
import wikipedia


#termlist = ['mother','person', 'girl', 'hello', 'teacher' ,'boy', 'father', 'sister' , 'brother', 'parents', 'family' ,'grandparents', 'relatives']
#termlist = set(nouns)


#Find if the links and backlinks contains a given term
def BoundedTerm(wikiPage, term):
    aList=wikiPage.links
    #print(aList)
    response = False
    #if any(term) in aList:
    if any(item in term for item in aList): 
        response = True
    return response

def wiki_who(termlist):
    '''
    termlist: nouns to check in wikipedia if it is a 'who' 
    '''
    # categories
    note = ['Human', 'Kinship', 'Adult', 'Profession', 'Child', 'Hero']
    who_container = []
    for val in termlist:
        try:
            cpage = wikipedia.WikipediaPage(val)

            # Identified as person if True
            if BoundedTerm(cpage, note) == True:
                who_container.append(val)
            
            else:
                continue

        except wikipedia.DisambiguationError as e:

            try:
                s = e.options[0]
                cpage = wikipedia.WikipediaPage(s)

                # Identified as person if True
                if BoundedTerm(cpage, note) == True:
                    who_container.append(val)
                
                else:
                    continue
            except:
                print("ERROR")
                
        except wikipedia.exceptions.PageError as e:
            print("None")

    return who_container


def professions(text):
    # Basic Professions
    professions = ["accountant", "actor", "actress", "architect", "astronomer", "author", "baker", "bricklayer", "driver", "butcher", "carpenter", "chef", "cook", "cleaner", "dentist", "designer", "doctor", "dustman", "electrician", "engineer", "worker", "farmer", "fireman", "fisherman", "florist", "gardener", "hairdresser", "journalist", "judge", "lawyer", "lecturer", "librarian", "lifeguard", "mechanic", "model", "newsreader", "nurse", "optician", "painter", "pharmacist", "photographer", "pilot", "plumber", "politician", "police", "policeman", "policewoman", "postman", "real estate agent", "agent", "receptionist", "scientist", "secretary", "shop assistant", "assistant", "soldier", "tailor", "teacher", "translator", "traffic warden", "waiter", "waitress", "surgeon"]
    if text.lower() in professions:
        text = text
    else:
        text = "NA"
    return text
