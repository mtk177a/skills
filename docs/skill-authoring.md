# Skill Authoring Guide

## 良い skill の書き方

良い skill は、読む agent が迷わず使いどころを判断でき、必要な手順や注意点が過不足なくまとまっているものです。

特に次を重視します。

- 何のための skill かが短く明確である
- いつ使うのか、使わないのかが判断できる
- 前提条件、入力、期待する出力が読み取れる
- 特定 agent に閉じた記述が必要以上に混ざっていない
- 補助スクリプトや参照資料の責務が明確である

## description の書き方

`description` は説明文ではなく、利用判断の入口です。次のような観点を入れます。

- どんな状況で使う skill か
- どの作業を助ける skill か
- 特定 agent に依存するなら何に依存するか

避けたい書き方:

- 抽象的すぎて利用場面が見えない説明
- 「便利な skill」のような主観だけの表現
- Codex 前提なのに、その前提が読み取れない説明

## common skill と agent-specific skill の分け方

まずは agent 非依存で表現できるかを考えます。

- common skill: 複数 agent で同じ目的・同じ手順で使えるもの
- agent-specific skill: 利用できるツール、入出力形式、実行手順が特定 agent に強く依存するもの

この repo では分類ディレクトリを増やさず、skill 名または `description` で差を表現します。たとえば agent 固有であることが重要なら、名前や説明にその前提を含めます。

## 外部 skill を fork / copy する判断基準

外部 skill は、原則としてこの repo にそのままコピーしません。外部 skill の導入管理は dotfiles 側の `apm.yml` / `apm.lock.yaml` で行います。

この repo に取り込む判断をしてよいのは、次のような場合です。

- 自分で継続的に改変・保守する必要がある
- 元の skill をそのまま使うより、再設計したほうがよい
- 自分の運用に合わせて構成や説明を明確に見直したい

取り込む場合も、単純コピーではなく、`frontmatter` と `description` を見直して、この repo の規約に合わせます。

## secrets / private information を入れない方針

次の情報は skill 本文、補助スクリプト、参照資料、素材のいずれにも含めません。

- API key、token、password
- 顧客名、個人情報
- 社内 URL、社内手順、非公開の運用情報
- ローカル環境にしか存在しない秘密ファイルへの参照

skill は将来ほかの環境や agent からも参照される前提で書きます。環境依存情報が必要な場合は、変数名やプレースホルダで表現します。

## scripts を含む skill の注意点

`scripts/` を持つ skill は便利ですが、移植性を崩しやすいため慎重に扱います。

- シェル、OS、アーキテクチャ依存を最小限にする
- 追加依存がある場合は明記する
- repo 外の絶対パスに依存しない
- 破壊的操作を行うなら、skill 側でも安全確認を促す
- 生成物やキャッシュを repo に混ぜない

MacBook Pro M1 と Windows WSL の両方で使う前提を崩す script は、必要性が明確でない限り避けます。

## empirical review 資産の置き方

skill を継続的に改善する場合は、本文だけでなく評価資産も一緒に管理します。

- skill 単体の scenario や checklist は `skills/<skill-name>/evals/` に置く
- 複数 skill をまたぐ flow 評価は `docs/empirical-prompt-tuning/` に置く
- まず Iter 0 として `description` と本文の整合、出力フォーマット、隣接 skill への受け渡し条件を静的に点検する
- その後、blank-slate subagent で回せる scenario と requirements checklist を固定する
- checklist には最低 1 つ `[critical]` 項目を置き、成功判定を曖昧にしない

empirical review の目的は「作者の主観」ではなく「別 agent が迷わず再現できるか」を見ることです。所感メモよりも、scenario、判断基準、失敗パターンの再利用性を優先します。

## Codex 専用 skill を他 agent でも使えるようにする注意

Codex 専用だった skill を Claude Code や GitHub Copilot でも使いやすくする際は、Codex 固有の表現をそのまま残すかどうかを見直します。

確認ポイント:

- 特定ツール名に依存しすぎていないか
- 依頼の受け方や出力形式が他 agent でも通じるか
- 手順が Codex の機能前提になりすぎていないか
- agent 固有の差分を `description` や本文で十分に説明できているか

Codex 固有の記述を残してよいのは、その前提が skill の価値そのものになっている場合です。そうでない場合は、目的と判断基準を中心に書き換え、手段だけを差し替えやすくします。
