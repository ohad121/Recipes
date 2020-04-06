# -*- coding: utf-8 -*-
"""
Takes a list of URLs from allrecipes.com
"""
import time
from urllib.request import urlopen
# import pandas as pd
from bs4 import BeautifulSoup
import re
import pickle
# from sys import setrecursionlimit
import json
import gc

# use pickle to import the scraped URLs from scrapeURLs.py
# urlList = pickle.load(open("urlList.p", "rb"))
urlList = [line.strip() for line in open('urlList.txt')]

# delete repeats
urlList = list(set(urlList))
urlList2 = urlList[0:1000]

i = 0
dictionaryList = []

for url in urlList2:
    i += 1
    print(i)
    print(url)
    # clear dictionaryTemp
    dictionaryTemp = {}

    # Query the website and return the html to the variable 'page'
    page = urlopen(url)
    # time.sleep(3)
    # Parse the html in the 'page' variable, and store it in Beautiful Soup format
    soup = BeautifulSoup(page, "lxml")

    # print(soup.prettify())

    # return content between openeing an closing tag, including tag
    # soup.span.recipe-ingred_txt.added
    htmlIngredients = soup.find_all('span', {'class': "recipe-ingred_txt added"})

    # make empty list for ingredient list
    ingredientList = []
    ingredientIdList = []
    # iterate throught the list of tags to extract the ingredients
    for ingredient in htmlIngredients:
        ingredientList.append(ingredient.string)

        temp = re.search('(?<=data-nameid=")(\d*)(?=")', str(ingredient)).group(1)
        ingredientIdList.append(temp)

    img_v1 = soup.find('img', {'class': 'rec-photo'})
    if img_v1 is not None:
        imgURL = img_v1["src"]
    else:
        imgURL = soup.find('div', {'class': 'image-container'}).find('div', {'class': 'lazy-image'})['data-src']

    rec_directions = ""
    for direction in soup.findAll('span', {'class': 'recipe-directions__list--item'}):
        rec_directions += direction.text.strip() + '\n'

    if rec_directions == "":
        for direction in soup.findAll('ul', {'class': 'instructions-section'})[0].find_all("p"):
            rec_directions += direction.text.strip() + '\n'

    # get the title
    header_v1 = soup.find_all("h1", {'class': "recipe-summary__h1"})
    header_v2 = soup.find_all("h1", {'class': "headline heading-content"})
    if header_v1:
        title = header_v1[0].text
    else:
        title = header_v2[0].text

    re.sub(r'\W+', ' ', title)

    dictionaryTemp = {"title": title,
                      "ingredients": ingredientList,
                      "ingredientIDs": ingredientIdList,
                      "directions": rec_directions,
                      "img": imgURL,
                      "url": url}

    dictionaryList.append(dictionaryTemp)

del temp, dictionaryTemp, ingredientIdList, ingredientList
del urlList, urlList2, title, url, i

# this makes a ~600 mb file for just 1000 recipes. Use JSON instead.
# setrecursionlimit(10000)
# pickle.dump(dictionaryList, open( "dictionary.p","wb" ))
# setrecursionlimit(1000)

with open("data.json", "w") as f:
    json.dump(dictionaryList, f)

del dictionaryList
gc.collect()

# test to see if it loads properly
# text = open("dictionary0001-1000.json", "r").read()
# dictionaryListLoad = json.loads(text)
# text = open("dictionary1001-4000.json", "r").read()
# dictionaryListLoad1 = json.loads(text)

# df = pd.DataFrame.from_dict(dictionaryList)

# use pandas to convert list to data frame
# df = pd.DataFrame(title,columns=['Title'])
# df['Rating']=strRating
# df['# of Reviews']=strReviews
# df['URL']=url
# df['Ingredients']=ingredientList
# df['Ingredient ID List']=ingredientIdList
#
# df
