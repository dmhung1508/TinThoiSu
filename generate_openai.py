import torch
import time
import openai,re
from tqdm import tqdm
from database import Database
from pymongo import MongoClient
import config
from openai import OpenAI
from langdetect import detect
import markdown
import requests
import json,os
import csv
from rerank import reranker, analyze_component_similarity, analyze_all_components
def get_name(link):
    a = requests.get("https://api.tinthoisu.vn/articles/detail?link="+link)
    return a.json()['data']['item']['sourceName']
def remove_number_prefix(text):
    # Sử dụng regex để tìm và xóa các số thứ tự từ 1 đến 10 ở đầu chuỗi
    result = re.sub(r'^(1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21)\.\s*', '', text)
    return result
def extract_first_item_or_text(text):
    # Tách các dòng
    lines = text.strip().split('\n')
    # Nếu có nhiều dòng
    if len(lines) > 1:
        # Duyệt qua từng dòng để tìm dòng đầu tiên có số thứ tự
        for line in lines:
            line = line.strip()
            if line.startswith(('1.', '2.', '3.', '4.', '5.')):
                # Lấy nội dung sau số thứ tự
                content = line.split('. ', 1)[1]
                # Xóa ký tự nháy ở đầu và ở cuối nếu có
                if content.startswith('"') and content.endswith('"'):
                    content = content[1:-1]
                return content
    # Nếu chỉ có một dòng
    else:
        text = text.strip()
        # Xóa ký tự nháy ở đầu và ở cuối nếu có
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        return text




client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),


    api_key = os.getenv("OPENAI_API_KEY")
)

def generate_keyword(text, config):
    text = "\n".join(text)
    #print(text)
    prompt = text + "\n" + config.PROMPT_GENERATE_KEYWORD
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": config.PROMPT_GENERATE_KEYWORD
            },
            {
                'role': 'user',
                'content': text
            }
        ],
        temperature=0,
        max_tokens = 256,
        
        #request_timeout=config.REQUEST_TIMEOUT,
        model='gpt-4o-mini',
    )
    keyword = chat_completion.choices[0].message.content
    return keyword
def generate_keyword_ver2(text, config):
    key = []
    for t in text:

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    'role': 'system',
                    'content': "Hãy tóm tắt tiêu đề trên chỉ còn 6 từ, không dài dòng lan man, giữ được đúng ý của nó. Giúp người đọc có thể hiểu luôn được tiêu đề đó,Chỉ trả lời bằng tiếng Việt Nam, ngôn ngữ Việt Nam"
                },
                {
                    'role': 'user',
                    'content': 'Cháy nhà trọ ở Hà Nội, nhiều người thương vong',
                },
                {
                    'role': 'assistant',
                    'content': "Cháy nhà trọ Hà Nội"
                },
                {
                    'role': 'user',
                    'content': "Quan chức cấp cao của Nga bị bắt trong cuộc đàn áp tham nhũng",
                },
                {
                    'role': 'assistant',
                    'content': "Quan chức Nga tham nhũng"
                },
                {
                    'role': 'user',
                    'content': "28 Người Bị Chấn Thương Não, Cột Sống Sau Sự Cố Của Singapore Airlines",
                },
                {
                    'role': 'assistant',
                    'content': "28 chấn thương Singapore Airlines",
                },
                {
                    'role': 'user',
                    'content': "Ngôi sao Ngoại Hạng Anh đối mặt án phạt cấm thi đấu 10 năm vì dàn xếp tỷ số",
                },
                {
                    'role': 'assistant',
                    'content': "Ngôi sao Anh bị cấm",
                },
                {
                    'role': 'user',
                    'content': t
                }
            ],
            temperature=0,
            max_tokens = 60,
            
            #request_timeout=config.REQUEST_TIMEOUT,
            model='gpt-4o-mini',
        )
        paper =  chat_completion.choices[0].message.content
        #print(paper)
        key.append(paper)
    #key = "; ".join(key)
    return key

def generate_title_paper(clusters, list_text, config):
    num_token_input = 0
    text_full = []
    step = 0
    for idx in tqdm(clusters):
        if step == 0 and len(list_text[idx][2]) > config.MIN_OF_TOKEN:
            continue
        step += 1
        num_token_input += len(list_text[idx][2])
        if num_token_input >= config.MIN_OF_TOKEN:
            break
        text_full.append(list_text[idx][2] + "\n")
    
    merge_text = " ".join(text_full)
    if merge_text.strip() == "":
        print("Rỗng")
        merge_text = " ".join(list_text[idx][1:])
        merge_text_words = merge_text.split()
        if len(merge_text_words) > 1024:
            merge_text = " ".join(merge_text_words[:1024])
    #print(merge_text)
    
    prompt = merge_text + "\n" + config.PROMPT_GENERATE_TITLE
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": config.PROMPT_GENERATE_TITLE
            },
            {
                'role': 'user',
                'content': merge_text
            }
        ],
        temperature=0,
        max_tokens=200,
        model='gpt-4o-mini',
    )
    
    quick_link = chat_completion.choices[0].message.content
    first_item = extract_first_item_or_text(quick_link)
    return first_item

