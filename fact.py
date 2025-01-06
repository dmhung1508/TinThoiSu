from FactScoreLite import FactScore
import os
from dotenv import load_dotenv
load_dotenv()
def check_fact(facts, knowledge_source):
    ft = FactScore()
    a,b = ft.get_factscore([facts], [knowledge_source])
    if b > 0:
        return True
    else:
        return False
