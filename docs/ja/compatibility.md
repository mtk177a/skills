> **注記:** 英語版 (`docs/compatibility.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# 互換性

この文書では、portable な Agent Skills format の互換性と、client 固有の discovery、invocation、permission、実行挙動を分けます。Skill の構造が有効でも、特定の client で意図どおり読み込まれ、発火し、実行されるとは限りません。

このリポジトリでは、証拠を次の 4 状態に分けます。
各状態は記録した範囲にだけ適用し、記録していない client behavior まで裏付けるものではありません。

| 状態 | 意味 |
| --- | --- |
| Format-compatible | Skill package が Agent Skills specification に準拠している。client が Skill を発見または実行できることまでは示さない |
| Documented | 現行の client 公式文書に、対象の discovery、invocation、extension、runtime behavior が記載されている。このリポジトリで実行済みとは限らない |
| Locally verified | client version、日付、観測した discovery または invocation の結果を、このリポジトリに記録している。観測していない invocation path は未検証のままとする |
| Behavior-tested | 定義済みの scenario set について、Skill が選択され、指示に従ったかを targeted evaluation evidence に記録している。特定範囲の証拠であり、一般的な support guarantee ではない |

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

Format 互換性は、client の discovery、invocation、behavioral compatibility の証拠ではありません。
公式文書は Documented の根拠になりますが、Locally verified または Behavior-tested とするには、記録されたローカル実行結果が必要です。

## Client matrix

| Client または層 | 文書上の位置付け | リポジトリ内の証拠 | 現在の状態 |
| --- | --- | --- | --- |
| Codex | 公式文書には、暗黙選択と、Codex CLI または IDE extension で `/skills` か `$` による Skill mention を使う明示的 invocation が記載されている。任意の `agents/openai.yaml` は OpenAI 固有の表示と dependency metadata を提供する。sandbox、approval、rules、tools、runtime access は Skill 本文とは別の制御面である | repository-local discovery と、対象を限定した暗黙選択および behavior を観測済み。明示的な `/skills` と `$` invocation、UI behavior、live permission behavior は、このリポジトリについて未実行 | Documented。記録済み scenario について Locally verified かつ Behavior-tested。明示的 invocation はローカルで未検証 |
| Claude Code | 公式文書には、Claude Code 固有の Skill discovery、invocation、frontmatter、permission、hook behavior が記載されている。これらの client 固有 control は、portable Skill の format 互換性からは導けない | repository installation、discovery、明示・暗黙 invocation、permission、behavior の実行記録なし | Format-compatible。runtime behavior は未検証 |
| GitHub Copilot / `gh skill` | client 固有の discovery、invocation、metadata、permission、runtime behavior は、現行公式文書と対象 version に照らして確認する必要がある | repository installation、discovery、invocation、permission、behavior の実行記録なし | Format-compatible。runtime behavior は未検証 |
| Gemini CLI | client 固有の discovery、invocation、metadata、permission、runtime behavior は、現行公式文書と対象 version に照らして確認する必要がある | repository installation、discovery、invocation、permission、behavior の実行記録なし | Format-compatible。runtime behavior は未検証 |
| その他の client | 標準 package を扱える可能性はあるが、format 互換性だけでは discovery または実行を確認できない | 下記の検証記録に version 付きで載っていない client は未検証 | 下記に記録がない限り未検証 |
| APM | このリポジトリを `agent-skills` package として配布するが、実行 client ではない。target 選択と installation layout は、downstream の invocation または behavior を示さない | 下記の package check を実行済み | 記録した範囲の distribution のみ検証済み |

client が対応しているという理由だけで、client 固有 metadata を全 Skills に追加しません。その client の invocation control、UI 表示、tool dependency declaration、permission behavior が必要な場合だけ追加します。portable な `name`、`description`、instructions、resources を共通層として維持します。

## 検証記録

次の表は、文書から推測した support claim ではなく、観測済みの repository check を記録します。

| 対象 | Version | 検証日 | 観測した範囲 |
| --- | --- | --- | --- |
| Claude Code | — | — | 未実行。installation、discovery、明示・暗黙 invocation、permission、behavior は未検証 |
| Codex | 0.145.0 | 2026-07-24 | repository-local discovery、baseline/candidate 16 selection run での target Skill open 観測、影響 case の 5 回の再実行を含む candidate/baseline 29 behavior run。明示的な `/skills` と `$` invocation、UI、live permission behavior は未実行 |
| GitHub Copilot / `gh skill` | — | — | 未実行。installation、discovery、invocation、permission、behavior は未検証 |
| Gemini CLI | — | — | 未実行。installation、discovery、invocation、permission、behavior は未検証 |
| APM | 0.26.0 | 2026-07-21 | install resolution、frozen dry-run、offline pack dry-run、audit |
| `npx skills add` の利用先を含むその他の client | — | — | 個別の記録がない限り未実行 |

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
