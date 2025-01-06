import torch
import time
import openai
from tqdm import tqdm
from database import Database
from pymongo import MongoClient
import hung
import hung
from langchain import PromptTemplate, LLMChain
import hung
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

llm = ChatOllama(model="gpt-3.5-turbo", temperature= 0.1)

def generate_keyword(text, hung):

    full_prompt = PromptTemplate(template=hung.PROMPT_GENERATE_KEYWORD, input_variables=['question'])
    llm_chain = LLMChain(prompt=full_prompt, llm=llm)
    
    
    keyword = llm_chain.run(text)
    return keyword

def generate_title_paper(clusters, list_text, hung):
    num_token_input = 0
    text_full = []
    step = 0
    for idx in tqdm(clusters):
        if step == 0 and len(list_text[idx][2]) > hung.MIN_OF_TOKEN:
            continue
        step += 1
        num_token_input +=  len(list_text[idx][2])
        if num_token_input >= hung.MIN_OF_TOKEN:
            break
        text_full.append(list_text[idx][2]+"\n")
    merge_text = " ".join(text_full)

    full_prompt = PromptTemplate(template=hung.PROMPT_GENERATE_TITLE, input_variables=['question'])
    llm_chain = LLMChain(prompt=full_prompt, llm=llm)
    
    
    title = llm_chain.run(merge_text)

    return title



def generate_new_paper(clusters, list_text, hung):
    num_token_input = 0
    text_full = []
    step = 0
    for id in tqdm(clusters):
        if step == 0 and len(list_text[id][1]) > hung.MIN_OF_TOKEN:
            continue
        step+=1
        num_token_input +=  len(list_text[id][1])
        if num_token_input >= hung.MIN_OF_TOKEN:
            break
        text_full.append(list_text[id][1]+"\n")
    merge_text = " ".join(text_full)

    full_prompt = PromptTemplate(template=hung.PROMT_GENERATE_PAPER, input_variables=['question'])
    llm_chain = LLMChain(prompt=full_prompt, llm=llm)
    
    
    paper = llm_chain.run(merge_text)
    return paper


def generate_summary_paper(clusters, list_text, hung):
    num_token_input = 0
    text_full = []
    step = 0
    for id in tqdm(clusters):
        if step == 0 and len(list_text[id][1]) > hung.MIN_OF_TOKEN:
            continue
        step+=1
        num_token_input +=  len(list_text[id][1])
        if num_token_input >= hung.MIN_OF_TOKEN:
            break
        text_full.append(list_text[id][1]+"\n")
    new_text = " ".join(text_full)


    full_prompt = PromptTemplate(template=hung.PROMPT_GENERATE_SUMMARY, input_variables=['question'])
    llm_chain = LLMChain(prompt=full_prompt, llm=llm)
    
    
    paper = llm_chain.run(new_text)
    return paper


def generate_keyword_of_cluster(text, hung):
    full_prompt = PromptTemplate(template=hung.PROMPT_GENERATE_KEYWORD_CLUSTER, input_variables=['question'])
    llm_chain = LLMChain(prompt=full_prompt, llm=llm)
    hashtag =  llm_chain.run(text)
    return hashtag
