# CommonMark ベストプラクティス整理 (簡易)

> **Attribution:** This file is an original summary authored for this repository.
> Rules are derived from the [CommonMark Specification](https://spec.commonmark.org) (CC BY-SA 4.0).

このファイルは CommonMark を基準に「一般的に妥当な整備ルール」を分類する。
ルールは必ず **推奨 / 状況依存 / 非推奨** に分けて判断する。

## 推奨

- 行末の不要スペースは削除する
- 見出しの前後に空行を入れる
- リストの前後に空行を入れる
- コードフェンスの前後に空行を入れる
- 箇条書きの記号を統一する (例: `-`)
- 連続する空行は 1 行に揃える
- リンクはインライン記法で統一する (例: `[text](url)`)

## 状況依存

- コードフェンスの言語指定を必須にするか
- 見出し記法を ATX のみに統一するか
- 自動折り返しの有無
- HTML を許容するか
- URL の自動リンクを許容するか

## 非推奨

- Markdown 方言特有の構文を CommonMark で必須扱いにする
- 意味を変える整形 (改行位置で意味が変わる箇所の強制整形)

## 判断のヒント

- CommonMark に含まれない拡張 (例: 表、チェックボックス) は状況依存に分類する
- 既存の運用ルールがある場合は尊重し、衝突時は承認を取る
 - 推奨は原則適用。ただし既存スタイルと衝突する場合は除外する
