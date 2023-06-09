# -*- coding: utf-8 -*-
"""【公開用】07章_コピペで簡単実行！キテレツおもしろ自然言語処理_付録コード.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aLve4kLym5dxJ25R2verjp7fE2bJ48W2
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



"""■ Janomeのインストール："""

!pip install janome

"""■ 三国志の文章から名詞と動詞と形容詞を抽出：

"""

# Janomeのロード
from janome.tokenizer import Tokenizer

# Tokenizerインスタンスの生成 
tokenizer = Tokenizer()

# 名詞、動詞原形、形容詞を配列で抽出する関数
def extract_words(text):
  tokens = tokenizer.tokenize(text)
  return [token.base_form for token in tokens 
          if token.part_of_speech.split(',')[0] in['名詞', '動詞', '形容詞']]

# 例文で結果を確かめてみる
sampletext = u"劉備と関羽と張飛の三人は桃園で義兄弟の契りを結んだ"
print(extract_words(sampletext))

"""■  GoogleDriveのマウントコマンド："""

from google.colab import drive
drive.mount('/content/drive')

"""■ 武将名簿のダウンロード："""

# KITERETU フォルダをマウントしたGoogleDriveフォルダ(MyDrive)内に作成する
!mkdir -p /content/drive/MyDrive/KITERETU

# 武将名簿ファイルのダウンロード：
!curl -o /content/drive/MyDrive/KITERETU/sangokusi_jinbutu_list.csv https://storage.googleapis.com/nlp_youwht/san/sangokusi_jinbutu_list.csv

# 名簿の冒頭部分を眺めてみる
!head "/content/drive/MyDrive/KITERETU/sangokusi_jinbutu_list.csv"

""" 武将名簿をユーザ辞書に変換して保存："""

#人物の名前が列挙してあるテキストをリスト形式で読み込む
import codecs
def getKeyWordList(input_file_path):
  input_file = codecs.open(input_file_path, 'r', 'utf-8')
  # ファイルの読み込み。各行ごとが格納されたリストになる
  line_list = input_file.readlines()
  # 改行コードを消去するstrip()をそれぞれにほどこす
  return [line.strip() for line in line_list]

keyword_list = getKeyWordList('/content/drive/MyDrive/KITERETU/sangokusi_jinbutu_list.csv')

userdict_str = ""
# コストや品詞の設定などを行い、ユーザ辞書形式にする
for keyword in keyword_list:
  userdict_one_str = keyword + ",-1,-1,-5000,名詞,一般,*,*,*,*," + keyword + ",*,*"
  userdict_str += userdict_one_str+"\n"

#作成したユーザ辞書形式をcsvで保存しておく
with open("/content/drive/MyDrive/KITERETU/sangokusi_userdic.csv", "w", encoding="utf8") as f:
  f.write(userdict_str)

"""■ 用意したユーザ辞書を使って形態素解析：

"""

# Janomeのロード
from janome.tokenizer import Tokenizer

# Tokenizerインスタンスの生成 
tokenizer = Tokenizer("/content/drive/MyDrive/KITERETU/sangokusi_userdic.csv", udic_enc='utf8')
# 変更前は以下であった。
# tokenizer = Tokenizer()

# 名詞・動詞原形のみを配列で抽出する関数
def extract_words(text):
  tokens = tokenizer.tokenize(text)
  return [token.base_form for token in tokens 
          if token.part_of_speech.split(',')[0] in['名詞', '動詞', '形容詞']]

# 例文で結果を確かめてみる
sampletext = u"劉備と関羽と張飛の三人は桃園で義兄弟の契りを結んだ"
print(extract_words(sampletext))

"""■ 反董卓連合軍でも試してみる：

