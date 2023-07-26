import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
import pandas as pd
from loguru import logger
import time
import datetime
from datetime import date
# from db_connector import DB_Connector
from plotter import DataFramePlotter







def get_html_from_url(url):


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Send HTTP request to site and save the response from server in a response object called r
    r = requests.get(url, headers=headers)

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(r.text, 'html.parser')

    # Extract the desired info (the offers in this case)
    # The selector depends on the structure of the webpage, inspect the webpage to find the right selector
    offers = soup.select('div.offer')

    while True:
        response = requests.get(url)

        if response.status_code == 429:  # HTTP 429 means Too Many Requests
            print("Hit rate limit, sleeping for a bit...")
            time.sleep(10)  # Wait for 10 seconds before trying again
            continue

        # If the response was not a 429, break the loop
        break

    # You might also want to check here if the response was a 200 OK
    # If not, you could raise an exception or return some default value
    if response.status_code != 200:
        print(f"Got unexpected status code {response.status_code}")
        return None

    return response.text


def find_all(string, substring):
    start = 0
    while True:
        start = string.find(substring, start)
        if start == -1: return
        end = start + 100
        yield string[start:end]
        start += len(substring) # use start += 1 to find overlapping matches


def get_cat_overview(url):


    page = get_html_from_url(url)

    substring_damen, substring_herren = "/damen", "/herren"


    cat_urls_uncut_damen = set(find_all(page, substring_damen))
    cat_urls_uncut_herren = set(find_all(page, substring_herren))



    cat_urls_cut_damen, cat_urls_cut_herren, cat_names_damen, cat_names_herren = [],[],[],[]


    for i in cat_urls_uncut_damen:
        i = i.split(sep='\"')
        cat_urls_cut_damen.append("https://www.vinted.de{}".format(i[0]))
        cat_names_damen.append(i[0])
        # print(i)

    for i in cat_urls_uncut_herren:
        i = i.split(sep='\"')
        cat_urls_cut_herren.append("https://www.vinted.de{}".format(i[0]))
        cat_names_herren.append(i[0])

    print("We found {} categories for women on vinted that we can scrape".format(len(cat_urls_uncut_damen)))
    print("We found {} categories for men vinted that we can scrape".format(len(cat_urls_uncut_herren)))
    # for name in cat_names_damen:
    #     print(name)
    return cat_urls_cut_damen, cat_urls_cut_herren, cat_names_damen, cat_names_herren
    


def filter_doubles(titles_cut):
    doubles = []
    for i in titles_cut:
        c = titles_cut.count(i)

            # print("Title: {} occured {} times.".format(i,c))
        doubles.append((i,c))

    set_d = set(doubles)
    # for i in set_d:
        # print(i)
    names = list(set_d)
    return names

def get_display_titles(cat_urls_cut,cat_names):

    c = 0
    display_titles = []
    for url, name in tqdm(zip(cat_urls_cut,cat_names)):
        if c <= 10:
            # Send HTTP request to site and save the response from server in a response object called r
            r = requests.get(url)
            c += 1
            # print(c)
            
            # Get the index of display title 
            index_title = r.text.find("<title>")
            title_uncut = r.text[index_title:index_title+100]
            splt = title_uncut.split(sep=" |")
            display_titles.append(splt[0])

            # Create a BeautifulSoup object and specify the parser      
            soup = BeautifulSoup(r.text, 'html.parser')
            filename = "%s.txt" % name[1:]
            filename = filename.replace("/","_")


    titles_cut = []
    for title in display_titles:
        title = title[7:]
        title = title.replace("&amp;","\\u0026")
        titles_cut.append(title)
    return titles_cut

def get_display_titles_wrapper(cat_names_damen,cat_names_herren, cat_urls_cut_damen, cat_urls_cut_herren):
    sub_path = path + '/categories'
    if not os.path.exists(sub_path):
        os.makedirs(sub_path)
    # print(sub_path)

    display_titles_damen = get_display_titles(cat_urls_cut_damen,cat_names_damen)
    display_titles_herren = get_display_titles(cat_urls_cut_herren,cat_names_herren)

    
    titles_cut_with_count_damen = filter_doubles(display_titles_damen)
    titles_cut_with_count_herren = filter_doubles(display_titles_herren)

    return titles_cut_with_count_damen, titles_cut_with_count_herren



def get_single_property(str:str,p:str):
    i = str.find(p)
    sub = str[i:]
    sub = sub.split(",")
    sub = sub[0]
    prop_len = len(p)
    name = sub[:prop_len]
    sub = sub[prop_len+1:]
    return name, sub




def get_dataframe(url, names, properties):

    index_page = get_html_from_url(url)

    for i in names:
        start = 0
        for j in range(i[1]):
            
            list_name = []
            dict_props = {}
            ind = index_page.find(i[0], start)
            
            # Get rough length to be cut 
            sub = index_page[ind-20:ind+1000]
            
            # Assign the new start for str.find() as to not retrieve the same index 2x
            start = ind + len(sub)


            sub = sub.replace("{","")
            sub = sub.replace("\"","")

            # Obtain all single desired properties of substring
            for p in properties:
                name, value = get_single_property(sub, p)
                dict_props[p] = value


            # convert the dictionary to a pandas DataFrame
            df = pd.DataFrame(dict_props, index=[0])
            yield df


