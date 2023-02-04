---
title: "【Python】webスクレイピング時にPDFファイルをローカルへ保存せずにテキスト抽出する"
emoji: "🤖"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["Python","pdfminer"]
published: false
---
# 1. 概要

`BeautifulSoup`などを利用したwebスクレイピングにおいて、PDFファイルの解析時にファイルを一度ローカルに書き込んでしまうと余計な時間がかかります。このページは取得したPDFのバイナリデータをストリーム形式に変換することでそのまま解析する方法のメモになります。PDFの解析ライブラリには`pdfminer`を利用します。

## 1.1. 環境

|Name|Version|
|----|----|
|Python|3.10.6|
|pdfminer.six|20221105|

## 1.2. pdfminer

PDFを`Python`で解析するためのライブラリです。`pip`でインストールできます。

```bash:terminal
$ pip install pdfminer.six
```

公式ドキュメントに`pdfminer`のチュートリアルやAPIリファレンスが記載されています。

https://pdfminersix.readthedocs.io/en/latest/index.html

## 1.3. プログラム

記事内で利用しているプログラムです。
https://github.com/Tab-Ki/Zenn/tree/main/src/web_scraping/script.py

# 2. PDFファイルのテキスト抽出
## 2.1. 単純な例
web上のPDFファイルを`urllib.request`や`requests`などを利用して取得すると、その中身はバイナリデータになっています。これを`Python`の標準ライブラリに含まれている`io.BytesIO`によってバイナリストリームに変換します。こうすることで、一度ローカルに保存してから`with open("path", 'rb') as f:`で読み込んだオブジェクトと同様に扱うことができます。

以下ではIPAのホームページに掲載されている[「情報処理技術者試験　新試験制度の手引」](https://www.jitec.ipa.go.jp/1_00topic/topic_20071225_shinseido_4.pdf)というPDFファイルを例にテキスト抽出しています。

```Python:script.py
# web上のPDFファイルをローカルに保存せずに文字列情報を取得
from io import BytesIO
from urllib import request
from pdfminer.high_level import extract_text

url = "https://www.jitec.ipa.go.jp/1_00topic/topic_20071225_shinseido_4.pdf"

with request.urlopen(url) as res:
    f = BytesIO(res.read())
    text = extract_text(f)
    print(text[:300])
```

出力は以下のようになります。

```Text:outputs
情 報 処 理 技 術 者 試 験
新 試 験 制 度 の 手 引

ー 高 度 Ｉ Ｔ 人 材 へ の 道 標 ー

情報処理技術者試験が

　　　　　大きく変わります。

2007.12.25

ＩＴ人材育成本部 情報処理技術者試験センター

 
◆◇◆  はじめに  ◆◇◆ 

独立行政法人  情報処理推進機構では，2007 年 7 月 20 日にとりまとめられた産業
構造審議会情報経済分科会情報サービス・ソフトウェア小委員会人材育成ワーキング
グループの報告書「高度 IT 人材の育成をめざして」の中で示された試験制度改革の
方向性を踏まえ，新たな試験制度の具体化を検討するため，「新
```

## 2.2. 読み取る際のパラメータを指定する場合

利用方法の詳細は[公式リファレンス](https://pdfminersix.readthedocs.io/en/latest/reference/highlevel.html#extract-text)を見ていただくのが最良ですが、例えば文字列を抽出する際の設定を変更するには以下のように`LAParams`オブジェクトを作成し、`extract_text()`のオプションに指定します。

```Python:script.py
from pdfminer.layout import LAParams

laparams = LAParams(
    line_overlap=0.5,
    char_margin=2,
    line_margin=0.5,
    word_margin=0.1,
    boxes_flow=0.5,
    detect_vertical=False,
    all_texts=False
)

with request.urlopen(url) as res:
    f = BytesIO(res.read())
    text = extract_text(f, laparams=laparams, page_numbers=[0])
```

上の例では`page_numbers`を指定することでPDFの最初のページだけを対象にしています。

`LAParams`のパラメータは基本デフォルトで問題ないかと思いますが、縦書きの文字を解析する場合は`detect_vertical=True`、図や表の内部の文字も解析する場合は`all_texts=True`を指定します。

## 2.3. ページ単位で処理する場合

PDFをページ単位で解析したい場合、また抽出したテキストがPDFのどこに存在するかを把握したい場合は、`extract_pages()`を利用します。以下はPDFの最初のページに含まれている要素を全て出力するコードの例になります。

```Python:script.py
from pdfminer.high_level import extract_pages

with request.urlopen(url) as res:
    f = BytesIO(res.read())
    for page_layout in extract_pages(f, page_numbers=[0]):
        for element in page_layout:
            print(element)
```

```Text:outputs
<LTTextBoxHorizontal(0) 27.820,521.735,384.817,597.734 '情 報 処 理 技 術 者 試 験\n新 試 験 制 度 の 手 引\n'>
<LTTextBoxHorizontal(1) 27.650,494.612,258.679,511.612 'ー 高 度 Ｉ Ｔ 人 材 へ の 道 標 ー\n'>
<LTTextBoxHorizontal(2) 71.859,354.332,218.159,367.632 '情報処理技術者試験が\n'>
...
```

`extract_pages()`の戻り値は`LTPage`オブジェクトの集合です。`LTPage`オブジェクトの内部は階層構造になっており、そのページに含まれるテキストや画像のPDF内座標情報などが格納されています。`LTPage`オブジェクトに関しては、こちらの[「PDFからテキストを抽出(プログラム)【Python】」](https://juu7g.hatenablog.com/entry/Python/PDF/program#LTPage%E3%82%AA%E3%83%96%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)でも詳細に解説されています。

# 3. 終わりに

webスクレイピングにおいて指定したURLのHTMLに含まれるURLを再帰的に辿っていると、解析対象のPDFも数十数百と増加していくため、ファイル書き込み＆読み込みの時間をカットすることは重要です。PDFに限らずexcelやwordファイルなども同様の方法で直接ライブラリに渡すことが可能です。