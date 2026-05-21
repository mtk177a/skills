# design-agent-instructions evals

`design-agent-instructions` の単体運用を評価するためのメモです。`AGENTS.md` を含む指示文書セットを、不要な文書を増やさずに設計・作成提案できるかを見ます。

## Iter 0

- `description` と本文が「指示文書セットの設計・作成」に揃っているか
- `AGENTS.md` / `CLAUDE.md` / `.github/copilot-instructions.md` / `GEMINI.md` の役割分担が分かるか
- 必要な文書だけを提案し、不要な文書を前提に増やさないか
- 単体で承認判断に進める情報量があるか

## Scenarios

### Scenario A: 最小構成の指示文書セット設計

新しいリポジトリで `AGENTS.md` と `.github/copilot-instructions.md` は必要そうだが、`CLAUDE.md` と `GEMINI.md` はまだ必要か不明。executor には、一次情報、読み込み順、文書ごとの役割分担を整理し、必要な文書だけを提案させる。

Requirements checklist:

1. [critical] 必要な文書だけを提案し、不要な文書を当然の前提として増やさない
2. 読み込み順を明記する
3. 文書ごとの役割分担を分けて書く
4. 承認前に作成・編集へ進まない

### Scenario B: 既存文書の責務衝突を含む再設計

既存の `AGENTS.md` と `CLAUDE.md` に同じルールが重複し、`.github/copilot-instructions.md` は要約不足、`GEMINI.md` は不要そうに見える。executor には、責務衝突を整理し、どこに何を書くかと何を書かないかを文書セット案として返させる。

Requirements checklist:

1. [critical] 文書間の責務衝突や重複を整理する
2. `GEMINI.md` を任意メンバーとして扱い、不要なら無理に採用しない
3. 共通事実と文書固有事項を切り分ける
4. 影響やリスクを承認判断用に残す

## Failure Ledger Seed

- `all documents proposed by default`
- `document roles overlap without exclusion rules`
- `agent-specific optional document treated as mandatory`

## Iteration 1

### Changes (diff from previous)

- 初回実行。Skill 本文は Iter 0 のまま。
- Pattern applied: `(baseline)`

### Execution results (per scenario)

| Scenario | Success/Failure | Accuracy | steps | duration | retries | Weak phase |
|---|---|---|---|---|---|---|
| A | ○ | 100% | N/A | N/A | 0 | — |
| B | ○ | 100% | N/A | N/A | 0 | — |

`spawn_agent` / `wait_agent` では `tool_uses` と `duration_ms` を取得できなかったため、この iteration の steps / duration は未記録。

### Structured reflection (newly surfaced this time)

- Scenario A: [critical] drop なし
  - Issue: 補助文書の要否判断は、実際にどのエージェントを使うかという運用前提に依存する。
  - Cause: 本文は「必要な文書だけを提案する」と書けているが、補助文書を増やす条件はより upfront に書けてもよい。
  - General Fix Rule: optional な補助文書を持つ Skill は、採用条件を `使う場面` か `手順` の早い段で明示する。
- Scenario B: [critical] drop なし
  - Issue: 文書間重複の整理はできるが、共通事実をどこへ寄せるかの canonical な寄せ先が読み手判断に少し依存する。
  - Cause: `AGENTS.md` を正式契約と書いてある一方で、README / docs 側へ残す事実の境界は実例が少ない。
  - General Fix Rule: 文書セット設計 Skill では、契約、補助指示、一般ドキュメントへの振り分け基準を 1 行ずつでも例示する。

### Discretionary fill-ins (newly surfaced this time)

- Scenario A: `CLAUDE.md` と `GEMINI.md` は「そのエージェントを実運用する場合のみ」と補って判断された。
- Scenario B: `AGENTS.md` を唯一の正式契約に寄せ、重複文書は参照先の明記に倒す方が安全と判断された。

### Ledger updates

- Re-seen: `all documents proposed by default` - 今回は再発せず、必要文書だけの提案を維持できた
- Re-seen: `agent-specific optional document treated as mandatory` - 再発せず、`GEMINI.md` は optional に保てた
- Added: `optional document criteria inferred, not surfaced early`

### Next fix proposal

- `使う場面` か `手順` に、補助文書は対象エージェントを実運用するときだけ候補に含める旨を 1 行で前倒しする

(Convergence check: 0 consecutive clears / 2 rounds remaining to stop condition)
