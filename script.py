from bs4 import BeautifulSoup
import datetime
from random import shuffle
import requests

def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_details(html, category):
    
    stamp = {}
    
    try:
        stock_num = html.select('td')[0].get_text().strip()
        stamp['stock_num'] = stock_num
    except: 
        stamp['stock_num'] = None
        
    try:
        raw_text = html.select('td')[1].get_text().strip()
        raw_text = raw_text.replace(u'\xa0', u'')
        raw_text = raw_text.replace('\n\t', '')
        raw_text = raw_text.replace('\n', '')
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None 
    
    sold = 0 
    try:
        price = html.select('td')[2].get_text().strip()
        if price == 'SOLD':
           sold = 1
        stamp['price'] = price
    except:
        stamp['price'] = None  
        
    stamp['sold'] = sold    
        
    stamp['category'] = category   

    stamp['currency'] = "GBP"

    # image_urls should be a list
    images = []                    
    try:
        img_cont = html.select('td')[3]
        img_src = img_cont.select('a')[0].get('href')
        img = 'https://www.midphil.com/' + img_src
        images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 
        
    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    print(stamp)
    print('+++++++++++++')
           
    return stamp

def get_page_items(url):
    
    items = []

    try:
        html = get_html(url)
    except:
        return items

    try:
        for item in html.select('tr'):
            if item not in items and item.select('a') and (len(item.select('td')) > 3):
                items.append(item)
    except:
        pass
    
    shuffle(list(set(items)))
    
    return items

def get_categories():
    
    url = 'https://www.midphil.com/navigation.htm'
    
    items = {}

    try:
        html = get_html(url)
    except:
        return items

    try:
        for item in html.select('p font a'):
            item_href = item.get('href')
            item_link_parts = item_href.split('#')
            item_link = 'https://www.midphil.com/' + item_link_parts[0]
            item_name = item.get_text().strip()
            item_name = item_name.replace('\n', '')
            if item_link not in items: 
                items[item_name] = item_link
    except: 
        pass
    
    shuffle(list(set(items)))
    
    return items

categories = get_categories()
for category_name in categories:
    category = categories[category_name]
    page_items = get_page_items(category)
    for page_item in page_items:
        stamp = get_details(page_item, category_name)

