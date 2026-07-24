> **注記:** 英語版 (`docs/compatibility.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# 互換性

この文書では、portable な Agent Skills format の互換性と、client 固有の discovery、invocation、permission、実行挙動を分けます。Skill の構造が有効でも、特定の client で意図どおり読み込まれ、発火し、実行されるとは限りません。

## 互換性の層

| 層 | 確認する問い |
| --- | --- |
| Format | 有効な `SKILL.md` と、直接発見できる resources があるか |
| Discovery と installation | client はどこを探索し、Skill はどのように配布されるか |
| Invocation | ユーザーが明示実行できるか、model が暗黙選択できるか、それぞれを無効化できるか |
| Client extensions | client 固有 metadata、UI、tools、lifecycle 機能に依存するか |
| Enforcement | どの permission、sandbox、policy、hook が実行を実際に制約するか |
| Runtime | scripts、dependencies、filesystem access、network access が対象環境で利用できるか |
| Verification | 以上のうち、version と日付を記録してローカルで観測したものは何か |

Format 互換性は挙動互換性の証拠ではありません。公式文書とローカル実行結果を分けて記録します。

## Client matrix

| Client または層 | Format と discovery の位置付け | Invocation と client extensions | Enforcement と runtime の位置付け | ローカル検証 |
| --- | --- | --- | --- | --- |
| Codex | Codex 文書に従った Agent Skills と repository / user Skill discovery をサポートする | 暗黙選択と明示的な `$skill` / picker invocation。任意の `agents/openai.yaml` が Codex の UI metadata と dependencies を提供する | sandbox、approval、rules、利用可能な tools は Skill 本文と別の制御面。runtime access は実行中の Codex 環境に依存する | repository-local の targeted selection と behavior のみ |
| Claude Code | Claude Code の discovery と plugin surface で Skills をサポートする | 暗黙選択と `/skill-name`。`disable-model-invocation`、`user-invocable` などの frontmatter が invocation を変更し、`context: fork` が実行 context を変更する | `allowed-tools` は列挙 tool を事前承認するが、他の tool を禁止しない。settings では permission deny rule が禁止を強制し、CLI の `--disallowedTools` と SDK の `disallowed_tools` はそれぞれ固有の制御面である。hooks と settings も Skill 本文とは別の制御面である | 保留 |
| GitHub Copilot / `gh skill` | client が標準 Skill package を発見する場合に動作を期待する | client 固有の invocation と metadata は対象 version で確認する必要がある | permission、tool、runtime の挙動は未検証 | 保留 |
| Gemini CLI | client が標準 Skill package を発見する場合に動作を期待する | client 固有の invocation と metadata は対象 version で確認する必要がある | permission、tool、runtime の挙動は未検証 | 保留 |
| APM | このリポジトリを `agent-skills` package として配布する。実行 client ではない | target 選択と installation layout は APM の関心事であり、Skill invocation semantics ではない | install と audit policy は downstream client の挙動を証明しない | 下記の範囲で検証済み |
| Claude API Skills | Claude Code の local runtime ではなく API Skill execution environment を使う | Claude Code frontmatter や local plugin behavior を API surface へ投影しない | network と package availability は API execution environment に制約されるため、現行 API 文書で確認する | 未実行 |

client が対応しているという理由だけで、client 固有 metadata を全 Skills に追加しません。その client の invocation control、UI 表示、tool dependency declaration、permission behavior が必要な場合だけ追加します。portable な `name`、`description`、instructions、resources を共通層として維持します。

## 検証記録

次の表は、文書から推測した support claim ではなく、観測済みの repository check を記録します。

| 対象 | Version | 検証日 | 観測した範囲 |
| --- | --- | --- | --- |
| Claude Code | — | — | 未実行 |
| Codex | 0.145.0 | 2026-07-24 | repository-local discovery、baseline/candidate 16 selection run での target Skill open 観測、影響 case の5回の再実行を含む candidate/baseline 29 behavior run。明示的な `$skill`、UI、live permission behavior は未検証 |
| GitHub Copilot / `gh skill` | — | — | 未実行 |
| Gemini CLI | — | — | 未実行 |
| APM | 0.26.0 | 2026-07-21 | install resolution、frozen dry-run、offline pack dry-run、audit |
| `npx skills add` | — | — | 未実行 |

新しい結果を記録するときは、client と version、日付、installation path、観測できる場合は明示・暗黙 invocation の結果、隣接 Skills、model、permission mode、観測できなかった挙動を含めます。`not exposed` と `not executed` は pass ではありません。

## Installation paths

### APM 経由の Claude Code

```bash
apm install mtk177a/skills
```

または `apm.yml` で package を宣言します:

```yaml
dependencies:
  apm:
    - mtk177a/skills
```

### 個別 Skill

```bash
apm install mtk177a/skills/skills/review-changes
```

APM は複数 client を対象にできます。installation command を実行証拠として扱わず、対象ごとの解決 path と discovery behavior を検証します。

## 検証

利用可能な場合は `skills-ref` で Agent Skills format への適合を確認します:

```bash
skills-ref validate
```

repository の非配布 frozen APM check も実行します:

```bash
apm install --frozen --dry-run --no-policy
```

どちらの command も、triggering、instruction following、permission behavior、output quality を証明しません。それらの claim には [evaluation.md](evaluation.md) の targeted evaluation procedure を使い、第三者と executable capability の review には [security.md](security.md) を使います。

## 現行情報源

- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code Skills](https://code.claude.com/docs/en/slash-commands)
- [Claude Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)

client extension と runtime behavior は core package format より頻繁に変わります。設計または監査に影響する場合は、現行公式情報を再確認します。
