from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import requests
from fake_useragent import UserAgent

# 自定义函数，用于处理每个URL的操作
def process_url(url):
    # 创建WebDriver实例
    driver = webdriver.Edge()
    hearders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58'}
    driver.get(url)

    # 在每个窗口上执行相应的操作
    # ...
    for i in range(1,10000):
        # 提交每个URL的处理任务给线程池，并获得对应的Future对象
        # 隧道域名:端口
        driver.add_cookie({'name': 'Device-Id', 'value': 'cGz9jmoTIrUeVpRPtKxJ'})
        driver.add_cookie({'name': 'Locale-Supported', 'value': 'zh-Hans'})
        driver.add_cookie({'name': 'P_INFO',
                           'value': '187******39|1683687813|1|netnease_buff|00&99|null&null&null#CN&null#10#0|&0|null|187******39'})#电话号打码
        driver.add_cookie({'name': 'csrf_token',
                           'value': 'ImY5MDFlMWU5M2M5NWE4YjQ0YTRhZmI4YzMwYzZmMzFiMDZkNjY5NGQi.F4FRZA.5ako_jdLaLDZuoWyLYS51koyY-Y'})
        driver.add_cookie({'name': 'game', 'value': 'csgo'})
        driver.add_cookie({'name': 'remember_me', 'value': 'U1100645020|4NwXXcQ2BJb6tqEayjLQw72RbLzZNkb2'})
        driver.add_cookie({'name': 'session', 'value': '1-XJuGCzWZh9yhDv9siya8NkGP4bKg_APmKc0NUWbz-11m2035555780'})
        # # tunnel = "y214.kdltps.com:15818"
        # # 用户名密码方式
        # username = "t18429028503663"
        # password = "c8c8c3ft"
        # proxies = {
        #     "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
        #     "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
        # }

        #要访问的目标网页
        if requests.get(url).status_code==429:
            driver.quit()
            time.sleep(1)
            process_url(url)

        driver.refresh()  # 刷新页面
        time.sleep(1)
        c = driver.find_element(By.XPATH, '/html/body/div[7]/div/div[7]/table/tbody/tr[2]/td[5]/div[1]/strong')
        cheap = float(''.join(re.findall(r"\d+\.?\d*", c.text)))  # 正则表达式运用，c.text是列表。.join()可转化为字符串。最后float转化为浮点数进行比较
        print(cheap)

        d = driver.find_element(By.XPATH, '/html/body/div[7]/div/div[7]/table/tbody/tr[3]/td[5]/div[1]/strong')
        expensive = float(''.join(re.findall(r"\d+\.?\d*", d.text)))
        print(expensive)
        print('*' * 10)
        # if (expensive - cheap) / cheap <= 0.1:
        #     driver.find_element(By.XPATH, '/html/body/div[7]/div/div[7]/table/tbody/tr[2]/td[6]/a[1]').click()
        #     time.sleep(60)

    # 关闭当前窗口和浏览器实例

pool = ThreadPoolExecutor(max_workers=2)####最大线程为max_workers

# URL列表
urls = [("https://buff.163.com/goods/33960#tab=selling"),
        ("https://buff.163.com/goods/33962#tab=selling"),
        ("https://buff.163.com/goods/33961#tab=selling"),
        ("https://buff.163.com/goods/33959#tab=selling")
]

# 创建线程池
with ThreadPoolExecutor() as executor:
    while True:
        futures = [pool.submit(process_url, url) for url in urls]
        # 获取已完成的任务的结果
        for future in as_completed(futures):
            try:
                # 获取任务的结果，如果有异常则抛出
                result = future.result()
            except Exception as e:
                print(f"Error occurred: {e}")

        # 循环处理URL列表，这里假设每次循环间隔为1分钟

        time.sleep(60)
