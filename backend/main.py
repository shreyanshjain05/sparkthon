

#############################################################################
# TESTING
#############################################################################
# Test functions for each tool

def test_extract_recipe_ingredients():
    """Test extracting recipe ingredients"""
    print("\n=== Testing extract_recipe_ingredients ===")
    
    # Test cases
    test_cases = ["I want to make pasta", "pizza for dinner", "fresh salad", "unknown recipe"]
    
    for test in test_cases:
        result = extract_recipe_ingredients.invoke({"recipe_request": test})
        print(f"Request: '{test}' -> Recipe: {result['recipe']}, Ingredients: {len(result['ingredients'])}")
    
    return True

def test_create_cart_session():
    """Test creating cart sessions"""
    print("\n=== Testing create_cart_session ===")
    
    test_user = "test_user_001"
    
    # Test different session types
    for session_type in ["recipe_based", "general", "bulk_order"]:
        result = create_cart_session.invoke({
            "user_id": test_user,
            "session_type": session_type
        })
        
        if result['success']:
            print(f"✓ Created {session_type} session: {result['session_id']}")
            return result['session_id']  # Return for use in other tests
        else:
            print(f"✗ Failed to create session: {result['error']}")
    
    return None

def test_check_ingredient_availability():
    """Test checking ingredient availability"""
    print("\n=== Testing check_ingredient_availability ===")
    
    # Test ingredients
    test_ingredients = ["pasta", "tomato", "cheese", "nonexistent_item"]
    
    for ingredient in test_ingredients:
        result = check_ingredient_availability.invoke({
            "ingredient_name": ingredient
        })
        
        print(f"Ingredient: '{ingredient}' -> Available: {result['available']}, "
              f"Options: {result['count']}")
        
        if result['available'] and result['options']:
            print(f"  First option: {result['options'][0]['item_name']} - "
                  f"{result['options'][0]['brand']}")
    
    return True

def test_get_product_details_for_comparison():
    """Test getting product details for comparison"""
    print("\n=== Testing get_product_details_for_comparison ===")
    
    # First, get some SKUs from available products
    check_result = check_ingredient_availability.invoke({"ingredient_name": "pasta"})
    
    if check_result['available'] and check_result['options']:
        skus = [item['sku'] for item in check_result['options'][:3]]
        
        result = get_product_details_for_comparison.invoke({"skus": skus})
        
        print(f"Comparing {len(result)} products:")
        for product in result:
            print(f"  - {product['brand']} {product['item_name']}: "
                  f"${product['price']} ({product['price_per_unit']})")
            print(f"    Calories: {product['nutritional_info']['calories_per_100g']}")
    
    return True

def test_add_to_cart():
    """Test adding items to cart"""
    print("\n=== Testing add_to_cart ===")
    
    test_user = "test_user_001"
    
    # Create a session first
    session_result = create_cart_session.invoke({
        "user_id": test_user,
        "session_type": "recipe_based"
    })
    session_id = session_result.get('session_id') if session_result['success'] else None
    
    # Get a product to add
    check_result = check_ingredient_availability.invoke({"ingredient_name": "pasta"})
    
    if check_result['available'] and check_result['options']:
        sku = check_result['options'][0]['sku']
        
        # Test adding item
        result = add_to_cart.invoke({
            "user_id": test_user,
            "sku": sku,
            "quantity": 2,
            "notes": "For pasta recipe",
            "session_id": session_id
        })
        
        if result['success']:
            print(f"✓ Added item to cart: {result['message']}")
            print(f"  Product: {result['data']['product_name']}")
            print(f"  Quantity: {result['data']['quantity']}")
            print(f"  Total: ${result['data']['total_price']}")
        else:
            print(f"✗ Failed to add item: {result['error']}")
    
    return True

