from flask import request, jsonify, current_app as app
from .models import db, Recipe, recipes_schema, recipe_schema, Ingredient, ingredient_schema, ingredients_schema, \
    IngredientRecipe


@app.route('/recipe', methods=['GET'])
def get_recipes():
    ingredients_ids_str = request.args.get('ingredients')
    if ingredients_ids_str:
        ingredients_ids = map(int, ingredients_ids_str.split(","))
        recipes = db.session.query(Recipe).join(IngredientRecipe, Recipe.id == IngredientRecipe.recipe_id) \
            .filter(IngredientRecipe.ingredient_id.in_(ingredients_ids)).all()
        for recipe in recipes:
            ingredients_display = []
            for ingredient_recipe in get_recipe_ingredient_by_recipe_id(recipe.id):
                ingredients_display.append(ingredient_recipe.ingredient_display)
            recipe.ingredients_display = ingredients_display
            missing_ingredients = []
            recipes_ingredient = get_ingredients_by_recipe_id(recipe.id)
            for ingredient in list(filter(lambda ing: str(ing.id) not in ingredients_ids_str.split(","),
                                          recipes_ingredient)):
                missing_ingredients.append(ingredient.title)
            recipe.missing_ingredients = missing_ingredients
        recipes.sort(key=lambda rec: len(rec.missing_ingredients))
    else:
        recipes = Recipe.query.all()
    result = recipes_schema.dump(recipes)
    return jsonify(result)


# Create a Recipe
@app.route('/recipe', methods=['POST'])
def add_recipe():
    title = request.json['title']
    description = request.json['directions']
    new_recipe = Recipe(title, description)
    db.session.add(new_recipe)
    db.session.commit()
    return recipe_schema.jsonify(new_recipe)


# Get All Recipes
@app.route('/recipe/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    ingredients = []
    for ingredient in get_ingredients_by_recipe_id(recipe_id):
        ingredients.append(ingredient.title)
    recipe.ingredients = ingredients
    ingredients_display = []
    recipes_ingredients = get_recipe_ingredient_by_recipe_id(recipe_id)
    for recipe_ingredient in recipes_ingredients:
        ingredients_display.append(recipe_ingredient.ingredient_display)
    recipe.ingredients_display = ingredients_display
    result = recipe_schema.dump(recipe)
    return jsonify(result)


# Create a Ingredient
@app.route('/ing', methods=['POST'])
def add_ingredient():
    title = request.json['title']
    new_ingredient = Ingredient(title)
    db.session.add(new_ingredient)
    db.session.commit()
    return ingredient_schema.jsonify(new_ingredient)


# Get All Ingredients
@app.route('/ingredients', methods=['GET'])
def get_ingredients():
    recipe_id = request.args.get('recipe_id')
    prefix = request.args.get('prefix')
    if recipe_id is not None:
        ingredients = get_ingredients_by_recipe_id(recipe_id)
    elif prefix is not None:
        ingredients = Ingredient.query.filter(Ingredient.title.startswith(prefix)).all()
    else:
        ingredients = Ingredient.query.all()
    result = ingredients_schema.dump(ingredients)
    return jsonify(result)


def get_recipe_ingredient_by_recipe_id(recipe_id):
    return db.session.query(IngredientRecipe).filter(IngredientRecipe.recipe_id == recipe_id).all()


def get_ingredients_by_recipe_id(recipe_id):
    return db.session.query(Ingredient). \
        join(IngredientRecipe, Ingredient.id == IngredientRecipe.ingredient_id) \
        .filter(IngredientRecipe.recipe_id == recipe_id).all()
