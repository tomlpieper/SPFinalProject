# Required Libraries
import requests  # to send HTTP requests
from bs4 import BeautifulSoup  # for parsing HTML documents
import os  # for OS-level operations
from tqdm import tqdm  # for progress bar
import pandas as pd  # for data manipulation and analysis
from loguru import logger  # for logging
import time  # for time-related tasks
import datetime  # for working with dates
from datetime import date  # to get the date
import seaborn as sns  # for data visualization
import matplotlib.pyplot as plt  # for creating static, animated, and interactive visualizations in Python
import numpy as np  # for numerical operations

# from db_connector import DB_Connector  # Local DB Connector Module (File is not provided)
from plotter import DataFramePlotter  # Local Plotter Module (File is not provided)

# The Scraper Class
class Scraper():

    # Class initialization method
    def __init__(self, db_connector):
        # Connecting to the database
        self.db_connector = db_connector
        # Get current working directory
        self.path = os.getcwd()

    # Method to get HTML from URL
    def get_html_from_url(self,url):
        # Headers to send along with the request
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        # Send HTTP request to site and save the response from server in a response object called r
        r = requests.get(url, headers=headers)
        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(r.text, 'html.parser')
        # Extract the desired info (the offers in this case)
        # The selector depends on the structure of the webpage, inspect the webpage to find the right selector
        offers = soup.select('div.offer')

        # Keep trying the request if a rate limit or server error is encountered
        while True:
            response = requests.get(url)

            # HTTP 429 means Too Many Requests / 500 server error
            if response.status_code == 429:
                print("Hit rate limit, sleeping for a bit...")
                time.sleep(5)  # Wait for 5 seconds before trying again
                continue
            # Any other error than rate limit
            if response.status_code != 200:
                print("Encountered Server Error, sleeping for a bit longer...")
                time.sleep(240)  # Wait for 240 seconds before trying again
                continue

            # If the response was not a 429 or 500, break the loop
            break

        # Return the text of the response
        return response.text

    # Method to find all instances of a substring in a string and yield a section of the string around the substring
    def find_all(self,string, substring):
        start = 0
        while True:
            start = string.find(substring, start)
            if start == -1: return
            end = start + 100
            yield string[start:end]
            start += len(substring) # use start += 1 to find overlapping matches

    # Method to get an overview of all categories of products for men and women
    def get_cat_overview(self,url):
        # Get HTML from the URL
        page = self.get_html_from_url(url)

        # Substrings to look for
        substring_damen, substring_herren = "/damen", "/herren"

        # Use the find_all method to get all instances of the substrings
        cat_urls_uncut_damen = set(self.find_all(page, substring_damen))
        cat_urls_uncut_herren = set(self.find_all(page, substring_herren))

        # Lists to store the final URLs and names
        cat_urls_cut_damen, cat_urls_cut_herren, cat_names_damen, cat_names_herren = [],[],[],[]

        # Process the raw URLs to get the final URLs and names
        for i in cat_urls_uncut_damen:
            i = i.split(sep='\"')
            cat_urls_cut_damen.append("https://www.vinted.de{}".format(i[0]))
            cat_names_damen.append(i[0])

        for i in cat_urls_uncut_herren:
            i = i.split(sep='\"')
            cat_urls_cut_herren.append("https://www.vinted.de{}".format(i[0]))
            cat_names_herren.append(i[0])

        # Print the number of categories found
        print("We found {} categories for women on vinted that we can scrape".format(len(cat_urls_uncut_damen)))
        print("We found {} categories for men vinted that we can scrape".format(len(cat_urls_uncut_herren)))

        return cat_urls_cut_damen, cat_urls_cut_herren, cat_names_damen, cat_names_herren

        

# Filter for double values, just in case
    def filter_doubles(self,titles_cut):
        doubles = []
        for i in titles_cut:
            c = titles_cut.count(i)
            doubles.append((i,c))

        # Set function removes doubles from the doubles list
        set_d = set(doubles)

        names = list(set_d)
        return names


# For unique ID retireval, we sadly need to get each page and extract the TITLE form the top of th HTML
    def get_display_titles(self,cat_urls_cut,cat_names):

        display_titles = []
        c = 0
        # Monitor the progress with tqdm
        pbar = tqdm(total=len(cat_urls_cut))
        for url, name in zip(cat_urls_cut,cat_names):
            if c <= 4:
                c += 1
                # Send HTTP request to site and save the response from server in a response object called r
                r = requests.get(url)
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
                pbar.update()

        pbar.close()
        titles_cut = []
        # HTML Parsing and selection
        for title in display_titles:
            title = title[7:]
            title = title.replace("&amp;","\\u0026") # Here we replace the HTML version of and by a bit version, we will change this later back
            titles_cut.append(title)
        return titles_cut