def test_get_user_cart():
    """Test retrieving user cart"""
    print("\n=== Testing get_user_cart ===")
    
    test_user = "test_user_001"
    
    result = get_user_cart.invoke({
        "user_id": test_user,
        "status": "active"
    })
    
    if 'error' not in result:
        print(f"Cart for user {test_user}:")
        print(f"  Items: {result['item_count']}")
        print(f"  Total quantity: {result['total_items']}")
        print(f"  Total price: ₹{result['total_price']}")
        print(f"  Brands: {result['brands_summary']}")
        
        for item in result['items']:
            print(f"  - {item['product_name']} x{item['quantity']} = ${item['total_price']}")
    else:
        print(f"Error: {result['error']}")
    
    return True

def test_update_cart_quantity():
    """Test updating cart quantity"""
    print("\n=== Testing update_cart_quantity ===")
    
    test_user = "test_user_001"
    
    # Get current cart
    cart = get_user_cart.invoke({"user_id": test_user})
    
    if cart['items']:
        sku = cart['items'][0]['sku']
        old_quantity = cart['items'][0]['quantity']
        
        # Update quantity
        result = update_cart_quantity.invoke({
            "user_id": test_user,
            "sku": sku,
            "new_quantity": old_quantity + 1
        })
        
        if result['success']:
            print(f"✓ Updated quantity from {old_quantity} to {result['data']['quantity']}")
            print(f"  New total: ${result['data']['total_price']}")
        else:
            print(f"✗ Failed to update: {result['error']}")
    
    return True

def test_remove_from_cart():
    """Test removing item from cart"""
    print("\n=== Testing remove_from_cart ===")
    
    test_user = "test_user_001"
    
    # Add an item first
    check_result = check_ingredient_availability.invoke({"ingredient_name": "cheese"})
    if check_result['available']:
        sku = check_result['options'][0]['sku']
        add_to_cart.invoke({
            "user_id": test_user,
            "sku": sku,
            "quantity": 1
        })  
        
        # Now remove it
        result = remove_from_cart.invoke({
            "user_id": test_user,
            "sku": sku
        })
        
        if result['success']:
            print(f"✓ {result['message']}")
        else:
            print(f"✗ Failed to remove: {result.get('error', result.get('message'))}")
    
    return True

def test_search_alternatives():
    """Test searching for alternatives"""
    print("\n=== Testing search_alternatives ===")
    
    result = search_alternatives.invoke({
        "ingredient_name": "pasta",
        "exclude_skus": [],
        "category": None
    })
    
    print(f"Found {len(result)} alternatives for 'pasta':")
    for alt in result:
        print(f"  - {alt['brand']} {alt['item_name']} ({alt['sku']})")
        print(f"    Price: ₹{alt['price']} for {alt['quantity']}")
        print(f"    Category: {alt['category']}, In stock: {alt['in_stock']}")
    
    # Test with exclusions
    if result:
        exclude_skus = [result[0]['sku']]
        result2 = search_alternatives.invoke({
            "ingredient_name": "pasta",
            "exclude_skus": exclude_skus,
            "category": None
        })
        print(f"\nExcluding {exclude_skus[0]}, found {len(result2)} alternatives")
    
    return True

def test_get_nutrition_comparison():
    """Test nutrition comparison"""
    print("\n=== Testing get_nutrition_comparison ===")
    
    # Get some pasta products
    check_result = check_ingredient_availability.invoke({"ingredient_name": "pasta"})
    
    if check_result['available'] and len(check_result['options']) >= 2:
        skus = [item['sku'] for item in check_result['options'][:3]]
        
        result = get_nutrition_comparison.invoke({"skus": skus})
        
        print(f"Comparing nutrition for {len(result)} products:")
        for product in result:
            print(f"\n{product['name']} ({product['sku']}):")
            print(f"  Per 100g: {product['nutrition_per_100g']}")
            print(f"  Allergens: {', '.join(product['allergens'])}")
    
    return True

