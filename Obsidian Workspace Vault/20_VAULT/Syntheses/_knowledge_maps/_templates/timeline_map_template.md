# [プロジェクト/トピック] タイムライン

<!--
📌 **非侵襲性の原則**: このマップは既存文書に変更を要求しません
- ファイルの作成日時・更新日時を活用
- ファイル名から日付情報を抽出（可能な場合）
- フォルダ構造から時系列を推測
-->

---
map_type: timeline
map_config:
  scope: "[時系列で追跡する対象の説明]"
  refresh_frequency: weekly
  primary_query: "時系列での知識の進化を追跡"
---

## 📅 概要

[このタイムラインマップの目的と見方を説明]

## 📈 時系列ビュー

### 月別アクティビティ
```dataview
TABLE WITHOUT ID
  dateformat(date(file.ctime), "yyyy-MM") as "年月",
  length(rows) as "作成数",
  length(filter(rows, (r) => r.file.mtime != r.file.ctime)) as "更新数"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
GROUP BY dateformat(date(file.ctime), "yyyy-MM")
SORT dateformat(date(file.ctime), "yyyy-MM") DESC
```

### 最近の活動（過去30日）
```dataview
TABLE 
  file.link as "文書",
  file.folder as "場所",
  dateformat(file.mtime, "MM-dd HH:mm") as "更新時刻",
  choice(file.mtime = file.ctime, "🆕 新規", "📝 更新") as "種別"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND file.mtime > date(today) - dur(30 days)
SORT file.mtime DESC
```

## 🎯 フェーズ別整理

### フォルダ構造による時期分類
```dataview
TABLE 
  file.link as "文書",
  file.ctime as "作成日",
  file.mtime as "最終更新"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND contains(file.folder, "[フェーズ識別子]")
SORT file.ctime ASC
```

## 📊 進化の分析

### 知識の成長曲線
```dataview
TABLE WITHOUT ID
  file.folder as "領域",
  min(rows.file.ctime) as "開始",
  max(rows.file.mtime) as "最終活動",
  length(rows) as "文書数",
  round((date(max(rows.file.mtime)) - date(min(rows.file.ctime))).days) as "活動日数"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
GROUP BY file.folder
SORT min(rows.file.ctime) ASC
```

### 重要な転換点
```dataview
LIST file.link
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND (contains(file.name, "変更") 
    OR contains(file.name, "移行")
    OR contains(file.name, "更新")
    OR contains(file.name, "v2")
    OR contains(file.name, "新"))
SORT file.ctime DESC
```

## 🔄 更新パターン

### 頻繁に更新される文書
```dataview
TABLE 
  file.link as "文書",
  file.ctime as "作成",
  file.mtime as "最終更新",
  round((date(file.mtime) - date(file.ctime)).days) as "経過日数"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND file.mtime != file.ctime
  AND (date(file.mtime) - date(file.ctime)).days > 7
SORT file.mtime DESC
LIMIT 15
```

## 📌 マイルストーン

### 主要な成果物
```dataview
LIST file.link + " (" + dateformat(file.ctime, "yyyy-MM-dd") + ")"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND (contains(file.name, "完了")
    OR contains(file.name, "成果")
    OR contains(file.name, "レポート")
    OR contains(file.name, "最終"))
SORT file.ctime DESC
```

## 📝 使用上の注意

- `[キーワード]`を実際のプロジェクト名やトピックに置換
- 日付範囲を調整したい場合は`dur()`関数の値を変更
- フェーズ識別子はプロジェクトに応じてカスタマイズ

---

*テンプレートバージョン: 1.0*  
*作成日: [YYYY-MM-DD]*