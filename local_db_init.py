import sqlite3
import random

# Comprehensive grocery items with multiple brands
grocery_items = [
    # PIZZA INGREDIENTS (Original items with enhanced details)
    ("All-purpose flour", "DOUGH-FLOUR-500G-GOLD", "Gold Medal", 1, "500g", "baking", 280, 12, 2, 58, 1, "Contains: Gluten", 3.49),
    ("All-purpose flour", "DOUGH-FLOUR-500G-KING", "King Arthur", 1, "500g", "baking", 290, 11, 1, 60, 0, "Contains: Gluten", 4.29),
    ("All-purpose flour", "DOUGH-FLOUR-500G-PILLA", "Pillsbury", 1, "500g", "baking", 275, 10, 1, 57, 2, "Contains: Gluten", 3.79),
    
    ("Active dry yeast", "DOUGH-YEAST-10G-FLEISCH", "Fleischmann's", 1, "10g", "baking", 35, 4, 0, 5, 0, "None", 2.99),
    ("Active dry yeast", "DOUGH-YEAST-10G-REDSTAR", "Red Star", 1, "10g", "baking", 32, 4, 0, 4, 1, "None", 2.79),
    
    ("Sugar", "DOUGH-SUGAR-500G-DOMINO", "Domino", 1, "500g", "baking", 1935, 0, 0, 500, 500, "None", 2.89),
    ("Sugar", "DOUGH-SUGAR-500G-CRYSTAL", "Crystal", 1, "500g", "baking", 1940, 0, 0, 500, 500, "None", 2.69),
    
    ("Salt", "DOUGH-SALT-500G-MORTON", "Morton", 1, "500g", "spices", 0, 0, 0, 0, 0, "None", 1.49),
    ("Salt", "DOUGH-SALT-500G-DIAMOND", "Diamond Crystal", 1, "500g", "spices", 0, 0, 0, 0, 0, "None", 1.69),
    
    ("Olive oil", "COMMON-OLIVEOIL-500ML-BERTOLLI", "Bertolli", 1, "500ml", "oils", 4050, 0, 450, 0, 0, "None", 8.99),
    ("Olive oil", "COMMON-OLIVEOIL-500ML-POMPEIAN", "Pompeian", 1, "500ml", "oils", 4000, 0, 445, 0, 0, "None", 7.49),
    ("Olive oil", "COMMON-OLIVEOIL-500ML-COLAVITA", "Colavita", 1, "500ml", "oils", 4080, 0, 453, 0, 0, "None", 9.29),
    
    ("Tomato puree", "SAUCE-TOMATO-400G-HUNT", "Hunt's", 1, "400g", "canned", 140, 6, 1, 32, 24, "None", 1.89),
    ("Tomato puree", "SAUCE-TOMATO-400G-CONTADINA", "Contadina", 1, "400g", "canned", 135, 6, 0, 30, 22, "None", 1.69),
    
    ("Mozzarella cheese", "TOPPINGS-CHEESE-200G-KRAFT", "Kraft", 1, "200g", "dairy", 570, 50, 40, 8, 2, "Contains: Milk", 4.99),
    ("Mozzarella cheese", "TOPPINGS-CHEESE-200G-SARGENTO", "Sargento", 1, "200g", "dairy", 560, 48, 42, 6, 1, "Contains: Milk", 5.49),
    ("Mozzarella cheese", "TOPPINGS-CHEESE-200G-GALBANI", "Galbani", 1, "200g", "dairy", 580, 52, 38, 10, 3, "Contains: Milk", 6.29),
    
    # FRESH PRODUCE
    ("Bananas", "FRUIT-BANANA-1KG-CHIQUITA", "Chiquita", 1, "1kg", "fruits", 890, 11, 3, 228, 122, "None", 2.49),
    ("Bananas", "FRUIT-BANANA-1KG-DOLE", "Dole", 1, "1kg", "fruits", 900, 12, 3, 230, 120, "None", 2.39),
    ("Bananas", "FRUIT-BANANA-1KG-ORGANIC", "Organic Valley", 1, "1kg", "fruits", 880, 11, 2, 226, 125, "None", 3.19),
    
    ("Apples", "FRUIT-APPLE-1KG-GALA", "Gala", 1, "1kg", "fruits", 520, 3, 2, 138, 104, "None", 3.99),
    ("Apples", "FRUIT-APPLE-1KG-HONEYCRISP", "Honeycrisp", 1, "1kg", "fruits", 540, 3, 2, 142, 108, "None", 4.99),
    ("Apples", "FRUIT-APPLE-1KG-GRANNY", "Granny Smith", 1, "1kg", "fruits", 480, 2, 1, 128, 98, "None", 3.49),
    
    ("Carrots", "VEG-CARROT-1KG-BOLTHOUSE", "Bolthouse Farms", 1, "1kg", "vegetables", 410, 9, 2, 96, 47, "None", 2.79),
    ("Carrots", "VEG-CARROT-1KG-GRIMMWAY", "Grimmway Farms", 1, "1kg", "vegetables", 400, 9, 2, 94, 45, "None", 2.59),
    ("Carrots", "VEG-CARROT-1KG-ORGANIC", "Organic Baby", 1, "1kg", "vegetables", 420, 10, 2, 98, 49, "None", 3.49),
    
    ("Spinach", "VEG-SPINACH-300G-FRESH", "Fresh Express", 1, "300g", "vegetables", 69, 9, 1, 11, 1, "None", 2.99),
    ("Spinach", "VEG-SPINACH-300G-DOLE", "Dole", 1, "300g", "vegetables", 72, 9, 1, 11, 1, "None", 2.79),
    ("Spinach", "VEG-SPINACH-300G-ORGANIC", "Earthbound Farm", 1, "300g", "vegetables", 66, 8, 1, 11, 1, "None", 3.99),
    
    # DAIRY PRODUCTS
    ("Milk", "DAIRY-MILK-1L-HORIZON", "Horizon Organic", 1, "1L", "dairy", 600, 32, 32, 48, 48, "Contains: Milk", 4.99),
    ("Milk", "DAIRY-MILK-1L-LACTAID", "Lactaid", 1, "1L", "dairy", 620, 32, 35, 50, 50, "Contains: Milk", 4.49),
    ("Milk", "DAIRY-MILK-1L-GREAT", "Great Value", 1, "1L", "dairy", 590, 31, 30, 46, 46, "Contains: Milk", 3.29),
    
    ("Eggs", "DAIRY-EGGS-12CT-EGGLAND", "Eggland's Best", 12, "pieces", "dairy", 840, 72, 60, 6, 0, "Contains: Eggs", 3.99),
    ("Eggs", "DAIRY-EGGS-12CT-CAGE", "Cage Free", 12, "pieces", "dairy", 860, 74, 58, 8, 0, "Contains: Eggs", 4.49),
    ("Eggs", "DAIRY-EGGS-12CT-ORGANIC", "Organic Valley", 12, "pieces", "dairy", 820, 70, 55, 6, 0, "Contains: Eggs", 5.99),
    
    ("Greek Yogurt", "DAIRY-YOGURT-500G-CHOBANI", "Chobani", 1, "500g", "dairy", 600, 100, 20, 36, 32, "Contains: Milk", 5.99),
    ("Greek Yogurt", "DAIRY-YOGURT-500G-FAGE", "Fage", 1, "500g", "dairy", 580, 105, 18, 32, 28, "Contains: Milk", 6.49),
    ("Greek Yogurt", "DAIRY-YOGURT-500G-OIKOS", "Oikos", 1, "500g", "dairy", 620, 95, 22, 38, 35, "Contains: Milk", 5.49),
    
    # MEAT & SEAFOOD
    ("Chicken Breast", "MEAT-CHICKEN-1KG-PERDUE", "Perdue", 1, "1kg", "meat", 1650, 310, 36, 0, 0, "None", 12.99),
    ("Chicken Breast", "MEAT-CHICKEN-1KG-TYSON", "Tyson", 1, "1kg", "meat", 1680, 315, 38, 0, 0, "None", 11.99),
    ("Chicken Breast", "MEAT-CHICKEN-1KG-ORGANIC", "Organic Prairie", 1, "1kg", "meat", 1620, 305, 35, 0, 0, "None", 16.99),
    
    ("Ground Beef", "MEAT-BEEF-500G-85LEAN", "85% Lean", 1, "500g", "meat", 1125, 100, 75, 0, 0, "None", 8.99),
    ("Ground Beef", "MEAT-BEEF-500G-93LEAN", "93% Lean", 1, "500g", "meat", 825, 115, 35, 0, 0, "None", 10.99),
    ("Ground Beef", "MEAT-BEEF-500G-GRASS", "Grass Fed", 1, "500g", "meat", 850, 110, 40, 0, 0, "None", 13.99),
    
    ("Salmon", "FISH-SALMON-500G-ATLANTIC", "Atlantic Farm", 1, "500g", "seafood", 1030, 110, 60, 0, 0, "Contains: Fish", 18.99),
    ("Salmon", "FISH-SALMON-500G-WILD", "Wild Caught", 1, "500g", "seafood", 980, 120, 45, 0, 0, "Contains: Fish", 24.99),
    ("Salmon", "FISH-SALMON-500G-COHO", "Coho Pacific", 1, "500g", "seafood", 1050, 115, 55, 0, 0, "Contains: Fish", 21.99),
    
    # PANTRY STAPLES
    ("Rice", "PANTRY-RICE-1KG-UNCLE", "Uncle Ben's", 1, "1kg", "grains", 3650, 80, 8, 780, 2, "None", 4.99),
    ("Rice", "PANTRY-RICE-1KG-JASMINE", "Jasmine", 1, "1kg", "grains", 3600, 78, 6, 790, 1, "None", 5.49),
    ("Rice", "PANTRY-RICE-1KG-BASMATI", "Basmati", 1, "1kg", "grains", 3580, 82, 7, 785, 1, "None", 6.99),
    
    ("Pasta", "PANTRY-PASTA-500G-BARILLA", "Barilla", 1, "500g", "grains", 1750, 60, 7, 350, 12, "Contains: Gluten", 2.99),
    ("Pasta", "PANTRY-PASTA-500G-OLVERDE", "De Cecco", 1, "500g", "grains", 1780, 62, 8, 355, 10, "Contains: Gluten", 3.49),
    ("Pasta", "PANTRY-PASTA-500G-RONZONI", "Ronzoni", 1, "500g", "grains", 1720, 58, 6, 345, 14, "Contains: Gluten", 2.49),
    
    ("Bread", "BAKERY-BREAD-500G-WONDER", "Wonder", 1, "500g", "bakery", 1250, 40, 20, 240, 40, "Contains: Gluten, Soy", 2.99),
    ("Bread", "BAKERY-BREAD-500G-PEPPERIDGE", "Pepperidge Farm", 1, "500g", "bakery", 1300, 45, 25, 230, 35, "Contains: Gluten, Eggs", 3.99),
    ("Bread", "BAKERY-BREAD-500G-DAVE", "Dave's Killer", 1, "500g", "bakery", 1400, 55, 30, 220, 30, "Contains: Gluten, Nuts, Seeds", 5.49),
    
    # BEVERAGES
    ("Orange Juice", "BEV-OJ-1L-TROPICANA", "Tropicana", 1, "1L", "beverages", 460, 8, 0, 112, 100, "None", 3.99),
    ("Orange Juice", "BEV-OJ-1L-MINUTE", "Minute Maid", 1, "1L", "beverages", 480, 8, 0, 116, 104, "None", 3.49),
    ("Orange Juice", "BEV-OJ-1L-SIMPLY", "Simply Orange", 1, "1L", "beverages", 440, 7, 0, 108, 96, "None", 4.49),
    
    ("Coffee", "BEV-COFFEE-340G-FOLGERS", "Folgers", 1, "340g", "beverages", 10, 1, 0, 0, 0, "None", 6.99),
    ("Coffee", "BEV-COFFEE-340G-MAXWELL", "Maxwell House", 1, "340g", "beverages", 10, 1, 0, 0, 0, "None", 5.99),
    ("Coffee", "BEV-COFFEE-340G-STARBUCKS", "Starbucks", 1, "340g", "beverages", 15, 1, 0, 1, 0, "None", 12.99),
    
    # SNACKS
    ("Potato Chips", "SNACK-CHIPS-150G-LAYS", "Lay's", 1, "150g", "snacks", 800, 12, 50, 100, 2, "None", 3.49),
    ("Potato Chips", "SNACK-CHIPS-150G-PRINGLES", "Pringles", 1, "150g", "snacks", 825, 10, 55, 95, 1, "Contains: Milk", 2.99),
    ("Potato Chips", "SNACK-CHIPS-150G-KETTLE", "Kettle Brand", 1, "150g", "snacks", 780, 11, 48, 92, 2, "None", 4.29),
    
    ("Cookies", "SNACK-COOKIES-300G-OREO", "Oreo", 1, "300g", "snacks", 1600, 16, 70, 240, 140, "Contains: Gluten, Soy", 3.99),
    ("Cookies", "SNACK-COOKIES-300G-CHIPS", "Chips Ahoy!", 1, "300g", "snacks", 1650, 18, 75, 235, 135, "Contains: Gluten, Milk", 3.49),
    ("Cookies", "SNACK-COOKIES-300G-PEPPERIDGE", "Pepperidge Farm", 1, "300g", "snacks", 1580, 20, 65, 230, 130, "Contains: Gluten, Eggs, Milk", 4.99),
    
    # FROZEN FOODS
    ("Frozen Pizza", "FROZEN-PIZZA-400G-DIGIORNO", "DiGiorno", 1, "400g", "frozen", 1120, 48, 44, 132, 16, "Contains: Gluten, Milk", 6.99),
    ("Frozen Pizza", "FROZEN-PIZZA-400G-TOMBSTONE", "Tombstone", 1, "400g", "frozen", 1080, 45, 42, 128, 14, "Contains: Gluten, Milk", 5.99),
    ("Frozen Pizza", "FROZEN-PIZZA-400G-CALIFORNIA", "California Pizza Kitchen", 1, "400g", "frozen", 1000, 52, 38, 120, 12, "Contains: Gluten, Milk", 7.99),
    
    ("Ice Cream", "FROZEN-ICECREAM-1L-HAAGEN", "Häagen-Dazs", 1, "1L", "frozen", 2200, 40, 140, 240, 220, "Contains: Milk, Eggs", 8.99),
    ("Ice Cream", "FROZEN-ICECREAM-1L-BREYERS", "Breyers", 1, "1L", "frozen", 1800, 32, 90, 200, 180, "Contains: Milk", 5.99),
    ("Ice Cream", "FROZEN-ICECREAM-1L-BEN", "Ben & Jerry's", 1, "1L", "frozen", 2400, 44, 160, 280, 240, "Contains: Milk, Eggs, Nuts", 9.99),
    
    # CLEANING SUPPLIES
    ("Dish Soap", "CLEAN-DISH-500ML-DAWN", "Dawn", 1, "500ml", "cleaning", 0, 0, 0, 0, 0, "None", 2.99),
    ("Dish Soap", "CLEAN-DISH-500ML-PALMOLIVE", "Palmolive", 1, "500ml", "cleaning", 0, 0, 0, 0, 0, "None", 2.49),
    ("Dish Soap", "CLEAN-DISH-500ML-JOY", "Joy", 1, "500ml", "cleaning", 0, 0, 0, 0, 0, "None", 2.79),
    
    ("Laundry Detergent", "CLEAN-LAUNDRY-2L-TIDE", "Tide", 1, "2L", "cleaning", 0, 0, 0, 0, 0, "None", 12.99),
    ("Laundry Detergent", "CLEAN-LAUNDRY-2L-GAIN", "Gain", 1, "2L", "cleaning", 0, 0, 0, 0, 0, "None", 11.49),
    ("Laundry Detergent", "CLEAN-LAUNDRY-2L-PERSIL", "Persil", 1, "2L", "cleaning", 0, 0, 0, 0, 0, "None", 13.99),
]

