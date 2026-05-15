# record-session-handoff evals

`record-session-handoff` の単体運用を評価するためのメモです。セッション継続に必要な決定事項、未決事項、次アクションを外部メモとして安全に整理できるかを見ます。

## Iter 0

- `description` と本文が「セッション横断の handoff 運用」に揃っているか
- Session Log と Handoff (latest) の役割が分かれているか
- 確定事項と未確定事項が分離されているか
- 保存先未指定時に止まることが明確か

## Scenarios

### Scenario A: 長い作業を次セッションへ引き継ぐ

決定事項と保留事項が混在した状態で、次回すぐ再開できる handoff を作る。

Requirements checklist:

1. [critical] Decisions と Open Questions を混同しない
2. First Step Next Session が具体的に残る
3. Session Log と Handoff の役割が分かれている
4. 確定事項だけを decisions 保存先へ昇格する

### Scenario B: 保存先が未指定のまま使おうとする

メモ化したいが、セッションログや latest handoff の保存先が決まっていない。無理に運用を始めない。

Requirements checklist:

1. [critical] 保存先未指定を Ask first として止める
2. 会話履歴だけを唯一の記録にしない
3. 必要な入力項目が分かる
4. Open Questions を decisions として確定扱いしない

## Failure Ledger Seed

- `decisions and open questions conflated`
- `handoff written without destination`
- `session log and latest handoff blurred`
- `open questions promoted to durable decisions`
