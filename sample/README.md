# sample

python-pptx でプレミアリーグの試合結果スライドを生成するサンプル集。

参考: https://python-pptx.readthedocs.io/en/latest/

## サンプル一覧

`src/sample/` 配下に、難易度順で 3 つのサンプルがある。すべて 1 試合 = 1 スライドの方針で、各スクリプトは `.pptx` を生成したあと続けて `.pdf` に変換する。

| ファイル | 内容 | 出力 |
| --- | --- | --- |
| `match_simple.py` | チーム名・スコア・日付だけのミニマル | `match_simple.pptx` + `.pdf` (1 枚) |
| `match_detailed.py` | スタジアム・観客数・得点者リスト付き | `match_detailed.pptx` + `.pdf` (1 枚) |
| `matchday_batch.py` | 試合データのリストから複数スライドを一括生成 | `matchday_batch.pptx` + `.pdf` (カバー + 試合数ぶん) |
| `pdf_export.py` | LibreOffice 経由で `.pptx → .pdf` 変換するヘルパー | — |

## セットアップ

このリポジトリは [rye](https://rye-up.com/) で管理されている。初回のみ依存をインストール。

```bash
cd sample
rye sync
```

rye を使わない場合は仮想環境に `python-pptx` を入れれば良い。

```bash
cd sample
python -m venv .venv && source .venv/bin/activate
pip install python-pptx
```

PDF 変換には **LibreOffice** が別途必要。

```bash
# macOS
brew install --cask libreoffice
# Ubuntu / Debian
sudo apt-get install libreoffice
# Windows
# https://www.libreoffice.org/download/ から導入
```

インストール後、`soffice` コマンドが PATH に通っていることを確認:

```bash
soffice --version
```

## 実行方法

`sample/` ディレクトリから、生成したいサンプルのスクリプトを実行する。

```bash
# rye を使う場合
rye run python src/sample/match_simple.py
rye run python src/sample/match_detailed.py
rye run python src/sample/matchday_batch.py

# venv を使う場合
python src/sample/match_simple.py
python src/sample/match_detailed.py
python src/sample/matchday_batch.py
```

実行したカレントディレクトリに `.pptx` と同名の `.pdf` が生成される。PowerPoint / Keynote / LibreOffice Impress で開けるほか、PDF はそのまま配布や印刷に使える。

## 自分のデータに差し替える

各スクリプト先頭の `MATCH` または `FIXTURES` 定数を書き換えるだけで内容を差し替えられる。
将来的に football-data.org などの API から取得して流し込めば、定期実行で自動化できる。
