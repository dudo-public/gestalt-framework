# 標準作業手順書（SOP）: Atom化 (Atomization)

### 実行トリガー
この手順書は、私がデータや情報に対して「原子化して」「Atom化して」といった指示を出した時に実行されます。

### このタスクにおけるあなたの役割
このタスクを実行する際、あなたは「知識の解析者」です。あなたの仕事は、提供された未加工の情報を分析し、再利用可能な知識の最小単位である「Atomic Note」へと丁寧に加工することです。

### ディレクトリの文脈
- **入力ソース:** Atom化の対象となるデータは、主に`00_RAW`ディレクトリから提供されます。あるいは、プロンプトの指示の中に貼り付けられることもあります。
- **出力先:** あなたが生成した全てのAtomic Noteは、`20_VAULT/Atoms/`ディレクトリに保存されることを前提として、構成してください。

### 【必須】実行前チェック
⚠️ **以下を実行せずに作業を開始することは禁止されています** ⚠️
1. このドキュメント内の「チェックリスト」セクションを必ず確認
2. `tags_glossary.md` で既存タグを確認
3. 各Atomのタイトルはidではなく内容を元に独自に生成すること
4. 前計画・実行計画・後計画の3段階計画を作成し、ユーザーに提示

### ステップごとの処理手順

**ステップ1: 分析 (Analyze)**
- 提供されたRawデータを深く理解し、それが「単一の完結した概念」か、それとも「複数の概念にまたがる複合的な情報」かを判断します。

**ステップ2: 既存Atomの重複確認 (Check Existing Atoms)**

00_RAWのファイルを処理する前に、以下の手順で既存のAtomを確認します：

