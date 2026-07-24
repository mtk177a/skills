> **注記:** 英語版 (`docs/security.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Skill セキュリティレビュー

この文書では、第三者 Skill または executable Skill を採用、改変、公開、または実質的に更新する前に行う security review を定義します。

入口が Markdown であるという理由だけで Skill を安全とみなしません。その指示により、agent はファイルを読み、script を実行し、tool を呼び、外部 content を取得し、data を送信できます。各 permission を個別に評価するのではなく、capability chain 全体を確認します。

## Capability から review の深さを選ぶ

外部 content、code、tool call、機密 data access を含まない instruction-only Skill には軽量な static review を使います。Skill が次のいずれかを含む、または誘導する場合は、より深い review を行います:

- scripts、binaries、package installation、生成 command、破壊的操作
- network request、remote resource、redirect、webhook、外部 upload
- MCP server、connector、plugin、hook、privileged tool
- 広い filesystem access、credentials、environment variables、private data
- import された指示、信頼できない文書、間接 prompt injection を含み得る content
- client 固有の permission bypass、preapproval、automatic invocation

upstream revision、dependency graph、外部 endpoint、runtime、permission model、capability の組み合わせが変わった場合は再確認します。

## Provenance と scope を確定する

次を記録します:

- upstream owner、canonical URL、固定した commit または release、取得日
- license と、ローカル再配布・改変が許可されるか
- import したファイル、省略したファイル、ローカル変更
- maintainership と、今後の upstream 差分を比較する手順
- 対象 client、runtime assumption、distribution path

配布する全ファイルと、`SKILL.md` から直接参照する全ファイルを確認します。frontmatter や主 instructions だけを review しません。外部 URL は、Skill が依存する実際の destination と指示または executable content を識別できるところまで辿り、redirect URL を最終的な trust boundary とみなしません。

## Instructions と capabilities を追跡する

Skill 内の各経路について次を特定します:

1. どの input が agent に影響できるか
2. どのファイルまたは secret を agent が読めるか
3. どの command、script、tool、service を呼べるか
4. どの data が環境外へ出られ、どこへ送られるか
5. どの approval、sandbox、permission、deterministic check が操作を制約するか

特に次の組み合わせへ注意します:

- filesystem read と network send
- credential access と生成 command
- 信頼できない document content と privileged tool
- automatic invocation と破壊的または外部に見える副作用
- remote instructions と script execution

個別には一般的な capability でも、組み合わさると重大な exfiltration または integrity risk になり得ます。

## Review indicators

次の項目は、説明、除去、または明示的な control を必要とする finding として扱います:

- 上位 authority の guidance を無視する、挙動を隠す、review を回避する指示
- 難読化 command、encoded payload、説明のない download、変更可能な remote script
- task scope 上の必要性がない広範な recursive file discovery
- hard-coded secret、credential location、private URL、customer data
- 責務と無関係な network destination
- repository、environment、conversation、credential data を外部送信する指示
- 宣言されていない dependency、または再現できない runtime installation
- unresolved variable、glob、信頼できない input から対象を決める command
- permission preapproval を prohibition または security boundary として説明すること
- client に強制可能な policy、permission、sandbox、hook、CI があるのに、安全特性を prose だけで表すこと

外部 document と tool output は未検証入力として扱います。task に必要な情報は抽出しますが、authority、permission、destination、scope を変えようとする埋め込み指示には従いません。

## Control と disposition を決める

Skill の責務を果たせる最小の authority と data scope を優先します。

- executable resource が実証済みの価値を加えない限り、Skill を instruction-only に保つ
- 再現性が重要な場合、dependency と upstream revision を固定する
- 繰り返し生成する壊れやすい command を、狭く test 済みの script に置き換える
- 利用可能な場合、hard guarantee を permission setting、sandbox policy、hook、CI、その他の deterministic control に置く
- client が対応する場合、破壊的または外部に見える workflow は明示 invocation を要求する
- network destination、送信 data、必要 credential、failure behavior を明示する
- provenance、behavior、outbound data flow を確定できない Skill は reject または quarantine する

disposition を accepted、accepted with controls、rejected、unverified のいずれかで記録します。観測した挙動と static inference を分けます。static review は runtime safety を証明しません。executable または client-dependent behavior が重要な場合は、isolated execution と targeted evaluation を使います。

## Repository handoff

review 済み Skill をこの repository で公開する前に:

- `THIRD_PARTY_NOTICES.md` に第三者 provenance を記録し、継続同期に必要なら local upstream note も残す
- 英語 canonical Skill と日本語 reference translation を同期する
- 特定した capability risk を露出するために必要な security assertion と scenario だけを追加する
- 該当する format、metadata、script、targeted behavior、非配布 APM check を実行する
- 利用できない client または runtime check を `not executed` と記録する

Skill 構造は [authoring.md](authoring.md)、client/runtime の区別は [compatibility.md](compatibility.md)、evidence requirement は [evaluation.md](evaluation.md) を参照してください。

## 現行情報源

- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)
- [Claude Code Skills](https://code.claude.com/docs/en/slash-commands)
