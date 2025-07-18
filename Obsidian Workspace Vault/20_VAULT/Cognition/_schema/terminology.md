---
id: cognition_terminology
title: プロジェクト用語集と命名規則
type: schema
status: active
tags:
  - cognition
  - terminology
  - schema
  - naming_convention
created: 2025-01-17
updated: 2025-01-17
---

# プロジェクト用語集と命名規則

## 概要

Obsidian Vault内で使用される固有名詞、プロジェクト名、技術用語などの正式な表記を定義します。また、Vault内の各要素の命名規則も規定します。文書作成時は必ずこのドキュメントを参照し、統一された表記と命名を使用してください。

## 命名規則

### 基本原則

このVaultでは、「誰が読むか」に基づいて言語を使い分けます：

#### 英語を使用（システム層）
開発者やAIが主に参照する技術的・システム的な要素

- **90_INSTRUCTIONS/** - 全てのSOP、ガイドライン
- **_で始まる要素** - _attachments、_schema等
- **メタデータフィールド** - id、type、status等
- **システムファイル名** - _で始まるファイル、設定ファイル等は英語
- **ツール類** - queries、templates、scripts等

#### 日本語を使用（知識層）
ユーザーが日常的に参照・理解する知識要素

- **Synthesesのディレクトリ名** - プロジェクト名（例：TTS開発、AI面接戦略）
- **Atomsのファイル名** - 内容を表す日本語名（例：音声認識API検証結果レポート.md）
- **ドキュメントのtitle** - 日本語の知識は日本語タイトル
- **見出し・本文** - 内容に応じて自然な日本語

### 具体例

```yaml
# ファイル名: 音声認識API検証結果レポート.md (日本語)
---
id: id_20250616_obsidian_report  # 英語（システム識別子）
title: Obsidianレポート  # 日本語
type: technical-report  # 英語
```

```
20_VAULT/
├── Syntheses/
│   └── Obsidian/             # 日本語（知識層）
│       └── 概要・使い方.md  # 日本語
└── Atoms/
    ├── Obsidianとは.md  # 日本語
    └── Obsidian使い方サマリー.md     # 日本語
```

### ファイル名の規則

1. **Atoms**：内容を表す簡潔な日本語名
   - 長すぎない（30文字程度まで）
   - 内容が一目で分かる
   - IDプレフィックスは不要（frontmatterのidで管理）

2. **Syntheses**：プロジェクト名や統合テーマ名
   - ディレクトリ名は日本語
   - ファイル名も日本語（概要.md、進捗.md等）

3. **システムファイル**：英語のまま
   - _で始まるファイル・ディレクトリ
   - INSTRUCTIONSディレクトリ内
   - 設定ファイル、スクリプト等

### 例外規則

1. **固有名詞** - 元の表記を維持（Obsidian, ClaudeCode等）
2. **技術用語** - 一般的な表記に従う（API, Fine-tuning等）
3. **ID** - 必ず英語（システム識別子のため）
4. **英語の方が自然な場合** - 日本語化すると不自然になる場合は英語のまま

### リンク方式

本Vaultでは、IDベースリンクシステムを採用しています：

1. **Atomファイルの必須要素**
   - 日本語ファイル名
   - frontmatterのid（英語）
   - aliases配列にidを含める

2. **2つのリンク方式**
   - `[[ファイル名]]` - 日常的な使用
   - `[[id_YYYYMMDD_xxx]]` - 長期安定性が必要な場合

3. **詳細は** `90_INSTRUCTIONS/vault_structure.md` の「リンク戦略」セクションを参照

### 用語集

*この用語集は、プロジェクトの進展に応じて継続的に更新されます。*
