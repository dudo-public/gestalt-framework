# Obsidian Vaultのディレクトリ構造とパス仕様


!!!
もし初めてこのファイルを開いた場合は、ユーザーに
・作業ディレクトリ
・Obsidian Vaultパス
を問い合わせてください
!!!

## 基本パス情報
- **作業ディレクトリ**:  `...`
- **Vault本体**: `...`

## ツールごとのパス使用方法
- **mcp__obsidian__**: Vault内の相対パス（例: `90_INSTRUCTIONS/atomization.md`）

## 主要ディレクトリ構造
```
Obsidian Workspace Vault/
├── 00_RAW/                    # 未処理の生データ
│   ├── *.md                   # Markdownファイル
│   ├── *.pdf                  # PDFファイル
│   └── */                     # サブディレクトリ（HTML等）
│       ├── *.html
│       └── images/
├── 10_WORKSPACE/              # 作業中のファイル
│   └── */                     # プロジェクト別作業ディレクトリ
├── 20_VAULT/                  # Atom化された知識
│   ├── Atoms/                 # 最小単位の知識
│   ├── Syntheses/             # 統合された知識
│   │   ├── */                 # トピック別統合レポート
│   │   └── _knowledge_maps/   # 知識マップ管理
│   │       ├── README.md
│   │       ├── _templates/    # マップテンプレート
│   │       ├── knowledge_maturity_maps/
│   │       ├── pattern_maps/
│   │       ├── problem_solution_maps/
│   │       ├── relationship_maps/
│   │       ├── timeline_maps/
│   │       └── topic_maps/
│   └── Cognition/             # メタ認知・スキーマ
│       ├── _schema/           # スキーマ定義
│       │   ├── tags_glossary.md
│       │   └── terminology.md
│       └── patterns/          # 思考パターン
│           ├── hypothesis_validation_evolution/
│           └── time_series_discussion/
├── 30_ARCHIVE/                # アーカイブ
│   └── */                     # トピック別アーカイブ
├── 90_INSTRUCTIONS/           # SOPと手順書
│   ├── _maintenance/          # 保守管理
│   │   ├── README.md
│   │   ├── reports/           # 健全性レポート
│   │   └── vault_health.py   # 健全性チェックスクリプト
│   ├── atomization.md
│   ├── continuous_improvement_guidelines.md
│   ├── framework_evolution_log.md
│   ├── import_guidelines.md
│   ├── knowledge_processing_guidelines.md
│   ├── maintenance_guide.md
│   ├── overview.md
│   ├── pattern_application.md
│   ├── task_mapping.md
│   └── vault_structure.md     # このファイル
├── _attachments/              # 添付ファイル（画像、PDF等）
├── _evernote/                 # Evernoteからのインポート
├── _sandbox/                  # 実験・一時ファイル
└── _tools/                    # Vault管理ツール
    └── dataview_renderer/     # DataViewレンダラー
        ├── README.md
        └── dataview_renderer.js
```

## パスに関する注意事項
1. Obsidian MCPツールは自動的にVault内を参照するため、相対パスで十分
2. ファイルシステムツールを使う場合は必ずフルパスを指定
3. 日本語ファイル名も存在（例: `00_RAW/DUDO_会社設立_PR.md`）
4. HTMLファイルは通常、独自のディレクトリ内にimagesフォルダと共に配置

## 各ディレクトリの役割

### コンテンツディレクトリ
- **00_RAW**: 未処理の生データ。Atom化の対象
- **10_WORKSPACE**: 作業中のファイル。プロジェクト単位で整理
- **20_VAULT**: 構造化された知識の中核
  - **Atoms**: 最小単位の知識。一つのテーマ・概念・事実を表現
  - **Syntheses**: 複数のAtomから統合された知識
  - **Cognition**: メタ認知層。フレームワーク全体の思考パターンとスキーマ
- **30_ARCHIVE**: 過去バージョンや非アクティブな知識の保管

### システムディレクトリ
- **90_INSTRUCTIONS**: フレームワークの動作を定義するSOP群
  - **_maintenance**: Vault健全性管理ツールとレポート
- **_attachments**: 画像、PDF、その他メディアファイル
- **_evernote**: Evernoteからインポートしたコンテンツ
- **_sandbox**: 実験的なファイルや一時的な作業領域
- **_tools**: Vault管理・操作のための自動化ツール

### 特殊ディレクトリ
- **_knowledge_maps**: 知識の関係性を可視化するマップ群
  - 成熟度マップ、パターンマップ、問題解決マップなど
  - 知識の体系的な整理と発見を支援

## リンク戦略

### IDベースリンクシステム

このVaultでは、ファイル名とIDの両方でリンクできる柔軟なシステムを採用しています。

#### 基本原理
1. **すべてのAtomファイル**は以下を持つ：
   - 日本語のファイル名（例：`Obsidian使い方.md`）
   - frontmatterのidフィールド（例：`id: id_20250616_how_to_use_obsidian`）
   - aliasesフィールド（例：`aliases: [id_20250616_how_to_use_obsidian]`）

2. **これにより2つのリンク方式が使用可能**：
   - ファイル名リンク：`[[Obsidian使い方]]`
   - IDリンク：`[[id_20250616_how_to_use_obsidian]]`

#### 使い分けガイドライン

**ファイル名リンクを使う場合**：
- 日常的な文書作成
- 読みやすさを重視する場合
- 新規作成時のデフォルト

**IDリンクを使う場合**：
- 長期的な安定性が必要な場合
- ファイル名が変更される可能性がある場合
- 自動化スクリプトやテンプレート内
- 複数のAtomを系統的に参照する場合

#### リンクの例
```markdown
# ファイル名でのリンク（標準）
詳細は[[Obsidian使い方]]を参照してください。

# IDでのリンク（安定性重視）
[[id_20250617_how_to_use_obsidian]]

# IDリンクに表示名を付ける
[[id_20250617_how_to_use_obsidian|Obsidian使い方]]
```

#### 重要な注意事項
- **新規Atom作成時**：必ずaliasesフィールドを追加（atomization.md参照）
- **ファイル名変更時**：IDは変更しないこと
- **リンク切れ防止**：長期的な文書にはIDリンクを推奨
