from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pickle
import os
import pandas as pd


def save_cookies(driver, cookies_file):
    with open(cookies_file, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)


def load_cookies(driver, cookies_file):
    if os.path.exists(cookies_file):
        with open(cookies_file, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)


def amazon_login_and_save_cookies(driver, email, password, cookies_file):
    driver.get("https://www.amazon.com/-/zh/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ap_email"))).send_keys(email)
    driver.find_element(By.ID, "continue").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ap_password"))).send_keys(password)
    driver.find_element(By.ID, "signInSubmit").click()

    # 等待验证码输入框出现
    # otp_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "auth-mfa-otpcode")))

    # 获取验证码
    # otp_code = get_otp_code()
    #
    # # 输入验证码
    # otp_input.send_keys(otp_code)
    # driver.find_element(By.ID, "auth-signin-button").click()

    # 等待主页加载
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "nav-link-accountList")))

    # 保存Cookies
    save_cookies(driver, cookies_file)


# def get_otp_code():
#     # 此处可以是从电子邮件、SMS等渠道获取验证码的逻辑
#     otp_code = input("请输入从手机获取的验证码：")
#     return otp_code


def get_reviews_selenium_with_cookies(URL, cookies_file, max_reviews=100):
    reviews = []
    chrome_driver_path = "chromedriver.exe"  # 替换为你的 ChromeDriver 路径
    driver = webdriver.Chrome(executable_path=chrome_driver_path)

    try:
        driver.get("https://www.amazon.com")
        load_cookies(driver, cookies_file)
        driver.get(URL)
        page = 1

        while len(reviews) < max_reviews:
            # 等待评论加载完成
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-hook="review"]'))
            )

            # 解析评论
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            review_divs = soup.find_all('div', {'data-hook': 'review'})

            for div in review_divs:
                review = {}
                review['url'] = URL
                review['rating'] = div.find('i', {'data-hook': 'review-star-rating'}).text.strip() if div.find('i', {
                    'data-hook': 'review-star-rating'}) else '无评分'
                if 'rating' in review and review['rating'] != '无评分':
                    # 提取评分数字并添加满分信息
                    review['rating'] = f"{review['rating'].split()[0]} out of 5 stars"
                review['author'] = div.find('span', {'class': 'a-profile-name'}).text.strip() if div.find('span', {
                    'class': 'a-profile-name'}) else '无作者'
                review['date'] = div.find('span', {'data-hook': 'review-date'}).text.strip() if div.find('span', {
                    'data-hook': 'review-date'}) else '无日期'
                review['content'] = div.find('span', {'data-hook': 'review-body'}).text.strip() if div.find('span', {
                    'data-hook': 'review-body'}) else '无内容'
                reviews.append(review)
                print(URL)
                print(review)

                if len(reviews) >= max_reviews:  # 最多获取100条评论
                    break

            print(f"{URL} 第 {page} 页评论爬取成功。")

            if len(review_divs) == 0 or len(reviews) >= max_reviews:
                break  # 如果当前页面没有评论或者已经获取到足够的评论，停止爬取

            page += 1  # 下一页

            # 点击“下一页”按钮
            time.sleep(3)
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'li.a-last > a')
                next_button.click()
            except Exception as e:
                print(f"未找到下一页按钮，爬取结束: {e}")
                break

            time.sleep(3)  # 等待加载新页面

        print(f"{URL} 爬取了 {len(reviews)} 条评论。")

    except Exception as e:
        print(f"爬取 {URL} 出错: {e}")

    driver.quit()
    return reviews[:max_reviews]  # 返回前100条评论或少于100条的所有评论


def get_reviews_url(product_url):
    product_id = product_url.split('/dp/')[1].split('/')[0]
    return f"https://www.amazon.com/product-reviews/{product_id}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&language=en_US"


# 从文本文件中读取URL
with open('Recycled Claim Standard 100-100个sku.txt', 'r') as file:
    urls = file.readlines()

all_reviews = []

# 亚马逊登录信息
email = "ngzhewee@hotmail.com"
password = "@^dN08:amazon"
cookies_file = "amazon_cookies.pkl"

# 检查是否已有Cookies文件
if not os.path.exists(cookies_file):
    chrome_driver_path = "chromedriver.exe"  # 替换为你的 ChromeDriver 路径
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    amazon_login_and_save_cookies(driver, email, password, cookies_file)
    driver.quit()

# 爬取每个URL的评论
for url in urls:
    if url == '\n':
        continue
    url = url.strip()  # 去除首尾空格和换行符
    review_url_template = get_reviews_url(url)

    # 获取评论信息
    reviews = get_reviews_selenium_with_cookies(review_url_template, cookies_file)
    all_reviews.extend(reviews)

# 将评论信息写入表格
df = pd.DataFrame(all_reviews)
df.to_excel('Recycled Claim Standard 100-100个sku.xlsx', index=False)
print("评论信息已写入 Recycled Claim Standard 100-100个sku.xlsx 文件。")
