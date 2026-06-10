> **注記:** 英語版 (`docs/evaluation.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Skill の評価

このドキュメントは、このリポジトリの Skill に使用する評価アプローチを説明します。

## Skill ごとの評価資産

各 Skill は `evals/` ディレクトリを持ちます:

```
skills/<skill-name>/
└── evals/
    └── README.md    # Iter 0 確認、シナリオ、実行結果、振り返り
```

## evals/README.md の構成

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

評価は blank-slate サブエージェント (このリポジトリへの事前知識のない状態で起動したエージェント) を使い、手動で実施します。

**Blank-slate executor プロトコル:**
1. リポジトリコンテキストを持たない新しいサブエージェントを起動する
2. SKILL.md の内容とシナリオの説明を提供する
3. 出力が要件チェックリストの各項目を満たすかを観察する
4. 結果を正直に記録する。実行していない場合は "not yet executed" と明記する

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

Skill を大幅に改訂するとき、変更が改善であり既存シナリオをリグレッションしていないことを確認するため、`evals/README.md` に before/after の比較を記録します。
