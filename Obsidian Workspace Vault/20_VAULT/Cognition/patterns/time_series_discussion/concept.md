---
id: cognition_time_series_discussion_pattern_concept
title: 時系列議論パターン - 概念定義
type: pattern_definition
status: active
tags:
  - cognition
  - pattern
  - discussion
  - time_series
  - framework
created: 2025-06-19
updated: 2025-06-19
---

# 時系列議論パターン - 概念定義

## 概要

ビジネスや技術開発において、ステークホルダー間の議論は「要請→回答→フォローアップ」というターン制で進行することが多い。特にインフラやアーキテクチャのような複雑な議題では、数か月にわたって議論が継続し、各ターンで新たな情報や制約が追加される。このパターンは、そうした時系列的な議論の流れをVault内で体系的に記録・追跡するためのフレームワークである。

## パターンの特徴

### 1. ターン制の議論構造
```
要請（DuDo） → 回答（HBLAB） → 追加質問（DuDo） → 詳細回答（HBLAB） → ...
```
- 明確な送信者と受信者
- 各ターンには役割（request/response/follow-up）
- 前後関係の明示的な記録

### 2. 要約による文脈保持
- 各Atomに前ターンの要約（300文字以内）を含める
- 長大な議論でも文脈を失わない
- 後から参照する際の理解を助ける

### 3. 非線形な進化
- 一つの要請から複数の回答が分岐
- 並行して異なるトピックが進行
- 時には過去の議論に立ち返る

## メタデータ構造

### discussion_context
```yaml
discussion_context:
  turn: 3                    # ターン番号（議論開始から数えて）
  role: "response"           # request/response/follow-up
  sender: "HBLAB"           # 送信者
  receiver: "DuDo"          # 受信者
  responds_to: "id_xxx"     # 前のターンのAtom ID
  responded_by: ["id_yyy"]  # このターンへの回答のAtom ID（複数可）
  previous_summary: |       # 前ターンの要約（300文字以内）
    DuDoから〇〇についての要請があり、
    特に△△の点が課題として挙げられた。
    コスト削減と品質維持のバランスが
    重要なポイントとして議論された。
  key_points:              # このターンの重要ポイント
    - Reserved Instance提案
    - 起動時間15分の制約
    - GPU供給不足の課題
```

### thread_info（スレッド情報）
```yaml
thread_info:
  thread_id: "infra_optimization_2025"  # 議論スレッドの識別子
  thread_title: "AI面接インフラ最適化議論"
  phase: "Phase-4_5"                    # 該当するフェーズ
  started: "2025-04-01"                 # スレッド開始日
  main_participants:                    # 主要参加者
    - "DuDo"
    - "HBLAB"
```

## 適用判断基準

このパターンを適用すべきケース：
1. 複数の組織間でのやり取りがある
2. 議論が複数ターンにわたって継続する
3. 時系列での意思決定の追跡が重要
4. 後から議論の経緯を理解する必要がある

## シンプルさの原則

このパターンは意図的にシンプルに設計されている：
- 複雑な状態管理は不要
- 前後1世代のみの参照で十分
- 要約は簡潔に要点のみ
- 過度な構造化を避ける

## 実例

### AI面接インフラ最適化議論の場合
1. **Turn 1**: リソース不足の報告（DuDo→HBLAB）
2. **Turn 2**: 技術的分析と対策案（HBLAB→DuDo）
3. **Turn 3**: マルチテナント構想提案（HBLAB→DuDo）
4. **Turn 4**: コスト最適化要請（DuDo→HBLAB）
5. **Turn 5**: Reserved Instance提案（HBLAB→DuDo）
6. **Turn 6**: 詳細運用方針（DuDo→HBLAB）

各ターンで前の議論を要約し、新たな情報や決定事項を追加していく。

## 期待される効果

1. **議論の可視化**: 長期にわたる議論の流れが一目瞭然
2. **意思決定の追跡**: なぜその決定に至ったかの文脈保持
3. **効率的な参照**: 要約により素早く過去の議論を理解
4. **知識の継承**: 新メンバーも議論の経緯を把握可能

## 他のパターンとの関係

- **仮説検証進化パターン**: 技術的な試行錯誤を記録
- **時系列議論パターン**: ビジネス的な合意形成を記録
- 両者は補完関係にあり、プロジェクトの技術面とビジネス面を包括的に記録