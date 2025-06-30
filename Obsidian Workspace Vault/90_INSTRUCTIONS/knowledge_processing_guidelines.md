# 知識処理ガイドライン - Dataviewクエリの取り扱い

## 概要

このガイドラインは、ゲシュタルトフレームワーク内でDataviewクエリを含む知識資産を適切に処理するための標準手順を定めています。特に、_knowledge_mapsなどの動的ビューを含むファイルを参照する際の必須プロセスを規定します。

## 原則

### 1. レンダリングファースト原則
Dataviewクエリを含むファイルは、**必ずレンダリング（静的化）してから参照する**ことを原則とします。これにより：
- 時点での正確な情報を保証
- 外部ツールからの参照を可能に
- 処理の再現性を確保

### 2. 一元管理原則
レンダリング結果は`_sandbox/rendered_dataviews/`に一元管理し、散在を防ぎます。

### 3. 自動化推奨原則
可能な限りAdvanced URIを使用した自動化を推奨し、手動作業を最小化します。

## 処理フロー

### ステップ1: Dataviewクエリの識別

以下のパターンを含むファイルはレンダリングが必要です：
- ` ```dataview` ブロック
- ` ```dataviewjs` ブロック
- インラインクエリ: `$=` または `dv()`

### ステップ2: レンダリング実行

#### 方法A: QuickAdd経由（手動）
1. 対象ファイルを開く
2. コマンドパレット → `QuickAdd: DataviewRenderer`
3. `_sandbox/rendered_dataviews/`に結果が出力される

#### 方法B: Advanced URI経由（推奨）
```bash
open "obsidian://advanced-uri?vault=Obsidian%20Workspace%20Vault&filepath=<ファイルパス>&commandname=QuickAdd%3A%20DataviewRenderer"
```

### ステップ3: レンダリング結果の参照

レンダリングされたファイルは以下の命名規則で保存されます：
```
_sandbox/rendered_dataviews/<元のファイル名>_rendered.md
```

## 具体的な適用場面

### 1. Knowledge Maps参照時
```yaml
対象: 20_VAULT/Syntheses/_knowledge_maps/**/*.md
理由: 動的なクエリ結果を静的に保存する必要がある
頻度: 参照の都度
```

### 2. 統合文書の作成時
```yaml
対象: Dataviewクエリを含むSyntheses層のファイル
理由: 時点での正確な情報を文書に含める
頻度: 統合文書作成時
```

### 3. 外部ツールとの連携時
```yaml
対象: 外部から参照されるすべてのDataviewクエリ
理由: 外部ツールはDataviewを実行できない
頻度: 連携実行時
```

## チェックリスト

### レンダリング前チェック
- [ ] 対象ファイルにDataviewクエリが含まれているか確認
- [ ] Dataviewプラグインが有効になっているか確認
- [ ] QuickAdd: DataviewRendererが設定されているか確認

### レンダリング後チェック
- [ ] `_sandbox/rendered_dataviews/`に出力ファイルが生成されたか
- [ ] レンダリング結果に期待されるデータが含まれているか
- [ ] 画像リンクなどが適切に処理されているか

## トラブルシューティング

### 問題: レンダリング結果が空
**原因と対策:**
1. クエリ構文エラー → Dataviewクエリを修正
2. 対象データなし → クエリ条件を確認
3. プラグイン無効 → Dataviewプラグインを有効化

### 問題: Advanced URIが動作しない
**原因と対策:**
1. Obsidian未起動 → Obsidianを起動
2. URIエンコーディング誤り → エンコーディングを確認
3. コマンド名の誤り → `QuickAdd: DataviewRenderer`を正確に指定

## ベストプラクティス

### 1. バッチ処理の活用
複数のKnowledge Mapsを一度にレンダリングする場合：
```bash
# 将来的な拡張例
for file in $(find . -name "*知識マップ.md"); do
  open "obsidian://advanced-uri?vault=..."
  sleep 2
done
```

### 2. 定期的なレンダリング
重要なKnowledge Mapsは定期的にレンダリングし、変化を追跡：
- 週次レポート用
- 月次アーカイブ用
- プロジェクト完了時

### 3. レンダリング結果の活用
- Git管理でバージョン管理
- 差分検出で変化を可視化
- 静的サイトジェネレータとの連携

## 関連文書

- [[_tools/dataview_renderer/README|DataviewRenderer詳細]]
- [[20_VAULT/Syntheses/_knowledge_maps/README|Knowledge Maps概要]]
- [[90_INSTRUCTIONS/task_mapping|タスクマッピング]]

## 今後の拡張

1. **自動レンダリング機能**
   - ファイル保存時の自動実行
   - スケジュールベースの実行

2. **差分管理機能**
   - 前回レンダリングとの比較
   - 変更箇所のハイライト

3. **統合機能**
   - 他のツールとの連携強化
   - APIエンドポイントの提供

---

*このガイドラインは、フレームワークの進化に応じて更新されます。*