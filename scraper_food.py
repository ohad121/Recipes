# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import json
import gc
from selenium import webdriver

urlList = [line.strip() for line in open('urlList.txt')]
driver = webdriver.Firefox()
# delete repeats
urlList = list(set(urlList))

i = 0
dictionaryList = []
for url in urlList:
    try:
        i += 1
        print(i)
        print(url)
        # clear dictionaryTemp
        dictionaryTemp = {}

        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html')

        # recipe title
        recipe_title = soup.find_all('div', {'class': 'recipe-title'})[0].text
        recipe_img = soup.find('div', {'class': 'recipe-image theme-gradient'})
        if recipe_img is not None:
            recipe_img = recipe_img.img['src']

        link = driver.find_element_by_link_text('CLICK TO SEE FULL RECIPE')
        link.click()

        ingredients = []
        ingredients_display = []
        for ultag in soup.find_all('ul', {'class': 'recipe-ingredients__list'}):
            for litag in ultag.find_all('li'):
                ingredient = litag.find('a')
                ingredient_display = re.sub(' +', ' ', litag.text).lstrip(' ')
                if ingredient is not None:
                    ingredients.append(ingredient.text)
                else:
                    ingredients.append(ingredient_display)
                ingredients_display.append(ingredient_display)

        recipe_directions = ""
        for ultag in soup.find_all('ul', {'class': 'recipe-directions__steps'}):
            for litag in ultag.find_all('li'):
                recipe_directions += litag.text + '\n'

        dictionaryTemp = {"title": recipe_title,
                          "ingredients": ingredients,
                          "ingredientsDisplay": ingredients_display,
                          "directions": recipe_directions,
                          "img": recipe_img,
                          "url": url}
    except Exception as e:
        print("Error with: %s exception: %s", url, e)
        continue
    dictionaryList.append(dictionaryTemp)

del recipe_title, ingredients, ingredients_display, recipe_directions, recipe_img, url, i, urlList

with open("data_food.json", "w") as f:
    json.dump(dictionaryList, f)

del dictionaryList
gc.collect()
