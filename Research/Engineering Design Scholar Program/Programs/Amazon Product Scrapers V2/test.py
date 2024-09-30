from DrissionPage import ChromiumPage
import pandas as pd
import re
from parsel import Selector
import os
import random

def random_delay(page, scroll_times=random.randint(0, 2), delay=random.uniform(0, 2)):
    for _ in range(scroll_times):
        page.actions.scroll(0, random.randint(60, 1000))
        page.wait(delay)

def extract_product_details(page, product_url):
    page.get(product_url)
    page.wait(random.uniform(1,3))#随机延时，避免风控
    sel = Selector(text=page.html)
    random_delay(page)#随机动作链，避免风控
    #提取价格信息
    price_whole = sel.css('span.a-price-whole::text').get()
    price_fraction = sel.css('span.a-price-fraction::text').get()
    if price_whole and price_fraction:
        price = f"{price_whole.strip()}.{price_fraction.strip()}"
    else:
        price = None

    #提取产品描述
    description_items = sel.css('ul.a-unordered-list.a-vertical.a-spacing-mini li span.a-list-item::text').getall()
    description = ' '.join([item.strip() for item in description_items])

    #提取可持续性特性
    sustainability_sections = sel.css('div.a-section.a-spacing-base')
    sustainability_features = []
    for section in sustainability_sections:
        title = section.css('span.a-size-base-plus.a-text-bold::text').get()
        if title:
            feature_text = section.css('p.a-size-base::text').get()
            certifications = section.css('div.climatePledgeFriendlyAttributePillText a::text').getall()
            certification_text = ' '.join(certifications).strip()
            feature_detail = f"{title.strip()}\n{feature_text.strip() if feature_text else ''}\nAs certified by\n{certification_text}"
            sustainability_features.append(feature_detail)
    sustainability_features_text = '\n\n'.join(sustainability_features)

    product_details = {
        'name': sel.css('#productTitle::text').get().strip(),
        'price': price,
        'product_dimensions': sel.css('tr.po-item_depth_width_height td.a-span9 span.a-size-base.po-break-word::text').get(),
        'description': description,
        'sustainability_features': sustainability_features_text,
        'rating': sel.css('span.a-icon-alt::text').get(),
        'number_of_reviews': sel.css('#acrCustomerReviewText::text').get(),
        'product_page_url': product_url
    }
    
    return product_details

def process_urls(file_path):    #提取TXT文件中的URL
    with open(file_path, 'r') as file:
        product_urls = file.readlines()

    all_products = []

    page = ChromiumPage()

    for url in product_urls:
        product_url = url.strip()
        if product_url:
            details = extract_product_details(page, product_url)
            all_products.append(details)

    page.quit()

    return all_products

def save_products_to_csv(products, output_path):    #保存到CSV文件
    df = pd.DataFrame(products)
    df.to_csv(output_path, index=False)

def process_all_files(folder_path):    #遍历文件夹内的所有TXT文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            txt_file_path = os.path.join(folder_path, file_name)
            csv_output_path = os.path.join(folder_path, file_name.replace('.txt', '.csv'))
            
            all_products = process_urls(txt_file_path)
            save_products_to_csv(all_products, csv_output_path)

#处理文件夹中的所有TXT文件并保存结果
folder_path = r'C:\Users\32613\Desktop\URL'  #包含TXT文件的文件夹路径
process_all_files(folder_path)
