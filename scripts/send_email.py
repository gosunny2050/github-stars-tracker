import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def create_email_content(repos):
    """创建邮件内容"""
    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            h1 { color: #24292e; }
            .repo { margin-bottom: 20px; border-bottom: 1px solid #e1e4e8; padding-bottom: 10px; }
            .repo-name { font-size: 18px; font-weight: bold; }
            .repo-url { color: #0366d6; text-decoration: none; }
            .repo-desc { color: #586069; }
            .repo-meta { color: #6a737d; font-size: 14px; }
        </style>
    </head>
    <body>
        <h1>GitHub Daily Trending Repositories</h1>
        <p>Here are the top 10 repositories with the fastest growing stars today:</p>
    """
    
    for i, repo in enumerate(repos, 1):
        html += f"""
        <div class="repo">
            <div class="repo-name">{i}. {repo['name']}</div>
            <div class="repo-url"><a href="{repo['url']}">{repo['url']}</a></div>
            <div class="repo-desc">{repo['description']}</div>
            <div class="repo-meta">
                Language: {repo['language']} | Stars: {repo['stars']}
            </div>
        </div>
        """
    
    html += """
    </body>
    </html>
    """
    
    return html

def send_email(repos, to_email):
    """发送邮件"""
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL')
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = f"GitHub Trending Repositories - {datetime.now().strftime('%Y-%m-%d')}"
    
    html_content = create_email_content(repos)
    msg.attach(MIMEText(html_content, 'html'))
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
    
    print(f"Email sent to {to_email}")

def main():
    date = datetime.now().strftime('%Y-%m-%d')
    data_file = f"data/{date}.json"
    
    if not os.path.exists(data_file):
        print(f"No data file found for {date}")
        return
    
    with open(data_file) as f:
        repos = json.load(f)
    
    to_email = os.getenv('TO_EMAIL')
    if not to_email:
        print("Please set TO_EMAIL in environment variables")
        return
    
    send_email(repos, to_email)

if __name__ == "__main__":
    main()