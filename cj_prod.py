import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import os
import re
import functools
import operator
prime_link='https://cjdropshipping.com'
def return_session():
    session=requests.Session()
    jar=requests.cookies.RequestsCookieJar()
    prime_link='https://cjdropshipping.com'
    response = requests.get(prime_link)
    Cookies=list(response.cookies)
    cj_csrf= str(Cookies[-1]).split(' ')[1].split('=')[1]#splitting the string to get the csrf

    # cj_csrf=get_cj_csrf_token(link)
    jar.set('csrfToken',cj_csrf)
    session.cookies=jar
    return session


class cj_lookup_interest:
    '''
    session-session req
    sub_cat-sub_cat list
    '''
    def __init__(self,session,sub_cats_links):
          self.session=session
          self.sub_cats=sub_cats_links
          self.filter_list='?feildType=1&isAsc=0'
    def return_session(self):
        session=requests.Session()
        jar=requests.cookies.RequestsCookieJar()
        prime_link='https://cjdropshipping.com'
        response = requests.get(prime_link)
        Cookies=list(response.cookies)
        cj_csrf= str(Cookies[-1]).split(' ')[1].split('=')[1]#splitting the string to get the csrf

        # cj_csrf=get_cj_csrf_token(link)
        jar.set('csrfToken',cj_csrf)
        session.cookies=jar
        return session     
    def get_cj_location(self,session,link):
        return bs(session.get(link).content)
           
    def get_cj_links(self,location,session):
        return list(map(lambda temp_var: temp_var['href'],location.find_all("a",{'class':'detail-anchor'})))
           
    def get_cj_price(self,location,session):
       return list(map(lambda temp_var: temp_var.getText(),location.find_all("div",{'class':'price'})))
           
    def get_cj_interest(self,location,session):
       return list(map(lambda total_link:(''.join(filter(str.isdigit, total_link.getText()))), location.findAll("span",{'class':'list'})))
     
    def get_cj_img(self,location,session):
         images=list(map(lambda img_var: ((img_var.find('img'))),location.find_all("a",{'class':'detail-anchor'})))
        # print(list(map(lambda img_var: ((print(img_var['src']))),images)))
         images = list(filter(None, images))#removing none values
         images_link=list(map(lambda image_link:image_link['src'],images))
         return [images_link]
        
    def get_cj_img_text(self,location,session):
         images=list(map(lambda img_var: ((img_var.find('img'))),location.find_all("a",{'class':'detail-anchor'})))
        # print(list(map(lambda img_var: ((print(img_var['src']))),images)))
         images = list(filter(None, images))#removing none values
         images_text=list(map(lambda image_link:image_link['alt'],images))
         return images_text  
        
    def get_page_limit(self,link):    
        cntnt=bs(self.session.get(link).content)
       
        bottom=cntnt.find_all('div',{'class':'to-go'})
        #print(bottom)
        for bottom_bar in bottom:
            bottom_bar=bottom_bar.find_all('span')
            return int(bottom_bar[1].text.split(' ')[1])
        
    def write_data(self,folder_name,items_name,items_interest,items_price):
        to_be_written=[]
        if not os.path.exists('cj_prods_list/'+str(folder_name)):
                os.makedirs('cj_prods_list/'+str(folder_name))
        for name,interest,price in zip(items_name,items_interest,items_price):    
                combined=[interest,price]
                to_be_written.append(({name:combined}))
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H%M%S")
        print("date and time =", dt_string)
        #for interest list
        geeky_file = open('cj_prods_list/'+str(folder_name)+"/"+str(dt_string)+'.txt', 'wt', encoding='utf-8')
        geeky_file.write(str(to_be_written))
        geeky_file.close()
        
    def scrape_the_link(self):
        for sub_cat in self.sub_cats:
            for k,v in sub_cat.items():
               print(k)
               cj_links=[]
               cj_price=[]
               cj_img=[]
               cj_img_text=[]
               cj_interest=[]
               limit=self.get_page_limit(v)
               for page in range(0,limit):
                     if page==0:
                        location=self.get_cj_location(self.session,v)
                        cj_interest=cj_interest+self.get_cj_interest(location,self.session)
                        cj_links=cj_links+self.get_cj_links(location,self.session)
                        cj_price=cj_price+self.get_cj_price(location,self.session)
                        cj_img=cj_img+self.get_cj_img(location,self.session)
                        #print(list(zip(cj_img_text,cj_interest,cj_price)))
                     else:
                        location=self.get_cj_location(self.session,v+'&pageNum={}&pageSize=60'.format(page))
                        cj_interest=cj_interest+self.get_cj_interest(location,self.session)
                        cj_links=cj_links+self.get_cj_links(location,self.session)
                        cj_price=cj_price+self.get_cj_price(location,self.session)
                        cj_img=cj_img+self.get_cj_img(location,self.session)#list of lists consists image_link and image text
                        cj_img_text=cj_img_text+self.get_cj_img_text(location,self.session)      
               self.write_data(k,cj_img_text,cj_interest,cj_price)
                                           
session=return_session()
content=bs(session.get('https://cjdropshipping.com/list-detail').content)
content=content.find_all('div',{'class':'category-content'})
sub_categories_name_with_links=[]
sub_cat_links=[]
sub_cat_names=[]
for c in content:
  new_c=c.find_all('a')
  for new_C in new_c[1:]:#0-all the categories
        try:
            sub_categories_name_with_links.append({new_C.text.strip():(prime_link+new_C['href'])})
            sub_cat_links.append(prime_link+new_C['href'])
            sub_cat_names.append(new_C.text.strip())
        except Exception as KeyError:
            pass

bull_cj=cj_lookup_interest(session,sub_categories_name_with_links)
bull_cj.scrape_the_link()