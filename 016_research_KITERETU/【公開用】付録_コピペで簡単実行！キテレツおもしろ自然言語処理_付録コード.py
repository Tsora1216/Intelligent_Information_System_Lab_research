# -*- coding: utf-8 -*-
"""【公開用】付録_コピペで簡単実行！キテレツおもしろ自然言語処理_付録コード.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MEwZpnJAhWBrpDtEZpN1AveXaZAWxnu2
"""



"""ここに掲載されているコードは、  
『コピペで簡単実行！キテレツおもしろ自然言語処理～PythonとColaboratoryで身につく基礎の基礎』書籍の付録です。    
本ファイルの公開用URLや、本ファイル内のコードを、みだりに他の人へ共有しないでください。  

本ファイルは、書籍に記載のコードのコピペの手間を省くために作られました。  
本ファイルの公開用URLにアクセスすると、  
お手元のGoogleアカウントに本ファイルのコピーが作成されます。  
（つまり、コレをご覧になっているということは、コピーをご覧になっています）    
そのコピーは、あなただけのファイルとして生成されるため、    
書籍をお買い求め済みの方は、自由に変更したり実行したり保存したりして問題ありません。   

初期状態では、ご参考までに筆者が実行した出力結果を残してあります。  
ご自身で実行する際には、「編集」⇒「出力を全て消去」により、  
出力結果を消去してから実行なさると良いでしょう。  

※注：Googleの公式が作成したファイルではないため、実行時に  
「警告: このノートブックは Google が作成したものではありません。」  
という警告が出ます。  
気になる方は、ご自身の環境に都度コードをコピーして実行しても良いでしょう。


"""



"""■ 青空文庫からのダウンロード＆加工用共通コード"""

# 青空文庫からのダウンロードzip展開＆テキスト抽出

import re
import zipfile
import urllib.request
import os.path,glob
# 青空文庫のURLから小説テキストデータを得る関数
def get_flat_text_from_aozora(zip_url):
  # zipファイル名の取得
  zip_file_name = re.split(r'/', zip_url)[-1]
  print(zip_file_name)
  
  # 既にダウンロード済みか確認後、URLからファイルを取得
  if not os.path.exists(zip_file_name):
    print('Download URL = ',zip_url)
    data = urllib.request.urlopen(zip_url).read()
    with open(zip_file_name, mode="wb") as f:
      f.write(data)
  else:
    print('May be already exists')
  
  # 拡張子を除いた名前で、展開用フォルダを作成
  dir, ext = os.path.splitext(zip_file_name)
  if not os.path.exists(dir):
    os.makedirs(dir)
  
  # zipファイルの中身を全て、展開用フォルダに展開
  unzipped_data = zipfile.ZipFile(zip_file_name, 'r')
  unzipped_data.extractall(dir)
  unzipped_data.close()
  
  # zipファイルの削除
  os.remove(zip_file_name)
  # 注：展開フォルダの削除は入れていない
  
  # テキストファイル(.txt)の抽出
  wild_path = os.path.join(dir,'*.txt')
  # テキストファイルは原則一つ同梱。最初の一つを取得
  txt_file_path = glob.glob(wild_path)[0]

  print(txt_file_path)
  # 青空文庫はshift_jisのためデコードしてutf8にする
  binary_data = open(txt_file_path, 'rb').read()
  main_text = binary_data.decode('shift_jis')

  # 取得したutf8のテキストデータを返す
  return main_text


# 青空文庫のデータを加工して扱いやすくするコード

# 外字データ変換のための準備
# 外字変換のための対応表（jisx0213対応表）のダウンロード
# ※事前にダウンロード済みであれば飛ばしても良い
!wget http://x0213.org/codetable/jisx0213-2004-std.txt

import re

# 外字変換のための対応表（jisx0213対応表）の読み込み
with open('jisx0213-2004-std.txt') as f:
  #ms = (re.match(r'(\d-\w{4})\s+U\+(\w{4})', l) for l in f if l[0] != '#')
  # 追加：jisx0213-2004-std.txtには5桁のUnicodeもあるため対応
  ms = (re.match(r'(\d-\w{4})\s+U\+(\w{4,5})', l) for l in f if l[0] != '#')
  gaiji_table = {m[1]: chr(int(m[2], 16)) for m in ms if m}

