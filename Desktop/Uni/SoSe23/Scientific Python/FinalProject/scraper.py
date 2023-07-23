import requests
from bs4 import BeautifulSoup

# Specify the category you want to search in
category = "herren/schuhe/sneaker"  # replace with the category you want
print("Bla")

# Define the URL of the site
url = f"https://www.vinted.de/{category}"
url = f"https://www.vinted.de/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Send HTTP request to site and save the response from server in a response object called r
r = requests.get(url, headers=headers)

# Create a BeautifulSoup object and specify the parser
soup = BeautifulSoup(r.text, 'html.parser')

# Extract the desired info (the offers in this case)
# The selector depends on the structure of the webpage, inspect the webpage to find the right selector
offers = soup.select('div.offer')

# Loop over the offers and print each one
# for offer in offers:
#     print(offer.text)

# Get response code
print(r)

# Get HTML text
page = requests.get(url)
# print(page.text)
with open ("test.txt",'w') as f:
    f.write((str(page.text)))


def find_all(string, substring):
    start = 0
    while True:
        start = string.find(substring, start)
        if start == -1: return
        yield start
        start += len(substring) # use start += 1 to find overlapping matches


substring = "WOMEN"

matches = list(find_all(page.text, substring))
print(matches)
print(len(matchesW))




# with open ("test.txt",'r') as f:
#     for line in f:
#         if "data-" in line:
#             print(line)     

# for line in page.text:
#     # if "\"code\":\"WOMEN\"" in line:
#     print(line)


print("The boy said \"Hello!\" to the girl")

    

