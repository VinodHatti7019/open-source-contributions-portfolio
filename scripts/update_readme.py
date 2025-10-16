#!/usr/bin/env python3
"""
Update README Script

This script updates the README.md file with generated statistics and contribution data.
It replaces content between AUTO-GENERATED markers with fresh data.

Author: Auto-generated for Open Source Contributions Portfolio
Date: 2025
"""

import os
import json
import sys
import re
from datetime import datetime
from typing import Dict, List, Any


class ReadmeUpdater:
    """Updates README.md with contribution data"""
    
    def __init__(self,
                 contributions_file: str = 'data/contributions.json',
                 stats_file: str = 'data/statistics.json',
                 readme_file: str = 'README.md'):
        self.contributions_file = contributions_file
        self.stats_file = stats_file
        self.readme_file = readme_file
        self.contributions = self.load_json(contributions_file)
        self.stats = self.load_json(stats_file)
        self.readme_content = self.load_readme()
    
    def load_json(self, filepath: str) -> Dict[str, Any]:
        """Load JSON data from file"""
        if not os.path.exists(filepath):
            print(f"Warning: {filepath} not found, using empty data")
            return {}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_readme(self) -> str:
        """Load README.md content"""
        if not os.path.exists(self.readme_file):
            print(f"Error: {self.readme_file} not found")
            sys.exit(1)
        
        with open(self.readme_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def save_readme(self):
        """Save updated README.md"""
        with open(self.readme_file, 'w', encoding='utf-8') as f:
            f.write(self.readme_content)
        print(f"  README.md updated successfully")
    
    def update_section(self, start_marker: str, end_marker: str, new_content: str):
        """Update a section between markers in README"""
        pattern = f"({re.escape(start_marker)}).*?({re.escape(end_marker)})"
        replacement = f"\\1\n{new_content}\n\\2"
        self.readme_content = re.sub(pattern, replacement, self.readme_content, flags=re.DOTALL)
    
    def generate_stats_table(self) -> str:
        """Generate overall statistics table"""
        overall = self.stats.get('overall', {})
        last_updated = datetime.utcnow().strftime('%Y-%m-%d')
        
        table = f"""### Overall Metrics

| Metric | Count | Last Updated |
|--------|-------|-------------|
| Total Commits | `{overall.get('total_commits', 0)}` | `{last_updated}` |
| Pull Requests | `{overall.get('total_prs', 0)}` | `{last_updated}` |
| Issues Opened | `{overall.get('total_issues', 0)}` | `{last_updated}` |
| Repositories Contributed | `{overall.get('total_repositories', 0)}` | `{last_updated}` |
| Active Forks | `{overall.get('forked_repos', 0)}` | `{last_updated}` |
| Own Repositories | `{overall.get('own_repos', 0)}` | `{last_updated}` |

### Contribution Streak

🔥 **Current Streak**: `{self.stats.get('streaks', {}).get('current_streak', 0)} days`  
⭐ **Longest Streak**: `{self.stats.get('streaks', {}).get('longest_streak', 0)} days`  
📅 **Last Contribution**: `{self.stats.get('streaks', {}).get('last_contribution', 'N/A')}`"""
        
        return table
    
    def generate_contributions_table(self) -> str:
        """Generate recent contributions table"""
        commits = self.contributions.get('commits', [])[:10]
        prs = self.contributions.get('pull_requests', [])[:10]
        issues = self.contributions.get('issues', [])[:10]
        
        content = """### 🗓️ Last 30 Days Activity

#### Commits\n\n"""
        
        if commits:
            content += "| Date | Repository | Commit | Description | Link |\n"
            content += "|------|-----------|--------|-------------|------|\n"
            for commit in commits:
                date = commit['date'].split('T')[0]
                repo = commit['repository'].split('/')[-1]
                sha = commit['sha']
                msg = commit['message'][:50] + '...' if len(commit['message']) > 50 else commit['message']
                content += f"| `{date}` | `{repo}` | `{sha}` | {msg} | [🔗 View]({commit['url']}) |\n"
        else:
            content += "No recent commits found.\n"
        
        content += "\n#### Pull Requests\n\n"
        
        if prs:
            content += "| Date | Repository | PR # | Title | Status | Link |\n"
            content += "|------|-----------|------|-------|--------|------|\n"
            for pr in prs:
                date = pr['created_at'].split('T')[0]
                repo = pr['repository'].split('/')[-1]
                num = pr['number']
                title = pr['title'][:40] + '...' if len(pr['title']) > 40 else pr['title']
                status_icon = '✅ Merged' if pr['status'] == 'merged' else '🔄 Open' if pr['state'] == 'open' else '❌ Closed'
                content += f"| `{date}` | `{repo}` | `#{num}` | {title} | {status_icon} | [🔗 View]({pr['url']}) |\n"
        else:
            content += "No recent pull requests found.\n"
        
        content += "\n#### Issues\n\n"
        
        if issues:
            content += "| Date | Repository | Issue # | Title | Status | Link |\n"
            content += "|------|-----------|---------|-------|--------|------|\n"
            for issue in issues:
                date = issue['created_at'].split('T')[0]
                repo = issue['repository'].split('/')[-1]
                num = issue['number']
                title = issue['title'][:40] + '...' if len(issue['title']) > 40 else issue['title']
                status_icon = '🔓 Open' if issue['state'] == 'open' else '✅ Closed'
                content += f"| `{date}` | `{repo}` | `#{num}` | {title} | {status_icon} | [🔗 View]({issue['url']}) |\n"
        else:
            content += "No recent issues found.\n"
        
        return content
    
    def generate_repositories_table(self) -> str:
        """Generate repositories table"""
        repo_stats = self.stats.get('repositories', {}).get('repositories', [])
        
        content = """### My Active Projects\n\n"""
        
        if repo_stats:
            content += "| Repository | Commits | PRs | Issues | Last Activity |\n"
            content += "|-----------|---------|-----|--------|---------------|\n"
            for repo in repo_stats[:10]:
                name = repo['repository'].split('/')[-1]
                commits = repo.get('commits', 0)
                prs = repo.get('prs', 0)
                issues = repo.get('issues', 0)
                content += f"| `{name}` | `{commits}` | `{prs}` | `{issues}` | - |\n"
        else:
            content += "No repository data available.\n"
        
        return content
    
    def generate_language_chart(self) -> str:
        """Generate language distribution chart"""
        languages = self.stats.get('languages', {})
        
        content = """### Language Distribution\n\n```\n"""
        
        if languages:
            for lang, data in list(languages.items())[:5]:
                percentage = data.get('percentage', 0)
                bar_length = int(percentage / 5)
                bar = '█' * bar_length + '░' * (20 - bar_length)
                content += f"{lang:15} {bar}  {percentage}%\n"
        else:
            content += "No language data available.\n"
        
        content += "```"
        
        return content
    
    def update_timestamp(self):
        """Update the last auto-update timestamp"""
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        
        # Replace timestamp in the footer
        pattern = r'\*Last auto-update:.*?\*'
        replacement = f'*Last auto-update: `{timestamp}` via GitHub Actions*'
        self.readme_content = re.sub(pattern, replacement, self.readme_content)
    
    def run(self):
        """Main execution method"""
        print("="*60)
        print("README Updater")
        print("="*60)
        print(f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print("="*60)
        
        # Update each section
        print("Updating statistics section...")
        stats_content = self.generate_stats_table()
        self.update_section(
            '<!-- AUTO-GENERATED-STATS:START -->',
            '<!-- AUTO-GENERATED-STATS:END -->',
            stats_content
        )
        
        print("Updating contributions section...")
        contributions_content = self.generate_contributions_table()
        self.update_section(
            '<!-- AUTO-GENERATED-CONTRIBUTIONS:START -->',
            '<!-- AUTO-GENERATED-CONTRIBUTIONS:END -->',
            contributions_content
        )
        
        print("Updating repositories section...")
        repos_content = self.generate_repositories_table()
        self.update_section(
            '<!-- AUTO-GENERATED-REPOS:START -->',
            '<!-- AUTO-GENERATED-REPOS:END -->',
            repos_content
        )
        
        print("Updating language analytics...")
        lang_content = self.generate_language_chart()
        self.update_section(
            '<!-- AUTO-GENERATED-ANALYTICS:START -->',
            '<!-- AUTO-GENERATED-ANALYTICS:END -->',
            lang_content
        )
        
        print("Updating timestamp...")
        self.update_timestamp()
        
        # Save updated README
        self.save_readme()
        
        print("="*60)
        print("README Update Complete!")
        print("="*60)


def main():
    """Main entry point"""
    try:
        updater = ReadmeUpdater()
        updater.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
