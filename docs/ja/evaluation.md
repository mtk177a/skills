> **注記:** 英語版 (`docs/evaluation.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Skill の評価

このドキュメントは、このリポジトリの Skill に使用する評価アプローチを説明します。

## Skill ごとの評価資産

各 Skill は `evals/` ディレクトリを持ちます。README は必須です。反復評価の再現性を高める場合は、任意の構造化資産を追加します。

```
skills/<skill-name>/
└── evals/
    ├── README.md       # 目的、手順、結果要約、振り返り
    ├── triggers.json   # 任意の trigger、non-trigger、near-miss ケース
    └── evals.json      # 任意の実課題、入力、assertion、baseline 条件
```

この構造へ合わせるためだけに、既存 Skill を一括移行しません。他の26 Skill は、それぞれを次に大幅改訂するときに構造化資産へ移行できます。

## 評価資産の責務

### evals/README.md

人が読む評価契約と結果の要約を保持します。

- 目的と期待する挙動
- 実行手順と環境
- 静的確認とシナリオの概要
- 結果、失敗、未実行項目の要約
- iteration の記録と次の検証課題

見出しは固定しません。README を raw evidence の代用にせず、raw trace を埋め込みません。

### evals/triggers.json

次の再利用可能なケースを置く任意資産です。

- `should-trigger`
- `should-not-trigger`
- 対象責務に似ているが別の workflow に属する near-miss
- 実行回数、observability 規則、合格基準

trigger ケースは複数回実行します。trigger の挙動は環境や実行ごとに変わりうるため、client、model、date、run count を記録します。

client が公開する evidence だけを trigger 判定に使います。Skill load が観測できない場合は `not exposed` と記録し、出力の文面から load event を推測しません。

### evals/evals.json

次を置く任意資産です。

- 現実的な課題と入力
- 行動 assertion と critical requirement
- baseline 条件
- isolation と coexistence の構成

期待する答えを課題文へ埋め込まず、判断の誤りを露出できるだけの現実性を持たせます。

## evals/README.md の構成例

```markdown
# <skill-name> evals

## Iter 0 — Static check

- description と本文が内部的に一致している
- 出力フォーマットが定義されているか明確に示されている
- Skill が自己完結している
- 少なくとも1つの `[critical]` アサーションが特定されている

## Scenarios

### Scenario A: <タイトル>

<1文のコンテキスト>

Requirements checklist:
1. [critical] <重要な要件>
2. <その他の要件>

## Failure Pattern Ledger

- `<既知の失敗パターン>`

## Iter N — YYYY-MM-DD

### Changes

- <前回からの変更内容>

### Execution results

| Scenario | Result | steps | duration | retries | Weak phase |
|---|---|---|---|---|---|
| A | ○ | N/A | N/A | 0 | — |

### Structured reflection

- Scenario A:
  - Issue: ...
  - Cause: ...
  - General Fix Rule: ...

### Ledger updates

- Re-seen: `pattern`
- Added: `pattern`

### Next fix proposal

- <提案>
```

## 評価の実施方法

評価には blank-slate executor を使います。リポジトリの履歴を持たず、シナリオに必要な入力だけを受け取るエージェントまたは client session です。

**Blank-slate executor プロトコル:**

1. リポジトリコンテキストを持たない新しい executor を起動する
2. SKILL.md の内容とシナリオの説明を提供する
3. 出力が要件チェックリストの各項目を満たすかを観察する
4. 結果を正直に記録する

次の両方を評価します。

- **Isolation:** 不足を隠しうる隣接 Skill を有効にせず、対象 Skill を単独で評価する
- **Coexistence:** 通常利用時に存在する隣接 Skill や instruction surface と一緒に評価する

観測できない項目は `not exposed`、実行しなかった項目は `not executed` と記録します。どちらも合格として扱いません。

評価者の役割は主観的な判断ではなく、動作の再現性を確認することです。

このアプローチは、[mizchi/skills](https://github.com/mizchi/skills) に記載されている empirical prompt-tuning 手法を参考にしています。`THIRD_PARTY_NOTICES.md` を参照してください。

## Iter 0 静的チェック

シナリオを書く前に、Iter 0 の静的チェックを実施します:

1. `description` と本文が内部的に一致している
2. 出力フォーマットが定義されているか明確に示されている
3. Skill が自己完結している (他の Skill やエージェントへの依存を前提としない)
4. 少なくとも1つの `[critical]` アサーションが特定されている

Iter 0 を通過してから、`evals/README.md` にシナリオを整備します。

## ベースライン比較

Skill を大幅に改訂するとき、candidate を旧版と比較します。旧版を利用できない場合は Skill なしを baseline にします。両者で課題入力、client、model、reasoning 設定、環境を揃えます。candidate が isolation で合格しただけでは完了とせず、baseline 比較と coexistence を確認します。

## 結果 metadata と artifact の扱い

次を記録します。

- client、model、reasoning 設定、date
- run count と trigger rate
- 根拠付きの assertion 結果
- isolation と coexistence の構成
- client が公開する場合は token と duration
- `not executed` と `not exposed` の項目

raw JSONL、認証情報、完全な session log は、リポジトリ外の一時ディレクトリだけに保存します。credential、raw session、未加工の trace を commit しません。
