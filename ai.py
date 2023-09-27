# 必要モジュールのインポート
import os
from dotenv import load_dotenv
import openai

# .envファイルの内容を読み込見込む
load_dotenv()

# 生成AIに投げたい質問をユーザに入力させる
question = input('質問を入力してください: ')
print(question)

# ChatGPTに質問
openai.api_key = os.environ['CHATGPT_API']
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "関西弁で面白く簡潔に質問に短く答えてください"},
        #{"role": "user", "content": "APIってなに？"},
        {"role": "user", "content": question},
    ]   
)

# ChatGPTからの回答を表示
print(f"ChatGPT: {response['choices'][0]['message']['content']}")
print(response['usage'])