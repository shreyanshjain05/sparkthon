import os
import json
import shopify
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Shopify credentials
SHOP_URL = os.getenv("SHOPIFY_SHOP_URL")
API_VERSION = os.getenv("API_VERSION", "2023-10")  # Default version
ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")

# In-memory cart to store items and their quantities
cart: Dict[str, int] = {}


def create_shopify_session():
    """Initialize and activate a Shopify session."""
    session = shopify.Session(SHOP_URL, API_VERSION, ACCESS_TOKEN)
    shopify.ShopifyResource.activate_session(session)


def get_products(limit: int = 5) -> List[Dict]:
    """Fetch products from the Shopify store."""
    try:
        products = shopify.Product.find(limit=limit)
        return [product.to_dict() for product in products]
    except Exception as e:
        print(f"Error fetching products: {e}")
        return []


def add_product_to_cart(item_name: str, quantity: int) -> Dict[str, str]:
    """Add or update a product in the in-memory cart."""
    try:
        if item_name in cart:
            cart[item_name] += quantity
        else:
            cart[item_name] = quantity

        return {
            "status": "success",
            "message": f"Added {quantity} of '{item_name}' to cart."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# ---------- Main Execution Block ----------
if __name__ == "__main__":
    try:
        # Setup Shopify session
        print("Setting up Shopify session...")
        create_shopify_session()
        print("Shopify session activated.")

        # Fetch and display products
        print("\nFetching products...")
        products = get_products(limit=5)

        if products:
            print(f"\nSuccessfully fetched {len(products)} product(s):")
            print(json.dumps(products, indent=2))
        else:
            print("No products found or error occurred.")

        # Test adding a product to the cart
        print("\nAdding product to cart...")
        result = add_product_to_cart("Sample Product", 2)
        print(f"Cart status: {result}")

        # Optional: Print final cart
        print(f"\nCurrent cart: {cart}")

    except Exception as e:
        print(f"\nError setting up Shopify session: {e}")
        print("Please check your credentials and try again.")