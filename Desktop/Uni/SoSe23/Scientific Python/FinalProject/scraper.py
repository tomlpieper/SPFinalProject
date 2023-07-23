import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
import pandas as pd
from loguru import logger
import time

path = os.getcwd()
# Specify the category you want to search in
# category = "herren/schuhe/sneaker"  # replace with the category you want






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


    # Get HTML text
    page = requests.get(url)
    return page.text


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
        i = "https://www.vinted.de{}".format(i[0])

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
    for i in set_d:
        print(i)
    names = list(set_d)
    return names

def get_display_titles(cat_names_damen,cat_names_herren, cat_urls_cut_damen, cat_urls_cut_herren):
    sub_path = path + '/categories'
    if not os.path.exists(sub_path):
        os.makedirs(sub_path)
    # print(sub_path)

    display_titles = []
    # c = 0
    for url, name in tqdm(zip(cat_urls_cut_damen,cat_names_damen)):
        # Send HTTP request to site and save the response from server in a response object called r
        r = requests.get(url)
        # c += 1
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

    titles_cut_with_count = filter_doubles(titles_cut)
    return titles_cut_with_count



def get_single_property(str:str,p:str):
    i = str.find(p)
    sub = str[i:]
    sub = sub.split(",")
    sub = sub[0]
    prop_len = len(p)
    name = sub[:prop_len]
    sub = sub[prop_len+1:]
    return name, sub




def get_dataframe(url, names,properties):

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




if __name__ == "__main__":

    # Define the URL of the site
    url = f"https://www.vinted.de/"
    properties = ['id','title','code','item_count','url']

    # Get CatNames
    cat_urls_cut_damen, cat_urls_cut_herren, cat_names_damen, cat_names_herren = get_cat_overview(url)

    display_titles = get_display_titles(cat_names_damen,cat_names_herren,cat_urls_cut_damen, cat_urls_cut_herren)

    dfs = list(get_dataframe(url, display_titles,properties))
    combined = pd.concat(dfs)

    # Check that there is no duplicates in list and have a look into the df
    print( True in combined['id'].duplicated())
    print(combined.head())