def generate_6W2H(prompt):
  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {
        "role": "system",
        "content": [
          {
            "type": "text",
            "text": config.PROMPT_6W2H
          }
        ]
      },
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt
          }
        ]
      }
    ],
    temperature=0,
    max_tokens=2048,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    response_format={
      "type": "json_object"
    }
  )
  #print(response.choices[0].message.content)
  return json.loads(response.choices[0].message.content)

def generate_6w2h_cluster(clusters, list_text, config):
    text_full = []
    step = 0
    for idx in tqdm(clusters):
        text_full.append(list_text[idx][1] + "\n")
    for i in range(len(text_full)):
        text_full[i] = "Nguồn " + str(i) + ": " + text_full[i]
    text_full = "\n".join(text_full)
    patterns = [
        r"Nguồn (\d+): \s*(.*?)\s*Source_name : \s*(.*?)\s*Link : \s*(https://[^\s]+)",
        r"Nguồn (\d+): \s*(.*?)\s*Source_name : \s*(.*?)\s*Youtube : \s*(https://[^\s]+)",
        r"Nguồn (\d+): \s*(.*?)\s*Source_name : \s*(.*?)\s*Facebook : \s*(https://[^\s]+)"
    ]
    seen_sources = set()
    seen_links = set()
    source_text_list = []
    # Extracted data and check for duplicates
    for pattern in patterns:
        matches = re.findall(pattern, text_full)
        for match in matches:
            source_number, text, source_name, link = match
            text = text.replace("_", " ")
            # Check if the source name or link is a duplicate
            if source_name in seen_sources:
                
                print(f"Duplicate source name found: {source_name}")
            elif link in seen_links:
                print(f"Duplicate link found: {link}")
            else:
                # Add to seen sets
                seen_sources.add(source_name)
                seen_links.add(link)
                source_text = ""
                source_text += f"Source {source_number}:\n"
                source_text += f"Text: {text}\n"
                source_text += f"Source Name: {source_name}\n"
                source_text += f"Link: {link}"
                source_text_list.append(source_text)
    six_w2h_list = [generate_6W2H(article) for article in source_text_list]
    results_json = analyze_all_components(six_w2h_list, seen_links)
    return json.loads(results_json)



def generate_new_paper_comment(clusters, list_text, config):
    num_token_input = 0
    text_full = []
    step = 0
    url_web = []
    for id in tqdm(clusters):

        step+=1
        num_token_input +=  len(list_text[id][1])
        # if num_token_input >= config.MIN_OF_TOKEN:
        #     break
        text_full.append(list_text[id][1]+"\n")
        if len(text_full) > 10:
            break
    for i in range(len(text_full)):
        text_full[i] = "Nguồn " + str(i) + ": " + text_full[i]
    text_full = "\n".join(text_full)
    patterns = [
        r"Nguồn (\d+): \s*(.*?)\s*Source_name : \s*(.*?)\s*Link : \s*(https://[^\s]+)",
        r"Nguồn (\d+): \s*(.*?)\s*Source_name : \s*(.*?)\s*Youtube : \s*(https://[^\s]+)",
        r"Nguồn (\d+): \s*(.*?)\s*Source_name : \s*(.*?)\s*Facebook : \s*(https://[^\s]+)"
    ]


    # To track duplicates
    seen_sources = set()
    seen_links = set()
    source_text = ""
    #print("text_full: ", text_full)
    dem = 0
    # Extracted data and check for duplicates
    for pattern in patterns:
        matches = re.findall(pattern, text_full)
        for match in matches:
            source_number, text, source_name, link = match
            
            # Check if the source name or link is a duplicate
            if source_name in seen_sources:
                print(f"Duplicate source name found: {source_name}")
            elif link in seen_links:
                print(f"Duplicate link found: {link}")
            else:
                # Add to seen sets
                seen_sources.add(source_name)
                seen_links.add(link)
                source_text += f"Source {source_number}:\n"
                source_text += f"Text: {text}\n"
                source_text += f"Source Name: {source_name}\n"
                source_text += f"Link: {link}\n\n"
                source_text += "\n\n"
                dem = dem + 1
        if dem >= 4:
            break

    #print(merge_text)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": config.PROMT_GENERATE_PAPER_COMMENT
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": source_text,
                }
            ]
            }
            
        ],
        temperature=0,
        max_tokens=6417,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "json_object"
        }
        )
    # chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": config.PROMT_GENERATE_PAPER_COMMENT
    #         },
    #         {
    #             'role': 'user',
    #             'content': merge_text
    #         }
    #     ],
    #     temperature=0.2,
    #     max_tokens=7410,
    #     top_p=1,
    #     frequency_penalty=0,
    #     presence_penalty=0,
    #     response_format={
    #         "type": "json_object"
    #     }
    #     #request_timeout=config.REQUEST_TIMEOUT,
    #     model='gpt-4o-mini',
    # )
    paper =  response.choices[0].message.content
    return json.loads(paper)
    datajs = json.loads(paper)
    for source in datajs['sources']:
        source['source_name'] = get_name(source['link'])
    return str(datajs)
    #html = markdown.markdown(paper)
    # num_words = len(paper.split())
    # i = 0
    # while num_words < 50 or num_words > 1200:
    #     chat_completion = client.chat.completions.create(
    #         messages=[
    #             {
    #                 "role": "system",
    #                 "content": config.PROMT_GENERATE_PAPER
    #             },
    #             {
    #                 'role': 'user',
    #                 'content': merge_text
    #             }
    #         ],
    #         temperature=0.4,
    #         max_tokens = 4096,
            
    #         #request_timeout=config.REQUEST_TIMEOUT,
    #         model='gpt-4o-mini',
    #     )
    #     paper =  chat_completion.choices[0].message.content
    #     num_words = len(paper.split())
    #     i = i+1
    #     if i == 10:
    #         break
    return paper
