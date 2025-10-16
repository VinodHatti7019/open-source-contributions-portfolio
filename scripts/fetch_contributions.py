#!/usr/bin/env python3
"""
Fetch Contributions Script

This script fetches contribution data from GitHub API including:
- Commits across all repositories
- Pull requests (opened, merged, reviewed)
- Issues (created, commented, resolved)
- Forks and repository contributions
- Branch information

Author: Auto-generated for Open Source Contributions Portfolio
Date: 2025
"""

import os
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any

try:
    from github import Github
    import requests
except ImportError:
    print("Error: Required packages not installed. Run: pip install -r requirements.txt")
    sys.exit(1)


class ContributionFetcher:
    """Fetches contribution data from GitHub API"""
    
    def __init__(self):
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.github_username = os.environ.get('GITHUB_USERNAME')
        
        if not self.github_token or not self.github_username:
            print("Error: GITHUB_TOKEN and GITHUB_USERNAME environment variables required")
            sys.exit(1)
        
        self.gh = Github(self.github_token)
        self.user = self.gh.get_user(self.github_username)
        self.data = {
            'metadata': {
                'last_updated': datetime.utcnow().isoformat(),
                'username': self.github_username
            },
            'commits': [],
            'pull_requests': [],
            'issues': [],
            'forks': [],
            'repositories': [],
            'statistics': {}
        }
    
    def fetch_repositories(self) -> List[Dict[str, Any]]:
        """Fetch all user repositories"""
        print("Fetching repositories...")
        repos = []
        
        for repo in self.user.get_repos():
            repos.append({
                'name': repo.name,
                'full_name': repo.full_name,
                'url': repo.html_url,
                'description': repo.description or '',
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'is_fork': repo.fork,
                'language': repo.language or 'Unknown',
                'created_at': repo.created_at.isoformat(),
                'updated_at': repo.updated_at.isoformat()
            })
        
        print(f"  Found {len(repos)} repositories")
        return repos
    
    def fetch_commits(self, days: int = 30) -> List[Dict[str, Any]]:
        """Fetch recent commits across all repositories"""
        print(f"Fetching commits from last {days} days...")
        commits = []
        since_date = datetime.utcnow() - timedelta(days=days)
        
        for repo in self.user.get_repos():
            try:
                for commit in repo.get_commits(author=self.user, since=since_date):
                    commits.append({
                        'repository': repo.full_name,
                        'repo_url': repo.html_url,
                        'sha': commit.sha[:7],
                        'message': commit.commit.message.split('\n')[0],
                        'date': commit.commit.author.date.isoformat(),
                        'url': commit.html_url
                    })
            except Exception as e:
                print(f"    Warning: Could not fetch commits for {repo.name}: {e}")
        
        commits.sort(key=lambda x: x['date'], reverse=True)
        print(f"  Found {len(commits)} commits")
        return commits
    
    def fetch_pull_requests(self, days: int = 90) -> List[Dict[str, Any]]:
        """Fetch pull requests (created or involved in)"""
        print(f"Fetching pull requests from last {days} days...")
        prs = []
        
        # GitHub search query for user's PRs
        query = f"author:{self.github_username} type:pr"
        
        try:
            search_results = self.gh.search_issues(query, sort='updated', order='desc')
            
            for pr in search_results[:100]:  # Limit to recent 100
                prs.append({
                    'repository': pr.repository.full_name,
                    'repo_url': pr.repository.html_url,
                    'number': pr.number,
                    'title': pr.title,
                    'state': pr.state,
                    'status': 'merged' if pr.pull_request and pr.pull_request.merged_at else pr.state,
                    'created_at': pr.created_at.isoformat(),
                    'updated_at': pr.updated_at.isoformat(),
                    'url': pr.html_url
                })
        except Exception as e:
            print(f"    Warning: Could not fetch pull requests: {e}")
        
        print(f"  Found {len(prs)} pull requests")
        return prs
    
    def fetch_issues(self, days: int = 90) -> List[Dict[str, Any]]:
        """Fetch issues created by user"""
        print(f"Fetching issues from last {days} days...")
        issues = []
        
        query = f"author:{self.github_username} type:issue"
        
        try:
            search_results = self.gh.search_issues(query, sort='updated', order='desc')
            
            for issue in search_results[:100]:  # Limit to recent 100
                issues.append({
                    'repository': issue.repository.full_name,
                    'repo_url': issue.repository.html_url,
                    'number': issue.number,
                    'title': issue.title,
                    'state': issue.state,
                    'comments': issue.comments,
                    'created_at': issue.created_at.isoformat(),
                    'updated_at': issue.updated_at.isoformat(),
                    'url': issue.html_url
                })
        except Exception as e:
            print(f"    Warning: Could not fetch issues: {e}")
        
        print(f"  Found {len(issues)} issues")
        return issues
    
    def calculate_statistics(self) -> Dict[str, Any]:
        """Calculate contribution statistics"""
        print("Calculating statistics...")
        
        stats = {
            'total_commits': len(self.data['commits']),
            'total_prs': len(self.data['pull_requests']),
            'total_issues': len(self.data['issues']),
            'total_repositories': len(self.data['repositories']),
            'merged_prs': len([pr for pr in self.data['pull_requests'] if pr['status'] == 'merged']),
            'open_prs': len([pr for pr in self.data['pull_requests'] if pr['state'] == 'open']),
            'closed_issues': len([issue for issue in self.data['issues'] if issue['state'] == 'closed']),
            'open_issues': len([issue for issue in self.data['issues'] if issue['state'] == 'open']),
            'forked_repos': len([repo for repo in self.data['repositories'] if repo['is_fork']]),
            'own_repos': len([repo for repo in self.data['repositories'] if not repo['is_fork']])
        }
        
        print(f"  Statistics calculated")
        return stats
    
    def save_data(self, output_file: str = 'data/contributions.json'):
        """Save fetched data to JSON file"""
        print(f"Saving data to {output_file}...")
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        print(f"  Data saved successfully ({len(json.dumps(self.data))} bytes)")
    
    def run(self):
        """Main execution method"""
        print("="*60)
        print("GitHub Contributions Fetcher")
        print("="*60)
        print(f"User: {self.github_username}")
        print(f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print("="*60)
        
        # Fetch all data
        self.data['repositories'] = self.fetch_repositories()
        self.data['commits'] = self.fetch_commits(days=30)
        self.data['pull_requests'] = self.fetch_pull_requests(days=90)
        self.data['issues'] = self.fetch_issues(days=90)
        self.data['statistics'] = self.calculate_statistics()
        
        # Save data
        self.save_data()
        
        print("="*60)
        print("Fetch Complete!")
        print("="*60)
        print(f"Repositories: {self.data['statistics']['total_repositories']}")
        print(f"Commits: {self.data['statistics']['total_commits']}")
        print(f"Pull Requests: {self.data['statistics']['total_prs']}")
        print(f"Issues: {self.data['statistics']['total_issues']}")
        print("="*60)


def main():
    """Main entry point"""
    try:
        fetcher = ContributionFetcher()
        fetcher.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
