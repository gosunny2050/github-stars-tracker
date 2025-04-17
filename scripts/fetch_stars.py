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
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
    except Exception as e:
        print(f"请求GitHub趋势页面失败: {e}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    repos = []
    
    # 更健壮的选择器
    for article in soup.select('article.Box-row'):
        try:
            repo_info = {}
            
            # 获取仓库名称和链接
            h1 = article.select_one('h1.h3 a')
            if not h1:
                continue
                
            repo_info['name'] = h1.get_text(strip=True).replace('\n', '').replace(' ', '')
            repo_info['url'] = f"https://github.com{h1['href']}"
            
            # 获取描述
            desc = article.select_one('p.col-9')
            repo_info['description'] = desc.get_text(strip=True) if desc else ''
            
            # 获取语言
            lang = article.select_one('span[itemprop="programmingLanguage"]')
            repo_info['language'] = lang.get_text(strip=True) if lang else ''
            
            # 获取star数
            stars = article.select('a.Link--muted')[0]
            repo_info['stars'] = stars.get_text(strip=True)
            
            repos.append(repo_info)
            
            if len(repos) >= 10:
                break
        except Exception as e:
            print(f"解析仓库信息时出错: {e}")
            continue
    
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