"""

sampletext = u"第一鎮として後将軍南陽の太守袁術、字は公路を筆頭に、\
第二鎮、冀州の刺史韓馥、第三鎮、予州の刺史孔伷、\
第四鎮、兗州の刺史劉岱、第五鎮、河内郡の太守王匡、\
第六鎮、陳留の太守張邈、第七鎮、東郡の太守喬瑁"
print(extract_words(sampletext))

"""■ 字リストのダウンロード："""

# 字リストのダウンロード
!curl -o /content/drive/MyDrive/KITERETU/sangokusi_azana_list.csv https://storage.googleapis.com/nlp_youwht/san/sangokusi_azana_list.csv

# 冒頭部の内容確認
!head "/content/drive/MyDrive/KITERETU/sangokusi_azana_list.csv"

"""■ 字（あざな）の名寄せ用変換データ作成："""

import csv
# 字（あざな）の一覧ファイルを読み込む
csv_file = open("/content/drive/MyDrive/KITERETU/sangokusi_azana_list.csv", "r", encoding="utf8")
# CSVファイルをリスト形式で読み出す
csv_reader = csv.reader(csv_file, delimiter=",")
AZANA_LIST = [ e for e in csv_reader ]
csv_file.close()

# 字(あざな)と本名を入れると、３パターンの呼び⽅＆本名の組を作成する関数
def make_yobikata_list(azana, name):
  result_list = []
  
  # ①["関羽雲長","関羽"] や、["諸葛亮孔明","諸葛亮"]の形を作る
  result_list.append([name + azana, name])
  
  # ②["関雲長","関羽"] や、["諸葛孔明","諸葛亮"]の形を作る
  result_list.append([name[:-1] + azana, name])
  
  # ③["雲長","関羽"] や、["孔明","諸葛亮"]の形を作る
  result_list.append([azana, name])
  
  # なお、最後の字のみの変換は、①の実行後に行うので③は最後に追加した
  return result_list

# 全武将の呼び方＋本名の組み合わせを作成する
ALL_YOBIKATA_LIST = []
for azana_name in AZANA_LIST:
  # １武将ずつ、３パターンの呼び方＆本名の組を作成し追加していく
  ALL_YOBIKATA_LIST += make_yobikata_list(azana_name[0], azana_name[1])

# 結果は２重リスト（リストのリスト）であり、最初の９個の結果を見る
print(ALL_YOBIKATA_LIST[0:9])

"""■ 字（あざな）変換用関数の作成と実行："""

def azana_henkan(input_text):
  result_text = input_text
  # ループで、全部の変換パターンの置換処理を行う
  for yobikata_name in ALL_YOBIKATA_LIST:
    # yobikata_name もリストであり、[0]に呼び方、[1]に本名が入っている
    result_text = result_text.replace(yobikata_name[0], yobikata_name[1])
  return result_text

sampletext = u"趙子龍は、白馬を飛ばして、馬上から一気に彼を槍で突き殺した。"
print(azana_henkan(sampletext))
sampletext = u"子龍は、なおも進んで敵の文醜、顔良の二軍へぶつかって行った。"
print(azana_henkan(sampletext))
sampletext = u"趙雲子龍も、やがては、戦いつかれ、玄徳も進退きわまって、すでに自刃を覚悟した時だった。"
print(azana_henkan(sampletext))

"""【※ ここで付録を参照し、記載のコードを実行してください。】  
の、付録のコード  
■ 青空文庫からのダウンロード＆加工用共通コード：  

"""

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
  # テキストファイルは原則1つ同梱。最初の1つを取得
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
# ※事前にダウンロード済みであれば飛ばしてもよい
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
  # 不明な形式の場合、元の文字列をそのまま返す
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
    # 十分なデータ量があるため数件の失敗はスキップでよい
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
    
    # 青空文庫サーバに負荷をかけすぎないように１秒待ってから次の小説へ
    time.sleep(1)
  
  # 全部がつながった大きなテキストデータを返す
  return all_flat_text

"""■ URLを指定してダウンロード＆加工を実行："""

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
# 得た結果をファイルに書き込む
with open('/content/drive/MyDrive/KITERETU/sangokusi_org_text.txt', 'w') as f:
  print(sangokusi_org_text, file=f)
  print("★三国志ALLファイル出力完了")

"""■ 字（あざな）の変換を実施："""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# import codecs
# # 取得してあった原文を開く
# with codecs.open("/content/drive/MyDrive/KITERETU/sangokusi_org_text.txt", 'r', encoding='utf-8') as f:
#   org_text = f.read()
# 
# # 全テキストに字変換処理をほどこして新しいファイルに書き込む
# with open("/content/drive/MyDrive/KITERETU/sangokusi_henkango_text.txt", "w", encoding="utf8") as f:
#   f.write(azana_henkan(org_text))
#

"""■ 全文に対してキーワードの抽出、リスト化："""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# # Janomeのロード
# from janome.tokenizer import Tokenizer
# 
# # Tokenizerインスタンスの生成 
# #tokenizer = Tokenizer()
# tokenizer = Tokenizer("/content/drive/MyDrive/KITERETU/sangokusi_userdic.csv", udic_enc='utf8')
# 
# # テキストを引数として、形態素解析の結果、名詞・動詞原形のみを配列で抽出する関数
# def extract_words(text):
#   tokens = tokenizer.tokenize(text)
#   #どの品詞を採用するかも重要な調整要素
#   return [token.base_form for token in tokens 
#           if token.part_of_speech.split(',')[0] in['名詞', '動詞', '形容詞']]
# 
# import codecs
# # ['趙雲', '白馬', '飛ばす', '馬上', '彼', '槍', '突き', '殺す'] 
# # このようなリストのリスト（二次元リスト）を作る関数
# # Word2Vecでは、分かち書きされた１文ずつのリストを引数として使うため
# def textfile2wordlist(input_file_path):
#   input_file  = codecs.open(input_file_path, 'r', 'utf-8')
#   # ファイルの読み込み。各行ごとが格納されたリストになる
#   line_list = input_file.readlines()
#   result_word_list_list = []
#   for line in line_list:
#     # 1行ずつ、形態素解析した結果をリストに変換
#     tmp_word_list = extract_words(line)
#     result_word_list_list.append(tmp_word_list)
#   return result_word_list_list
# 
# # 実行
# sangokusi_wordlist = textfile2wordlist('/content/drive/MyDrive/KITERETU/sangokusi_henkango_text.txt')
# 
# # 作成したワードリストは、pickleを使って、GoogleDriveに保存しておく
# import pickle
# with open('/content/drive/MyDrive/KITERETU/sangokusi_wordlist.pickle', 'wb') as f:
#   pickle.dump(sangokusi_wordlist, f)
#

"""■ 作成したキーワードリストの内容確認：

