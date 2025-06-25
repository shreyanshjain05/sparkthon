import sqlite3
import datetime
from typing import List, Tuple, Optional
import os

def create_products_database(db_path: str = "grocery_products.db"):
    """
    Create and populate the main products database with comprehensive grocery items.
    """
    if os.path.exists(db_path):
        print(f"Database '{db_path}' already exists. ")
        return db_path
        
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
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create products table with enhanced structure
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
        price REAL NOT NULL,
        stock_quantity INTEGER DEFAULT 100,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Insert product data
    cursor.executemany("""
    INSERT OR IGNORE INTO products (item_name, sku, brand, quantity, unit, category, 
                                  calories_per_100g, protein_g, fat_g, carbs_g, sugar_g, 
                                  allergens, price)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, grocery_items)
    
    # Create indexes for better performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON products(category)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_brand ON products(brand)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_item_name ON products(item_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sku ON products(sku)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_price ON products(price)")
    
    # Commit changes
    conn.commit()
    
    # Display database statistics
    print("Products Database Created Successfully!")
    print(f"Database location: {db_path}")
    print(f"Total products inserted: {len(grocery_items)}")
    
    conn.close()
    return db_path



def create_shopping_cart_database(db_path: str = "shopping_carts.db"):
    """
    Create and populate the shopping cart database with sample cart data.
    Enhanced for recipe-based ingredient management and agentic operations.
    """
    if os.path.exists(db_path):
        print(f"Database '{db_path}' already exists.")
        return db_path
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Create shopping carts table with recipe context
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shopping_carts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        sku TEXT NOT NULL,
        product_name TEXT,
        brand TEXT,
        quantity INTEGER NOT NULL CHECK(quantity > 0),
        unit_price DECIMAL(10,2) NOT NULL CHECK(unit_price >= 0),
        total_price DECIMAL(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
        recipe_name TEXT,  -- Track which recipe this ingredient belongs to
        recipe_id TEXT,    -- Optional recipe identifier
        ingredient_category TEXT,  -- e.g., 'protein', 'vegetable', 'spice'
        notes TEXT,        -- Any special notes about the ingredient
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'active' CHECK(status IN ('active', 'purchased', 'removed', 'pending'))
    )
    """)
    
    # Create orders table for order history
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        order_number TEXT UNIQUE NOT NULL,
        total_amount DECIMAL(10,2) NOT NULL CHECK(total_amount >= 0),
        order_status TEXT DEFAULT 'pending' CHECK(order_status IN ('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled')),
        payment_method TEXT,
        shipping_address TEXT,
        delivery_date DATE,
        special_instructions TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create order items table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        sku TEXT NOT NULL,
        product_name TEXT,
        brand TEXT,
        quantity INTEGER NOT NULL CHECK(quantity > 0),
        unit_price DECIMAL(10,2) NOT NULL CHECK(unit_price >= 0),
        total_price DECIMAL(10,2) NOT NULL,
        recipe_name TEXT,  -- Track recipe context in orders too
        FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE
    )
    """)

        # Create cart sessions table for better session management
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        session_id TEXT UNIQUE NOT NULL,
        session_type TEXT DEFAULT 'general' CHECK(session_type IN ('general', 'recipe_based', 'bulk_order')),
        active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP,
        metadata TEXT  -- JSON string for additional session data
    )
    """)
    
    # Sample cart data for multiple users with recipe context
    sample_cart_data = [
        # User Alice's cart - Pizza Recipe
        ("alice_123", "DOUGH-FLOUR-500G-GOLD", "All-purpose flour", "Gold Medal", 1, 3.49, "Homemade Pizza", "RECIPE-001", "base", "For pizza dough"),
        ("alice_123", "DOUGH-YEAST-10G-FLEISCH", "Active dry yeast", "Fleischmann's", 1, 2.99, "Homemade Pizza", "RECIPE-001", "leavening", None),
        ("alice_123", "SAUCE-TOMATO-400G-HUNT", "Tomato puree", "Hunt's", 1, 1.89, "Homemade Pizza", "RECIPE-001", "sauce", None),
        ("alice_123", "TOPPINGS-CHEESE-200G-KRAFT", "Mozzarella cheese", "Kraft", 2, 4.99, "Homemade Pizza", "RECIPE-001", "topping", "Extra cheese"),
        ("alice_123", "COMMON-OLIVEOIL-500ML-BERTOLLI", "Olive oil", "Bertolli", 1, 8.99, "Homemade Pizza", "RECIPE-001", "oil", None),
        
        # User Bob's cart - Pasta Dish
        ("bob_456", "PANTRY-PASTA-500G-BARILLA", "Barilla Pasta", "Barilla", 2, 2.99, "Spaghetti Carbonara", "RECIPE-002", "base", None),
        ("bob_456", "DAIRY-EGGS-12CT-ORGANIC", "Organic Eggs", "Organic Valley", 1, 5.99, "Spaghetti Carbonara", "RECIPE-002", "protein", "For carbonara sauce"),
        ("bob_456", "TOPPINGS-CHEESE-200G-KRAFT", "Kraft Mozzarella", "Kraft", 1, 4.99, "Spaghetti Carbonara", "RECIPE-002", "cheese", None),
        ("bob_456", "COMMON-OLIVEOIL-500ML-BERTOLLI", "Bertolli Olive Oil", "Bertolli", 1, 8.99, "Spaghetti Carbonara", "RECIPE-002", "oil", None),
        
        # User Charlie's cart - Healthy Breakfast
        ("charlie_789", "DAIRY-YOGURT-500G-CHOBANI", "Chobani Greek Yogurt", "Chobani", 2, 5.99, "Protein Breakfast Bowl", "RECIPE-003", "protein", None),
        ("charlie_789", "FRUIT-BANANA-1KG-CHIQUITA", "Chiquita Bananas", "Chiquita", 1, 2.49, "Protein Breakfast Bowl", "RECIPE-003", "fruit", None),
        ("charlie_789", "BAKERY-BREAD-500G-DAVE", "Dave's Killer Bread", "Dave's Killer", 1, 5.49, "Protein Breakfast Bowl", "RECIPE-003", "carb", "Whole grain"),
        
        # User Diana's cart - Asian Stir Fry
        ("diana_101", "PANTRY-RICE-1KG-UNCLE", "Uncle Ben's Rice", "Uncle Ben's", 1, 4.99, "Vegetable Stir Fry", "RECIPE-004", "base", None),
        ("diana_101", "VEG-CARROT-1KG-BOLTHOUSE", "Bolthouse Carrots", "Bolthouse Farms", 1, 2.79, "Vegetable Stir Fry", "RECIPE-004", "vegetable", None),
        ("diana_101", "COMMON-OLIVEOIL-500ML-BERTOLLI", "Bertolli Olive Oil", "Bertolli", 1, 8.99, "Vegetable Stir Fry", "RECIPE-004", "oil", None),
        ("diana_101", "MEAT-CHICKEN-1KG-PERDUE", "Perdue Chicken Breast", "Perdue", 1, 12.99, "Vegetable Stir Fry", "RECIPE-004", "protein", "Cut into strips"),
    ]
    # Insert sample cart data
    cursor.executemany("""
    INSERT INTO shopping_carts (user_id, sku, product_name, brand, quantity, unit_price, recipe_name, recipe_id, ingredient_category, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_cart_data)
    
    # Sample completed orders
    sample_orders = [
        ("alice_123", "ORDER-001", 45.67, "completed", "credit_card", "123 Main St, City, State", "2025-06-25", "Leave at door"),
        ("bob_456", "ORDER-002", 32.89, "shipped", "debit_card", "456 Oak Ave, City, State", "2025-06-24", None),
        ("charlie_789", "ORDER-003", 78.45, "processing", "paypal", "789 Pine Rd, City, State", "2025-06-26", "Call before delivery"),
    ]
    
    cursor.executemany("""
    INSERT INTO orders (user_id, order_number, total_amount, order_status, payment_method, shipping_address, delivery_date, special_instructions)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_orders)
    
    # Create comprehensive indexes for better performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cart_user_id ON shopping_carts(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cart_sku ON shopping_carts(sku)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cart_status ON shopping_carts(status)")

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cart_user_status ON shopping_carts(user_id, status)")
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(order_status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_number ON orders(order_number)")
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_sku ON order_items(sku)")
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user ON cart_sessions(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_active ON cart_sessions(active)")
    
    # Create triggers for automatic timestamp updates
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS update_cart_timestamp 
    AFTER UPDATE ON shopping_carts
    BEGIN
        UPDATE shopping_carts SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END
    """)
    
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS update_order_timestamp 
    AFTER UPDATE ON orders
    BEGIN
        UPDATE orders SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END
    """)

    # Create views for common queries
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS active_cart_summary AS
    SELECT 
        user_id,
        recipe_name,
        recipe_id,
        COUNT(*) as item_count,
        SUM(quantity) as total_quantity,
        SUM(total_price) as total_amount,
        MIN(added_at) as first_added,
        MAX(updated_at) as last_updated
    FROM shopping_carts 
    WHERE status = 'active'
    GROUP BY user_id, recipe_id
    """)
    
    # Commit changes
    conn.commit()
    
    # Display database statistics
    cursor.execute("SELECT COUNT(*) FROM shopping_carts")
    cart_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM shopping_carts")
    user_count = cursor.fetchone()[0]

    
    print("Shopping Cart Database Created Successfully!")
    print(f"Database location: {db_path}")
    print(f"Total cart items: {cart_count}")
    print(f"Total users: {user_count}")
    
    conn.close()
    return db_path


def create_shopping_cart_database(db_path: str = "shopping_carts.db"):
    """
    Create and populate the shopping cart database with sample cart data.
    Enhanced for recipe-based ingredient management and agentic operations.
    """
    if os.path.exists(db_path):
        print(f"Database '{db_path}' already exists.")
        return db_path
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Create shopping carts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shopping_carts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        sku TEXT NOT NULL,
        product_name TEXT,
        brand TEXT,
        quantity INTEGER NOT NULL CHECK(quantity > 0),
        unit_price DECIMAL(10,2) NOT NULL CHECK(unit_price >= 0),
        total_price DECIMAL(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
        notes TEXT,        -- Any special notes about the ingredient
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'active' CHECK(status IN ('active', 'purchased', 'removed', 'pending'))
    )
    """)
    
    # Create orders table for order history
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        order_number TEXT UNIQUE NOT NULL,
        total_amount DECIMAL(10,2) NOT NULL CHECK(total_amount >= 0),
        order_status TEXT DEFAULT 'pending' CHECK(order_status IN ('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled')),
        payment_method TEXT,
        shipping_address TEXT,
        delivery_date DATE,
        special_instructions TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create order items table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        sku TEXT NOT NULL,
        product_name TEXT,
        brand TEXT,
        quantity INTEGER NOT NULL CHECK(quantity > 0),
        unit_price DECIMAL(10,2) NOT NULL CHECK(unit_price >= 0),
        total_price DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE
    )
    """)
    
    
    # Create cart sessions table for better session management
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        session_id TEXT UNIQUE NOT NULL,
        session_type TEXT DEFAULT 'general' CHECK(session_type IN ('general', 'recipe_based', 'bulk_order')),
        active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP,
        metadata TEXT  -- JSON string for additional session data
    )
    """)
    
    # Sample cart data for multiple users
    sample_cart_data = [
        # User Alice's cart
        ("alice_123", "DOUGH-FLOUR-500G-GOLD", "All-purpose flour", "Gold Medal", 1, 3.49, "For baking"),
        ("alice_123", "DOUGH-YEAST-10G-FLEISCH", "Active dry yeast", "Fleischmann's", 1, 2.99, None),
        ("alice_123", "SAUCE-TOMATO-400G-HUNT", "Tomato puree", "Hunt's", 1, 1.89, None),
        ("alice_123", "TOPPINGS-CHEESE-200G-KRAFT", "Mozzarella cheese", "Kraft", 2, 4.99, "Extra cheese"),
        ("alice_123", "COMMON-OLIVEOIL-500ML-BERTOLLI", "Olive oil", "Bertolli", 1, 8.99, None),
        
        # User Bob's cart
        ("bob_456", "PANTRY-PASTA-500G-BARILLA", "Barilla Pasta", "Barilla", 2, 2.99, None),
        ("bob_456", "DAIRY-EGGS-12CT-ORGANIC", "Organic Eggs", "Organic Valley", 1, 5.99, "For cooking"),
        ("bob_456", "TOPPINGS-CHEESE-200G-KRAFT", "Kraft Mozzarella", "Kraft", 1, 4.99, None),
        ("bob_456", "COMMON-OLIVEOIL-500ML-BERTOLLI", "Bertolli Olive Oil", "Bertolli", 1, 8.99, None),
        
        # User Charlie's cart
        ("charlie_789", "DAIRY-YOGURT-500G-CHOBANI", "Chobani Greek Yogurt", "Chobani", 2, 5.99, None),
        ("charlie_789", "FRUIT-BANANA-1KG-CHIQUITA", "Chiquita Bananas", "Chiquita", 1, 2.49, None),
        ("charlie_789", "BAKERY-BREAD-500G-DAVE", "Dave's Killer Bread", "Dave's Killer", 1, 5.49, "Whole grain"),
        
        # User Diana's cart
        ("diana_101", "PANTRY-RICE-1KG-UNCLE", "Uncle Ben's Rice", "Uncle Ben's", 1, 4.99, None),
        ("diana_101", "VEG-CARROT-1KG-BOLTHOUSE", "Bolthouse Carrots", "Bolthouse Farms", 1, 2.79, None),
        ("diana_101", "COMMON-OLIVEOIL-500ML-BERTOLLI", "Bertolli Olive Oil", "Bertolli", 1, 8.99, None),
        ("diana_101", "MEAT-CHICKEN-1KG-PERDUE", "Perdue Chicken Breast", "Perdue", 1, 12.99, "Cut into strips"),
    ]
    
    # Insert sample cart data
    cursor.executemany("""
    INSERT INTO shopping_carts (user_id, sku, product_name, brand, quantity, unit_price, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, sample_cart_data)

    # Sample completed orders
    sample_orders = [
        ("alice_123", "ORDER-001", 45.67, "delivered", "credit_card", "123 Main St, City, State", "2025-06-25", "Leave at door"),
        ("bob_456", "ORDER-002", 32.89, "shipped", "debit_card", "456 Oak Ave, City, State", "2025-06-24", None),
        ("charlie_789", "ORDER-003", 78.45, "processing", "paypal", "789 Pine Rd, City, State", "2025-06-26", "Call before delivery"),
    ]
    
    cursor.executemany("""
    INSERT INTO orders (user_id, order_number, total_amount, order_status, payment_method, shipping_address, delivery_date, special_instructions)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_orders)
    
    # Create indexes for better performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cart_user_id ON shopping_carts(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cart_sku ON shopping_carts(sku)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cart_status ON shopping_carts(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cart_user_status ON shopping_carts(user_id, status)")
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(order_status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_number ON orders(order_number)")
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_sku ON order_items(sku)")
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user ON cart_sessions(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_active ON cart_sessions(active)")
    
    # Create triggers for automatic timestamp updates
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS update_cart_timestamp 
    AFTER UPDATE ON shopping_carts
    BEGIN
        UPDATE shopping_carts SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END
    """)
    
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS update_order_timestamp 
    AFTER UPDATE ON orders
    BEGIN
        UPDATE orders SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END
    """)
    
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS update_recipe_timestamp 
    AFTER UPDATE ON orders
    BEGIN
        UPDATE orders SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END
    """)
    
    # Create views for common queries
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS active_cart_summary AS
    SELECT 
        user_id,
        COUNT(*) as item_count,
        SUM(quantity) as total_quantity,
        SUM(total_price) as total_amount,
        MIN(added_at) as first_added,
        MAX(updated_at) as last_updated
    FROM shopping_carts 
    WHERE status = 'active'
    GROUP BY user_id
    """)
    
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS user_cart_details AS
    SELECT *
    FROM shopping_carts
    WHERE status = 'active'
    """)
    
    # Commit changes
    conn.commit()
    
    # Display database statistics
    cursor.execute("SELECT COUNT(*) FROM shopping_carts")
    cart_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM shopping_carts")
    user_count = cursor.fetchone()[0]
    
    print("Shopping Cart Database Created Successfully!")
    print(f"Database location: {db_path}")
    print(f"Total cart items: {cart_count}")
    print(f"Total users: {user_count}")
    
    conn.close()
    return db_path

# Helper functions for cart operations (for use with LangGraph agents)
def get_user_cart(db_path: str, user_id: str, status: str = 'active'):
    """Get all cart items for a specific user"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT * FROM user_cart_details 
    WHERE user_id = ? AND status = ?
    ORDER BY recipe_name, added_at
    """, (user_id, status))
    
    results = cursor.fetchall()
    conn.close()
    return results

def add_ingredients_to_cart(db_path: str, user_id: str, ingredients: List[dict]):
    """Add multiple ingredients to user's cart"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Add ingredients to cart
        for ingredient in ingredients:
            cursor.execute("""
            INSERT INTO shopping_carts 
            (user_id, sku, product_name, brand, quantity, unit_price, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                ingredient.get('sku'),
                ingredient.get('product_name'),
                ingredient.get('brand'),
                ingredient.get('quantity', 1),
                ingredient.get('unit_price', 0.0),
                ingredient.get('notes')
            ))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error adding ingredients: {e}")
        return False
    finally:
        conn.close()

def update_cart_item_quantity(db_path: str, user_id: str, cart_item_id: int, new_quantity: int):
    """Update quantity of a specific cart item"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    UPDATE shopping_carts 
    SET quantity = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND user_id = ? AND status = 'active'
    """, (new_quantity, cart_item_id, user_id))
    
    affected_rows = cursor.rowcount
    conn.commit()
    conn.close()
    
    return affected_rows > 0

def remove_cart_item(db_path: str, user_id: str, cart_item_id: int):
    """Remove item from cart (soft delete by changing status)"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    UPDATE shopping_carts 
    SET status = 'removed', updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND user_id = ? AND status = 'active'
    """, (cart_item_id, user_id))
    
    affected_rows = cursor.rowcount
    conn.commit()
    conn.close()
    
    return affected_rows > 0

if __name__ == "__main__":
    print("Creating products database...")
    create_products_database()
    print("Creating shopping cart database...")
    create_shopping_cart_database()
    print("Databases created successfully!")




