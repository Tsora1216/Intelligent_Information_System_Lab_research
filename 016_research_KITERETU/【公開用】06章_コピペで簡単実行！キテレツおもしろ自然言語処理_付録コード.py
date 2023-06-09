# -*- coding: utf-8 -*-
"""【公開用】06章_コピペで簡単実行！キテレツおもしろ自然言語処理_付録コード.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vW8fQbzX2hf1HCdPiV3dqzu10mY6OEsJ
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



"""■  GoogleDriveのマウントコマンド：

"""

from google.colab import drive
drive.mount('/content/drive')

"""■ 100MBの単純テキストデータのダウンロード："""

# ダウンロード用のフォルダを作成
!mkdir -p /content/drive/MyDrive/KITERETU
# 100MBの単純テキストデータのダウンロード
!curl -o /content/drive/MyDrive/KITERETU/text8ja42.txt https://storage.googleapis.com/nlp_youwht/text8/text8ja42.txt

# ランダムに生成しているため、何パターンか準備してあります。
# データを変更して試したい方は以下をご使用ください。
# !curl -o /content/drive/MyDrive/KITERETU/text8ja75.txt https://storage.googleapis.com/nlp_youwht/text8/text8ja75.txt
# !curl -o /content/drive/MyDrive/KITERETU/text8ja97.txt https://storage.googleapis.com/nlp_youwht/text8/text8ja97.txt

"""■ 冒頭部分を読んでみる："""

# -c バイト数（表示するバイト数を指定します。）
!head -c 80 "/content/drive/MyDrive/KITERETU/text8ja42.txt"

"""■ 全ての文字の間に半角スペースを入れる加工処理："""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# import codecs
# input_file_path = "/content/drive/MyDrive/KITERETU/text8ja42.txt"
# output_file_path = "/content/drive/MyDrive/KITERETU/tmp_1kugiri.txt"
# 
# with codecs.open(input_file_path,"r", "utf-8") as f:
#   for line in f.readlines():
#     # 文字列を、１文字ごとのリストに変える（半角スペースは除く）
#     chars = [c for c in line if c != u' ']
#     with codecs.open(output_file_path,"a", "utf-8") as new_f:
#       # リストの文字を半角スペースで繋げた文字列にする
#       new_f.write(u' '.join(chars))
# 
#

"""■ 作成したデータの冒頭部分を読んでみる："""

!head -c 80  "/content/drive/MyDrive/KITERETU/tmp_1kugiri.txt"

"""■ Char2Vecモデルの作成：

※2023年1月にColaboratoryのバージョンアップ/仕様変更が入り、  
　ログが出なくなり、また実行時間が、20分程度⇒70分程度、に   
　増える傾向にあるようです。   
　（使える実行環境はGoogleCloudの混雑状況次第ですので、状況により異なるようです）    
　Colaboratoryは90分操作が無いとセッションが切れてしまいますので、  
　稀にマウスを動かすなど様子を見ながらご実行ください。  
"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# import logging
# from gensim.models import word2vec
# 
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# 
# # １文字ごとに区切ったテキストデータを指定する
# sentences = word2vec.Text8Corpus("/content/drive/MyDrive/KITERETU/tmp_1kugiri.txt")
# 
# # Word2Vecの学習実施
# model = word2vec.Word2Vec(sentences, 
#                           size = 60,
#                           min_count = 5,
#                           window = 30,
#                           iter = 10)
# 
# # できたモデルを保存する
# model.save("/content/drive/MyDrive/KITERETU/c2v.model")
#

"""■ できたモデルの内容を確認してみる："""

from gensim.models import word2vec

# 保存したモデルファイルの読み込み
model = word2vec.Word2Vec.load("/content/drive/MyDrive/KITERETU/c2v.model")

#出てきたモデルの確認
out = model.wv.most_similar(positive = [u'山'], topn=7)
print(out)
out = model.wv.most_similar(positive = [u'三'], topn=7)
print(out)
out = model.wv.most_similar(positive = [u'学'], topn=7)
print(out)
out = model.wv.most_similar(positive = [u'電'], topn=7)
print(out)
out = model.wv.most_similar(positive = [u'親'], topn=7)
print(out)

"""■ 2つの漢字の融合結果を見る："""

from gensim.models import word2vec

def make_name(model, char1, char2):
  out = model.wv.most_similar(positive = [char1,char2], topn=7)
  print(char1 + "＋" + char2)
  print(out)

# 保存したモデルファイルの読み込み
model = word2vec.Word2Vec.load("/content/drive/MyDrive/KITERETU/c2v.model")

make_name(model, '雅','美')
make_name(model, '洋','千')
make_name(model, '隆','菜')
make_name(model, '治','恵')
make_name(model, '昌','杏')

"""■ 某国民的有名家族で計算："""

make_name(model, '栄','鱒')
make_name(model, '螺','鱒')
make_name(model, '波','船')
make_name(model, '平','船')

"""■ 「みさえ」×「ひろし」⇒！？ ：

"""

make_name(model, '美','博')
make_name(model, '美','浩')
make_name(model, '美','弘')
make_name(model, '美','宏')
make_name(model, '美','寛')

make_name(model, '実','博')
make_name(model, '実','浩')
make_name(model, '実','弘')
make_name(model, '実','宏')
make_name(model, '実','寛')

make_name(model, '三','博')
make_name(model, '三','浩')
make_name(model, '三','弘')
make_name(model, '三','宏')
make_name(model, '三','寛')

"""■ 「三」＋「浩」の上位１２位まで出力してみる："""

out = model.wv.most_similar(positive = [u'三', u'浩'], topn=12)
print(out)