# 外字データの置き換えのための関数
def get_gaiji(s):
  # ※［＃「弓＋椁のつくり」、第3水準1-84-22］の形式を変換
  m = re.search(r'第(\d)水準\d-(\d{1,2})-(\d{1,2})', s)
  if m:
    key = f'{m[1]}-{int(m[2])+32:2X}{int(m[3])+32:2X}'
    return gaiji_table.get(key, s)
  # ※［＃「身＋單」、U+8EC3、56-1］の形式を変換
  m = re.search(r'U\+(\w{4})', s)
  if m:
    return chr(int(m[1], 16))
  # ※［＃二の字点、1-2-22］、［＃感嘆符二つ、1-8-75］の形式を変換
  m = re.search(r'.*?(\d)-(\d{1,2})-(\d{1,2})', s)
  if m:
    key = f'{int(m[1])+2}-{int(m[2])+32:2X}{int(m[3])+32:2X}'
    return gaiji_table.get(key, s)
  # 不明な形式の場合、もとの文字列をそのまま返す
  return s

# 青空文庫の外字データ置き換え＆注釈＆ルビ除去などを行う加工関数
def flatten_aozora(text):
  # textの外字データ表記を漢字に置き換える処理
  text = re.sub(r'※［＃.+?］', lambda m: get_gaiji(m[0]), text)
  # 注釈文や、ルビなどの除去
  text = re.split(r'\-{5,}', text)[2]
  text = re.split(r'底本：', text)[0]
  text = re.sub(r'《.+?》', '', text)
  text = re.sub(r'［＃.+?］', '', text)
  text = text.strip()
  return text


# 複数ファイルのダウンロードや加工を一括実行する関数

import time
# ZIP-URLのリストから全てのデータをダウンロード＆加工する関数
def get_all_flat_text_from_zip_list(zip_list):
  all_flat_text = ""
  for zip_url in zip_list: 
    # ダウンロードや解凍の失敗があり得るためTry文を使う
    # 十分なデータ量があるため数件の失敗はスキップで良い
    try:
      # 青空文庫からダウンロードする関数を実行
      aozora_dl_text = get_flat_text_from_aozora(zip_url)
      # 青空文庫のテキストを加工する関数を実行
      flat_text = flatten_aozora(aozora_dl_text) 
      # 結果を追記して改行。
      all_flat_text += flat_text + ("\n")
      print(zip_url+" : 取得＆加工完了")
    except:
      # エラー時の詳細ログが出るおまじない
      import traceback
      traceback.print_exc()
      print(zip_url+" : 取得or解凍エラーのためスキップ")
    
    # 青空文庫サーバに負荷をかけすぎないように１秒まってから次の小説へ
    time.sleep(1)
  
  # 全部がつながった大きなテキストデータを返す
  return all_flat_text

"""■ 走れメロスのデータをダウンロード＆加工"""

# ダウンロードしたいURLを入力する
ZIP_URL = 'https://www.aozora.gr.jp/cards/000035/files/1567_ruby_4948.zip'

# 青空文庫からダウンロードする関数を実行
aozora_dl_text = get_flat_text_from_aozora(ZIP_URL)

# 途中経過を見たい場合以下のコメントを解除
# 冒頭1000文字を出力
# print(aozora_dl_text[0:1000])

# 青空文庫のテキストを加工する関数を実行
flat_text = flatten_aozora(aozora_dl_text)

# 冒頭1000文字を出力
print(flat_text[0:1000])

"""■ 三国志全巻のデータを一気にダウンロード＆加工"""

import time

