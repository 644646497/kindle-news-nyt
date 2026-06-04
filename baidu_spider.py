import requests
from bs4 import BeautifulSoup
import re

# 目标网页 URL（百度百科“宇宙”词条）
url = 'https://baike.baidu.com/item/宇宙'

# 【核心】设置请求头，模拟真实浏览器访问，这是绕过百度百科反爬的关键
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
    # 发送 GET 请求
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 检查 HTTP 是否成功
    response.encoding = 'utf-8'  # 百度百科通常是 utf-8 编码
    
    # 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 删除不需要的标签（如脚本、样式表等）
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    
    # 【核心】精准提取正文区域（百度百科的正文通常在 class="lemma-summary" 或 "body-content" 中）
    content_div = soup.find('div', class_='lemma-summary') or soup.find('div', class_='body-content')
    
    if content_div:
        # 提取纯文本，并用换行符分隔段落
        text = content_div.get_text(separator='\n', strip=True)
        
        # 使用正则表达式清理多余的空白字符，让排版更干净
        cleaned_text = re.sub(r'\n\s*\n', '\n\n', text).strip()
        
        # 保存到本地文件
        with open('baidu_article.txt', 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        print("✅ 百度百科【宇宙】词条抓取成功！")
    else:
        print("❌ 未能找到正文区域，百度百科可能改版了！")

except Exception as e:
    print(f"❌ 抓取或解析失败: {e}")
