> **注記:** 英語版 (`docs/compatibility.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# 互換性

このドキュメントは、このリポジトリの Skill がエージェントクライアント間でどのように検証されているか、期待される互換性の姿勢を説明します。

## 検証スコープ

Skills は [Agent Skills specification](https://agentskills.io/specification) に従います。これは Codex、Claude Code、GitHub Copilot、Gemini CLI が採用する軽量フォーマットです。`skills/<name>/SKILL.md` ファイルを探索して読み込むクライアントであれば、このリポジトリで動作するはずです。

Claude Code が主要な開発・テストターゲットです。他のクライアントは標準的な `skills/<name>/SKILL.md` 探索フォーマットをサポートすれば動作することが期待されますが、正式には検証されていません。

以下の表に、明示的にテストされたクライアントを記載します。記載のないクライアントは標準フォーマットをサポートすれば動作する可能性がありますが、サポート対象とは主張しません。

| クライアント | 検証済み | 検証日 | スコープ |
|-------------|---------|--------|---------|
| Claude Code | — | — | インストール、一覧、呼び出し |
| Codex | — | — | インストール、一覧、呼び出し |
| GitHub Copilot / `gh skill` | — | — | インストール、一覧、呼び出し |
| Gemini CLI | — | — | インストール、一覧、呼び出し |
| APM (`apm install`) | ✓ | 2026-06-10 | インストール (apm 0.13.0)、frozen dry-run、pack dry-run (plugin 形式) |
| `npx skills add` | — | — | インストール |

検証が完了次第、確認済みエントリを埋めます。それまで、すべてのエントリは保留中です。

## インストールパス

### Claude Code

```bash
apm install mtk177a/skills
```

または `apm.yml` の依存関係として宣言:

```yaml
dependencies:
  apm:
    - mtk177a/skills
```

### 個別 Skill

```bash
apm install mtk177a/skills/skills/review-changes
```

## 検証

Skills が Agent Skills specification に準拠しているかを確認するには:

```bash
skills-ref validate
```

## 未テストクライアントに関する注意

表に記載されていないクライアントについて: Skills は標準的な `skills/<name>/SKILL.md` フォーマットに従っています。クライアントがそのパスで Skills を探索するなら、動作する可能性があります。互換性の保証や保証は一切しません。
