# DataviewRenderer - Dataviewクエリの実行とエクスポート

## 概要

DataviewRendererは、Obsidianノート内のDataviewクエリを実行し、その結果を静的なMarkdownファイルとしてエクスポートするツールです。これにより、動的なDataviewクエリの結果を他のツールで利用したり、スナップショットとして保存することができます。

## 主な用途

- **Knowledge Mapsのレンダリング**: _knowledge_maps内の動的なビューを静的ファイルに変換
- **分析結果の保存**: Dataviewクエリの実行結果をスナップショットとして保存
- **外部ツールとの連携**: 動的クエリの結果を外部から参照可能な形式に変換

## 使用方法

### 1. QuickAddでの手動実行

1. コマンドパレット（Cmd/Ctrl + P）を開く
2. 「QuickAdd: DataviewRenderer」を選択
3. 現在開いているファイルのDataviewクエリが実行される

### 2. Advanced URIでの自動実行

Obsidian Advanced URIプラグインを使用して、外部からDataviewRendererを実行できます。

#### 基本構文

```
obsidian://advanced-uri?vault=<Vault名>&filepath=<ファイルパス>&commandname=QuickAdd%3A%20DataviewRenderer
```

#### パラメータ説明

- `vault`: Vaultの名前（スペースは%20でエンコード）
- `filepath`: 処理対象ファイルのパス（スペースやスラッシュはURLエンコード）
- `commandname`: `QuickAdd: DataviewRenderer`（コロンとスペースも%3A%20でエンコード）

#### 実例：Obsidian開発知識マップのレンダリング

```
obsidian://advanced-uri?vault=Obsidian%20Workspace%20Vault&filepath=20_VAULT%2FSyntheses%2F_knowledge_maps%2Ftopic_maps%2FObsidian%E9%96%8B%E7%99%BA%E7%9F%A5%E8%AD%98%E3%83%9E%E3%83%83%E3%83%97.md&commandname=QuickAdd%3A%20DataviewRenderer
```

### 3. コマンドラインからの実行（macOS/Linux）

```bash
open "obsidian://advanced-uri?vault=Obsidian%20Workspace%20Vault&filepath=<ファイルパス>&commandname=QuickAdd%3A%20DataviewRenderer"
```

## 出力先

レンダリングされたファイルは以下の場所に保存されます：

```
_sandbox/rendered_dataviews/<元のファイル名>_rendered.md
```

## 技術仕様

### スクリプト: dataview_renderer.js

このツールは以下の処理を行います：

1. 現在アクティブなファイルを取得
2. ファイル内のDataviewクエリブロックを検出
3. 各クエリを実行し、結果を取得
4. 結果を整形してMarkdownファイルとして出力
5. 画像などのリンクを適切に処理

### 対応するDataviewクエリタイプ

- **TABLE**: テーブル形式のクエリ
- **LIST**: リスト形式のクエリ
- **TASK**: タスク形式のクエリ
- **dataviewjs**: JavaScript形式のクエリ

## トラブルシューティング

### Advanced URIが動作しない場合

1. **Obsidianが起動していることを確認**
   - Advanced URIはObsidianが起動している必要があります

2. **Advanced URIプラグインが有効であることを確認**
   - 設定 → コミュニティプラグイン → Advanced URI が有効になっているか確認

3. **正しいパラメータを使用しているか確認**
   - `commandid`ではなく`commandname`を使用する
   - コマンド名の前に`QuickAdd: `（スペース含む）が必要

4. **URLエンコーディングを確認**
   - スペース → `%20`
   - スラッシュ → `%2F`
   - コロン → `%3A`
   - 日本語 → UTF-8エンコード

### レンダリング結果が空の場合

- 対象ファイルにDataviewクエリが含まれているか確認
- Dataviewプラグインが有効になっているか確認
- クエリの構文が正しいか確認

## 関連文書

- [[90_INSTRUCTIONS/knowledge_processing_guidelines|知識処理ガイドライン]]
- [[20_VAULT/Syntheses/_knowledge_maps/README|Knowledge Maps概要]]
- [[20_VAULT/Atoms/_toolsと_knowledge_mapsの責務分離に関する考察]]
