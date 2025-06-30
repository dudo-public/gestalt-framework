# [プロジェクト/領域] 問題解決マップ

<!--
📌 **非侵襲性の原則**: このマップは既存文書に変更を要求しません
- ファイル名から問題・解決策を識別
- 文書内容から課題関連キーワードを検索
- タグがあれば活用、なければパターンマッチング
-->

---
map_type: problem_solution
map_config:
  scope: "[問題と解決策を追跡する範囲の説明]"
  refresh_frequency: weekly
  primary_query: "問題と解決策のペアリングを体系化"
---

## 🎯 概要

[この問題解決マップの目的と活用方法を説明]

## 🚨 問題の識別

### 課題・問題として識別された文書
```dataview
TABLE 
  file.link as "文書",
  file.folder as "場所",
  file.mtime as "最終更新",
  tags as "タグ"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND (contains(file.name, "課題")
    OR contains(file.name, "問題")
    OR contains(file.name, "issue")
    OR contains(file.name, "エラー")
    OR contains(file.name, "不具合")
    OR contains(tags, "problem")
    OR contains(tags, "issue"))
SORT file.mtime DESC
```

### 最近報告された問題
```dataview
TABLE 
  file.link as "問題",
  file.ctime as "報告日",
  choice(contains(file.name, "解決"), "✅ 解決済", "⚠️ 未解決") as "状態"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND (contains(file.name, "問題") OR contains(file.name, "課題"))
  AND file.ctime > date(today) - dur(30 days)
SORT file.ctime DESC
```

## 💡 解決策の追跡

### 解決策・改善案として識別された文書
```dataview
TABLE 
  file.link as "文書",
  file.folder as "場所",
  file.mtime as "最終更新"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND (contains(file.name, "解決")
    OR contains(file.name, "改善")
    OR contains(file.name, "対策")
    OR contains(file.name, "solution")
    OR contains(file.name, "fix")
    OR contains(tags, "solution"))
SORT file.mtime DESC
```

## 🔗 問題と解決のマッチング

### 同じフォルダ内の問題-解決ペア
```dataview
TABLE WITHOUT ID
  file.folder as "場所",
  filter(rows.file, (f) => contains(f.name, "問題") OR contains(f.name, "課題")) as "問題",
  filter(rows.file, (f) => contains(f.name, "解決") OR contains(f.name, "対策")) as "解決策"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND (contains(file.name, "問題") 
    OR contains(file.name, "課題")
    OR contains(file.name, "解決")
    OR contains(file.name, "対策"))
GROUP BY file.folder
WHERE length(filter(rows.file, (f) => contains(f.name, "問題") OR contains(f.name, "課題"))) > 0
  AND length(filter(rows.file, (f) => contains(f.name, "解決") OR contains(f.name, "対策"))) > 0
```

## 📊 問題のカテゴリ分析

### フォルダ別の問題分布
```dataview
TABLE WITHOUT ID
  file.folder as "領域",
  length(filter(rows, (r) => contains(r.file.name, "問題") OR contains(r.file.name, "課題"))) as "問題数",
  length(filter(rows, (r) => contains(r.file.name, "解決") OR contains(r.file.name, "対策"))) as "解決数",
  round(100 * length(filter(rows, (r) => contains(r.file.name, "解決") OR contains(r.file.name, "対策"))) / max(length(filter(rows, (r) => contains(r.file.name, "問題") OR contains(r.file.name, "課題"))), 1)) as "解決率%"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
GROUP BY file.folder
WHERE length(filter(rows, (r) => contains(r.file.name, "問題") OR contains(r.file.name, "課題"))) > 0
SORT length(filter(rows, (r) => contains(r.file.name, "問題") OR contains(r.file.name, "課題"))) DESC
```

## 🔍 未解決問題の特定

### 解決策が見つかっていない可能性のある問題
```dataview
LIST file.link + " (作成: " + dateformat(file.ctime, "MM-dd") + ")"
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND (contains(file.name, "問題") OR contains(file.name, "課題"))
  AND !contains(file.name, "解決")
  AND !contains(file.name, "完了")
  AND length(filter(this.file.folder, (f) => 
    contains(f.name, "解決") AND 
    contains(f.name, replace(this.file.name, "問題", ""))
  )) = 0
SORT file.ctime DESC
```

## 📈 解決までの時間分析

### 問題報告から解決までの期間
```dataview
TABLE WITHOUT ID
  problem.file.link as "問題",
  solution.file.link as "解決策",
  round((date(solution.file.ctime) - date(problem.file.ctime)).days) as "解決日数"
FROM "20_VAULT" as problem
WHERE contains(problem.file.path, "[キーワード]")
  AND contains(problem.file.name, "問題")
FLATTEN filter("20_VAULT", (s) => 
  contains(s.file.name, "解決") AND 
  contains(s.file.name, replace(problem.file.name, "問題", ""))
) as solution
WHERE solution
SORT problem.file.ctime DESC
```

## 🏆 ベストプラクティス

### 効果的だった解決策
```dataview
LIST file.link
FROM "20_VAULT"
WHERE contains(file.path, "[キーワード]")
  AND (contains(file.name, "成功")
    OR contains(file.name, "効果")
    OR contains(file.name, "ベスト")
    OR contains(tags, "best-practice"))
SORT file.mtime DESC
```

## 📝 使用上の注意

- `[キーワード]`を実際のプロジェクト名や領域名に置換
- 組織固有の命名規則に合わせてパターンを調整
- 問題と解決策の命名規則を統一すると、より正確なマッチングが可能

---

*テンプレートバージョン: 1.0*  
*作成日: [YYYY-MM-DD]*