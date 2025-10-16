#!/usr/bin/env python3
"""
Generate Statistics Script

This script processes contribution data and generates comprehensive statistics:
- Overall contribution metrics
- Contribution streaks and patterns
- Language distribution
- Repository analytics
- Time-based trends

Author: Auto-generated for Open Source Contributions Portfolio
Date: 2025
"""

import os
import json
import sys
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from typing import Dict, List, Any


class StatsGenerator:
    """Generates statistics from contribution data"""
    
    def __init__(self, data_file: str = 'data/contributions.json'):
        self.data_file = data_file
        self.data = self.load_data()
        self.stats = {
            'generated_at': datetime.utcnow().isoformat(),
            'overall': {},
            'streaks': {},
            'languages': {},
            'repositories': {},
            'trends': {}
        }
    
    def load_data(self) -> Dict[str, Any]:
        """Load contribution data from JSON file"""
        print(f"Loading data from {self.data_file}...")
        
        if not os.path.exists(self.data_file):
            print(f"Error: Data file {self.data_file} not found")
            sys.exit(1)
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"  Loaded data for user: {data.get('metadata', {}).get('username', 'Unknown')}")
        return data
    
    def calculate_overall_stats(self) -> Dict[str, Any]:
        """Calculate overall contribution statistics"""
        print("Calculating overall statistics...")
        
        stats = self.data.get('statistics', {})
        
        overall = {
            'total_commits': stats.get('total_commits', 0),
            'total_prs': stats.get('total_prs', 0),
            'total_issues': stats.get('total_issues', 0),
            'total_repositories': stats.get('total_repositories', 0),
            'merged_prs': stats.get('merged_prs', 0),
            'open_prs': stats.get('open_prs', 0),
            'closed_issues': stats.get('closed_issues', 0),
            'open_issues': stats.get('open_issues', 0),
            'forked_repos': stats.get('forked_repos', 0),
            'own_repos': stats.get('own_repos', 0)
        }
        
        # Calculate PR merge rate
        if overall['total_prs'] > 0:
            overall['pr_merge_rate'] = round(overall['merged_prs'] / overall['total_prs'] * 100, 1)
        else:
            overall['pr_merge_rate'] = 0
        
        # Calculate issue closure rate
        if overall['total_issues'] > 0:
            overall['issue_closure_rate'] = round(overall['closed_issues'] / overall['total_issues'] * 100, 1)
        else:
            overall['issue_closure_rate'] = 0
        
        print(f"  Calculated overall stats")
        return overall
    
    def calculate_contribution_streaks(self) -> Dict[str, Any]:
        """Calculate contribution streaks from commit data"""
        print("Calculating contribution streaks...")
        
        commits = self.data.get('commits', [])
        
        if not commits:
            return {
                'current_streak': 0,
                'longest_streak': 0,
                'last_contribution': None
            }
        
        # Extract unique dates from commits
        commit_dates = set()
        for commit in commits:
            date_str = commit['date'].split('T')[0]
            commit_dates.add(datetime.fromisoformat(date_str.replace('Z', '+00:00')).date())
        
        sorted_dates = sorted(commit_dates, reverse=True)
        
        # Calculate current streak
        current_streak = 0
        today = datetime.utcnow().date()
        check_date = today
        
        for date in sorted_dates:
            if date == check_date or date == check_date - timedelta(days=1):
                current_streak += 1
                check_date = date - timedelta(days=1)
            else:
                break
        
        # Calculate longest streak
        longest_streak = 0
        temp_streak = 1
        
        for i in range(len(sorted_dates) - 1):
            if sorted_dates[i] - sorted_dates[i + 1] == timedelta(days=1):
                temp_streak += 1
            else:
                longest_streak = max(longest_streak, temp_streak)
                temp_streak = 1
        
        longest_streak = max(longest_streak, temp_streak)
        
        streaks = {
            'current_streak': current_streak,
            'longest_streak': longest_streak,
            'last_contribution': sorted_dates[0].isoformat() if sorted_dates else None
        }
        
        print(f"  Current streak: {current_streak} days")
        print(f"  Longest streak: {longest_streak} days")
        return streaks
    
    def calculate_language_distribution(self) -> Dict[str, Any]:
        """Calculate programming language distribution"""
        print("Calculating language distribution...")
        
        repositories = self.data.get('repositories', [])
        
        language_counter = Counter()
        
        for repo in repositories:
            if not repo.get('is_fork', False):
                lang = repo.get('language', 'Unknown')
                if lang:
                    language_counter[lang] += 1
        
        total_repos = sum(language_counter.values())
        
        language_stats = {}
        for lang, count in language_counter.most_common(10):
            percentage = round(count / total_repos * 100, 1) if total_repos > 0 else 0
            language_stats[lang] = {
                'count': count,
                'percentage': percentage
            }
        
        print(f"  Found {len(language_stats)} languages")
        return language_stats
    
    def calculate_repository_stats(self) -> Dict[str, Any]:
        """Calculate per-repository statistics"""
        print("Calculating repository statistics...")
        
        repositories = self.data.get('repositories', [])
        commits = self.data.get('commits', [])
        prs = self.data.get('pull_requests', [])
        issues = self.data.get('issues', [])
        
        repo_stats = defaultdict(lambda: {
            'commits': 0,
            'prs': 0,
            'issues': 0,
            'stars': 0,
            'forks': 0
        })
        
        # Count commits per repo
        for commit in commits:
            repo_name = commit.get('repository', '')
            if repo_name:
                repo_stats[repo_name]['commits'] += 1
        
        # Count PRs per repo
        for pr in prs:
            repo_name = pr.get('repository', '')
            if repo_name:
                repo_stats[repo_name]['prs'] += 1
        
        # Count issues per repo
        for issue in issues:
            repo_name = issue.get('repository', '')
            if repo_name:
                repo_stats[repo_name]['issues'] += 1
        
        # Add stars and forks
        for repo in repositories:
            repo_name = repo.get('full_name', '')
            if repo_name in repo_stats:
                repo_stats[repo_name]['stars'] = repo.get('stars', 0)
                repo_stats[repo_name]['forks'] = repo.get('forks', 0)
        
        # Convert to list and sort by activity
        repo_list = []
        for repo_name, stats in repo_stats.items():
            activity_score = stats['commits'] + stats['prs'] + stats['issues']
            repo_list.append({
                'repository': repo_name,
                **stats,
                'activity_score': activity_score
            })
        
        repo_list.sort(key=lambda x: x['activity_score'], reverse=True)
        
        print(f"  Analyzed {len(repo_list)} repositories")
        return {'repositories': repo_list[:20]}  # Top 20 most active
    
    def calculate_trends(self) -> Dict[str, Any]:
        """Calculate contribution trends over time"""
        print("Calculating contribution trends...")
        
        commits = self.data.get('commits', [])
        prs = self.data.get('pull_requests', [])
        issues = self.data.get('issues', [])
        
        # Group by month
        monthly_commits = defaultdict(int)
        monthly_prs = defaultdict(int)
        monthly_issues = defaultdict(int)
        
        for commit in commits:
            month = commit['date'][:7]  # YYYY-MM
            monthly_commits[month] += 1
        
        for pr in prs:
            month = pr['created_at'][:7]  # YYYY-MM
            monthly_prs[month] += 1
        
        for issue in issues:
            month = issue['created_at'][:7]  # YYYY-MM
            monthly_issues[month] += 1
        
        # Convert to sorted list
        trends = []
        all_months = set(monthly_commits.keys()) | set(monthly_prs.keys()) | set(monthly_issues.keys())
        
        for month in sorted(all_months):
            trends.append({
                'month': month,
                'commits': monthly_commits.get(month, 0),
                'prs': monthly_prs.get(month, 0),
                'issues': monthly_issues.get(month, 0)
            })
        
        print(f"  Calculated trends for {len(trends)} months")
        return {'monthly': trends}
    
    def save_stats(self, output_file: str = 'data/statistics.json'):
        """Save generated statistics to JSON file"""
        print(f"Saving statistics to {output_file}...")
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        
        print(f"  Statistics saved successfully")
    
    def run(self):
        """Main execution method"""
        print("="*60)
        print("Statistics Generator")
        print("="*60)
        print(f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print("="*60)
        
        # Generate all statistics
        self.stats['overall'] = self.calculate_overall_stats()
        self.stats['streaks'] = self.calculate_contribution_streaks()
        self.stats['languages'] = self.calculate_language_distribution()
        self.stats['repositories'] = self.calculate_repository_stats()
        self.stats['trends'] = self.calculate_trends()
        
        # Save statistics
        self.save_stats()
        
        print("="*60)
        print("Statistics Generation Complete!")
        print("="*60)
        print(f"Overall Stats: {len(self.stats['overall'])} metrics")
        print(f"Languages: {len(self.stats['languages'])} tracked")
        print(f"Repositories: {len(self.stats['repositories'].get('repositories', []))} analyzed")
        print("="*60)


def main():
    """Main entry point"""
    try:
        generator = StatsGenerator()
        generator.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
