> **注記:** 英語版 [distribution.md](../distribution.md) を基準とする日本語参考訳です。

# Plugin 配布

`mtk177a-skills` は、公開 `skills/` カタログを 1 つの portable Agent Plugin として配布する。
初回バージョンは `0.1.0` とする。
Skill 本文と資源の管理元は `skills/` とし、配布用のコピーを別に保守しない。
単体の Skills と既存の APM bundle も引き続き利用できる。

## 同梱内容

ルートの `plugin.json` だけを Plugin manifest の管理元とし、Agent Plugins 1.0.0 のスキーマを宣言する。
OpenAI 固有の設定が必要になった場合は、このファイルの `extensions["com.openai"]` に記載する。
`.codex-plugin/plugin.json` は別に保守しない。
OpenAI はこの互換形式もサポートするが、ルートに OpenAI 拡張があれば、その設定を採用し、互換形式の設定とは結合しない。
[OpenAI の配布仕様](https://developers.openai.com/plugins/build/plugins) を参照する。

生成処理は `plugin.json`、`LICENSE`、`THIRD_PARTY_NOTICES.md` と、公開 `skills/` 内の追跡済みファイルを含める。
ただし、`evals/` と、ファイル名が `-ja.md` または `.ja.md` で終わるファイルは除外する。
参照資料、実行資源・メタデータ、2 つのミラーの `UPSTREAM.md` は、バイト単位で原本を保持する。
`.agents/` の保守用 Skill、リポジトリの指示、テスト、リポジトリ文書は除外する。
`skills/` に追加する追跡済みファイルは配布候補になるため、コミット前にスクリプト、外部参照、認証情報、生成物の混入を確認する。

初回のカタログは 29 Skill、14 個の参照資料、2 個の来歴文書からなる。
ルートの 3 ファイルと合わせ、ZIP は 48 ファイルを含む。
全 Skill を同梱するが、実行には [実行条件](compatibility.md#plugin-の実行条件) を満たす必要がある。
ZIP に余分な親ディレクトリは付けない。

## 候補版を生成する

Python 3.10 以降と Git を使う。
生成処理は Python の依存を追加せず、通信、インストール、アップロードも行わない。
配布元と同じリビジョンの checkout から生成処理を実行する。
指定した参照は一度だけコミットに解決し、未コミット・未追跡のファイルは含めない。
生成前に manifest のバージョンをコミットする。

```bash
python3 -B scripts/check_repository.py
python3 -B -m unittest discover -s tests
git diff --check
python3 -B scripts/build_plugin.py --ref <commit> --output-dir <outside-repository-output-directory>
```

出力は `<name>-<version>.zip`、`.sha256`、`.build.json` の 3 ファイルである。
生成記録には元コミット、ZIP のハッシュ、Skill 一覧、同梱ファイルごとのハッシュとモードを含める。
ZIP のファイル順と時刻を固定し、無圧縮で格納するため、圧縮ライブラリのバージョンに依存せず、再生成時にもバイト一致する。
既存の出力ファイルは上書きせず、エラーにする。

検証では、対応する manifest の識別項目、必須ファイル、Skill の起点、ミラーのハッシュ、相対 Markdown リンク、コードスパンにある明示的な `references/`・`../` 参照を、同梱対象に照らして確認する。
同梱対象にあるシンボリックリンクと submodule は拒否し、ZIP 内の各ファイルを元の Git blob とモードに照合する。
これは配布に必要な範囲の検査であり、完全な JSON Schema 検証、Markdown 解析、動作評価ではない。
一般的な例、通常の文章で示す参照、ツールの可用性、条件付きの指示は、Skill 変更時に別途確認する。

配布前に候補ブランチを push し、その正確なコミットをリポジトリ外の使い捨て利用側ディレクトリから検証する。
[APM の検証](compatibility.md#検証) に従い、全体 bundle、影響する選択導入、個別パス、frozen install、audit を確認する。
ソースの checkout 内で非 dry-run の APM install は実行しない。
ZIP、ハッシュ、元コミット、変更概要、検証結果を対応づけて保管する。
GitHub Releases での公開には別途許可が必要となる。

## 導入と更新

### ChatGPT と Codex

1. ChatGPT の個人用 Plugin のアーカイブアップロードから ZIP を導入する。
2. 次回以降は別の Plugin を作らず、既存 Plugin のメニューから「新しいバージョンをアップロード」を選ぶ。
3. 表示されたバージョンと Skill 一覧を確認し、新しい会話で明示利用を試す。
4. 利用可能な UI で Plugin を選び、「`mtk177a-skills` の `define-referents` を使い、参照資料を読んでから命名案を出してください」のように対象 Skill を依頼文で指定する。
5. 各利用先で、一覧への登録、観測できる場合は本文・参照資料の読み込み、出力を分けて確認する。

Chat、Work、dots、Codex で呼び出し構文や実行能力が同じだとは仮定しない。
妥当な回答だけから読み込みを断定せず、記録された検証なしに自動選択を仮定しない。
導入によってシェル、リポジトリ、外部接続、サブエージェント、書込権限が得られるわけではない。
アップロードはユーザーが行い、生成処理はアカウント設定を変更しない。

### Cursor

[Cursor の公式資料](https://cursor.com/docs/plugins) には、portable Agent Plugins の対応と、`~/.cursor/plugins/local/<plugin-name>/` でのローカル検証が記載されている。
同じ ZIP をこの Plugin ディレクトリへ展開し、直下に `plugin.json` を置く。
Cursor の再起動または **Developer: Reload Window** の後、Skill の登録と明示利用を確認する。
ローカル更新では必要なバックアップを確保してから、展開先をディレクトリ全体で入れ替える。
ファイルを重ねてコピーすると、削除された Skill が残る可能性がある。
この Skills 専用パッケージに `.cursor-plugin/plugin.json` は不要である。
これは文書上の導入方法であり、実機の動作は検証するまで未確認とする。
マーケットプレイスへの申請は対象外である。

### 重複導入を避ける

各実行環境で、同じ Skill の導入元を Plugin または単体・APM のどちらかに揃える。
正式版を有効にする前に、検証用 Plugin と重複する単体導入を特定し、クライアントが提供する方法で無効化または削除する。
無関係な Skill や認証情報は削除せず、未確認の優先順位や名前空間による重複解消を仮定しない。
新しい会話で正式版を確認し、復旧用に前のアーカイブを保持する。
Claude Code では既存の APM 導入を維持し、固有の Plugin manifest は追加しない。

## 配布と復旧

原本を更新し、変更した責務に必要な検証を行い、`plugin.json` のバージョンを上げてコミットしてから次のアーカイブを生成する。
配布物と利用側での検証を繰り返し、結果を保管した上で、ユーザーがアップロードと更新確認を行う。
配布済みの同じバージョンを別の内容で差し替えない。
復旧時は必要な旧版の原本を戻し、同じ検証を経て、新しいバージョンとして配布する。
直接のダウングレードは未検証である。
動作検証と、静的検査・利用側の導入確認を混同しない。
正式版の動作確認は、ユーザーがアップロードしたパッケージを対象の利用先で検証するまで未完了とする。
