from FactScoreLite import FactScore
import os
from dotenv import load_dotenv
load_dotenv()
def check_fact(facts, knowledge_source, source_link):
    os.remove('facts.json')
    ft = FactScore()
    fact_pairs = {}
    for i in range(len(knowledge_source)):

        a, b, decisions = ft.get_factscore([facts], [knowledge_source[i]])
        print("Link: ", source_link[i])
        print(decisions)
        for decision in decisions[0]['decision']:
            fact_pairs[decision['fact']] = []
        for decision in decisions[0]['decision']:
            if decision['output'] == 'True':
                fact_pairs[decision['fact']].append(source_link[i])
        
    fact_list_object = []
    dem = 0
    for fact in fact_pairs:
        if len(fact_pairs[fact]) > 0:
            dem += 1
        fact_list_object.append({'fact': fact, 'sources': fact_pairs[fact]})
    score = dem/len(fact_pairs)
    if score >= 0.4:
        legit = True
    else:
        legit = False
    return fact_list_object, legit