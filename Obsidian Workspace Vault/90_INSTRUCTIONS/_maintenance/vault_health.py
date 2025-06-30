#!/usr/bin/env python3
"""
Obsidian Vault健全性チェック・修正ツール

Usage:
    python vault_health.py check     # 全項目をチェック
    python vault_health.py fix       # 問題を自動修正（確認あり）
    python vault_health.py report    # 詳細レポート生成
"""

import os
import sys
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any


class VaultHealth:
    def __init__(self, vault_path: str = None):
        """Vault健全性チェッカーの初期化"""
        if vault_path is None:
            # デフォルトパス
            vault_path = "/Users/yuki/Workspace/obsidian/Obsidian Workspace Vault"
        
        self.vault_path = Path(vault_path)
        self.atoms_path = self.vault_path / "20_VAULT" / "Atoms"
        self.results = {
            'checked_files': 0,
            'issues': [],
            'fixed': []
        }
    
    def extract_frontmatter(self, file_path: Path) -> Dict[str, Any]:
        """ファイルからfrontmatterを抽出"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # frontmatterの抽出
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if not match:
                return {}
            
            # 簡易的なYAML解析（完全ではないが基本的な用途には十分）
            frontmatter = {}
            for line in match.group(1).split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # リスト形式の処理
                    if key == 'aliases' and value.startswith('['):
                        # aliasesの値を抽出
                        aliases_match = re.search(r'\[(.*?)\]', value)
                        if aliases_match:
                            frontmatter[key] = [aliases_match.group(1).strip()]
                    else:
                        frontmatter[key] = value
            
            return frontmatter
            
        except Exception as e:
            return {'error': str(e)}
    
    def check_frontmatter(self) -> Dict[str, List[str]]:
        """全AtomファイルのFrontmatterをチェック"""
        issues = {
            'missing_id': [],
            'missing_aliases': [],
            'mismatched_aliases': [],
            'errors': []
        }
        
        for md_file in self.atoms_path.glob("*.md"):
            self.results['checked_files'] += 1
            
            frontmatter = self.extract_frontmatter(md_file)
            
            if 'error' in frontmatter:
                issues['errors'].append(f"{md_file.name}: {frontmatter['error']}")
                continue
            
            # IDチェック
            if 'id' not in frontmatter:
                issues['missing_id'].append(md_file.name)
            
            # aliasesチェック
            if 'aliases' not in frontmatter:
                issues['missing_aliases'].append(md_file.name)
            elif 'id' in frontmatter:
                # IDとaliasesの一致チェック
                expected_alias = frontmatter['id']
                if expected_alias not in frontmatter.get('aliases', []):
                    issues['mismatched_aliases'].append(
                        f"{md_file.name}: id={frontmatter['id']}, aliases={frontmatter.get('aliases', [])}"
                    )
        
        return issues
    
    def check_links(self) -> Dict[str, List[str]]:
        """リンクの健全性をチェック"""
        issues = {
            'broken_links': [],
            'id_links_without_alias': []
        }
        
        # 既存ファイルのセットを作成
        all_files = set(f.stem for f in self.atoms_path.glob("*.md"))
        
        # _attachmentsフォルダ内のファイルも収集
        attachments_path = self.vault_path / "_attachments"
        all_attachments = set()
        if attachments_path.exists():
            all_attachments = set(f.stem for f in attachments_path.glob("*"))
        
        # aliasesを収集
        all_aliases = set()
        for md_file in self.atoms_path.glob("*.md"):
            frontmatter = self.extract_frontmatter(md_file)
            if 'aliases' in frontmatter:
                all_aliases.update(frontmatter['aliases'])
        
        # リンクをチェック
        for md_file in self.atoms_path.glob("*.md"):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # [[xxx]]形式のリンクを抽出（画像リンク![[xxx]]も含む）
            links = re.findall(r'!?\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
            
            for link in links:
                # 画像・添付ファイルのリンクをスキップ（.png, .jpg, .jpeg, .gif, .pdf等）
                if any(link.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.pdf', '.mp4', '.webm']):
                    # 拡張子を除いたファイル名で確認
                    file_stem = link.rsplit('.', 1)[0]
                    if file_stem in all_attachments:
                        continue  # 存在するのでスキップ
                
                # ファイル名でもaliasでも添付ファイルでもない場合は壊れたリンク
                if link not in all_files and link not in all_aliases and link not in all_attachments:
                    # _attachmentsパスが含まれている場合は除外
                    if '_attachments/' not in link:
                        issues['broken_links'].append(f"{md_file.name}: [[{link}]]")
                
                # ID形式のリンクでaliasがない場合
                if link.startswith('id_') and link not in all_aliases:
                    issues['id_links_without_alias'].append(f"{md_file.name}: [[{link}]]")
        
        return issues
    
    def check_all(self) -> Dict[str, Any]:
        """全ての健全性チェックを実行"""
        print("🔍 Vault健全性チェックを開始します...\n")
        
        # Frontmatterチェック
        print("📄 Frontmatterをチェック中...")
        frontmatter_issues = self.check_frontmatter()
        
        # リンクチェック
        print("🔗 リンクをチェック中...")
        link_issues = self.check_links()
        
        # 結果をまとめる
        all_issues = {}
        all_issues.update({f"frontmatter_{k}": v for k, v in frontmatter_issues.items() if v})
        all_issues.update({f"link_{k}": v for k, v in link_issues.items() if v})
        
        self.results['issues'] = all_issues
        self.results['timestamp'] = datetime.now().isoformat()
        
        return self.results
    
    def fix_aliases(self) -> None:
        """aliasesの問題を修正"""
        print("\n🔧 aliasesの修正を開始します...")
        
        fixed_count = 0
        
        for md_file in self.atoms_path.glob("*.md"):
            frontmatter = self.extract_frontmatter(md_file)
            
            if 'error' in frontmatter or 'id' not in frontmatter:
                continue
            
            file_id = frontmatter['id']
            needs_fix = False
            
            # aliasesが存在しない、またはIDが含まれていない場合
            if 'aliases' not in frontmatter or file_id not in frontmatter.get('aliases', []):
                needs_fix = True
            
            if needs_fix:
                print(f"  修正: {md_file.name}")
                
                # ファイル内容を読み込む
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # aliasesを追加または更新
                if 'aliases' not in frontmatter:
                    # tagsの後に挿入
                    content = re.sub(
                        r'(tags:.*?\n)',
                        f'\\1aliases: [{file_id}]\n',
                        content,
                        flags=re.DOTALL
                    )
                else:
                    # 既存のaliasesを更新（簡易的な実装）
                    print(f"    既存のaliasesの更新は手動で行ってください: {md_file.name}")
                    continue
                
                # ファイルを書き戻す
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                fixed_count += 1
                self.results['fixed'].append(md_file.name)
        
        print(f"\n✅ {fixed_count}個のファイルを修正しました")
    
    def generate_report(self) -> str:
        """詳細レポートを生成"""
        report = f"""# Vault健全性レポート

