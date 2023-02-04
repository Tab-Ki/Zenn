#%% web上のPDFファイルをローカルに保存せずに文字列情報を取得
from io import BytesIO
from urllib import request
from pdfminer.high_level import extract_text

url = "https://www.jitec.ipa.go.jp/1_00topic/topic_20071225_shinseido_4.pdf"

with request.urlopen(url) as res:
    f = BytesIO(res.read())
    text = extract_text(f)
    print(text[:300])
    # 何かしらの文字列処理

#%% 読み取る際の設定を指定
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
    # 何かしらの文字列処理

#%% PDFのページごとに処理。文字列や図の座標を取得したい場合など
from pdfminer.high_level import extract_pages

with request.urlopen(url) as res:
    f = BytesIO(res.read())
    for page_layout in extract_pages(f, page_numbers=[0]):
        for element in page_layout:
            print(element)

# %%
