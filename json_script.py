import difflib
import json




ingredients = set()
with open('train.json') as json_file:
    data = json.load(json_file)
for element in data:
    for ing in element['ingredients']:
        ingredients.add(ing)

difflib.get_close_matches('1 cup of olive oil', ingredients)

f = open("ingredients.txt", "w")
for ing in ingredients:
    f.write(ing + '\n')
f.close()

