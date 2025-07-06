import json

def load_inventory():
    with open('data/sample_inventory.json') as f:
        return json.load(f)

def suggest_meal(ingredients):
    if "egg" in ingredients:
        return "Omelette with toast"
    elif "rice" in ingredients and "lentils" in ingredients:
        return "Dal and Rice"
    elif "bread" in ingredients and "cheese" in ingredients:
        return "Grilled cheese sandwich"
    else:
        return "No idea today! Try adding more ingredients."

if __name__ == "__main__":
    inventory = load_inventory()
    print("Your ingredients:", inventory)
    meal = suggest_meal(inventory)
    print("Suggested Meal:", meal)