def generate_new_paper(clusters, list_text, config):
    num_token_input = 0
    text_full = []
    step = 0
    for id in tqdm(clusters):
        if step == 0 and len(list_text[id][1]) > config.MIN_OF_TOKEN:
            continue
        step+=1
        num_token_input +=  len(list_text[id][1])
        if num_token_input >= config.MIN_OF_TOKEN:
            break
        text_full.append(list_text[id][1]+"\n")
    merge_text = " ".join(text_full)

    prompt = merge_text+ "/n"+ config.PROMT_GENERATE_PAPER
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": config.PROMT_GENERATE_PAPER
            },
            {
                'role': 'user',
                'content': merge_text
            }
        ],
        temperature=0,
        max_tokens = 4096,
        
        #request_timeout=config.REQUEST_TIMEOUT,
        model='gpt-4o-mini',
    )
    paper =  chat_completion.choices[0].message.content
    html = markdown.markdown(paper)
    # num_words = len(paper.split())
    # i = 0
    # while num_words < 50 or num_words > 1200:
    #     chat_completion = client.chat.completions.create(
    #         messages=[
    #             {
    #                 "role": "system",
    #                 "content": config.PROMT_GENERATE_PAPER
    #             },
    #             {
    #                 'role': 'user',
    #                 'content': merge_text
    #             }
    #         ],
    #         temperature=0.4,
    #         max_tokens = 4096,
            
    #         #request_timeout=config.REQUEST_TIMEOUT,
    #         model='gpt-4o-mini',
    #     )
    #     paper =  chat_completion.choices[0].message.content
    #     num_words = len(paper.split())
    #     i = i+1
    #     if i == 10:
    #         break
    return html

def generate_one_paper(text, config):
    num_token_input +=  len(text)
    
    text_full = []
    if num_token_input >= config.MIN_OF_TOKEN:
        return False
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": config.PROMT_GENERATE_PAPER
            },
            {
                'role': 'user',
                'content': text
            }
        ],
        temperature=0,
        max_tokens = 2048,
        
        #request_timeout=config.REQUEST_TIMEOUT,
        model='gpt-4o-mini',
    )
    paper =  chat_completion.choices[0].message.content
    return paper

def generate_summary_paper(clusters, list_text, config):
    num_token_input = 0
    text_full = []
    step = 0
    for id in tqdm(clusters):
        # if step == 0 and len(list_text[id][1]) > config.MIN_OF_TOKEN:
        #     continue
        # step+=1
        num_token_input +=  len(list_text[id][1])
        # if num_token_input >= 4000:
        #     break
        text_full.append(list_text[id][1]+"\n")
        if len(text_full) > 4:
            break
    new_text = " ".join(text_full)
    # print("text summary: ", new_text)

    prompt = new_text+ "/n"+ config.PROMPT_GENERATE_SUMMARY
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": config.PROMPT_GENERATE_SUMMARY
            },
            {
                'role': 'user',
                'content': new_text
            }
        ],
        temperature=0.2,
        max_tokens = 2056,
        
        #request_timeout=config.REQUEST_TIMEOUT,
        model='gpt-4o-mini',
    )
    title =  chat_completion.choices[0].message.content
    
    return title


def generate_keyword_of_cluster(text, config):
    print("clusster: ", text)
    prompt = text + "/n"+ config.PROMPT_GENERATE_KEYWORD_CLUSTER
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": config.PROMPT_GENERATE_KEYWORD_CLUSTER
            },
            {
                'role': 'user',
                'content': text
            }
        ],
        temperature=0,
        max_tokens = 256,
        
        #request_timeout=config.REQUEST_TIMEOUT,
        model='gpt-4o-mini',
    )
    hashtag =  chat_completion.choices[0].message.content
    first_item = extract_first_item_or_text(hashtag)
    return first_item