"""

# なお、保存したpickleファイルは、以下のようにすれば復元出来る
with open('/content/drive/MyDrive/KITERETU/sangokusi_wordlist.pickle', 'rb') as f:
  sangokusi_wordlist = pickle.load(f)

# 結果の確認用①行数の表示
print(len(sangokusi_wordlist))

# ２重のリストをフラット（１重）にする関数
# ネストしたリスト内包表記を用いている。コピペでよく、理解する必要はない。
def flatten(nested_list):
  return [e for inner_list in nested_list for e in inner_list]

# 結果の確認用②キーワード数の表示
print(len(flatten(sangokusi_wordlist)))

# 結果の確認用③最初の５０個の内容確認
print(sangokusi_wordlist[0:50])

"""■ キーワードリストから、機械学習を行いモデルを作る：

"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# import logging
# from gensim.models import word2vec
# import pickle
# 
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# 
# #ワードリストをpickleから復元
# with open('/content/drive/MyDrive/KITERETU/sangokusi_wordlist.pickle', 'rb') as f:
#   word_list = pickle.load(f)
# 
# # Word2Vecの学習実施
# model = word2vec.Word2Vec(word_list, 
#                           size = 50,
#                           min_count = 5,
#                           window = 6,
#                           iter = 100)
# 
# model.save("/content/drive/MyDrive/KITERETU/w2v_sangokusi.model")
#

"""■ ベクトルにされた魏延を見る："""

from gensim.models import word2vec

# 保存したモデルファイルの読み込み
model = word2vec.Word2Vec.load("/content/drive/MyDrive/KITERETU/w2v_sangokusi.model")

print(model.__dict__['wv']['魏延'])

"""■ 「関羽」に近いTop7の表示：

"""

out = model.wv.most_similar(positive=[u'関羽'], topn=7)
print(out)

"""■ 「諸葛亮」に近いTop7の表示：

"""

out = model.wv.most_similar(positive=[u'諸葛亮'], topn=7)
print(out)

"""■ 「甘寧」＋「曹操」－「孫権」："""

# 「甘寧」＋「曹操」－「孫権」（孫権にとっての甘寧は、曹操にとって誰？）
print(model.wv.most_similar(positive=['甘寧','曹操'], negative=['孫権'],topn=5))
# 「甘寧」＋「劉備」－「孫権」（孫権にとっての甘寧は、劉備にとって誰？）
print(model.wv.most_similar(positive=['甘寧','劉備'], negative=['孫権'],topn=5))

"""■ 曹操にとっての張遼は誰か？：

"""

# 「張遼」＋「孫権」－「曹操」（曹操にとっての張遼は、孫権にとって誰？）
print(model.wv.most_similar(positive=['張遼','孫権'], negative=['曹操'],topn=5))
# 「張遼」＋「劉備」－「曹操」（曹操にとっての張遼は、劉備にとって誰？）
print(model.wv.most_similar(positive=['張遼','劉備'], negative=['曹操'],topn=5))

"""■ 劉備にとっての諸葛亮は誰か？："""

print(model.wv.most_similar(positive=['諸葛亮','曹操'], negative=['劉備'],topn=5))
print(model.wv.most_similar(positive=['諸葛亮','孫権'], negative=['劉備'],topn=5))

"""■ キーワードリストから「劉備」と「曹操」の数を数える："""

import pickle
with open('/content/drive/MyDrive/KITERETU/sangokusi_wordlist.pickle', 'rb') as f:
  sangokusi_wordlist = pickle.load(f)

# ２重のリストをフラット（１重）にする関数
def flatten(nested_list):
  return [e for inner_list in nested_list for e in inner_list]

flat_wordlist = flatten(sangokusi_wordlist)

print("劉備の登場回数：", flat_wordlist.count('劉備'))
print("曹操の登場回数：", flat_wordlist.count('曹操'))

