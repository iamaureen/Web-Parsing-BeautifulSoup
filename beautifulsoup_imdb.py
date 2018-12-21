#reference: https://www.dataquest.io/blog/web-scraping-beautifulsoup/
from requests import get
from bs4 import BeautifulSoup



url = 'http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1'

response = get(url)
#print(response.text[:500])
html_soup = BeautifulSoup(response.text, 'html.parser')
#print(type(html_soup))

#lets use find_all() method to extract all the div containers with class attribute of lister-item mode-advanced:
movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')
#print(type(movie_containers))
#print('total number of movies in this page :: ',len(movie_containers))

#------------------------- get data for the first movie -----------------------------------------
first_movie = movie_containers[0]

#If we run first_movie.div, we only get the content of the first div tag:
#print(first_movie.div)

#accessing the first <h3> tag brings us very close to get the movie name
#print(first_movie.h3)

#output
# <h3 class="lister-item-header">
# <span class="lister-item-index unbold text-primary">1.</span>
# <a href="/title/tt3315342/?ref_=adv_li_tt">Logan</a>
# <span class="lister-item-year text-muted unbold">(2017)</span>
# </h3>

#now we can access the a tag with the movie name
print(first_movie.h3.a.text)

#get the movie year from the same div as movie name (check the output)
first_year = first_movie.h3.find('span', class_ = 'lister-item-year text-muted unbold')
print(first_year.text)

first_imdb = float(first_movie.strong.text)
print(first_imdb)

#there are many span tags, so we use specific class to get the specific span text
first_mscore = first_movie.find('span', class_ = 'metascore favorable')
first_mscore = int(first_mscore.text)
print(first_mscore)

# <span name="nv" data-value="316536">316536</span>
# name attribute is different from the class attribute. Using BeautifulSoup we can access elements by any attribute
first_votes = first_movie.find('span', attrs = {'name':'nv'})
print(first_votes.text) #outputs 524,269

#We could use .text notation to access the <span> tag's content.
# It would be better though if we accessed the value of the data-value attribute. This way we can convert the extracted datapoint
# to an int without having to strip a comma.
first_votes = int(first_votes['data-value'])
print(first_votes) #outputs 524269

#------------------------- get data for all the 50 movies (single page) -----------------------------------------
# Lists to store the scraped data in
names = []
years = []
imdb_ratings = []
metascores = []
votes = []

# Extract data from individual movie container
for container in movie_containers:

    # If the movie has Metascore, then extract:
    if container.find('div', class_ = 'ratings-metascore') is not None:

        # The name
        name = container.h3.a.text
        names.append(name)

        # The year
        year = container.h3.find('span', class_ = 'lister-item-year').text
        years.append(year)

        # The IMDB rating
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)

        # The Metascore
        m_score = container.find('span', class_ = 'metascore').text
        metascores.append(int(m_score))

        # The number of votes
        vote = container.find('span', attrs = {'name':'nv'})['data-value']
        votes.append(int(vote))


import pandas as pd

test_df = pd.DataFrame({'movie': names,
                       'year': years,
                       'imdb': imdb_ratings,
                       'metascore': metascores,
                       'votes': votes})
print(test_df.info())

test_df.to_csv("movieimdb.csv", sep=',', encoding='utf-8')