# Connect to SQLite (or create database)
conn = sqlite3.connect("retail_grocery_store.db")
cursor = conn.cursor()

# Create enhanced table with nutritional info, allergens, and pricing
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    sku TEXT UNIQUE NOT NULL,
    brand TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit TEXT NOT NULL,
    category TEXT NOT NULL,
    calories_per_100g INTEGER,
    protein_g REAL,
    fat_g REAL,
    carbs_g REAL,
    sugar_g REAL,
    allergens TEXT,
    price REAL NOT NULL
)
""")

# Insert data
cursor.executemany("""
INSERT OR IGNORE INTO products (item_name, sku, brand, quantity, unit, category, calories_per_100g, protein_g, fat_g, carbs_g, sugar_g, allergens, price)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", grocery_items)

# Create indexes for better performance
cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON products(category)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_brand ON products(brand)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_item_name ON products(item_name)")

# Commit changes
conn.commit()

# Display some sample data
print("Retail Grocery Store Database Created Successfully!")
print("\nSample queries:")

# Show products by category
print("\n1. Products by category (Dairy):")
cursor.execute("SELECT item_name, brand, price, allergens FROM products WHERE category = 'dairy' LIMIT 5")
for row in cursor.fetchall():
    print(f"   {row[0]} - {row[1]} - ${row[2]} - Allergens: {row[3]}")

