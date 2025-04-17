import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import os
from github import Github
import argparse

def get_trending_repositories(date=None):
    """获取GitHub上star增长最快的项目"""
    if date:
        url = f"https://github.com/trending?since={date}"
    else:
        url = "https://github.com/trending"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    repos = []
    for article in soup.select('article.Box-row'):
        repo_info = {}
        
        # 获取仓库名称和链接
        h1 = article.select_one('h1 a')
        repo_info['name'] = h1.get_text().strip().replace('\n', '').replace(' ', '')
        repo_info['url'] = f"https://github.com{h1['href']}"
        
        # 获取描述
        desc = article.select_one('p')
        repo_info['description'] = desc.get_text().strip() if desc else ''
        
        # 获取语言
        lang = article.select_one('span[itemprop="programmingLanguage"]')
        repo_info['language'] = lang.get_text().strip() if lang else ''
        
        # 获取star数
        stars = article.select('a.Link--muted')[0]
        repo_info['stars'] = stars.get_text().strip()
        
        repos.append(repo_info)
        
        if len(repos) >= 10:
            break
    
    return repos

def save_data(repos, date=None):
    """保存数据到JSON文件"""
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    
    os.makedirs('data', exist_ok=True)
    filename = f"data/{date}.json"
    
    with open(filename, 'w') as f:
        json.dump(repos, f, indent=2)
    
    return filename

def main():
    parser = argparse.ArgumentParser(description='Fetch trending GitHub repositories.')
    parser.add_argument('--date', help='Specific date to fetch (format: YYYY-MM-DD)')
    args = parser.parse_args()
    
    repos = get_trending_repositories(args.date)
    filename = save_data(repos, args.date)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    main()