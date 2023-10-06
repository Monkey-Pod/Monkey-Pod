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
    print("【ChatGPTからの回答】\n")
    print(f"ChatGPT: {response['choices'][0]['message']['content']}" + "\n\n")

    return response['choices'][0]['message']['content']


def PALM2_to_ChatGPT(question):
    openai.api_key = os.environ['CHATGPT_API']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "このコードに対する説明が正しいか教えてください"},
            {"role": "user", "content": question},
        ]   
    )
    # ChatGPTからの回答を表示
    print("【PALM2の回答をChatGPTがレビューした結果】\n")
    print(f"PALM2 to ChatGPT: {response['choices'][0]['message']['content']}" + "\n\n")
    return response['choices'][0]['message']['content']


def PALM2(question):
    model = CodeChatModel.from_pretrained("codechat-bison@001")
    code_chat = model.start_chat( context="日本語で説明して", max_output_tokens=500, temperature=0.2, )

    response = code_chat.send_message(question)
    
    # PALM2からの回答を表示
    print("【PALM2からの回答】\n")
    print(f"PALM2: {response.text}" + "\n\n") 
    return response.text

def ChatGPT_to_PALM2(question):
    model = CodeChatModel.from_pretrained("codechat-bison@001")
    code_chat = model.start_chat( context="このコードと解説が正しいかどうかを教えてください", max_output_tokens=500, temperature=0.2, )

    response = code_chat.send_message(question)
    # PALM2からの回答を表示
    print("【ChatGPTの回答をPALM2がレビューした結果】\n")
    print(f"ChatGPT to PALM2: {response.text}" + "\n\n")
    return response.text

def GUI(ChatGPT_req, PALM2_req, ChatGPT_to_PALM2_req, PALM2_to_ChatGPT_req):
    # ウィンドウを作成
    output_window = tkinter.Tk()
    output_window.geometry("800x600")  

    # フォントの設定
    font_setting = ("Arial", 12)
    
    # テキストとスクロールバーを配置
    texts = [ChatGPT_req, PALM2_req, ChatGPT_to_PALM2_req, PALM2_to_ChatGPT_req]
    for i, text in enumerate(texts):
        text_widget = tkinter.Text(output_window, wrap='word', font=font_setting, height=10, width=40)
        text_widget.insert(tkinter.END, text)
        text_widget.grid(row=i//2, column=i%2, sticky="nsew", padx=5, pady=5)
        
        # スクロールバーの設定
        scrollbar = tkinter.Scrollbar(output_window, command=text_widget.yview)
        scrollbar.grid(row=i//2, column=i%2+1, sticky="ns")
        text_widget.config(yscrollcommand=scrollbar.set)
        
        # テキストウィジェットを読み取り専用に設定
        text_widget.config(state=tkinter.DISABLED)
        
    # グリッドのスペース調整
    output_window.grid_columnconfigure(0, weight=1)
    output_window.grid_columnconfigure(1, weight=1)
    output_window.grid_rowconfigure(0, weight=1)
    output_window.grid_rowconfigure(1, weight=1)

    # イベントループ
    output_window.mainloop()

# Tkクラス生成
root = tkinter.Tk()

# 画面サイズ
root.geometry('600x400')

# 画面タイトル
root.title('質問')

# ラベル
lbl = tkinter.Label(text='質問', font=("Arial", 14))
lbl.place(x=30, y=70)

# テキストボックス
txt = tkinter.Text(root, width=50, height=10, font=("Arial", 12))
txt.place(x=85, y=70)

# 送信ボタンの処理関数
def btn_click():
    print('ボタンがクリックされました')
    req = str(txt.get("1.0", tkinter.END))
    print(req + "\n")
    ChatGPT_req = ChatGPT(req)
    PALM2_req = PALM2(req)
    ChatGPT_to_PALM2_req = ChatGPT_to_PALM2(req + ChatGPT_req)
    PALM2_to_ChatGPT_req = PALM2_to_ChatGPT(req + PALM2_req)
    GUI("【ChatGPTからの回答】\n" + ChatGPT_req, "【PALM2からの回答】\n" + PALM2_req, "【ChatGPTの回答をPALM2がレビューした結果】\n" + ChatGPT_to_PALM2_req, "【PALM2の回答をChatGPTがレビューした結果】\n" + PALM2_to_ChatGPT_req)
    return 0

# ボタン作成
btn = tkinter.Button(root, text='送信', command=lambda:[btn_click()])
btn.place(x=400, y=270)


# 表示
root.mainloop()