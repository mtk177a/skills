# write-natural-japanese の評価

`SKILL.md` は日本語で記述する。Skill と参照資料は本リポジトリで作成した MIT ライセンスの内容であり、外部 Skill を翻案していない。

## 評価方法

動作定義は `evals.json`、呼出し定義は `triggers.json` に置く。`../../../docs/evaluation.md` に従い、変更した責務の例を選び、`scripts/run_skill_evaluation.py plan` で呼出し数を確かめてから実行する。採点条件は実行時のエージェントへ渡さない。

意味・条件・確度・発話意図、根拠、開示、変更範囲、正確な文字列を先に判定し、自然さで失敗を相殺しない。出力品質と、Skill の選択・参照資料の読込みは別の証拠として確認する。生の prompt、出力、トレース、一時 fixture はリポジトリ外に置く。

## 直近のモデル評価

評価対象は commit `a639216` の `SKILL.md` と `references/wording-decisions.md`。Codex CLI 0.155.1、gpt-6-luna、max reasoning、read-only fixture、既存 keyring 認証、一時 HOME で個人側の同名 Skill を隔離して実行した。`plan` の見積りは 6 呼出しで、各ケースを一回実行した。static check、catalog preflight、runtime read guard、isolation は全件通過した。

| ケース | 確認した結果 |
| --- | --- |
| N1 | 単独で利用者向けの新規稿を完成し、非公開の作業名や執筆指示を出さず、設定値・反映条件を保持した。 |
| N2 | A の忠実な推敲では調査手順と留保を保持し、B の要約では許された詳述だけを省き、未確定の原因と `review` の条件を残した。 |
| N3 | 例外を送出しないことと実行時に値を使わないことだけで完成し、ログ・画面通知の有無を作らなかった。 |
| N4 | 一般説明を「保存状態」とし、API 名 `storageState` と画面表示 “Storage State” を保持した。 |
| N7 | A の構造を保ち、B の再構成でも適用条件、確認前に実行しない依存、`#check` のリンク先を保持した。 |
| H | 原文の要件・条件・製品名を保って翻訳し、一般語を文脈に沿って表現した。 |

六例とも選定した条件を満たした。N4 と H のトレースには、当時の参照資料 5,755 文字を全文 `cat` した記録がある。本 README の後続編集や今回の文言・配置修正後にモデル評価を再実行した結果ではない。

## 判断に必要な先行証拠

- Issue #98 着手時の main `fdb93fe` では、N3 が「例外を送出しない」を「発生しない」に強め、N4 が一般説明の `storage state` を残した。その後の修正で両例を各一回通過した。
- N8 は旧版と候補版の双方が通過し、出力改善は確認できなかった。
- 隔離後の D1 は非呼出し、D2 は対象 Skill 読込みを直接観測した。元の HOME では D2 が fixture Skill を読まず、別の再試行は個人側の同名 Skill を読んだため無効とした。権限ガード不一致の原因は未解明。`description` は今回変えていない。
- Issue #47 の 2026-09-17 評価では、当時の Codex CLI 0.155.0-alpha.2.6 と gpt-5.6-luna で H の候補・比較元とも参照全文を読んだ。D3 は二つの Skill を明示指定した併用試験であり、必須依存の証拠ではない。詳細な経緯は Git 履歴と [PR #136](https://github.com/mtk177a/skills/pull/136) に残る。

## 未確認の範囲

- 今回の修正後のモデル出力と、N5・N6・N8、D1–D3 の再実行。
- 選定例の反復安定性、人の読解改善、共有スレッド文脈の直接試験。
- すべての Markdown・リンク、他のクライアント・モデルでの挙動。新規執筆の単独完結については N1 と先行版の N5 の直接例までを根拠とする。

## 参考資料

[Claude の Agent Skills ベストプラクティス](https://platform.claude.com/docs/ja/agents-and-tools/agent-skills/best-practices) と [OpenAI の Skills 作成ガイド](https://developers.openai.com/plugins/build/skills) を 2026-10-13 に参照し、簡潔な主指示、条件付きの参照リンク、長い参照資料の案内を構成の参考にした。確認したページに版番号はなかった。外部本文・例の転載や翻案はしておらず、再配布・翻案条件は確認していない。
