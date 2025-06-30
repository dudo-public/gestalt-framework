# [領域/プロジェクト] 知識成熟度マップ

<!--
📌 **非侵襲性の原則**: このマップは既存文書に変更を要求しません
- 更新頻度から知識の活性度を判断
- ファイル名パターンから成熟度を推測
- フォルダ構造から知識の階層を理解
-->

---
map_type: knowledge_maturity
map_config:
  scope: "[知識の成熟度を評価する範囲の説明]"
  refresh_frequency: monthly
  primary_query: "知識の信頼性と完成度を評価"
---

## 📊 概要

[この成熟度マップの目的と評価基準を説明]

## 🌱 知識の成長段階

### アイデア・初期段階の文書
```dataview
TABLE 
  file.link as "文書",
  file.ctime as "作成日",
  file.size as "サイズ",
  choice(file.size < 1000, "🌱 萌芽", "🌿 成長中") as "段階"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND (contains(file.name, "アイデア")
    OR contains(file.name, "案")
    OR contains(file.name, "draft")
    OR contains(file.name, "検討")
    OR contains(file.name, "仮"))
SORT file.ctime DESC
```

### 検証・実験段階の文書
```dataview
TABLE 
  file.link as "文書",
  file.mtime as "最終更新",
  round((date(file.mtime) - date(file.ctime)).days) as "経過日数"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND (contains(file.name, "検証")
    OR contains(file.name, "実験")
    OR contains(file.name, "テスト")
    OR contains(file.name, "試")
    OR contains(tags, "experimental"))
SORT file.mtime DESC
```

### 確立された知識
```dataview
TABLE 
  file.link as "文書",
  file.ctime as "作成日",
  file.size as "サイズ",
  length(file.inlinks) as "参照数"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND (contains(file.name, "完成")
    OR contains(file.name, "最終")
    OR contains(file.name, "確定")
    OR contains(file.name, "ガイド")
    OR contains(file.name, "マニュアル"))
SORT length(file.inlinks) DESC
```

## 📈 活性度分析

### 最近1ヶ月の更新頻度
```dataview
TABLE WITHOUT ID
  file.folder as "領域",
  length(filter(rows, (r) => r.file.mtime > date(today) - dur(30 days))) as "更新数",
  length(rows) as "総文書数",
  round(100 * length(filter(rows, (r) => r.file.mtime > date(today) - dur(30 days))) / length(rows)) as "活性度%"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
GROUP BY file.folder
SORT length(filter(rows, (r) => r.file.mtime > date(today) - dur(30 days))) DESC
```

## 🔍 知識の深さ分析

### 文書サイズによる成熟度評価
```dataview
TABLE WITHOUT ID
  choice(file.size < 500, "🌱 種子", 
    choice(file.size < 2000, "🌿 成長期",
      choice(file.size < 5000, "🌳 成熟期", "🌲 完成期"))) as "成熟度",
  length(rows) as "文書数",
  round(sum(rows.file.size) / 1000) as "合計KB",
  round(sum(rows.file.size) / length(rows) / 1000) as "平均KB"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
GROUP BY choice(file.size < 500, "🌱 種子", 
    choice(file.size < 2000, "🌿 成長期",
      choice(file.size < 5000, "🌳 成熟期", "🌲 完成期")))
```

## 🎯 信頼性指標

### 高信頼性文書（多く参照されている）
```dataview
TABLE 
  file.link as "文書",
  length(file.inlinks) as "被参照数",
  file.size as "サイズ",
  dateformat(file.mtime, "yyyy-MM") as "最終更新"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND length(file.inlinks) >= 3
SORT length(file.inlinks) DESC
LIMIT 20
```

### 要レビュー文書（長期間更新なし）
```dataview
TABLE 
  file.link as "文書",
  file.mtime as "最終更新",
  round((date(today) - date(file.mtime)).days) as "未更新日数"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND file.mtime < date(today) - dur(180 days)
  AND !contains(file.name, "アーカイブ")
  AND !contains(file.name, "完了")
SORT file.mtime ASC
LIMIT 20
```

## 📊 知識ポートフォリオ

### フォルダ別の知識成熟度分布
```dataview
TABLE WITHOUT ID
  file.folder as "領域",
  length(filter(rows, (r) => r.file.size < 1000)) as "初期",
  length(filter(rows, (r) => r.file.size >= 1000 AND r.file.size < 3000)) as "発展",
  length(filter(rows, (r) => r.file.size >= 3000)) as "成熟",
  length(rows) as "合計"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
GROUP BY file.folder
```

## 🚀 改善の機会

### 拡張が必要な可能性のある文書
```dataview
LIST file.link + " (サイズ: " + file.size + " bytes)"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND file.size < 500
  AND length(file.inlinks) > 0
  AND file.ctime < date(today) - dur(30 days)
SORT length(file.inlinks) DESC
```

## 📝 使用上の注意

- `[キーワード]`を実際の評価対象に置換
- 組織の知識成熟度基準に合わせてしきい値を調整
- ファイルサイズは成熟度の一指標であり、質とは必ずしも相関しない

---

*テンプレートバージョン: 1.0*  
*作成日: [YYYY-MM-DD]*