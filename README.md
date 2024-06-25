# scraping_con
国交省が出している企業情報検索システムのスクレイピング
1都3県の業者のリストを出すことを目的とする

# 開発環境として必要なもの
- VSCode
  - Python 3.12.4
- Docker Desktop

# 開発環境
1. VSCodeをインストールする
2. DevContainerを起動する

# 使用方法
`const.py`の都道府県番号を対象のものに変更する。
`main.py`を実行する。

再開する場合、重複や抜け漏れがないようにCSVファイルのデータを削除してから再開すること。
Port:7900のSeleniumのモニターのパスワードは`secret`

# 参考資料
- [建設業者・宅建業者等企業情報検索システム](https://etsuran2.mlit.go.jp/TAKKEN/kensetuKensaku.do?outPutKbn=1)