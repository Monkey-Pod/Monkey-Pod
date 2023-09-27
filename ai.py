# 必要モジュールのインポート
import os
from dotenv import load_dotenv
import openai
import tkinter

# .envファイルの内容を読み込見込む
load_dotenv()

# 生成AIに投げたい質問をユーザに入力させる
# question = input('質問を入力してください: ')
# print(question)


# Tkクラス生成
root = tkinter.Tk()

# 画面サイズ
root.geometry('500x500')

# 画面タイトル
root.title('質問')

# ラベル
lbl = tkinter.Label(text='質問')
lbl.place(x=30, y=70)

# テキストボックス
txt = tkinter.Entry(width=50)
txt.place(x=90, y=70)

# ボタンのクリックイベント
def btn_click():
    print('ボタンがクリックされました')
    question = str(txt.get())
    print(question)

# ボタン作成
btn = tkinter.Button(root, text='送信', command=btn_click)
btn.place(x=140, y=170)

# 表示
root.mainloop()
print(question)

# # ChatGPTに質問
# openai.api_key = os.environ['CHATGPT_API']
# response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "関西弁で面白く簡潔に質問に短く答えてください"},
#         #{"role": "user", "content": "APIってなに？"},
#         {"role": "user", "content": question},
#     ]   
# )
# # ChatGPTからの回答を表示
# print(f"ChatGPT: {response['choices'][0]['message']['content']}")
# print(response['usage'])
