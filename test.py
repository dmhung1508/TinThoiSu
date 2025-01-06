# import torch
# import time
# import openai
# from tqdm import tqdm
# from database import Database
# from pymongo import MongoClient

# from openai import OpenAI

# client = OpenAI(
#     base_url='http://localhost:11434/v1/',

#     # required but ignored
#     api_key='ollama',
# )

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "system",
#             "content": "Sinh ra một tiêu đề bằng tiếng Việt ngắn và hay nhất trong đoạn trên:"
#         },
#         {
#             'role': 'user',
#             'content': input()
#         }
#     ],
#     temperature=0.1,
#     max_tokens = 2056,
#     model='dinhhung1508/vistral7b:latest',
# )
# def generate_keyword(text, config):
#     text = "\n".join(text)

#     prompt = text + "\n" + config.PROMPT_GENERATE_KEYWORD
#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "system",
#                 "content": config.PROMPT_GENERATE_KEYWORD
#             },
#             {
#                 'role': 'user',
#                 'content': input()
#             }
#         ],
#         temperature=0.1,
#         max_tokens = 2056,
#         model='dinhhung1508/vistral7b:latest',
#     )
#     completion = openai.ChatCompletion.create(
#         model = config.OPEN_AI_MODEL_NAME,
#         messages = [
#         {'role': 'user', 'content': prompt}
#         ],
#         temperature = 0,
#         request_timeout=config.REQUEST_TIMEOUT    
#     )
#     keyword =  completion['choices'][0]['message']['content']
#     return keyword

# def generate_title_paper(clusters, list_text, config):
#     openai.api_key = config.API_KEY #API key của chatGPT
#     num_token_input = 0
#     text_full = []
#     step = 0
#     for idx in tqdm(clusters):
#         if step == 0 and len(list_text[idx][2]) > config.MIN_OF_TOKEN:
#             continue
#         step += 1
#         num_token_input +=  len(list_text[idx][2])
#         if num_token_input >= config.MIN_OF_TOKEN:
#             break
#         text_full.append(list_text[idx][2]+"\n")
#     merge_text = " ".join(text_full)


#     prompt = merge_text+ "\n"+ config.PROMPT_GENERATE_TITLE
#     completion = openai.ChatCompletion.create(
#         model = config.OPEN_AI_MODEL_NAME,
#         messages = [
#         {'role': 'user', 'content': prompt}
#         ],
#         temperature = 0,
#         request_timeout=config.REQUEST_TIMEOUT  
#     )
#     quick_link =  completion['choices'][0]['message']['content']
#     return quick_link



# def generate_new_paper(clusters, list_text, config):
#     openai.api_key = config.API_KEY #API key của chatGPT
#     num_token_input = 0
#     text_full = []
#     step = 0
#     for id in tqdm(clusters):
#         if step == 0 and len(list_text[id][1]) > config.MIN_OF_TOKEN:
#             continue
#         step+=1
#         num_token_input +=  len(list_text[id][1])
#         if num_token_input >= config.MIN_OF_TOKEN:
#             break
#         text_full.append(list_text[id][1]+"\n")
#     merge_text = " ".join(text_full)

#     prompt = merge_text+ "/n"+ config.PROMT_GENERATE_PAPER
#     completion = openai.ChatCompletion.create(
#         model = config.OPEN_AI_MODEL_NAME,
#         messages = [
#         {'role': 'user', 'content': prompt}
#         ],
#         temperature = 0,
#         request_timeout=config.REQUEST_TIMEOUT    
#     )
#     paper =  completion['choices'][0]['message']['content']
#     return paper



# def generate_summary_paper(clusters, list_text, config):
#     openai.api_key = config.API_KEY #API key của chatGPT
#     num_token_input = 0
#     text_full = []
#     step = 0
#     for id in tqdm(clusters):
#         if step == 0 and len(list_text[id][1]) > config.MIN_OF_TOKEN:
#             continue
#         step+=1
#         num_token_input +=  len(list_text[id][1])
#         if num_token_input >= config.MIN_OF_TOKEN:
#             break
#         text_full.append(list_text[id][1]+"\n")
#     new_text = " ".join(text_full)


#     prompt = new_text+ "/n"+ config.PROMPT_GENERATE_SUMMARY
#     completion = openai.ChatCompletion.create(
#         model = config.OPEN_AI_MODEL_NAME,
#         messages = [
#         {'role': 'user', 'content': prompt}
#         ],
#         temperature = 0  
#     )
#     title =  completion['choices'][0]['message']['content']
#     return title


# def generate_keyword_of_cluster(text, config):
#     openai.api_key = config.API_KEY #API key của chatGPT
#     prompt = text + "/n"+ config.PROMPT_GENERATE_KEYWORD_CLUSTER
#     completion = openai.ChatCompletion.create(
#         model = config.OPEN_AI_MODEL_NAME,
#         messages = [
#         {'role': 'user', 'content': prompt}
#         ],
#         temperature = 0,
#         request_timeout=config.REQUEST_TIMEOUT    
#     )
#     hashtag =  completion['choices'][0]['message']['content']
#     return hashtag

import py_vncorenlp

# Automatically download VnCoreNLP components from the original repository
# and save them in some local working folder
py_vncorenlp.download_model(save_dir='vncorenlp')

# Load VnCoreNLP from the local working folder that contains both `VnCoreNLP-1.2.jar` and `models` 
model = py_vncorenlp.VnCoreNLP(save_dir='vncorenlp')