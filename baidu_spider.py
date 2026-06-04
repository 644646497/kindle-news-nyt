from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

# 设置 Chrome 选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式，不弹出浏览器窗口
chrome_series_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# 初始化浏览器驱动
driver = webdriver.Chrome(options=chrome_options)

try:
    # 访问百度百科“宇宙”词条
    url = 'https://baike.baidu.com/item/宇宙'
    print(f"正在访问: {url}")
    driver.get(url)

    # 【关键步骤】等待页面加载完成，或者等待验证码出现
    # 如果出现验证码，Selenium 会暂停 20 秒，让你手动完成滑块验证
    # 如果没有验证码，它会自动继续
    try:
        # 等待正文区域出现 (class="lemma-summary")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".lemma-summary"))
        )
        print("✅ 页面加载成功，或验证码已通过！")
    except:
        print("❌ 页面加载超时，可能需要手动处理验证码。")
        # 如果代码执行到这里，说明出现了验证码，程序会暂停 20 秒
        # 你可以在这 20 秒内手动完成滑块验证
        time.sleep(20)

    # 获取页面源代码
    html = driver.page_source

    # 保存 HTML 到文件
    with open('baidu_article.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✅ 页面源代码已保存")

except Exception as e:
    print(f"❌ 抓取失败: {e}")

finally:
    driver.quit()