# Wrapper function, to get titles for each category
    def get_display_titles_wrapper(self,cat_names_damen,cat_names_herren, cat_urls_cut_damen, cat_urls_cut_herren):

        # for both genders get the titles
        display_titles_damen = self.get_display_titles(cat_urls_cut_damen,cat_names_damen)
        display_titles_herren = self.get_display_titles(cat_urls_cut_herren,cat_names_herren)

        # Again for both genders, filter the doubles, so we get clean data
        titles_cut_with_count_damen = self.filter_doubles(display_titles_damen)
        titles_cut_with_count_herren = self.filter_doubles(display_titles_herren)

        return titles_cut_with_count_damen, titles_cut_with_count_herren


    # A HTML parsing function, that gets a string and returns a property as substring, as well as the name of the property 
    def get_single_property(self, str:str,p:str):
        i = str.find(p)
        sub = str[i:]
        sub = sub.split(",")
        sub = sub[0]
        prop_len = len(p)
        name = sub[:prop_len]
        sub = sub[prop_len+1:]
        return name, sub



    # Here for the overview page, we try to get the general info, that we can already exctract, e.g. item count, title, code etc.
    def get_dataframe(self, url, names, properties):

        # Get the HTMl to parse
        index_page = self.get_html_from_url(url)

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
                    name, value = self.get_single_property(sub, p)
                    dict_props[p] = value


                # convert the dictionary to a pandas DataFrame
                df = pd.DataFrame(dict_props, index=[0])
                yield df

    # Here we have the same function that yields a pandas.df from wanted properties of a single category by HTML parsing
    def get_dataframe_category(self, html,subs, props):

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
                name, value = self.get_single_property(sub, p)
                dict_props[p] = value


            # convert the dictionary to a pandas DataFrame
            df = pd.DataFrame(dict_props, index=[0])

            yield df

    # Here we get more detailed values for the announces of a single category and again yield it as a pandas.df
    def get_announces_by_category(self, category_id, nr_pages, props):

        # The properties, we want to know, that we could filter by
        properties_announce = ['id','title','price','brand_title','size_title','user:id','login','profile_url'] 

        for page in tqdm(range(nr_pages), leave=False):
            try:
                    
                url = "https://www.vinted.de/catalog?catalog[]={}&page{}".format(category_id,page+1)

                html_string = self.get_html_from_url(url)


                l = list(self.get_items_ids(html_string))
                unique_id_references = ["\"id\":"+i for i in l]
                # print(unique_id_references)

                announces = list(self.get_dataframe_category(html=html_string, subs=unique_id_references, props= props))

                announces_df = pd.concat(announces)

                yield announces_df
                
            except Exception as e:
                logger.error("Error getting Category Information".format(e))

    # Functoin to retrieve the IDs that each category has, they are needed to get the urls, if we want to scrape page 2 or bigger of some category
    # basically consists of a lot of substring parsing and splitting
    def get_items_ids(self, page):
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
        for i in splt:
            yield i

    # Scraper internal function to access and save data to our local database
    def save_to_Database(self, db,df):    
        print("Function called", flush=True)
        today = date.today()
        docs = None
        docs = db.retrieve_data(today)
        # Check if the df returned is non-empty
        if not docs.empty :
            print(docs,flush=True)

        else:
            print("Returned nothing form db", flush=True)


    # Function to be called from the outside, basically wrapper that uses all the predefined functions to scrape vinted.de
    def scrape(self, scheduled):
 


        # Define the URL of the site
        url = f"https://www.vinted.de/"
        properties = ['id','title','code','item_count','url']
        properties_announce = ['id','title','price','brand_title','size_title','user:id','login','profile_url'] 

        # Get CatNames
        cat_urls_cut_damen, cat_urls_cut_herren, cat_names_damen, cat_names_herren = self.get_cat_overview(url)
        # Get the titles from sub-sites
        display_titles_women, display_titles_men = self.get_display_titles_wrapper(cat_names_damen,cat_names_herren,cat_urls_cut_damen, cat_urls_cut_herren)

        
        dfs_women = list(self.get_dataframe(url, display_titles_women,properties))
        dfs_men = list(self.get_dataframe(url, display_titles_men,properties))
        combined_women = pd.concat(dfs_women)
        combined_men = pd.concat(dfs_men)

        combined_women['gender'] = 'w'
        combined_men['gender'] = 'm'

        df = pd.concat([combined_women, combined_men])

        # Check that the values in id are actually useful numeric ints, otherwise remove the row in the dataframe
        df = df[df['id'] != 'null']
        df['overview'] = 1
        df['title'] = df['title'].str.replace('\\u0026', '&')
        df['id'] = pd.to_numeric(df['id'], errors='coerce')
        df = df.dropna(subset=['id'])
        df['id'] = df['id'].astype(np.int64)

        # Create lists for looping
        cat_ids = df['id'].values.tolist()
        cat_titles = df['title'].values.tolist()


        # Get information about the single categories and announces
        pbar = tqdm(total=len(cat_ids))
        for i, j in zip(cat_ids, cat_titles):
            try:
                announces = list(self.get_announces_by_category(i, 3, properties_announce))
                df_cat = pd.concat(announces)
                df_cat['cat_id'] = i
                df_cat['cat_title'] = j
                df_cat['overview'] = 0
                # db.save_data(df_cat)
                df =  pd.concat([df, df_cat])
                pbar.update()
            except Exception as e:
                print(e)
        pbar.close()

        # replace the bit version before saving, so the plotting looks nice
        df['title'] = df['title'].str.replace('\\u0026', '&')

        # Save to MongoDB Database
        try:
            self.db_connector.save_data(df)
        except Exception as e:
            logger.exception(e)
        # For the scheduled version of this function, there is no df returned, it is just saved to the DB
        # The return is just for the direct version that is initiated by the user/bot interaction
        if not scheduled:
            return df




