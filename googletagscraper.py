from bs4 import BeautifulSoup
from bs4 import Comment
from urllib.request import Request, urlopen
import re
import csv  


# Place URLs to scrape here
urls = [
'http://www.google.com',
'https://www.apple.com/',

]

# Place strings and number of characters after the string to return here
search_str = [['GTM-', 8], ['UA-', 11], ['G-', 10],]

data = []

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}


def searchStr(s,n,src):
    search_num = s + '.{' + str(n) + '}'
    tag = re.findall(r'({})'.format(search_num), src)
    if tag != []:
        return tag


for url in urls:
    try:
        req = Request(url, headers=headers)
        webpage = urlopen(req)
        
        soup = BeautifulSoup(webpage, 'html.parser')
        source = str(soup)
        comments = str(soup.find_all(string=lambda text: isinstance(text, Comment)))
        
        print(url)

        foundtags = []
        for item in search_str:
            srcsearch = searchStr(item[0], item[1], source)
            comsearch = searchStr(item[0], item[1], comments)
            if srcsearch != None:
                print(str(srcsearch))
                foundtags.append(srcsearch)
            if comsearch != None:
                print(str(comsearch))
                foundtags.append(comsearch)
        for tag in foundtags:
            data.append([url, tag])
        

    except:
        print(url + " - Error!!")
        data.append([url, 'Error!!'])

# Add name of CSV file here
with open('googletags.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    header = ['Site URL', 'Google Tags']
    writer.writerow(header)
    writer.writerows(data)