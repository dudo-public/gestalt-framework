# [トピック名] 知識マップ

<!--
📌 **非侵襲性の原則**: このマップは既存文書に変更を要求しません
- 既存のメタデータをそのまま活用
- メタデータがなくてもファイル名やフォルダから情報取得
- 新しいメタデータが追加されれば自動的に活用
-->

---
map_type: topic
map_config:
  scope: "[このマップがカバーする範囲の説明]"
  refresh_frequency: on_demand
  primary_query: "メインクエリの説明"
---

## 📊 概要

[このトピックマップの目的と活用方法を簡潔に説明]

## 🔍 全体像

### 関連文書の分布
```dataview
TABLE WITHOUT ID
  file.folder as "場所",
  length(rows) as "文書数",
  min(rows.file.ctime) as "最初の文書",
  max(rows.file.mtime) as "最終更新"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]") 
   OR contains(file.name, "[キーワード]")
   OR contains(tags, "[タグ名]")
GROUP BY file.folder
```

## 📚 文書一覧

### 最近更新された文書
```dataview
TABLE 
  file.link as "文書",
  file.folder as "場所",
  tags as "タグ",
  file.mtime as "更新日"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]") 
   OR contains(file.name, "[キーワード]")
   OR contains(tags, "[タグ名]")
SORT file.mtime DESC
LIMIT 20
```

### カテゴリ別文書
```dataview
TABLE 
  file.link as "文書",
  file.size as "サイズ",
  file.ctime as "作成日"
FROM "20_VAULT/Atoms"
WHERE contains(file.path, "[キーワード]")
SORT file.name ASC
```

## 🔗 関連性分析

### このトピックに言及している文書
```dataview
LIST
FROM "20_VAULT"
WHERE contains(file.content, "[キーワード]")
  AND !contains(file.path, "[キーワード]")
SORT file.mtime DESC
LIMIT 10
```

## 💡 洞察と発見

### 更新頻度の高い領域
```dataview
TABLE WITHOUT ID
  file.folder as "領域",
  length(rows) as "文書数",
  max(rows.file.mtime) as "最終更新",
  min(rows.file.mtime) as "最古更新"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
GROUP BY file.folder
SORT max(rows.file.mtime) DESC
```

## 📝 使用上の注意

- クエリ内の`[キーワード]`や`[タグ名]`を実際の値に置き換えてください
- パフォーマンスに問題がある場合は、`LIMIT`を追加してください
- 新しい視点が必要な場合は、クエリを自由にカスタマイズしてください

---

*テンプレートバージョン: 1.0*  
*作成日: [YYYY-MM-DD]*