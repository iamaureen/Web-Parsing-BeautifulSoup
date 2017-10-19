#ref 1: https://www.dataquest.io/blog/web-scraping-tutorial-python/
#ref 2: http://docs.python-requests.org/en/master/api/
import requests
from bs4 import BeautifulSoup
import json


page = requests.get("https://brainly.com/")
print(page) #prints response object
print(page.status_code) #prints status_code property
#print(page.content) #prints the HTML content of the website (in bytes)
#print(page.text) #prints the HTML content of the website (in unicode)
page_content = page.text

#parse this document using BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify()) #prints the byte content in html format

#select all the elements at the top level of the page using the children property of soup
#print(list(soup.children)) #output: ['\n', 'html', '\n', <html lang="en-US"> ....]
# select html tag and its children by taking the fourth element in the list
#html = list(soup.children)[3]
#print(list(html.children))
# but these are cumbersome. we can use specific methods to extract tags and elements
#print(soup.find_all('p')) #returns 2 <p> items #this returns a list

# find_all returns a list, so we’ll have to loop through, or use list indexing, it to extract text:
#print(soup.find_all('p')[1].get_text())

# search for any div tag that has the class "sg-content-box__content":
#print(soup.find_all('div', class_='sg-content-box__content'))

# look for any tag that has the class "sg-content-box__content":
#print(soup.find_all(class_='sg-content-box__content'))

# finds a tag inside div tag
#print(soup.select("div a"))
# -----------------------------------------------------------------------------------


