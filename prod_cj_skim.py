import requests
from bs4 import BeautifulSoup as bs


def get_cj_csrf_token(cj_link='https://cjdropshipping.com'):
    '''
    Usage
    get the csrf token 
    '''
    response = requests.get(cj_link)
    Cookies=list(response.cookies )
    # printing request cookies
    return str(Cookies[-1]).split(' ')[1].split('=')[1]#splitting the string to get the csrf

class scrape_it(): 

    '''
    Usage
     This class is used to scrape the pages exclusively for CJ_DROPSHIPPING.
     This class to be used for initial fresh scrapping only 
     
    returns
      type: lists
      desc:all the parameters local variables parameters
      
        
    Arguments
     scrape_till_page: number of pages to scrape
     session:for the particular session
    
    Local Variables
     cj_links:products details page lise
     cj_price:products original price
     cj_img:products images
     cj_interest:people who added to their lists 
    
    functions
      #get csrf and redirect to page - ok
      #get staring product details (name,images,product link,original price)-ok
      
      #todo
      #get individual sku and dropshipping price
      #store the product details
      #observe the interest with individual products
      
      #!!!!!!!!!!!!Social proofing!!!!!!!!!
      
      #possibilities
      #get product genre and type and check google trend 
      #check  reviews 
      #check google images and skim data 
      #
    '''
    global cj_links
    global cj_price
    global cj_img
    global cj_interest
    cj_links=[]
    cj_price=[]
    cj_img=[]
    cj_interest=[]
    scrape_till_page=20
    #need to change global afterwards to self
    def connect_to_site(link):
            session=requests.Session()
            jar=requests.cookies.RequestsCookieJar()
            prime_link='https://cjdropshipping.com'
            cj_csrf=get_cj_csrf_token(link)
            jar.set('csrfToken',cj_csrf)
            session.cookies=jar
            return session
        
    def get_cj_csrf_token(cj_link='https://cjdropshipping.com'):
        # ->get the csrf token of the site 
        response = requests.get(cj_link)
        Cookies=list(response.cookies)
        return str(Cookies[-1]).split(' ')[1].split('=')[1]#splitting the string to get the csrf

    def get_cj_location(session,link):
        return bs(session.get(link).content)
     
    def get_cj_links(location,session):
        return list(map(lambda temp_var: temp_var['href'],location.find_all("a",{'class':'detail-anchor'})))
           
    def get_cj_price(location,session):
       return list(map(lambda temp_var: temp_var.getText(),location.find_all("div",{'class':'price'})))
           
    def get_cj_interest(location,session):
       return list(map(lambda total_link:total_link.getText().split('\n')[3], location.findAll("span",{'class':'list'})))
     
    def get_cj_img(location,session):
         images=list(map(lambda img_var: ((img_var.find('img'))),location.find_all("a",{'class':'detail-anchor'})))
        # print(list(map(lambda img_var: ((print(img_var['src']))),images)))
         images = list(filter(None, images))#removing none values
         images_link=list(map(lambda image_link:image_link['src'],images))
         images_text=list(map(lambda image_link:image_link['alt'],images))
         return [images_link,images_text]
    session=connect_to_site('https://cjdropshipping.com')#with csrf binded
    location='' 
    for pages in range(0,scrape_till_page):
        
        try:
            print(pages)
            if pages==0:
                location=get_cj_location(session,'https://cjdropshipping.com/list-detail?feildType=1&isAsc=0')
                cj_links=get_cj_links(location,session)
                cj_price=get_cj_price(location,session)
                cj_img=get_cj_img(location,session)
                cj_interest=get_cj_interest(location,session)
            else:
                location=get_cj_location(session,'https://cjdropshipping.com/list-detail?feildType=1&isAsc=0&pageNum={}&pageSize=60'.format(pages))
                cj_interest=cj_interest+get_cj_interest(location,session)
                cj_links=cj_links+get_cj_links(location,session)
                cj_price=cj_price+get_cj_price(location,session)
                cj_img=cj_img+get_cj_img(location,session)#list of lists consists image_link and image text
        except Exception as e :
            print(e)
            pass
        
        def return_the_info(dummy):
            """
            return format list,list,list,*list of lists*(for images so 0->image_link,1->image_text)
            """
          return cj_interest,cj_links,cj_price,cj_img[0],cj_img[1]
        
prods=scrape_it()