生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## サマリー
- チェックしたファイル数: {self.results['checked_files']}
- 発見された問題: {sum(len(v) for v in self.results['issues'].values())}

## 詳細
"""
        
        if not self.results['issues']:
            report += "\n✅ 問題は見つかりませんでした！\n"
        else:
            for issue_type, items in self.results['issues'].items():
                if items:
                    report += f"\n### {issue_type.replace('_', ' ').title()}\n"
                    for item in items:
                        report += f"- {item}\n"
        
        if self.results['fixed']:
            report += f"\n## 修正済みファイル\n"
            for item in self.results['fixed']:
                report += f"- {item}\n"
        
        return report
    
    def run(self, command: str) -> None:
        """コマンドに応じた処理を実行"""
        if command == 'check':
            self.check_all()
            print(self.generate_report())
            
        elif command == 'fix':
            self.check_all()
            
            # 問題がある場合のみ修正を提案
            if self.results['issues']:
                print(self.generate_report())
                response = input("\n修正を実行しますか？ (y/N): ")
                if response.lower() == 'y':
                    self.fix_aliases()
            else:
                print("\n✅ 修正が必要な問題はありません")
                
        elif command == 'report':
            self.check_all()
            # reportディレクトリを作成
            report_dir = Path(__file__).parent / "reports"
            report_dir.mkdir(exist_ok=True)
            
            # レポートファイルを保存
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = report_dir / f"health_report_{timestamp}.md"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(self.generate_report())
            
            print(f"📄 レポートを保存しました: {report_file}")
            
        else:
            print("❌ 不明なコマンドです。check, fix, report のいずれかを指定してください。")


def main():
    """メイン処理"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    vault_health = VaultHealth()
    vault_health.run(command)


if __name__ == "__main__":
    main()