sangokusi_zip_list = [
"https://www.aozora.gr.jp/cards/001562/files/52410_ruby_51060.zip",
"https://www.aozora.gr.jp/cards/001562/files/52411_ruby_50077.zip",
"https://www.aozora.gr.jp/cards/001562/files/52412_ruby_50316.zip",
"https://www.aozora.gr.jp/cards/001562/files/52413_ruby_50406.zip",
"https://www.aozora.gr.jp/cards/001562/files/52414_ruby_50488.zip",
"https://www.aozora.gr.jp/cards/001562/files/52415_ruby_50559.zip",
"https://www.aozora.gr.jp/cards/001562/files/52416_ruby_50636.zip",
"https://www.aozora.gr.jp/cards/001562/files/52417_ruby_50818.zip",
"https://www.aozora.gr.jp/cards/001562/files/52418_ruby_50895.zip",
"https://www.aozora.gr.jp/cards/001562/files/52419_ruby_51044.zip",
"https://www.aozora.gr.jp/cards/001562/files/52420_ruby_51054.zip",
]

# 三国志の全データを取得する
sangokusi_org_text = get_all_flat_text_from_zip_list(sangokusi_zip_list)

# 冒頭1000文字を出力
print(sangokusi_org_text [0:1000])

"""以下詳細解説のサンプルコード

■ zipファイル名の取得
"""

import re
zip_url = "https://www.aozora.gr.jp/cards/001562/files/52410_ruby_51060.zip"
zip_file_name = re.split(r'/', zip_url)[-1]
print(zip_file_name)

"""■ URLからファイルを取得

"""

import urllib.request
zip_url = "https://www.aozora.gr.jp/cards/001562/files/52410_ruby_51060.zip"
zip_file_name = "52410_ruby_51060.zip"
data = urllib.request.urlopen(zip_url).read()
with open(zip_file_name, mode="wb") as f:
  f.write(data)

"""■ Colaboratory以外の環境でも、ファイルの有無を見るコード"""

import os
import glob
cwd_path = os.getcwd()
print(cwd_path)
cwd_file_dir_list = glob.glob(cwd_path + os.sep + "*")
print(cwd_file_dir_list)

"""■ 拡張子を除いた名前で、展開用フォルダを作成"""

import os.path
zip_file_name = "52410_ruby_51060.zip"
dir, ext = os.path.splitext(zip_file_name)
print(dir)
print(ext)

if not os.path.exists(dir):
  os.makedirs(dir)

"""■ zipファイルの中身を全て、展開用フォルダに展開"""

import zipfile
zip_file_name = "52410_ruby_51060.zip"
dir = "52410_ruby_51060"
# zipファイルの中身を全て、展開用フォルダに展開
unzipped_data = zipfile.ZipFile(zip_file_name, 'r')
unzipped_data.extractall(dir)
unzipped_data.close()

"""■ テキストファイル(.txt)の抽出"""

import os.path,glob
dir = "52410_ruby_51060"
# テキストファイル(.txt)の抽出
wild_path = os.path.join(dir,'*.txt')
print(wild_path)
 # テキストファイルは原則一つ同梱。最初の一つを取得
txt_file_path = glob.glob(wild_path)[0]
print(txt_file_path)

"""■ デコードしてutf8にしたテキストを取得"""

txt_file_path = "52410_ruby_51060/02toenno_maki.txt"
# 青空文庫はshift_jisのためデコードしてutf8にする
binary_data = open(txt_file_path, 'rb').read()
main_text = binary_data.decode('shift_jis')
print(main_text[0:270])

"""■ 正規表現によるタグ削除の例"""

import re
text = "すべての人類《くりーちゃー》を破壊《はかい》する。［＃５字下げ］それらは再生《さいせい》できない。"
text = re.sub(r'《.+?》', '', text)
text = re.sub(r'［＃.+?］', '', text)
print(text)

"""■ 「D.外字」の変換方法 / ひらがなをカタカナに直す関数"""

import re

# ひらがなをカタカナに直す関数
def hira_to_kata(input_str):
  return "".join([chr(ord(ch) + 96) if ("ぁ" <= ch <= "ん") else ch for ch in input_str])

text = "すべての人類《くりーちゃー》を破壊《はかい》する。それらは再生《さいせい》できない。"
text = re.sub(r'《.+?》', lambda m: hira_to_kata(m[0]), text)
print(text)

"""■ 外字変換のための対応表（jisx0213対応表）のダウンロード"""

!wget http://x0213.org/codetable/jisx0213-2004-std.txt

