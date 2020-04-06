import difflib
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application.models import Recipe, Ingredient, IngredientRecipe
import json

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

ingredients_set = set()
with open('train.json') as json_file:
    data = json.load(json_file)
for element in data:
    for ing in element['ingredients']:
        ingredients_set.add(ing)

with open('data_food.json') as json_file:
    recipes = json.load(json_file)
    for recipe in recipes:
        title = recipe['title']
        directions = recipe['directions']
        img = recipe['img']
        url = recipe['url']
        ingredients = recipe['ingredients']
        ingredients_display = recipe['ingredientsDisplay']
        new_recipe = Recipe(title, directions, img, url)
        db.session.add(new_recipe)
        db.session.flush()
        for ingredient, ingredient_display in zip(ingredients, ingredients_display):
            ing_title_matches = difflib.get_close_matches(ingredient, ingredients_set)
            if ing_title_matches:
                ing_title = ing_title_matches[0]
            ingredient_id = db.session.query(Ingredient.id).filter_by(title=ing_title).scalar()
            if ingredient_id is None:
                new_ingredient = Ingredient(ing_title)
                db.session.add(new_ingredient)
                db.session.flush()
                ingredient_id = new_ingredient.id
            new_recipe_ingredient = IngredientRecipe(new_recipe.id, ingredient_id, ingredient_display)
            db.session.add(new_recipe_ingredient)
            db.session.flush()
    db.session.commit()
