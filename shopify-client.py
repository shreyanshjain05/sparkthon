import shopify
import os
import json
from dotenv import load_dotenv
load_dotenv()

SHOP_URL = os.getenv("SHOPIFY_SHOP_URL")
API_VERSION = os.getenv("API_VERSION", "2023-10")  # Default to a stable version
ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")




try:
    # Create session with proper format
    session = shopify.Session(SHOP_URL, API_VERSION, ACCESS_TOKEN)
    shopify.ShopifyResource.activate_session(session)
    
    def get_products(limit=5):
        """Fetch products from Shopify store"""
        try:
            products = shopify.Product.find(limit=limit)
            return [product.to_dict() for product in products]
        except Exception as e:
            print(f"Error fetching products: {e}")
            return []
    
    # Test the connection
    print("\nTesting Shopify connection...")
    products = get_products(5)
    
    if products:
        print(f"\nSuccessfully fetched {len(products)} products:")
        print(json.dumps(products, indent=2))
    else:
        print("No products found or error occurred.")
        
except Exception as e:
    print(f"Error setting up Shopify session: {e}")
    print("\nPlease check your credentials and try again.")