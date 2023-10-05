# Monkey-Pod【ChatAIスクリプト】

## 概要
初心者Pentesterは参考になりそうなPOCコードを一読しても理解が難しい場合がある。
その際に、生成AIを活用してPOCコード理解の一助となればと思い作成した。
特に、生成AIとしてChatGPTとPaLM2を利用して複数のAIの意見を参考にできるように作成している。

質問内容はコード内で変更可能だが、デフォルトで以下のような質問を投げかける。
- ChatGTPへ
  - 「このコードの内容を解析して日本語で説明してください」
  - 「このコードと(PaLM2の)解説が正しいかどうかを教えてください」

- PaLM2へ
  - 「このコードの内容を解析して日本語で説明してください」
  - 「このコードと(ChatGPT2の)解説が正しいかどうかを教えてください」

## 想定する利用者
- Red Teamに着任したばかりの方
- 複数の生成AIを活用したい方

## 環境情報
- Python 3.11.2
- Kali Linux 6.1.0

## 事前準備
本アプリではChatGPT APIとPaLM2(Vertex AI) APIを使用します。
そのため、利用にあたって事前にサービスへのユーザ登録やAPIキーの準備が必要となります。

- OpenAIのアカウントの作成とAPIキーを取得
- GCPのサービスアカウントの作成とキー(json形式)の取得と認証

## 環境設定
- ソースコードを取得します
`git clone https://github.com/Monkey-Pod/Monkey-Pod.git`

- PythonのOpenAI Python Libraryをインストールします
`pip install openai`

- ChatGPT API利用のためにAPIキー以下のフォーマットで記載した`.env`ファイルを`ai.py`と同じディレクトリに作成します。
`CHATGPT_API='<API Key>'`

- PaLM2 API利用のための環境変数を設定します
`export GOOGLE_APPLICATION_CREDENTIALS="<認証情報が記載されたjsonファイルのパス>"`


## 実行方法
pythonスクリプトを実行して、GUIへ質問事項(POCコード)を入力する。

1. 実行コマンド
`python3 ai.py`

2. GUI
    1. 質問事項の入力

    2. 回答の表示


## 留意事項
生成AIの回答には限界があり不正確な内容となる場合が知れらています。
あくまで参考情報として活用することを推奨します。

## 参考URL

https://cloud.google.com/sdk/docs/install?hl=ja#linux

https://www.true-fly.com/entry/2022/02/14/080000