# Show different brands of same product
print("\n2. Different brands of Milk:")
cursor.execute("SELECT brand, price, calories_per_100g, allergens FROM products WHERE item_name = 'Milk'")
for row in cursor.fetchall():
    print(f"   {row[0]} - ${row[1]} - {row[2]} cal/100g - {row[3]}")

# Show products with allergens
print("\n3. Products containing nuts:")
cursor.execute("SELECT item_name, brand, allergens FROM products WHERE allergens LIKE '%Nuts%'")
for row in cursor.fetchall():
    print(f"   {row[0]} - {row[1]} - {row[2]}")

# Show price range for a category
print("\n4. Price range for Snacks:")
cursor.execute("SELECT MIN(price), MAX(price), AVG(price) FROM products WHERE category = 'snacks'")
min_price, max_price, avg_price = cursor.fetchone()
print(f"   Min: ${min_price:.2f}, Max: ${max_price:.2f}, Average: ${avg_price:.2f}")

# Show nutritional comparison
print("\n5. Protein content comparison (Meat category):")
cursor.execute("SELECT item_name, brand, protein_g FROM products WHERE category = 'meat' ORDER BY protein_g DESC")
for row in cursor.fetchall():
    print(f"   {row[0]} - {row[1]} - {row[2]}g protein per 100g")

print(f"\nTotal products in database: {len(grocery_items)}")
print("Categories available:", set([item[6] for item in grocery_items]))

conn.close()