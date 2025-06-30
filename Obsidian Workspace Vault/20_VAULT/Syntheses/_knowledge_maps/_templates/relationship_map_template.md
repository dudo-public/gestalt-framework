# [システム/プロジェクト] 関係性マップ

<!--
📌 **非侵襲性の原則**: このマップは既存文書に変更を要求しません
- file.outlinks と file.inlinks を活用してリンク関係を可視化
- フォルダ構造から階層関係を推測
- ファイル名のパターンから関連性を発見
-->

---
map_type: relationship
map_config:
  scope: "[関係性を分析する対象の説明]"
  refresh_frequency: weekly
  primary_query: "文書間の関連性とネットワークを可視化"
---

## 🔗 概要

[この関係性マップの目的と読み方を説明]

## 🌐 リンクネットワーク

### 最も参照されている文書（ハブ）
```dataview
TABLE 
  file.link as "文書",
  length(file.inlinks) as "被参照数",
  file.folder as "場所"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND length(file.inlinks) > 0
SORT length(file.inlinks) DESC
LIMIT 20
```

### 最も参照している文書（コネクター）
```dataview
TABLE 
  file.link as "文書",
  length(file.outlinks) as "参照数",
  file.folder as "場所"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND length(file.outlinks) > 0
SORT length(file.outlinks) DESC
LIMIT 20
```

## 🔄 相互参照

### 双方向リンクを持つ文書ペア
```dataview
TABLE WITHOUT ID
  file.link as "文書",
  filter(file.outlinks, (x) => contains(x.file.outlinks, this.file.link)) as "相互参照先"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND length(filter(file.outlinks, (x) => contains(x.file.outlinks, this.file.link))) > 0
```

## 📊 階層構造

### フォルダ間の関係
```dataview
TABLE WITHOUT ID
  key as "フォルダ",
  length(rows) as "文書数",
  length(flat(rows.file.outlinks)) as "外部参照数",
  length(flat(rows.file.inlinks)) as "被参照数"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
GROUP BY file.folder as key
SORT length(flat(rows.file.outlinks)) DESC
```

## 🎯 依存関係分析

### この文書に依存している文書
```dataview
LIST WITHOUT ID
  "→ " + link(file.path) + " (" + file.folder + ")"
FROM "20_VAULT"
WHERE contains(file.outlinks, this.file.link)
SORT file.name ASC
```

### この文書が依存している文書
```dataview
LIST WITHOUT ID
  "← " + link(outlink) + " (" + outlink.folder + ")"
FROM this.file.outlinks
WHERE contains(outlink.path, "20_VAULT")
SORT outlink.name ASC
```

## 🔍 クラスター分析

### 同じフォルダ内での関連性
```dataview
TABLE 
  file.link as "文書",
  length(filter(file.outlinks, (x) => x.folder = file.folder)) as "内部参照",
  length(filter(file.outlinks, (x) => x.folder != file.folder)) as "外部参照"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND length(file.outlinks) > 0
SORT length(file.outlinks) DESC
```

## 💫 孤立文書の発見

### リンクされていない文書
```dataview
LIST file.link
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND length(file.inlinks) = 0
  AND length(file.outlinks) = 0
SORT file.name ASC
```

## 🔗 名前パターンによる関連性

### 類似名を持つ文書グループ
```dataview
TABLE WITHOUT ID
  regexreplace(file.name, "_.*", "") as "パターン",
  map(rows.file, (f) => link(f.path, f.name)) as "文書"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
GROUP BY regexreplace(file.name, "_.*", "")
WHERE length(rows) > 1
```

## 📝 使用上の注意

- `[キーワード]`を実際の分析対象に置換
- 大規模なVaultでは`LIMIT`でパフォーマンスを調整
- 特定の関係性に注目する場合はクエリをカスタマイズ

---

*テンプレートバージョン: 1.0*  
*作成日: [YYYY-MM-DD]*