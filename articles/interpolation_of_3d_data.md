---
title: "Pythonで三次元データの補間を行う"
emoji: "🐥"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["Python"]
published: true
---
# 1. 概要

「地点 A ($x_a, y_a, z_a$) における気温 $T_a$ と地点 B ($x_b, y_b, z_b$) における気温 $T_b$ から、その間にある地点 C ($x_c, y_c, z_c$) の気温 $T_c$ を推測したい」など、三次元やより高次のデータに対して補間を行いたい場合があります。`Python` で N 次元データの補間を行いたい場合、`SciPy` の `RegularGridInterpolator` を利用するといいですよと教わったのですが、日本語記事が少なかったためメモを残します。

## 1.1. 環境

|Name|Version|
|----|----|
|Python|3.10.6|
|SciPy|1.9.3|

## 1.2. scipy.interpolate.RegularGridInterpolator

公式のリファレンスは以下です。
https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.RegularGridInterpolator.html

:::details 簡単な説明
```Python:definition
class scipy.interpolate.RegularGridInterpolator(points, values, method='linear', bounds_error=True, fill_value=nan)
```
<br>任意次元の構造化データ（グリッドデータ）に対して補間（内挿・外挿）を行うモジュールです。非構造化データの場合は `NearestNDInterpolator` や `LinearNDInterpolator` を用いるようです。

