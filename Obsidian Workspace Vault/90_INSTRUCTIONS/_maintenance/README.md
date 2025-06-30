# Vault メンテナンスツール

## 概要

`vault_health.py`は、Obsidian Vaultの健全性をチェックし、問題を修正するための統合ツールです。

## 使い方

```bash
# 全項目をチェック
python vault_health.py check

# 問題を自動修正（確認プロンプトあり）
python vault_health.py fix

# 詳細レポートを生成してファイルに保存
python vault_health.py report
```

## チェック項目

### Frontmatterチェック
- ✓ 全Atomファイルにidが存在するか
- ✓ 全Atomファイルにaliasesが存在するか
- ✓ aliasesにidが含まれているか

### リンクチェック
- ✓ 壊れたリンクの検出
- ✓ ID形式のリンクでaliasが設定されていないものの検出

## 自動修正機能

現在、以下の問題を自動修正できます：
- aliasesフィールドの追加（idから自動生成）

## レポート

`report`コマンドを実行すると、`reports/`ディレクトリに詳細なレポートが保存されます。

## 実行例

```bash
cd /Users/yuki/Workspace/obsidian/Obsidian Workspace Vault/90_INSTRUCTIONS/_maintenance
python vault_health.py check
```

出力例：
```
🔍 Vault健全性チェックを開始します...

📄 Frontmatterをチェック中...
🔗 リンクをチェック中...

# Vault健全性レポート

生成日時: 2025-06-18 12:00:00

## サマリー
- チェックしたファイル数: 16
- 発見された問題: 0

✅ 問題は見つかりませんでした！
```