1. **関連キーワードで検索**
   - ファイル名から主要なキーワードを抽出
   - `search_vault_simple` あるいは search_vault_smart`で関連するAtomを検索(これらはobsibian MCPで実行可能です)
   - sourceフィールドから元ファイルパスを確認

2. **候補の提示とユーザー確認**
   ```
   以下の既存Atomが見つかりました：
   
   ✅ [Atom ID]: [タイトル]
      - source: [元ファイルパス]
      - created: [作成日]
      - status: [ステータス]
   
   このファイルは既にAtom化済みの可能性があります。
   以下のいずれかを選択してください：
   1. スキップ（既存のまま）
   2. 新規作成（別のIDで作成）
   3. 書き換え（既存Atomを更新）
   ```

3. **ユーザー判断に基づく処理**
   - **スキップの場合**: 処理をスキップし、次のファイルへ
   - **新規作成の場合**: 新しいIDで通常のAtomization処理を実行
   - **書き換えの場合**: 
     - 既存のAtom IDを保持
     - 元のsourceを更新
     - updated日付を更新
     - context_noteに「再Atom化」の日付を記載
     - 内容を完全に新しい情報で書き換え

**ステップ3: 計画と確認 (Plan & Confirm)**
- 分析結果に基づき、実行計画を私に提示します。
    - **単一概念の場合:** 「このデータは一つのテーマについて書かれているようです。これを一つのAtomic Noteとして加工します。よろしいですか？」
    - **複数概念の場合:** 「このデータには、大きく分けて【X個】の異なる概念が含まれています。これらをそれぞれ独立したX個のAtomic Noteに分割・再構成しますが、よろしいですか？」
- 私の承認を得てから、次のステップに進みます。

**ステップ4: 加工 (Process)**

**【重要】Atom粒度の原則**
Atomは「独立して価値のある最小単位」であるべきです。以下の基準で判断してください：

1. **独立した価値**: 単体で意味のある知識単位か？
2. **再利用可能性**: 異なる文脈で参照・活用できるか？
3. **明確な焦点**: 1つの主要なテーマまたは概念に焦点を当てているか？
4. **タグの独自性**: 他のAtomと異なる特徴的なタグセットを持つか？

**統合すべきケース:**
- 同じドキュメントから分割された複数の断片で、個別では文脈が失われるもの
- 共通のタグセットを持つ密接に関連した内容
- 短すぎて単独では意味をなさない情報

**分割すべきケース:**
- 明確に異なるトピックが混在している
- 独立して参照される可能性が高い複数の概念
- 異なる時期や文脈に属する情報

*** 分割と統合に関する注意: 一連の密接な関連性を持つ内容を分割しすぎると文脈が失われます。全く別文脈のものが合わせて1つのファイルになっている場合は分割し、逆に一連のやり取りなど同じ文脈のものが分かれている場合は統合するのが適切です。

**実際の加工手順:**
- 承認された計画に基づき、Atomic Noteを生成します。
- **【最重要】複数概念の場合:** 単純に文章を機械的に分割するのではなく、各ノートが単体で意味を成すように、**情報を欠落させずに再構成・リライト（書き直し）**してください。目的は情報の要約ではなく、各概念が独立した価値を持つように整形することです。
- 全てのノートに、以下の要素を含む適切なYAMLフロントマターを付与します。
    ```yaml
    # 必須フィールド
    id: id_YYYYMMDD_英語識別子
    title: 日本語タイトル
    aliases: [id_YYYYMMDD_英語識別子]  # IDベースのリンキングのため
    type: "Atom"
    status: "processed"
    tags: [既存タグ, 新規候補タグ]
    source: "00_RAW/元ファイル.md"
    related: [関連するAtomのID]
    context_date: "YYYY-MM-DD"  # 文書作成時期
    
    # 必要に応じて追加
    supersedes: id_xxx  # 以前の思考を更新している場合
    superseded_by: id_xxx  # より新しい思考に置き換えられた場合
    phase: "Phase-[phase_id]"  # 該当するフェーズ[Optional] 開発フェーズなど、特定の時系列を有するもの
    ```
- md以外の形式(txt, pdf, html, etc...)などはmd形式として再生成してください。また、添付ファイルなどもしっかり関係性を保って保存してください。
    - **HTMLやPDFなど特殊な形式の場合**: `import_guidelines.md`を参照して、適切な変換とファイル管理を行ってください。
- **添付ファイルの管理**:
    - 画像やその他の添付ファイルは`_attachments`フォルダに直接配置します
    - **【最重要】`_attachments`フォルダの場所**: Vault直下にあります（`Obsidian Workspace Vault/_attachments/`）
        - 20_VAULT/Atoms/の下ではありません！
        - 不明な場合は必ず`vault_structure.md`を参照してください
    - **重要**: `_attachments`フォルダは基本的にサブフォルダ分けをしません
    - ファイル名は重複を避けるため、以下の命名規則を推奨：
        - `[AtomのID]_[元のファイル名]` 
        - 例: `id_20250117_ai_model_performance_image1.png`
    - Atom内では相対パスで参照：
        - 例: `![説明](_attachments/id_20250117_ai_model_performance_image1.png)`
- タグは20_VAULT/Cognition/_schema/tags_glossary.md で定義されています。既存のタグの中で合うものを選ぶ他、新しくAtom化する内容の中に新しくタグとして登録すべき内容があれば、**必ずユーザーに確認してください**。

**ステップ5: 納品 (Deliver)**
- 完成したAtomic Noteを、すぐにファイルとして保存できるMarkdown形式で、一つずつ提示しつつ、20_VAULT/Atoms/に保管します。

### 時系列・文脈管理と統合性維持のガイドライン

**原則: 分割されても失われない文脈**
Atom化は知識を最小単位に分解しますが、元の思考の流れや文脈を失わないことが重要です。

**時系列・文脈の記録方法**

1. **メタデータでの時系列管理**
   ```yaml
   context_date: 2025-06-16  # この思考・文書が形成された時期
   context_note: "現在の戦略的思考を反映"  # 時系列的な位置づけ
   importance: high  # 重要度（high/medium/low）
   superseded_by: id_xxx  # より新しい思考に置き換えられた場合
   supersedes: id_xxx  # 以前の思考を更新している場合
   ```

2. **統合性維持の実装方法**
   - **ID命名規則:** 関連するAtomには共通のプレフィックスを使用
     - 例: `id_20250616_how_to_use_obsidian_xxx`
   - **relatedフィールド:** 分割元が同じAtom同士を相互参照
   - **本文内での文脈明示:** 冒頭に元文書との関係を記載
     - 例: `> このノートは2025年6月時点での「○○」の一部です。`

3. **知識の再統合サポート**
   - 必要に応じてSyntheses層に統合文書の作成を提案
   - 各Atomが独立して理解可能でありながら、全体像も把握可能な構造

**注意事項**
- 「latest」のような一時的な表現は避け、具体的な日付や文脈を記録
- 古い思考も「海馬の一部」として保持し、思考の進化を追跡可能にする

## 🔴 必須チェックリスト

**このチェックリストを確認せずに作業を開始することは禁止されています。**
**特に重要：Atomのファイル名とタイトルは必ず日本語にすること。**

### 最重要ルール（これだけは絶対守る）
1. ✅ ファイル名は日本語（例：`Obsidianの使い方.md`）
2. ✅ titleフィールドも日本語
3. ✅ 情報の要約は禁止（完全転記）
4. ✅ 新規タグは必ずユーザーに確認

### 実行前チェックリスト

#### 1. 必須ドキュメントの確認
- [ ] `90_INSTRUCTIONS/atomization.md` を読み込んだ
- [ ] `20_VAULT/Cognition/_schema/terminology.md` のファイル名規則を確認した
- [ ] `20_VAULT/Cognition/_schema/tags_glossary.md` の既存タグを確認した
- [ ] `90_INSTRUCTIONS/overview.md` のAtom層の役割を理解した

#### 2. 作業準備
- [ ] 対象ファイルの内容を完全に読み込んだ
- [ ] 新規タグが必要な概念をリストアップした
- [ ] 各Atomの日本語ファイル名案を作成した
- [ ] 情報の完全性保持方針を確認した（要約・削除の禁止）

### 実行中チェックリスト

#### 各Atom作成時の確認事項
- [ ] **ファイル名**: 日本語で内容を表す簡潔な名前（30文字程度まで）
- [ ] **id**: `id_YYYYMMDD_英語識別子` 形式
- [ ] **title**: 日本語タイトル（ファイル名と同じ）
- [ ] **aliases**: idを含める
- [ ] **tags**: 既存タグから選択 + 新規タグはユーザーに確認
- [ ] **source**: 元ファイルの正確なパス
- [ ] **context_date**: 文書作成時期（YYYY-MM-DD形式）
- [ ] **phase**: 該当する開発フェーズ
- [ ] **related**: 関連Atomとの相互参照

#### 内容の品質確認
- [ ] 元文書の情報を**完全に保持**している（要約していない）
- [ ] 図表、数値、具体例を全て含めている
- [ ] 添付ファイル（画像等）への参照を保持している
- [ ] 時系列情報を明確に記載している

### 実行後チェックリスト

#### 全体確認
- [ ] 全てのAtomが日本語ファイル名になっている
- [ ] 元のRAWファイルと1対1で対応が取れている
- [ ] 情報の欠落がない（元文書と比較確認）
- [ ] 新規タグの提案と承認が完了している

#### メタデータ確認
- [ ] supersedes/superseded_by で時系列関係を表現している
- [ ] phase タグで開発フェーズを明示している
- [ ] related で関連Atom間の参照が設定されている

### タグ提案テンプレート

新規タグが必要な場合は、以下の形式でユーザーに提案：

#### タグ命名ルール検証
新規タグ提案前に必ず以下を確認：
- [ ] **Title Case**: 各単語の頭文字が大文字になっているか
- [ ] **使用可能文字**: A-Z, a-z, 0-9, -, _ のみを使用しているか
- [ ] **禁止文字**: スペース、ドット(.)、プラス(+)が含まれていないか
- [ ] **数字のみ禁止**: 数字のみのタグになっていないか
- [ ] **単語の接続**: 複数単語はハイフン(-)で接続されているか

#### 提案フォーマット
```
以下の新規タグの追加を提案します：

