import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import os
from iteration_utilities import deepflatten

#todo
class shopify_scan():
    def  __init__(self):
        self.genre=''
        
    def scan_top_500(self):  
        session=requests.Session()
        jar=requests.cookies.RequestsCookieJar()
        shopify_link='https://www.shopistores.com/top-500-most-successful-shopify-stores/'
        response = requests.get(shopify_link)
        Cookies=list(response.cookies)
        shopify_cookie=str(Cookies[1]).split('_csrf-frontend=')[1].split(' ')[0]
        jar.set('_csrf-frontend',shopify_cookie)
        session.cookies=jar
        for i in range(0,16):
            req='https://www.shopistores.com/shopify/{}'.format(str(i))
            sess=session.get(req).content
            ranks=list(map(lambda x:x.get_text().strip(),bs(sess).find_all('td',{'data-title':'Alexa Rank'})))
            names=list(map(lambda x:x.get_text().strip(),bs(sess).find_all('td',{'data-title':'Title'})))
            links=list(map(lambda x:(x.find_all('a')),bs(sess).find_all('td',{'data-title':'Store Address'})))
            for link,name,rank in zip(links,names,ranks):
                for a in link:
                    print(name,rank,a['href'])
    
    def get_genre_shops(self):
        session=requests.Session()
        jar=requests.cookies.RequestsCookieJar()
        shopify_link='https://www.shopistores.com'
        response = requests.get(shopify_link)
        Cookies=list(response.cookies)
        shopify_cookie=str(Cookies[1]).split('_csrf-frontend=')[1].split(' ')[0]
        jar.set('_csrf-frontend',shopify_cookie)
        session.cookies=jar
        req='https://www.shopistores.com/?keyword={}'.format(self.genre)
        sess=session.get(req).content
        ranks=list(map(lambda x:x.get_text().strip(),bs(sess).find_all('td',{'data-title':'Alexa Rank'})))
        names=list(map(lambda x:x.get_text().strip(),bs(sess).find_all('td',{'data-title':'Title'})))
        links=list(map(lambda x:(x.find_all('a')),bs(sess).find_all('td',{'data-title':'Store Address'})))
        
        flatten_list = [item for subl in links for item in subl]

        for q_link in list(href['href'] for href in flatten_list):
        #print(list(deepflatten(links)))
         self.get_best_products(q_link)
    def write_data(self,JSON):
         if not os.path.exists('shopify_store/'):
                os.makedirs('shopify_store/')
         with open('shopify_store/'+str(self.genre)+'.txt', 'w') as outfile:
                json.dump(JSON, outfile)
    def get_best_products(self,genre):
        #for top 30 products only 
        #origianlly wrote for tags only
        data = {}
        data['product'] = []
        
        fter='/collections/all/products.json?sort_by=best-selling'
        JSON=requests.get(genre+fter).content
        json_dict = json.loads(JSON)
        keywords = ('title,''price')
        for row in json_dict['products']:
            data['product'].append({
            "site":genre,
           "product_type":str(row['product_type']),
            'tags': str(row['tags']),
            "product name": row['title'],
            "sku":list(sku['sku'] for sku in row[ "variants"]),
            "price":''.join(price['price'] for price in row[ "variants"]),
            })
        self.write_data(data)

import json       
scan=shopify_scan()
#scan.scan_top_500()
niche_categories=['Jewellery',"Men's Fashion","Women's Fashion","Toys and Babies","Pets"]
for niche in niche_categories
    scan.genre=niche
    scan.get_genre_shops()