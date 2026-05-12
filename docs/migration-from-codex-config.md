# Migration from codex-config

## 方針

- 移行元: `mtk177a/codex-config` の `skills/personal` 配下
- 移行先: `mtk177a/agent-skills` の `skills/<skill-name>/SKILL.md`

この移行は、既存 skill を丸ごと複製する作業ではありません。`agent-skills` に置くべき skill かを見直しながら、将来 `gh skill` や `apm` から参照しやすい構成に整える作業です。

## 移行先の構成

各 skill は次の形にそろえます。

```text
skills/<skill-name>/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

`<skill-name>` は kebab-case にします。補助ディレクトリは必要な場合だけ追加します。

## 移行時のチェックリスト

- この skill は自作 skill、または自分で継続的に改変して保守する skill か
- 外部 skill の単純コピーになっていないか
- ディレクトリ名と `name` を kebab-case でそろえたか
- `description` を現在の用途に合わせて見直したか
- `SKILL.md` の frontmatter に `name` と `description` を入れたか
- 補助ファイルを持ち込む必要が本当にあるか確認したか
- secrets、個人情報、社内情報を含んでいないか
- MacBook Pro M1 / Windows WSL の両方で扱いにくい前提を増やしていないか

## Codex 固有の記述を残してよい場合

次のような場合は、Codex 固有の記述を残してよいです。

- Codex の機能や操作体系に強く依存している
- 他 agent へ無理に広げるより、Codex 向けとして明示したほうが誤解が少ない
- skill の価値が Codex 固有ワークフローにある

この場合でも、`description` から Codex 前提が分かるようにします。

## 汎用化すべき場合

次のような場合は、Codex 固有表現を見直して汎用化します。

- 目的自体は他 agent でも同じように成立する
- 違いがツール名や手順の細部にとどまる
- 将来 `gh skill` や `apm` から参照したい

汎用化では、目的、入力、判断基準を中心に残し、実行手段だけを agent ごとに読み替えやすくします。

## 移行時の進め方

1. `codex-config/skills/personal` から移したい候補を選ぶ。
2. `skills/<skill-name>/` を作り、`SKILL.md` の構成をこの repo の規約に合わせる。
3. `name` と `description` を見直し、利用場面が明確になるように書き換える。
4. 必要なら `references/`, `scripts/`, `assets/` を追加する。
5. Codex 固有記述を残すか、Claude Code / GitHub Copilot でも読めるように寄せるか判断する。
6. 外部 skill のコピー置き場になっていないか確認する。

## 移行後の形

移行後も、`skills/<skill-name>/` という単純な配置を維持します。これにより、`gh skill` や `apm` などから参照するときに、agent ごとの特別な探索ルールを前提にしなくて済みます。

この repo の目的は、skill の保守しやすい保管場所を作ることです。導入や配布の管理は引き続き dotfiles 側で行います。