- パラメータ
  - `points : tuple of ndarray of float, with shapes (m1, ), …, (mn, )`
  補間の元となるデータのグリッド情報を指定します。**1.概要**における気温の例の場合は、地点 A,B の座標データが対応します。
  - `values : array_like, shape (m1, …, mn, …)`
  補間の元となるデータの値を指定します。気温の例の場合は、地点 A,B の気温データが対応します。
  - `method : str, optional`
  補間方法を指定します。基本的には `linear` よりも `cubic` や `quintic` のように高次の多項式で補間する方が滑らかで性能がよいですが、データによっては[ルンゲ現象](https://ja.wikipedia.org/wiki/%E3%83%AB%E3%83%B3%E3%82%B2%E7%8F%BE%E8%B1%A1#:~:text=%E3%83%AB%E3%83%B3%E3%82%B2%E7%8F%BE%E8%B1%A1%EF%BC%88%E3%83%AB%E3%83%B3%E3%82%B2%E3%81%92%E3%82%93%E3%81%97%E3%82%87%E3%81%86,%E8%AA%BF%E3%81%B9%E3%81%A6%E3%81%84%E3%81%A6%E7%99%BA%E8%A6%8B%E3%81%97%E3%81%9F%E3%80%82)が起こる場合もあるため注意が必要です。

    |値|説明|
    |----|----|
    |linear|線形補間（デフォルト）|
    |nearest|最近傍補間|
    |slinear|スプライン補間（1次）|
    |cubic|スプライン補間（3次）|
    |quintic|スプライン補間（5次）|

  - `bounds_error : bool, optional`
  `True` の場合、`points` で定義されたグリッドの範囲外を補間しようとすると `ValueError` が発生します。`False` の場合、次の `fill_value` の値が利用されます。
  - `fill_value : float or None, optional`
  定義されたグリッドの範囲外を補間した際の値を指定します。`None` を指定すると、外挿が行われます。
:::

## 1.3. プログラム

記事で利用しているプログラムです。記事内では本筋と関係ない内容は省略しています。
https://github.com/Tab-Ki/Zenn/tree/main/src/interpolation_of_3d_data/script.py

# 2. 一次元データの補間

練習がてら一次元のデータに対して補間を試みます。

## 2.1. 補間の例

簡単な例として、変数 $x$ に対する値が関数 $f(x)=x^2$ に従うデータを扱います。補間の元となるデータを幾つかサンプリングします。

```Python:script.py
import numpy as np
import matplotlib.pyplot as plt

# データ生成関数
def func_1D(x):
    return x**2

# 描画関数
def show_data_1D(func, *args):
    # 省略

x = np.linspace(0, 9, 10)
data = func_1D(x)
show_data_1D(func_1D, (x, data))
```

![](/images/interpolation_of_3d_data/1.png)
*補間用データの準備*

青点で示した10個のデータが準備できました。

これらのデータを引数として `RegularGridInterpolator` のオブジェクトを初期化するだけで補間の準備は完了です。実行は初期化したオブジェクトを用いて以下のように行います。

```Python:script.py
from scipy.interpolate import RegularGridInterpolator
# グリッド情報 x はタプル型で与える
interp = RegularGridInterpolator((x,), data)

x2 = np.array([i + 0.5 for i in range(9)])
data2 = interp(x2)
show_data_1D(func_1D, (x, data), (x2, data2))
```

![](/images/interpolation_of_3d_data/2.png)
*補間されたデータのプロット*

青点のちょうど中間の $x$ に対する値 $f(x)$ を補間し、オレンジ点でプロットしました。オレンジ点に与えているのは青点の情報のみで、関数 $f(x)=x^2$ の情報は与えていませんが、おおよそ適切な値に補間されているのが確認できます。

## 2.2. 補間方法の変更
:::details 補間方法の変更
`RegularGridInterpolator` の `method` オプションにはデフォルトでは線形補間を意味する `"linear"` が指定されます。$f(x)=x^2$ の例では線形補間でも（グラフで見えるレベルでは）問題ありませんでしたが、もう少し複雑な関数、例えば $f(x)=sin(x)$ ではどうでしょうか。

```Python:script.py
data = np.sin(x)
interp = RegularGridInterpolator((x,), data) # method = "linear"
data2 = interp(x2)
show_data_1D(np.sin, (x, data), (x2, data2))
```

![](/images/interpolation_of_3d_data/3.png)
*method="linear"*

線形補間では青点同士を結んだ直線上にオレンジ点がプロットされるため、青点が実際に従っている関数 $f(x)=sin(x)$ との間にズレが生じてしまいます。

そこで、`RegularGridInterpolator` オブジェクトの初期化時に `method` オプションを指定するか、以下のように後から指定することで補間に利用するアルゴリズムを変更することが可能です。`"nearest"` は最も近い $x$ の値をそのまま用いる方法、`"slinear"`, `"cubic"`, `"quintic"` はそれぞれ1次、3次、5次のスプライン補間を用いる方法です。

```Python:script.py
interp.method = "nearest"
data2 = interp(x2)
show_data_1D(np.sin, (x, data), (x2, data2))

interp.method = "slinear"
data2 = interp(x2)
show_data_1D(np.sin, (x, data), (x2, data2))

interp.method = "cubic"
data2 = interp(x2)
show_data_1D(np.sin, (x, data), (x2, data2))

interp.method = "quintic"
data2 = interp(x2)
show_data_1D(np.sin, (x, data), (x2, data2))
```

![](/images/interpolation_of_3d_data/4.png)
*method="nearest"*
![](/images/interpolation_of_3d_data/5.png)
*method="slinear"*
![](/images/interpolation_of_3d_data/6.png)
*method="cubic"*
![](/images/interpolation_of_3d_data/7.png)
*method="quintic"*

各手法に対して、補間した値と正しい値の誤差を比較するために RMSD を計算したところ、以下表のようになりました。$f(x)=sin(x)$ の例では `"quintic"` で補間した値が最も正解との誤差が小さくなりました。

|method|RMSD|
|----|----|
|linear|0.0887|
|nearest|0.3441|
|slinear|0.0887|
|cubic|0.0123|
|quintic|0.0047|

:::

# 3. 三次元データの補間

データが三次元になっても基本的な操作は変わりません。

## 3.1. 補間の例

例としてここでは変数 $x,y,z$ に対する値が関数 $f(x,y,z)=x^3+y^2+z$ に従うデータを扱います。一次元の場合と同様に、まず補間元のデータをサンプリングします。以下では 6×6×6 の三次元グリッドと、その上の全ての格子点に対応する値 $f(x,y,z)$ を用意しています。


:::message
以下の例では一次元の場合と異なり、`np.meshgrid` 実行時に ``indexing=`ij` `` を指定する必要があります。
:::

```Python:script.py
from mpl_toolkits.mplot3d import Axes3D

# データ生成関数
def func_3D(x, y, z):
    return x**3 + y**2 + z

# 描画関数
def show_data_3D(*args):
    # 省略

x = y = z = np.linspace(0, 5, 6)
xg, yg, zg = np.meshgrid(x, y, z, indexing='ij')
data = func_3D(xg, yg, zg)
show_data_3D((xg, yg, zg, data))
```

![](/images/interpolation_of_3d_data/8.png)
*補間用データの準備*

これに対して、各点の丁度中間に位置する座標 $x,y,z$ における値 $f(x,y,z)$ を補間します。

```Python:script.py
interp = RegularGridInterpolator((x, y, z), data) # method = "linear"

x2 = y2 = z2 = np.array([i + 0.5 for i in range(5)])
xg2, yg2, zg2 = np.meshgrid(x2, y2, z2, indexing='ij')
data2 = interp((xg2, yg2, zg2))
show_data_3D((xg, yg, zg, data), (xg2, yg2, zg2, data2))
```

![](/images/interpolation_of_3d_data/9.png)
*補完されたデータのプロット*

補間元データと補間データの色は綺麗なグラデーションを形成しており、こちらもグラフで見えるレベルではある程度適切に補間できていることが分かります。

## 3.2. 補間方法の変更

:::details 補間方法の変更

同じデータに対して `method` を変更して複数の補間方法を試してみます。

```Python:script.py
interp.method = "nearest"
data2 = interp((xg2, yg2, zg2))
show_data_3D((xg, yg, zg, data), (xg2, yg2, zg2, data2))

interp.method = "slinear"
data2 = interp((xg2, yg2, zg2))
show_data_3D((xg, yg, zg, data), (xg2, yg2, zg2, data2))

interp.method = "cubic"
data2 = interp((xg2, yg2, zg2))
show_data_3D((xg, yg, zg, data), (xg2, yg2, zg2, data2))

interp.method = "quintic"
data2 = interp((xg2, yg2, zg2))
show_data_3D((xg, yg, zg, data), (xg2, yg2, zg2, data2))
```

<br>デフォルトの `"linear"` も含めて、各手法で補間した値の正解との誤差 RMSD は以下表のようになりました。今回の関数 $f(x,y,z)=x^3+y^2+z$ は $x$ の増加に対して値が大きく発散するため、それを反映することができない `"nearest"` の誤差が最も大きい結果となりました。`"cubic"`, `"quintic"` はいずれも誤差が殆どありませんでしたが、関数 $f(x,y,z)=x^3+y^2+z$ の影響で3次のスプライン補間である `"cubic"` の誤差が最小となっています。

|method|RMSD|
|----|----|
|linear|2.375|
|nearest|16.68|
|slinear|2.375|
|cubic|1.090e-14|
|quintic|2.303e-14|

:::

# 終わりに

それほど複雑なデータでなければこの `RegularGridInterpolator` で十分に精度のよい補間ができそうです。ただしこの方法では補間元のデータを常に保持しておく必要があるため、次は同様の課題を補間ではなく関数近似によって解決する方法を調べたいと考えています。