1. **Obsidian**: ローカルノート管理アプリObsidianに関する事柄
2. **ClaudeCode**: ClaudeCodeに関する事柄

理由：[各タグが必要な理由を説明]
```

### エラー防止のための注意事項

1. **要約の禁止**: 「本来あるべき姿」「要約すると」などの表現を使わない
2. **完全転記**: 元文書の全ての情報を保持する
3. **日本語優先**: ファイル名とタイトルは必ず日本語
4. **確認の徹底**: 不明な点は必ずユーザーに確認

### 日付管理ルール

**ID内の日付とcontext_dateの扱い**

1. **ID内の日付（id_YYYYMMDD_xxx）**
   - 原則としてAtom化を実行する日（今日）の日付を使用
   - IDは一意性を保つためのもので、作成日ベースで問題ない

2. **context_date（文書作成日）の判断基準**
   
   **context_dateを設定すべきケース:**
   - 時系列が重要な文書（議事録、Q&A、進捗報告など）
   - 「Phase-X」タグが付く開発関連文書
   - 意思決定や戦略に関する文書
   - 他の文書との前後関係が重要な内容
   
   **context_dateが不要なケース:**
   - 普遍的な技術情報や定義
   - 時系列に依存しない概念説明
   - 一般的な知識やノウハウ

3. **日付の確認方法**
   - **明示的な日付がある場合**: そのまま使用
   - **日付が不明だが必要と判断した場合**: 
     - 計画段階で「この文書は時系列的な文脈が重要と思われます。作成日はいつ頃でしょうか？」と確認
   - **推測が妥当な場合**:
     - 関連文書やファイル名から合理的に推測できる場合は、推測内容を明示して確認
     - 例：「Phase-4の議論のようですので、2025年5月頃と推測しますが、正確な日付はご存知ですか？」

4. **禁止事項**
   - ❌ 重要な文書で日付を勝手に決めない
   - ❌ 推測した日付を確認なしに使用しない
   - ❌ context_dateが必要な文書で、このフィールドを空欄のまま進めない
