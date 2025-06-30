---
id: cognition_time_series_discussion_pattern_implementation
title: 時系列議論パターン - 実装ガイド
type: pattern_implementation
status: active
tags:
  - cognition
  - pattern
  - discussion
  - implementation
  - framework
created: 2025-06-19
updated: 2025-06-19
---

# 時系列議論パターン - 実装ガイド

## 概要

このガイドは、時系列議論パターンを実際のAtomに適用する際の具体的な手順とベストプラクティスを提供します。

## 実装手順

### ステップ1: 議論の開始を特定

議論の起点となるAtomを特定し、以下を設定：
```yaml
discussion_context:
  turn: 1
  role: "request"
  sender: "DuDo"
  receiver: "HBLAB"
  responds_to: null  # 最初のターンなのでnull
  previous_summary: null  # 最初のターンなのでnull
```

### ステップ2: 回答Atomの作成時

前のターンを参照して設定：
```yaml
discussion_context:
  turn: 2
  role: "response"
  sender: "HBLAB"
  receiver: "DuDo"
  responds_to: "id_20250401_resource_shortage_report"
  previous_summary: |
    DuDoから複数同時接続時のリソース不足問題が報告された。
    アバターの停止、音声の途切れ、ビデオ切断などの
    具体的な不具合と、その原因調査・対策の要請があった。
```

### ステップ3: 要約の書き方

要約は以下の要素を含めて300文字以内で：
1. **誰から誰への**コミュニケーションか
2. **主要な議題**は何か
3. **重要な決定や提案**があれば記載
4. **未解決の課題**があれば言及

例：
```yaml
previous_summary: |
  HBLABからReserved Instanceによるコスト削減案が
  提示されたが、DuDoは初期費用の高さと
  小規模ユーザーのニーズに対応できない点を指摘。
  テナント共有型での柔軟な運用を要望した。
```

### ステップ4: 既存Atomの更新

既存のAtomに`discussion_context`を追加する際：
1. 時系列を確認してターン番号を決定
2. 前後のAtomのIDを`related`フィールドと照合
3. 適切な要約を作成
4. `responded_by`フィールドも更新（後続の議論がある場合）

## ベストプラクティス

### 1. ターン番号の管理
- 同一スレッド内で連番を維持
- 分岐がある場合は`3a`, `3b`のようにサブ番号を使用
- フェーズをまたぐ場合も番号は継続

### 2. 役割（role）の使い分け
- **request**: 新たな要請、問題提起、提案依頼
- **response**: 要請への回答、技術的分析、提案
- **follow-up**: 追加質問、詳細確認、決定事項

### 3. 要約の品質
- 客観的な事実を中心に記載
- 感情的な表現は避ける
- 次の読者が文脈を理解できる最小限の情報

### 4. スレッド管理
```yaml
thread_info:
  thread_id: "infra_cost_optimization_2025"
  thread_title: "AI面接システムインフラコスト最適化"
  sub_threads:  # 分岐したサブスレッド
    - "multi_tenant_architecture"
    - "gpu_instance_optimization"
```

## 実装例

### 完全な実装例
```yaml
---
id: id_20250609_ai_interview_infra_cost_optimization_policy
title: AI面接インフラコスト最適化方針
# ... 他のメタデータ ...

discussion_context:
  turn: 6
  role: "follow-up"
  sender: "DuDo"
  receiver: "HBLAB"
  responds_to: "id_20250606_hblab_infra_review_initial_response"
  responded_by: ["id_20250617_dev_team_response_infra_cost_optimization"]
  previous_summary: |
    HBLABからARMインスタンス移行とReserved Instance
    契約の提案があった。GPU起動に5-15分要し、
    東京リージョンでの供給不足も課題として挙げられた。
    3年契約で$460/月まで削減可能との試算が示された。
  key_points:
    - テナント共有型での初期運用方針
    - スタンダード/プレミアムプランの導入
    - 深夜時間帯のインスタンス停止
    - 待機時間の許容とUX改善

thread_info:
  thread_id: "infra_optimization_phase45"
  thread_title: "フェーズ4.5インフラ抜本的見直し"
  phase: "Phase-4_5"
  started: "2025-06-03"
  main_participants: ["DuDo", "HBLAB"]
---
```

## チェックリスト

Atomに時系列議論パターンを適用する際の確認事項：

- [ ] ターン番号は正しい順序か
- [ ] roleは適切に設定されているか
- [ ] 送信者と受信者は正確か
- [ ] responds_toで前のターンを正しく参照しているか
- [ ] 要約は300文字以内で要点を押さえているか
- [ ] key_pointsで重要事項を箇条書きにしているか
- [ ] thread_infoでスレッドの文脈を提供しているか
- [ ] relatedフィールドとの整合性は取れているか

## トラブルシューティング

### 議論の順序が不明な場合
- context_dateを基準に時系列を再構築
- ファイル名や内容から前後関係を推測
- 不明な場合はnullを設定し、notesに記載

### 要約が300文字を超える場合
- 最も重要な決定事項に絞る
- 技術的詳細は省略し、結論を重視
- 必要なら2つの要約に分割（前半・後半）

### 複数の議論が並行している場合
- sub_thread_idを使って区別
- それぞれ独立したターン番号を管理
- 合流点では両方のスレッドを参照