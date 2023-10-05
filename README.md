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
