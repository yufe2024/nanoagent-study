import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

response=client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role":"system","content":"请用简短的中文回答"},
        {"role":"user","content":"你好，请用一句话介绍你自己"},
    ],
)

print(response.model_dump_json(indent=2))