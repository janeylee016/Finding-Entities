# STEP9: LOCATIONS USING PATTERN EXTRACTIONS (NOUNS)
import spacy

from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

# rule 3 function - preposition
def where_rule(text):
    nlp = spacy.load('en_core_web_sm')
    loc_prep = ['above', 'across', 'after','against', 'along', 'among', 'around', 'at', 'behind', 'below', 'beside',
           'between', 'by', 'close to', 'down', 'from', 'in front of', 'inside', 'in', 'into',
           'near', 'next to', 'off', 'on', 'onto', 'opposite', 'out of', 'outside', 'over', 'past', 'round', 'through',
           'to', 'towards', 'under', 'up']

    doc = nlp(text)
    sent = []
    sent1 = []
    for token in doc:
        # look for prepositions
        if token.pos_ == 'ADP' and token.text in loc_prep:
            phrase = ''

            # if its head word is a noun or aux
            if token.head.pos_ in ['VERB']:
            #if token.head.pos_ in ['NOUN', 'AUX', 'VERB']:

                # append noun and preposition to phrase
                phrase += token.head.text
                phrase += ' ' + token.text
                
                # check the nodes to the right of the prepositions
                for right_tok in token.rights:
                    if (right_tok.pos_ in ['NOUN','PROPN']): 
                        phrase += ' '+right_tok.text
                        sent.append(phrase)
 
    return set(sent)


def sparql():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    # From https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples#Cats
    sparql.setQuery("""
    #PREFIX dbo: <http://dbpedia.org/ontology/>

    SELECT ?place ?placeLabel
    WHERE {
    {?place wdt:P279 wd:Q107425 .}
    UNION
    {?place wdt:P279 wd:Q2221906 .}
    UNION
    {?place wdt:P279 wd:Q2385804 .}
    UNION
    {?place wdt:P279 wd:Q334923 .}
    UNION
    {?place wdt:P279 wd:Q811430 .}
    UNION
    {?place wdt:P279 wd:Q7493941 .}
    UNION
    {?place wdt:P279 wd:Q41176 .}
    UNION
    {?place wdt:P279 wd:Q224922 .}
    UNION
    {?place wdt:P279 wd:Q17350442 .}
    UNION
    {?place wdt:P279 wd:Q13226383 .}
    UNION
    {?place wdt:P279 wd:Q180516 .}
    UNION
    {?place wdt:P279 wd:Q1656682 .}
    UNION
    {?place wdt:P279 wd:Q35145263 .}
    UNION
    {?place wdt:P279 wd:Q11755880 .}
    UNION
    {?place wdt:P279 wd:Q43229 .}
    UNION
    {?place wdt:P279 wd:Q11707 .}
    UNION
    {?place wdt:P279 wd:Q8463304 .}
    
    SERVICE wikibase:label {bd:serviceParam wikibase:language "[AUTO_LANGUAGE], en".}
    } 
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    results_df = pd.json_normalize(results['results']['bindings'])
    #print(results_df[['place.value', 'placeLabel.value']])
    return results_df["placeLabel.value"]