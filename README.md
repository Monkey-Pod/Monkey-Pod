# Monkey-Pod【Pentest-Tool】
## 概要
ペネトレーションテストの支援ツール。<br>
対象サーバに対し、nmapをかけた後に起動しているサービスに応じて自動的に必要な探索を行い情報をまとめることができる。<br>
脆弱な点が見つかれば、CVE番号からgithubで検索を行いヒットすればそのURLを出力する。<br>
その後のexploitコードを用いたテストにスムーズに移行ができ有用である。

## 想定する利用者
・Red Teamに着任したばかりの方<br>
・ペネトレーションテストの大枠を理解したい方

## 環境情報
Python 3.11.2<br>
Kali linux
## 環境設定
### dirsearchのインストール
```
$ cd ~
$ git clone https://github.com/maurosoria/dirsearch.git
$ cd dirsearch
$ pip3 install -r requirements.txt
$ python3 dirsearch.py -h

$ echo "#dirsearch" >> ~/.zshrc
$ echo "export PATH=$PATH:/home/kali/dirsearch" >> ~/.zshrc
$ tail  ~/.zshrc
$ source ~/.zshrc
```
### nucleiのインストール
``` $ sudo apt install nuclei ```

## 実行方法
``` $ python pentest.py <target-IP> ```

## 実行結果
### 一部抜粋① 実行後すぐにNmapコマンドで探索を行う
![image](https://github.com/Monkey-Pod/Monkey-Pod/assets/146339446/ad03da37-645b-4f55-9b39-8c55c1e278f4)
### 一部抜粋② SMBサーバへの探索例
![image](https://github.com/Monkey-Pod/Monkey-Pod/assets/146339446/935cd297-d7a5-4811-b377-d808e52b483d)
### 一部抜粋③ telnet,sshサーバへの探索例
![image](https://github.com/Monkey-Pod/Monkey-Pod/assets/146339446/a9727abf-a3e6-4dde-aa3a-37df4cb47dee)
### 一部抜粋④ httpサーバへの探索例
![image](https://github.com/Monkey-Pod/Monkey-Pod/assets/146339446/af81f49e-7040-49b8-8dbe-094c4372a394)
### 一部抜粋⑤ PoCが見つかった脆弱性についてGithubのURLを返している
![image](https://github.com/Monkey-Pod/Monkey-Pod/assets/146339446/bad32656-3b6a-4f51-9992-258f1d854d83)





