---
id: cognition_hypothesis_validation_evolution_implementation
title: 仮説検証進化パターン - 実装ガイド
type: pattern_implementation
status: active
tags:
  - cognition
  - pattern
  - implementation
  - hypothesis_validation
created: 2025-06-17
updated: 2025-06-17
---

# 仮説検証進化パターン - 実装ガイド

## 概要

このガイドは、仮説検証進化パターンをObsidian Vault内で実装するための具体的な手順を提供します。

## 実装ステップ

### 1. パターン適用の判断

#### 確認すべきポイント
- RAWファイルが提案、検証結果、改善案のいずれかに該当するか
- 既存の仮説検証サイクルの一部である可能性があるか
- 複数の改善アプローチが考えられる内容か

#### ユーザーへの確認例
```
このファイルは以下のいずれかに該当しますか？

1. 新しい提案・仮説
2. 既存提案の検証結果・フィードバック
3. 検証結果を受けた改善案

既存の何かに関連する場合は、その文書名やIDをお教えください。
```

### 2. ノートタイプの決定

#### hypothesis（仮説）の特徴
- 「〜を提案する」「〜というアプローチを試す」
- 期待される成果や目標が明記されている
- 実装計画やガイドラインが含まれる

#### validation（検証）の特徴
- 「〜を試した結果」「〜の評価」
- メリット・デメリットの分析
- 期待との差異や発見された問題

#### insight（洞察）の特徴
- 検証から得られた一般的な原則
- 他のプロジェクトにも適用可能な教訓
- パターンや傾向の発見

### 3. メタデータの設定

#### 基本構造
```yaml
---
id: id_YYYYMMDD_descriptive_name
title: タイトル
type: hypothesis | validation | insight
status: active
tags: [関連タグ]
source: 元のRAWファイルパス
related: [関連Atom]
created: YYYY-MM-DD
updated: YYYY-MM-DD
evolution_context:
  cycle: N
  role: "hypothesis|validation|insight"
  validates: "id_xxx"  # validationの場合
  validated_by: "id_xxx"  # hypothesisの場合
  leads_to: ["id_xxx"]  # 次の仮説へのリンク
  note: "この文書の文脈説明"
lineage:
  root_problem: "解決したい根本的な問題"
  branch: "アプローチの系統名"
  generation: N
  parent: "id_parent"
  siblings: ["id_sibling"]
---
```

### 4. 内容の構造化

#### 仮説（hypothesis）の構造
```markdown
# タイトル

## 概要
提案の要点を簡潔に説明

## 背景
なぜこの提案をするのか、解決したい問題は何か

## 提案内容
具体的なアプローチや実装計画

## 期待される成果
この提案が成功した場合の効果

## リスクと課題
予想される困難や注意点

## 実装計画
具体的なステップや必要なリソース
```

#### 検証（validation）の構造
```markdown
# タイトル

## 概要
検証の要点と結論

## 検証対象
何を検証したか（仮説へのリンク）

## 検証方法
どのように検証を実施したか

## 結果
### 成功した点
- 期待通りだった部分

### 課題・問題点
- 発見された問題
- 予想外の結果

## 分析
結果の原因分析

## 次のステップ
この結果を受けた改善案や代替案
```

#### 洞察（insight）の構造
```markdown
# タイトル

## 概要
得られた洞察の要点

## 元となった検証
どの検証から得られた洞察か

## 発見された原則
一般化可能な知見

## 適用可能な領域
この洞察が活用できる他の分野

## 注意事項
この原則の限界や適用条件
```

### 5. 関連付けの実施

#### 前後関係の明確化
1. **親子関係**: parentフィールドで親文書を指定
2. **検証関係**: validates/validated_byで相互参照
3. **発展関係**: leads_toで次の仮説を指定

#### 系統管理
- 同じroot_problemを持つ文書は同一プロジェクト
- branchで異なるアプローチを区別
- generationで進化の世代を追跡

### 6. 検索性の確保

#### タグの付与
- プロジェクト固有のタグ
- 技術分野のタグ
- フェーズを示すタグ（hypothesis, validation等）

#### クエリ対応
Dataviewクエリで追跡できるよう、メタデータを正確に設定

## チェックリスト

- [ ] パターン適用の妥当性を確認
- [ ] ノートタイプを正しく判定
- [ ] evolution_contextを完全に記入
- [ ] lineage情報を適切に設定
- [ ] 関連文書との相互リンクを設定
- [ ] 内容を推奨構造に従って整理
- [ ] タグを適切に付与

## トラブルシューティング

### Q: 既存の系統に属するか判断できない
A: ユーザーに確認を求め、不明な場合は新規系統として開始

### Q: 複数のノートタイプに該当しそう
A: 主要な役割で判断。検証結果に洞察が含まれる場合は、別々のAtomに分割も検討

### Q: サイクル番号が不明
A: 親文書のcycle + 1。新規の場合は1から開始