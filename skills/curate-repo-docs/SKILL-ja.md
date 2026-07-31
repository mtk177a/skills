> **Note:** The English version (`SKILL.md`) is the canonical source.
> This Japanese translation is provided as a reference only.

# リポジトリドキュメントを整理する

## 目的

- 文章を書く前に、リポジトリのドキュメントを変更する必要があるか判断する。
- 対象読者に必要で、利用可能な根拠または権限のある決定に裏付けられた情報だけを掲載する。
- 情報を正本へ配置し、許可された最小限の変更を加え、調査時のコンテキストをドキュメントへ持ち込まずに検証する。

## 根拠と権限

適用されるリポジトリ指示、対象文書、実装、テスト、スキーマ、生成元、承認済みの決定、関連する履歴を確認する。
ドキュメント変更の判断に必要な根拠だけを使用する。

掲載候補の情報を内部的に分類する。

- **Verified:** コード、テスト、スキーマ、実行結果、承認済み文書で確認できる
- **Normative:** 要件を決定する権限を持つ人または情報源が明示的に決定している
- **Inferred:** もっともらしいが、明示的には確定していない
- **Unknown:** 利用可能な情報では確認できない、矛盾している、または判断できない

Verified と Normative の情報は事実として掲載してよい。
Inferred の情報を事実として掲載しない。
重要な Unknown は、もっともらしい内容で補わず報告する。

コードは現在の挙動を示す根拠になり得る。
コードだけでは、業務要件、設計理由、方針、恒久的な制約、所有者、SLO、許容可能なリスクを確定できない。

## 手順

1. 依頼された成果、編集権限、対象範囲、適用されるリポジトリ指示を確認する。説明、評価、レビューの依頼は、編集も許可されていない限り read-only として扱う。
2. 読者、読者が完了すべきタスク、文書の役割を特定する。文書の種類を選択または新規作成する場合は、[document-kinds.md](references/document-kinds.md) を読む。
3. 掲載候補の主張について正本を特定する。手作業で複製された Reference より、生成可能または実行可能な情報源を優先する。
4. ドキュメントへの影響を、次のいずれか 1 つとして判断する。
   - `Update required`
   - `No documentation impact`
   - `Blocked by unknowns`
5. 執筆前に、`Audience`、`Reader task`、`Document role`、`Canonical sources`、`Claims to publish`、`Explicit decisions`、`Excluded context`、`Unknowns`、`Validation`、`Update triggers` を含む一時的な Document Contract を作る。ユーザーが求めた場合、またはリポジトリが文書 metadata として定義している場合を除き、この Contract は保存しない。
6. 次の両方を満たす主張だけを掲載する。
   - 読者のタスク、正確性、安全性のいずれかに必要である
   - Verified または Normative である
7. 許可された更新では、[repository-writing.md](references/repository-writing.md) を読み、既存の言語と有用な構造を維持し、最小の一貫した section だけを編集する。正本を複製せず、正本へ link する。
8. 調査経緯、棄却した仮説、一般的な best practice の説明、template を埋めるためだけの section、重複する例、関係のない書き換えを削除する。見出し、段落、例を削除してもタスクの完了、正確性、安全性が損なわれない場合は削除する。
9. 変更内容に関係するリポジトリ既定の検査を実行する。この workflow を完了するためだけに新しいドキュメントツールを導入しない。実行できない検査は、成功ではなく未実行として記録する。
10. 報告前に、実行したと記載する各検査を、観測済みの command または execution trace と照合する。trace にない検査を実行済みとして記載せず、inspection から導いた結論を、実行時に観測した結果として記載しない。

## 判断の扱い

変更が読者に見える挙動、契約、運用、architecture、configuration、その他の文書化された事実へ影響しない場合は、編集せず `No documentation impact` を返す。

必要な主張が、欠けている権限または根拠に依存する場合は、内容を捏造せず `Blocked by unknowns` を返す。
続行に必要な情報源または決定を具体的に示す。

現行挙動を reverse-engineering する場合は、規範ではなく記述的な文書であることを示し、可能であれば確認した revision または commit を記録する。
未定義または矛盾する挙動は Unknown として残す。

## 検証と報告

Markdown の構文だけでなく、変更した主張を検証する。
リポジトリに応じて次を使用する。

- ドキュメントの lint、link 検査、strict なドキュメント build
- 変更したコマンドまたは例の実行
- API、configuration、database、生成用 schema との比較
- 再生成後の clean diff 検査
- 相対 link、識別子、用語、成功条件の確認

次を報告する。

- ドキュメントへの影響状態
- 変更した文書と読者にとっての目的、または編集しなかった理由
- 使用した正本
- 実行した検査と結果
- 重要な Unknown、未実行の検査、残るドキュメントへの影響

ユーザーが根拠の記録を求めない限り、報告は調査内容より短くする。

## 境界

- Skill の起動を、ファイル編集、公開、その他の外部書き込みの権限として扱わない。
- 局所的な文書作業を理由に、ドキュメント体系を再設計したり、リポジトリ全体の鮮度監査や方針策定を行ったりしない。
- `japanese-tech-writing` または `cognitive-rhythm-writing` を自動適用しない。ユーザーが複数の writing Skill を明示的に組み合わせた場合も、掲載内容、根拠、正本、編集範囲はこの Skill が管理し、他の Skill は採用済みの内容の表現だけを調整する。
- 未決定の設計判断には設計用 workflow を使用する。この Skill では、権限のある情報源が決定済みの事項だけを記録する。
- 完成済みの変更のレビューには diff review workflow を使用し、cold pass または独立した改稿をユーザーが明示した場合だけ fresh revision workflow を使用する。
