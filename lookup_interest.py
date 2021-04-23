import functools
import operator
import os

class interest_spike():
   '''
    looks up the file and collect the data and gives up the interest 
   '''
    
    def collect_the_files(self):
        return (os.listdir('cj_prods_list/'))

    def lookup_interest_keys(repeating_keys):
         return list(set(functools.reduce(operator.iconcat,repeating_keys, [])))

    def check_interest_spike(interest_list):
        interest_spike=[]
        for i_prod in interest_list:
            for k,v in i_prod.items():
                interest_spike.append({k:(int(max(v))-int(min(v)))})
        return interest_spike
    def lookup_interest(filesList):
        filesList=os.listdir('cj_prods_list/')
        #get unique names in repeting list
        #make dict of list of interest of unique names 
                 #or
        #directly calculate the elevation of interest over a peiod of time  
        whole_content=[]
        for file in filesList:
            my_file = open('cj_prods_list/'+file, "r")
            content_list = eval(my_file.read())
            #print(content_list.keys())
            whole_content.append((content_list))
        whole_content_unique_keys = lookup_interest_keys(whole_content)

        main_interest=[]
        for a_key in  whole_content_unique_keys:
             seller_interest_data=[]#for every unique key prepare a list of seller interst in the specific product
             for a_dict in  whole_content:
                    try: 
                        #print(str(a_key)+str(a_dict[a_key]))
                        seller_interest_data.append(a_dict[a_key])
                    except Exception as KeyError:
                        pass
             main_interest.append({a_key:seller_interest_data})
        spike=check_interest_spike(main_interest)
        return spike



lookup=interest_spike()
lookup.lookup_interest()