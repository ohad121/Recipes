from . import db, ma


# Recipe Class/Model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    directions = db.Column(db.String(200))
    img = db.Column(db.String(200))
    url = db.Column(db.String(200))

    def __init__(self, title, directions, img, url):
        self.title = title
        self.directions = directions
        self.img = img
        self.url = url


class RecipeSchema(ma.Schema):
    class Meta:
        fields = ('title', 'ingredients', 'ingredients_display', 'missing_ingredients', 'directions', 'img', 'url')


recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)


# Ingredient Class/Model
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)

    def __init__(self, title):
        self.title = title


# Ingredient Schema
class IngredientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title')


ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)


class IngredientRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, unique=False)
    ingredient_id = db.Column(db.Integer, unique=False)
    ingredient_display = db.Column(db.String, unique=False)

    def __init__(self, recipe_id, ingredient_id, ingredient_display):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.ingredient_display = ingredient_display


# Ingredient Schema
class IngredientRecipeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'recipe_id', 'ingredient_id', 'ingredient_display')


ingredient_recipe_schema = IngredientRecipeSchema()