def test_checkout_cart():
    """Test checkout process"""
    print("\n=== Testing checkout_cart ===")
    
    test_user = "test_user_001"
    
    # First ensure cart has items
    cart = get_user_cart.invoke({"user_id": test_user})
    
    if cart['item_count'] == 0:
        # Add some items first
        print("Adding items to cart for checkout test...")
        check_result = check_ingredient_availability.invoke({"ingredient_name": "pasta"})
        if check_result['available']:
            add_to_cart.invoke({
                "user_id": test_user,
                "sku": check_result['options'][0]['sku'],
                "quantity": 2
            })
    
    # Now checkout
    result = checkout_cart.invoke({
        "user_id": test_user,
        "shipping_address": "123 Test Street, Test City, TC 12345",
        "delivery_date": (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
        "special_instructions": "Please leave at door"
    })
    
    if result['success']:
        print(f"✓ Order created successfully!")
        print(f"  Order ID: {result['order_id']}")
        print(f"  Order Number: {result['order_number']}")
        print(f"  Total Amount: ${result['total_amount']}")
        print(f"  Items: {result['item_count']}")
    else:
        print(f"✗ Checkout failed: {result['error']}")
    
    return result.get('success', False)

def test_clear_expired_sessions():
    """Test clearing expired sessions"""
    print("\n=== Testing clear_expired_sessions ===")
    
    # First create an expired session for testing
    test_user = "test_expired_user"
    
    # Manually create an expired session
    expired_session_data = {
        "user_id": test_user,
        "session_id": f"expired_session_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "session_type": "general",
        "active": True,
        "expires_at": (datetime.now() - timedelta(hours=1)).isoformat(),  # Already expired
        "metadata": {"test": "expired_session"}
    }
    
    try:
        supabase.table('cart_sessions').insert(expired_session_data).execute()
        print("Created test expired session")
    except:
        print("Could not create test expired session")
    
    # Now clear expired sessions
    result = clear_expired_sessions.invoke({})
    
    if result['success']:
        print(f"✓ Cleared {result['sessions_expired']} expired sessions")
    else:
        print(f"✗ Error clearing sessions: {result['error']}")
    
    return True

def run_all_tests():
    """Run all test functions in sequence"""
    print("=" * 60)
    print("RUNNING ALL TOOL TESTS")
    print("=" * 60)
    
    test_functions = [
        test_extract_recipe_ingredients,
        test_create_cart_session,
        test_check_ingredient_availability,
        test_get_product_details_for_comparison,
        test_add_to_cart,
        test_get_user_cart,
        test_update_cart_quantity,
        test_remove_from_cart,
        test_search_alternatives,
        test_get_nutrition_comparison,
        test_checkout_cart,
        test_clear_expired_sessions
    ]
    
    results = {}
    for test_func in test_functions:
        try:
            print(f"\n{'='*60}")
            success = test_func()
            results[test_func.__name__] = "PASS" if success else "FAIL"
        except Exception as e:
            print(f"ERROR in {test_func.__name__}: {str(e)}")
            results[test_func.__name__] = "ERROR"
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for test_name, result in results.items():
        status_symbol = "✓" if result == "PASS" else "✗"
        print(f"{status_symbol} {test_name}: {result}")
    
    pass_count = sum(1 for r in results.values() if r == "PASS")
    print(f"\nTotal: {pass_count}/{len(results)} tests passed")

def setup_test_data():
    """Setup initial test data in the database"""
    print("\n=== Setting up test data ===")
    
    # Add test products if they don't exist
    test_products = [
        {
            "item_name": "Spaghetti",
            "sku": "PASTA001",
            "brand": "Barilla",
            "quantity": 500,
            "unit": "g",
            "category": "Pasta",
            "calories_per_100g": 371,
            "protein_g": 13,
            "fat_g": 1.5,
            "carbs_g": 75,
            "sugar_g": 3.5,
            "allergens": "Gluten",
            "price": 2.99,
            "stock_quantity": 50
        },
        {
            "item_name": "Penne",
            "sku": "PASTA002",
            "brand": "De Cecco",
            "quantity": 500,
            "unit": "g",
            "category": "Pasta",
            "calories_per_100g": 356,
            "protein_g": 11.5,
            "fat_g": 1.2,
            "carbs_g": 73.4,
            "sugar_g": 2.8,
            "allergens": "Gluten",
            "price": 3.49,
            "stock_quantity": 30
        },
        {
            "item_name": "Marinara Sauce",
            "sku": "SAUCE001",
            "brand": "Rao's",
            "quantity": 680,
            "unit": "g",
            "category": "Sauces",
            "calories_per_100g": 60,
            "protein_g": 2,
            "fat_g": 3,
            "carbs_g": 7,
            "sugar_g": 5,
            "allergens": "",
            "price": 7.99,
            "stock_quantity": 25
        },
        {
            "item_name": "Parmesan Cheese",
            "sku": "CHEESE001",
            "brand": "BelGioioso",
            "quantity": 200,
            "unit": "g",
            "category": "Cheese",
            "calories_per_100g": 431,
            "protein_g": 38,
            "fat_g": 29,
            "carbs_g": 4.1,
            "sugar_g": 0.9,
            "allergens": "Milk",
            "price": 8.99,
            "stock_quantity": 15
        }
    ]
    
    for product in test_products:
        try:
            # Check if product exists
            existing = supabase.table('products').select('sku').eq('sku', product['sku']).execute()
            if not existing.data:
                supabase.table('products').insert(product).execute()
                print(f"✓ Added product: {product['brand']} {product['item_name']}")
            else:
                print(f"- Product already exists: {product['sku']}")
        except Exception as e:
            print(f"✗ Error adding product {product['sku']}: {str(e)}")

def cleanup_test_data():
    """Clean up test data after tests"""
    print("\n=== Cleaning up test data ===")
    
    test_user = "test_user_001"
    
    try:
        # Mark test user's active cart items as removed
        supabase.table('shopping_carts').update({
            'status': 'removed'
        }).eq('user_id', test_user).eq('status', 'active').execute()
        
        print("✓ Cleaned up test cart items")
    except Exception as e:
        print(f"✗ Error cleaning up: {str(e)}")

# Interactive test runner
def interactive_test():
    """Interactive test menu"""
    while True:
        print("\n" + "="*60)
        print("TOOL TEST MENU")
        print("="*60)
        print("1. Run all tests")
        print("2. Setup test data")
        print("3. Test individual tool")
        print("4. Cleanup test data")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ")
        
        if choice == "1":
            run_all_tests()
        elif choice == "2":
            setup_test_data()
        elif choice == "3":
            print("\nAvailable tools to test:")
            tools_list = [
                "extract_recipe_ingredients",
                "create_cart_session",
                "check_ingredient_availability",
                "get_product_details_for_comparison",
                "add_to_cart",
                "get_user_cart",
                "update_cart_quantity",
                "remove_from_cart",
                "search_alternatives",
                "get_nutrition_comparison",
                "checkout_cart",
                "clear_expired_sessions"
            ]
            for i, tool in enumerate(tools_list, 1):
                print(f"{i}. {tool}")
            
            tool_choice = input("\nEnter tool number: ")
            try:
                tool_index = int(tool_choice) - 1
                if 0 <= tool_index < len(tools_list):
                    test_func = globals()[f"test_{tools_list[tool_index]}"]
                    test_func()
                else:
                    print("Invalid choice")
            except:
                print("Invalid input")
        elif choice == "4":
            cleanup_test_data()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice")

# Main execution
if __name__ == "__main__":
    print("Shopping Cart Tools Test Suite")
    print("==============================")
    
    # Option 1: Run all tests automatically
    # setup_test_data()
    # run_all_tests()
    # cleanup_test_data()
    
    # Option 2: Interactive testing
    interactive_test()



    # Example usage in LangGraph

# Create tool node
tool_node = ToolNode(tools)