# Gestalt Framework

**参考記事:** [ClaudeCode/Gemini CLIとObsidianで人間のゲシュタルトを再現できるか](https://note.com/dudo_inc/n/n658023186f4e)

## 概要

私たちの思考は、方針、信念、こだわり、妥協、規律、基準といった様々な機微に基づいています。このフレームワークは、そうした思考の全体像（ゲシュタルト）をAIに転移させ、特定の専門領域に特化した「第二の脳」を育てることを目的としています。

### コンセプト：3つの知識階層

このフレームワークは、知識の成長と進化を促すシンプルな三層構造を核心としています。

1.  **素材層 (Atoms)**

      * **場所**: `20_VAULT/Atoms/`
      * **役割**: 知識を構成する、再利用可能な最小単位。メモ、ノート、事実、アイデア、議事録など、あらゆる情報が「原子」として保管されます。

2.  **統合層 (Syntheses)**

      * **場所**: `20_VAULT/Syntheses/`
      * **役割**: 素材（Atoms）同士が結びつき、"文脈"を吹き込まれた知識の集合体。特定のテーマに関するレポートや深い考察など、思考の成果物がここに形成されます。

3.  **認知層 (Cognition)**

      * **場所**: `20_VAULT/Cognition/`
      * **役割**: 最も高次の階層。自身の思考原則、信条、哲学、判断の拠り所となる「知恵」が記述されます。フレームワーク全体の方向性を決定します。

この3層は、認知層の知恵がAtomsの整理方法を規定し、Atomsから生まれたSynthesesが新たな知恵をCognition層に還元するという、上下双方向のフィードバックループによって進化し続けます。

-----

## 必要なツール

  - **Obsidian**: メインとなる知識管理ツール。
  - **Claude Code / Gemini CLI**: Vaultを操作し、思考のパートナーとなるAI。

### 必要なObsidianコミュニティプラグイン
このフレームワークを最大限に活用するために、以下のコミュニティプラグインをインストールし、有効化してください。

 - Dataview: ノート内のメタデータを元に、動的な知識のリストやテーブルを生成します。_knowledge_maps機能の根幹をなします。

 - Templater: テンプレートから新しいノートを効率的に作成できます。_knowledge_maps/_templates 内のテンプレートを活用する際に非常に便利です。

 - QuickAdd: JavaScriptによる自動化スクリプトの実行環境を提供します。DataviewRendererスクリプトの実行に必要です。

 - Advanced URI: 外部からObsidianのコマンドを実行可能にします。CLIツールからDataviewRendererを呼び出すために使用します。

 - pdf-mistral-plugin: (任意) PDFファイルをMarkdownに変換する際に役立ちます。
-----

## セットアップ

### 1\. Vaultの準備

1.  新しいObsidian Vaultを作成します。Vault名は「**Obsidian Workspace Vault**」としてください。
      * *もし別のVault名を使用する場合は、後述するスクリプトやURI内のパスを適宜修正してください。*
2.  Obsidianの「設定」→「コミュニティプラグイン」で、上記のプラグインをインストールし、有効化します。

### 2\. ディレクトリ構造の作成

AIが効率的に情報を巡回できるよう、以下のディレクトリ構造をVaultの直下に作成します。

```
Obsidian Workspace Vault/
├── 00_RAW/                    # 未処理の生データ
├── 10_WORKSPACE/              # 作業中のファイル
├── 20_VAULT/                  # Atom化された知識
│   ├── Atoms/                 # 最小単位の知識
│   ├── Syntheses/             # 統合された知識
│   │   └── _knowledge_maps/   # 知識マップ管理
│   │       ├── README.md
│   │       └── _templates/    # マップテンプレート
│   └── Cognition/             # メタ認知・スキーマ
│       ├── _schema/           # スキーマ定義
│       └── patterns/          # 思考パターン
├── 30_ARCHIVE/                # アーカイブ
├── 90_INSTRUCTIONS/           # SOPと手順書
├── _attachments/              # 添付ファイル（画像、PDF等）
├── _sandbox/                  # 実験・一時ファイル
└── _tools/                    # Vault管理ツール
    └── dataview_renderer/     # DataViewレンダラー
        ├── README.md
        └── dataview_renderer.js
```

### 3\. 初期ファイルの作成

#### a. AI起動ファイル

Vaultの直下に、使用するAIに応じた起動ファイル (`CLAUDE.md` または `GEMINI.md`) を作成します。これにより、AIは最初に何をすべきかを理解します。

**`CLAUDE.md` / `GEMINI.md`**:

```markdown
# Gestalt Framework AI

あなたはObsidian Vaultを管理・運用するための、私の思考パートナーとなるAIアシスタントです。
このVaultは、「問題解決型ゲシュタルトフレームワーク」という独自の思想に基づいて構築されています。

あなたの役割、システムの全体像、そして具体的なタスクの実行方法に関する全ての指示は、**`90_INSTRUCTIONS`**ディレクトリに集約されています。

**あなたの最初の行動として、必ず `90_INSTRUCTIONS/overview.md` を読み込み、このフレームワークの基本理念とあなたの行動原則を理解してください。**

全ての詳細な指示は、そこから参照される各SOP（標準作業手順書）に記載されています。

## 作業開始時の強制確認事項

⚠️ **重要：以下を実行せずに作業を開始することは禁止されています** ⚠️

タスクの指示を受けたら、必ず以下を実行してください：

1.  **関連するSOPファイルをすべて読み込む**
    - `task_mapping.md`で該当するSOPを確認
    - チェックリストがある場合は必ず確認
2.  **編集作業は3段階計画を作成し、ユーザーに提示**
    - 前計画（準備フェーズ）
    - 実行計画（作業フェーズ）
    - 後計画（還元フェーズ）
3.  **ユーザーの承認を得てから作業開始**

この手順を省略した場合、作業の質が著しく低下し、ルール違反となります。
```

#### b. INSTRUCTIONS (指示書)

このフレームワークの核となる各種SOP（標準作業手順書）を `90_INSTRUCTIONS/` ディレクトリに配置します。リポジトリ内のサンプルファイルを参考に、ご自身の運用に合わせてカスタマイズしてください。最低限、`overview.md`, `atomization.md`, `vault_structure.md` などを準備することが推奨されます。

### 4\. Dataviewレンダリングスクリプトの設定

CLIツールはObsidianのDataviewクエリを直接実行できないため、クエリ結果を静的なMarkdownとして書き出すスクリプトを設定します。

1.  **スクリプトの配置**:

      * リポジトリ内の `_tools/dataview_renderer/dataview_renderer.js` を、あなたのVaultの同じパスに配置します。

2.  **QuickAddの設定**:

    1.  Obsidianのコマンドパレット (`Cmd/Ctrl + P`) を開き、「QuickAdd: Configure」を選択します。
    2.  「Manage Macros」をクリックし、新しいマクロを作成します（例：`DataviewRenderer`）。
    3.  作成したマクロの「Configure」をクリックし、「User Scripts」から `_tools/dataview_renderer/dataview_renderer.js` を追加して設定を保存します。
    4.  QuickAddの設定画面に戻り、作成したマクロの右側にある稲妻マーク（⚡️）をONにして、コマンドパレットから呼び出せるようにします。

-----

## 基本的な使い方

このフレームワークは、以下の循環プロセスを辿ることで「生きた」ものとなります。

1.  **情報投入**: あらゆる未加工の情報（Webクリップ、メモ、PDFなど）を `00_RAW/` に保存します。
2.  **原子化 (Atomization)**: AIに「このファイルをAtom化して」と指示します。AIは `90_INSTRUCTIONS/atomization.md` に従って情報を分析し、再利用可能な最小単位の知識（Atom）として `20_VAULT/Atoms/` に保存します。
3.  **作業と統合 (Synthesis)**: 特定の課題（例：「新サービスの企画」）に取り組む際は `10_WORKSPACE/` で作業します。AIは `20_VAULT` 内の関連Atomを収集・統合し、`20_VAULT/Syntheses/` に新たな統合知識（レポートなど）を生成します。
4.  **知恵の還元 (Cognition)**: 作業を通じて得られた洞察や学び（例：「スピード重視の開発原則」）を `20_VAULT/Cognition/` に知恵として蓄積します。
5.  **改善**: `Cognition`に蓄積された知恵や、日々の運用で発見した問題点を元に `90_INSTRUCTIONS` のルールを改善し、フレームワーク自体を常に進化させます。

### Dataviewコンテンツのレンダリング

Knowledge Mapなど、Dataviewクエリを含むノートをCLIツールで扱えるようにするには、以下のコマンド（macOS/Linuxの場合）でレンダリングスクリプトを実行します。

```bash
# 例: Obsidian開発知識マップを静的Markdownに変換する
open "obsidian://advanced-uri?vault=Obsidian%20Workspace%20Vault&filepath=20_VAULT%2FSyntheses%2F_knowledge_maps%2Ftopic_maps%2FObsidian%E9%96%8B%E7%99%BA%E7%9F%A5%E8%AD%98%E3%83%9E%E3%83%83%E3%83%97.md&commandname=QuickAdd%3A%20DataviewRenderer"
```

  * 実行後、レンダリングされたファイルが `_sandbox/rendered_dataviews/` に出力されます。
  * `filepath` は対象のファイルパスに、`commandname` はQuickAddで設定したコマンド名に合わせてください。（パスやコマンド名はURLエンコードが必要です）

