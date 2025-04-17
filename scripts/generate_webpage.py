import json
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import argparse

def load_all_data():
    """加载所有历史数据"""
    data = []
    for filename in sorted(os.listdir('data'), reverse=True):
        if filename.endswith('.json'):
            date = filename[:-5]
            with open(f"data/{filename}") as f:
                daily_data = json.load(f)
                data.append({
                    'date': date,
                    'repos': daily_data
                })
    return data

def generate_webpage(date=None):
    """生成网页"""
    env = Environment(loader=FileSystemLoader('templates'))
    
    # 生成每日页面
    if date:
        data_file = f"data/{date}.json"
        if not os.path.exists(data_file):
            print(f"No data found for {date}")
            return
        
        with open(data_file) as f:
            repos = json.load(f)
        
        os.makedirs('docs/archives', exist_ok=True)
        template = env.get_template('daily.html')
        output = template.render(date=date, repos=repos)
        
        with open(f"docs/archives/{date}.html", 'w') as f:
            f.write(output)
        
        print(f"Generated archive page for {date}")
        return
    
    # 生成主页面
    all_data = load_all_data()
    
    template = env.get_template('base.html')
    output = template.render(days=all_data)
    
    os.makedirs('docs', exist_ok=True)
    with open('docs/index.html', 'w') as f:
        f.write(output)
    
    print("Generated main index page")

def main():
    parser = argparse.ArgumentParser(description='Generate GitHub trending webpage.')
    parser.add_argument('--date', help='Specific date to generate (format: YYYY-MM-DD)')
    args = parser.parse_args()
    
    generate_webpage(args.date)

if __name__ == "__main__":
    main()