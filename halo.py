import torch
import time
import openai
from tqdm import tqdm
from database import Database
from pymongo import MongoClient
import config
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1/',

    # required but ignored
    api_key='ollama',
)

def generate_one_paper(text, config):
    text = "\n".join(text)

    prompt = text + "\n" + config.PROMT_GENERATE_PAPER
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Bạn là một trợ lí Tiếng Việt nhiệt tình và trung thực. Hãy luôn trả lời một cách hữu ích nhất có thể, đồng thời giữ an toàn.\n hãy viết lại bài báo dưới đây một cách chuyên nghiệp, đầy đủ thông tin"
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        temperature=0,
        max_tokens = 2056,
        model='gpt-3.5-turbo:latest',
    )
    keyword = chat_completion.choices[0].message.content
    return keyword

print(generate_one_paper(input(), config))