def get_dataframe_category(html,subs, props):

    for i in subs:
        dict_props = {}
        ind = html.find(i)
        
        # Get rough length to be cut 
        sub = html[ind:ind+5000]
        splt = sub.split("\",\"content_source\"")
        sub = splt[0]    


        sub = sub.replace("{","")
        sub = sub.replace("\"","")

        # Obtain all single desired properties of substring
        for p in props:
            name, value = get_single_property(sub, p)
            dict_props[p] = value


        # convert the dictionary to a pandas DataFrame
        df = pd.DataFrame(dict_props, index=[0])
        # print(df.head())

        yield df


def get_announces_by_category(category_id, nr_pages, props):

    properties_announce = ['id','title','price','brand_title','size_title','user:id','login','profile_url'] 

    for page in tqdm(range(nr_pages)):
        try:
                
            url = "https://www.vinted.de/catalog?catalog[]={}&page{}".format(category_id,page+1)
            # print(url)
            html_string = get_html_from_url(url)
            # print(html_string)

            l = list(get_items_ids(html_string))
            unique_id_references = ["\"id\":"+i for i in l]
            # print(unique_id_references)

            announces = list(get_dataframe_category(html=html_string, subs=unique_id_references, props= props))

            announces_df = pd.concat(announces)
            # print(announces_df.head())
            # time.sleep(2)
            yield announces_df
            
        except Exception as e:
            logger.exception(e)

def get_items_ids(page):
    length = 1500
    s = "{\"catalogItems\":{\"ids\":"
    index = page.find(s)
    sub = page[index:index+length]

    # Remove everything around the ids
    splts = sub.split("[")
    sub = splts[1]
    splts = sub.split("]")
    sub = splts[0]
    
    splt = sub.split(",")
    # time.sleep(0.2)
    # time.sleep(1)
    for i in splt:
        yield i


def save_to_Database(db,df):    
    print("Function called", flush=True)
    today = date.today()
    docs = None
    docs = db.retrieve_data(today)
    if docs != None:
        print(docs,flush=True)
    else:
        print("Returned nothing form db", flush=True)



if __name__ == "__main__":


# Get MongoDB username, password, and hostname from environment variables
    username = os.environ['MONGO_USERNAME']
    password = os.environ['MONGO_PASSWORD']
    hostname = os.environ['MONGO_HOSTNAME']

    # db = DB_Connector(username=username,password=password,hostname=hostname)

    path = os.getcwd()


    # Define the URL of the site
    url = f"https://www.vinted.de/"
    properties = ['id','title','code','item_count','url']
    properties_announce = ['id','title','price','brand_title','size_title','user:id','login','profile_url'] 

    # Get CatNames
    cat_urls_cut_damen, cat_urls_cut_herren, cat_names_damen, cat_names_herren = get_cat_overview(url)

    display_titles_women, display_titles_men = get_display_titles_wrapper(cat_names_damen,cat_names_herren,cat_urls_cut_damen, cat_urls_cut_herren)

    
    dfs_women = list(get_dataframe(url, display_titles_women,properties))
    dfs_men = list(get_dataframe(url, display_titles_men,properties))
    combined_women = pd.concat(dfs_women)
    combined_men = pd.concat(dfs_men)

    combined_women['gender'] = 'w'
    combined_men['gender'] = 'm'

    df = pd.concat([combined_women, combined_men])

    df = df[df['id'] != 'null']
    df['overview'] = 1
    df['title'] = df['title'].str.replace('\\u0026', '&')
    print(df.head())
    # Check that there is no duplicates in list and have a look into the df
  
    # db.save_data(df)


    # ==================================================
    # ========= Get announces by category ==============
    # ==================================================
    
    cat_ids = df['id'].values.tolist()
    cat_titles = df['title'].values.tolist()
    
    # cat_ids = cat_ids[cat_idss['id'].notna()]
    cat_ids = cat_ids[:4]
    print(cat_ids)
    for i, j in zip(cat_ids, cat_titles):
        
        announces = list(get_announces_by_category(i, 10, properties_announce))
        df_cat = pd.concat(announces)
        df_cat['cat_id'] = i
        df_cat['cat_title'] = j
        df_cat['overview'] = 0
        # db.save_data(df_cat)
        df =  pd.concat([df, df_cat])

    # test_df = db.retrieve_data(date=date.today())
    # df = pd.DataFrame(test_df)
    # df.to_csv('mydf.csv',index=False)
    print(df)
    print(type(df))
    print(df.shape[0])

    plotter = DataFramePlotter(df)
    plotter.plot_amount_categories_MW()
    plotter.plot_amount_announces_per_category()
    plotter.plot_average_price_per_category()

    # db.save_data(df)
    





