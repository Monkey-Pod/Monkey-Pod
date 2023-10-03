import os
import vertexai
from vertexai.language_models import TextGenerationModel, CodeChatModel
from dotenv import load_dotenv
import openai
import tkinter

# .envファイルの内容を読み込見込む
load_dotenv()

# ChatGPTに質問し、回答を表示する関数
def ChatGPT(question):
    openai.api_key = os.environ['CHATGPT_API']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "このコードの内容を解析して日本語で説明してください"},
            {"role": "user", "content": question},
        ]   
    )
    # ChatGPTからの回答を表示
    print(f"ChatGPT: {response['choices'][0]['message']['content']}")
    print(response['usage'])

    return response['choices'][0]['message']['content']


def PALM2_to_ChatGPT(question):
    openai.api_key = os.environ['CHATGPT_API']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "このコードと解説が正しいかどうかを教えてください"},
            {"role": "user", "content": question},
        ]   
    )
    # ChatGPTからの回答を表示
    print(f"PALM2 to ChatGPT: {response['choices'][0]['message']['content']}")
    print(response['usage'])

    return response['choices'][0]['message']['content']


def PALM2(question):
    vertexai.init(project="monkey-pod-400110", location="us-central1")
    parameters = {
        "max_output_tokens": 256,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }

    model = CodeChatModel.from_pretrained("codechat-bison@001")
    code_chat = model.start_chat( context="コードの内容を日本語で説明して", max_output_tokens=500, temperature=0.2, )

    response = code_chat.send_message(question)
    
    print(f"PALM2: {response.text}")
    return response.text

def ChatGPT_to_PALM2(question):
    vertexai.init(project="monkey-pod-400110", location="us-central1")
    parameters = {
        "max_output_tokens": 256,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }

    model = CodeChatModel.from_pretrained("codechat-bison@001")
    code_chat = model.start_chat( context="このコードと解説が正しいかどうかを教えてください", max_output_tokens=500, temperature=0.2, )

    response = code_chat.send_message(question)
    
    print(f"ChatGPT to PALM2: {response.text}")
    return response.text

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

# 送信ボタンの処理関数
def btn_click():
    print('ボタンがクリックされました')
    req = str(txt.get())
    print(req)
    ChatGPT_req = ChatGPT(req)
    PALM2_req = PALM2(req)
    # print(ChatGPT_req)
    # print(PALM2_req)
    ChatGPT_to_PALM2_req = ChatGPT_to_PALM2(req + ChatGPT_req)
    PALM2_to_ChatGPT_req = PALM2_to_ChatGPT(req + PALM2_req)
    return 0

# ボタン作成
btn = tkinter.Button(root, text='送信', command=lambda:[btn_click()])
btn.place(x=140, y=170)

# 表示
root.mainloop()
print(question)