from typing import List, Dict, TypedDict, Optional, Literal
from langchain.tools import tool
from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import uuid
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.prebuilt import ToolNode
from IPython.display import Image, display


# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# State definition
class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    session_id: str

# Tool definitions
@tool
def extract_recipe_ingredients(recipe_request: str) -> Dict[str, List[str]]:
    """Extract required ingredients from a recipe request"""
    # This could use an LLM or a predefined recipe database
    recipes = input("Whats are you looking for today?")
    
    recipe_request_lower = recipe_request.lower()
    for recipe, ingredients in recipes.items():
        if recipe in recipe_request_lower:
            return {"recipe": recipe, "ingredients": ingredients}
    
    return {"recipe": "unknown", "ingredients": []}

@tool
def create_cart_session(user_id: str, session_type: str = "recipe_based") -> Dict:
    """Create a new cart session for the user"""
    try:
        session_data = {
            "user_id": user_id,
            "session_id": f"session_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "session_type": session_type,
            "active": True,
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
            "metadata": {"created_from": "recipe_assistant"}
        }
        
        response = supabase.table('cart_sessions').insert(session_data).execute()
        
        return {
            "success": True,
            "session_id": response.data[0]["session_id"],
            "data": response.data[0]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@tool
def check_ingredient_availability(ingredient_name: str, category: Optional[str] = None) -> Dict:
    """Check if an ingredient exists in the products table and fetch available options"""
    try:
        # Build query
        query = supabase.table('products').select('*').eq('is_active', True)
        
        # Search by item name
        query = query.ilike('item_name', f'%{ingredient_name}%')
        
        # Filter by category if provided
        if category:
            query = query.eq('category', category)
        
        response = query.execute()
        
        if response.data:
            return {
                "available": True,
                "options": response.data,
                "count": len(response.data)
            }
        else:
            return {
                "available": False,
                "options": [],
                "count": 0
            }
    except Exception as e:
        return {
            "available": False,
            "error": str(e),
            "options": []
        }

@tool
def get_product_details_for_comparison(skus: List[str]) -> List[Dict]:
    """Fetch detailed product information including nutritional values for comparison"""
    try:
        response = supabase.table('products').select('*').in_('sku', skus).eq('is_active', True).execute()
        
        # Format product details for comparison
        products = []
        for item in response.data:
            products.append({
                "id": item.get("id"),
                "sku": item.get("sku"),
                "item_name": item.get("item_name"),
                "brand": item.get("brand"),
                "price": float(item.get("price", 0)),
                "quantity": item.get("quantity"),
                "unit": item.get("unit"),
                "price_per_unit": f"${float(item.get('price', 0))}/{item.get('quantity')}{item.get('unit')}",
                "category": item.get("category"),
                "nutritional_info": {
                    "calories_per_100g": item.get("calories_per_100g"),
                    "protein_g": float(item.get("protein_g", 0)),
                    "fat_g": float(item.get("fat_g", 0)),
                    "carbs_g": float(item.get("carbs_g", 0)),
                    "sugar_g": float(item.get("sugar_g", 0))
                },
                "allergens": item.get("allergens", "").split(",") if item.get("allergens") else [],
                "stock_quantity": item.get("stock_quantity", 0),
                "in_stock": item.get("stock_quantity", 0) > 0
            })
        
        # Sort by price for easy comparison
        products.sort(key=lambda x: x["price"])
        
        return products
    except Exception as e:
        print(f"Error fetching product details: {e}")
        return []

@tool
def add_to_cart(user_id: str, sku: str, quantity: int = 1, notes: str = "", session_id: str = None) -> Dict:
    """Add a selected product to the shopping cart with session tracking"""
    try:
        # First, get product details
        product_response = supabase.table('products').select('*').eq('sku', sku).single().execute()
        product = product_response.data
        
        if not product:
            return {
                "success": False,
                "error": "Product not found"
            }
        
        # Check stock availability
        if product.get('stock_quantity', 0) < quantity:
            return {
                "success": False,
                "error": f"Insufficient stock. Only {product.get('stock_quantity')} available"
            }
        
        # Check if item already exists in active cart
        existing = supabase.table('shopping_carts').select('*').match({
            'user_id': user_id,
            'sku': sku,
            'status': 'active'
        }).execute()
        
        unit_price = float(product.get('price', 0))
        
        if existing.data:
            # Update quantity if item exists
            new_quantity = existing.data[0]['quantity'] + quantity
            total_price = new_quantity * unit_price
            
            response = supabase.table('shopping_carts').update({
                'quantity': new_quantity,
                'total_price': total_price,
                'updated_at': datetime.now().isoformat()
            }).eq('id', existing.data[0]['id']).execute()
            
            action = "updated"
        else:
            # Insert new item WITH SESSION_ID
            cart_item = {
                'user_id': user_id,
                'sku': sku,
                'product_name': product.get('item_name'),
                'brand': product.get('brand'),
                'quantity': quantity,
                'unit_price': unit_price,
                'notes': notes,
                'status': 'active',
                'session_id': session_id  
            }
            
            response = supabase.table('shopping_carts').insert(cart_item).execute()
            action = "added"
        
        return {
            "success": True,
            "message": f"Item {action} to cart",
            "data": response.data[0]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@tool
def get_user_cart(user_id: str, status: str = "active") -> Dict:
    """Retrieve the current cart contents for a user"""
    try:
        # Get cart items with product details
        response = supabase.table('shopping_carts').select('*').match({
            'user_id': user_id,
            'status': status
        }).execute()
        
        cart_items = response.data
        total_price = sum(float(item.get('total_price', 0)) for item in cart_items)
        total_items = sum(item.get('quantity', 0) for item in cart_items)
        
        # Group by brand for summary
        brands = {}
        for item in cart_items:
            brand = item.get('brand', 'Unknown')
            if brand not in brands:
                brands[brand] = 0
            brands[brand] += 1
        
        return {
            "user_id": user_id,
            "items": cart_items,
            "item_count": len(cart_items),
            "total_items": total_items,
            "total_price": round(total_price, 2),
            "brands_summary": brands,
            "status": status
        }
    except Exception as e:
        return {
            "error": str(e),
            "items": [],
            "total_price": 0
        }

@tool
def remove_from_cart(user_id: str, sku: str) -> Dict:
    """Remove an item from the user's cart by marking it as removed"""
    try:
        # Update status to 'removed' instead of deleting
        response = supabase.table('shopping_carts').update({
            'status': 'removed',
            'updated_at': datetime.now().isoformat()
        }).match({
            'user_id': user_id,
            'sku': sku,
            'status': 'active'
        }).execute()
        
        if response.data:
            return {
                "success": True,
                "message": "Item removed from cart"
            }
        else:
            return {
                "success": False,
                "message": "Item not found in cart"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@tool
def update_cart_quantity(user_id: str, sku: str, new_quantity: int) -> Dict:
    """Update the quantity of an item in the cart"""
    try:
        if new_quantity <= 0:
            return remove_from_cart(user_id, sku)
        
        # Get current cart item and product info
        cart_item = supabase.table('shopping_carts').select('*').match({
            'user_id': user_id,
            'sku': sku,
            'status': 'active'
        }).single().execute()
        
        if not cart_item.data:
            return {
                "success": False,
                "error": "Item not found in cart"
            }
        
        # Check stock availability
        product = supabase.table('products').select('stock_quantity').eq('sku', sku).single().execute()
        if product.data.get('stock_quantity', 0) < new_quantity:
            return {
                "success": False,
                "error": f"Insufficient stock. Only {product.data.get('stock_quantity')} available"
            }
        
        # Update quantity and total price
        unit_price = float(cart_item.data.get('unit_price', 0))
        new_total = new_quantity * unit_price
        
        response = supabase.table('shopping_carts').update({
            'quantity': new_quantity,
            'updated_at': datetime.now().isoformat()
        }).eq('id', cart_item.data['id']).execute()
        
        return {
            "success": True,
            "message": "Quantity updated",
            "data": response.data[0]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@tool
def search_alternatives(ingredient_name: str, exclude_skus: List[str] = [], category: str = None) -> List[Dict]:
    """Search for alternative products when the requested item is not available"""
    try:
        query = supabase.table('products').select('*').eq('is_active', True)
        
        # Search in item_name or category
        if category:
            query = query.or_(f'item_name.ilike.%{ingredient_name}%,category.eq.{category}')
        else:
            query = query.ilike('item_name', f'%{ingredient_name}%')
        
        # Exclude specific SKUs if provided
        if exclude_skus:
            query = query.not_.in_('sku', exclude_skus)
        
        # Only get items in stock
        query = query.gt('stock_quantity', 0)
        
        response = query.limit(5).execute()
        
        alternatives = []
        for product in response.data:
            alternatives.append({
                "sku": product.get("sku"),
                "item_name": product.get("item_name"),
                "brand": product.get("brand"),
                "price": float(product.get("price", 0)),
                "quantity": f"{product.get('quantity')} {product.get('unit')}",
                "category": product.get("category"),
                "in_stock": product.get("stock_quantity", 0) > 0
            })
        
        return alternatives
    except Exception as e:
        print(f"Error finding alternatives: {e}")
        return []

@tool
def checkout_cart(user_id: str, shipping_address: str, delivery_date: str = None, special_instructions: str = "") -> Dict:
    """Convert active cart items to an order"""
    try:
        # Get active cart items
        cart_response = supabase.table('shopping_carts').select('*').match({
            'user_id': user_id,
            'status': 'active'
        }).execute()
        
        if not cart_response.data:
            return {
                "success": False,
                "error": "Cart is empty"
            }
        
        # Calculate total amount
        total_amount = sum(float(item.get('total_price', 0)) for item in cart_response.data)
        
        # Create order
        order_number = f"ORD-{user_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        order_data = {
            'user_id': user_id,
            'order_number': order_number,
            'total_amount': total_amount,
            'order_status': 'pending',
            'shipping_address': shipping_address,
            'delivery_date': delivery_date,
            'special_instructions': special_instructions
        }
        
        order_response = supabase.table('orders').insert(order_data).execute()
        order_id = order_response.data[0]['id']
        
        # Create order items from cart
        order_items = []
        for cart_item in cart_response.data:
            order_items.append({
                'order_id': order_id,
                'sku': cart_item.get('sku'),
                'product_name': cart_item.get('product_name'),
                'brand': cart_item.get('brand'),
                'quantity': cart_item.get('quantity'),
                'unit_price': cart_item.get('unit_price'),
                'total_price': cart_item.get('total_price')
            })
        
        # Insert order items
        supabase.table('order_items').insert(order_items).execute()
        
        # Update cart items with order_id and status to 'purchased'
        cart_ids = [item['id'] for item in cart_response.data]
        supabase.table('shopping_carts').update({
            'status': 'purchased',
            'order_id': order_id,  # Add order_id reference
            'updated_at': datetime.now().isoformat()
        }).in_('id', cart_ids).execute()
        
        # Update product stock quantities
        for cart_item in cart_response.data:
            product_response = supabase.table('products').select('stock_quantity').eq('sku', cart_item['sku']).single().execute()
            new_stock = product_response.data['stock_quantity'] - cart_item['quantity']
            
            supabase.table('products').update({
                'stock_quantity': max(0, new_stock),
                'updated_at': datetime.now().isoformat()
            }).eq('sku', cart_item['sku']).execute()
        
        return {
            "success": True,
            "order_id": order_id,
            "order_number": order_number,
            "total_amount": total_amount,
            "item_count": len(order_items)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
@tool
def get_nutrition_comparison(skus: List[str]) -> List[Dict]:
    """Compare nutritional information for multiple products"""
    try:
        response = supabase.table('products').select(
            'sku, item_name, brand, calories_per_100g, protein_g, fat_g, carbs_g, sugar_g, allergens'
        ).in_('sku', skus).execute()
        
        comparisons = []
        for product in response.data:
            comparisons.append({
                "sku": product.get("sku"),
                "name": f"{product.get('brand')} {product.get('item_name')}",
                "nutrition_per_100g": {
                    "calories": product.get("calories_per_100g", 0),
                    "protein": f"{product.get('protein_g', 0)}g",
                    "fat": f"{product.get('fat_g', 0)}g",
                    "carbs": f"{product.get('carbs_g', 0)}g",
                    "sugar": f"{product.get('sugar_g', 0)}g"
                },
                "allergens": product.get("allergens", "None").split(",") if product.get("allergens") else ["None"]
            })
        
        return comparisons
    except Exception as e:
        print(f"Error comparing nutrition: {e}")
        return []

@tool
def clear_expired_sessions() -> Dict:
    """Clean up expired cart sessions"""
    try:
        # Update expired sessions to inactive
        response = supabase.table('cart_sessions').update({
            'active': False
        }).lt('expires_at', datetime.now().isoformat()).eq('active', True).execute()
        
        return {
            "success": True,
            "sessions_expired": len(response.data)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Create the tool list for LangGraph
tools = [
    extract_recipe_ingredients,
    create_cart_session,
    check_ingredient_availability,
    get_product_details_for_comparison,
    add_to_cart,
    get_user_cart,
    remove_from_cart,
    update_cart_quantity,
    search_alternatives,
    checkout_cart,
    get_nutrition_comparison,
    clear_expired_sessions
]


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
)


# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)

# Define the system prompt
SYSTEM_PROMPT = """You are a helpful shopping assistant that helps users order ingredients for recipes.

When a user mentions a recipe:
1. First use extract_recipe_ingredients to get the ingredient list
2. Create a cart session using create_cart_session with the user_id from state
3. For each ingredient:
   - Use check_ingredient_availability to find options
   - If multiple options exist, present them clearly to the user and wait for selection
   - If only one option exists, add it directly to cart
   - If no options exist, use search_alternatives
4. Use add_to_cart with the session_id from state when adding items
5. Show cart summary with get_user_cart
6. Ask if they want to checkout

Always be helpful and explain the options clearly, including prices and quantities."""

def cartbot(state: State):
    """Main chatbot that processes messages and decides on tool usage"""
    messages = state["messages"]
    #Add system messgage if not present
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    # Add user id or sessionid on the latest message
    if state.get("user_id") or state.get("session_id"):
        context = f"Context user_id: {state.get('user_id')}, session_id: {state.get('session_id')}"
        messages = messages + [SystemMessage(content=context)]

    response = llm_with_tools.invoke(messages)
    return {'messages': [response]}

# routing function
def should_continue(state: State) -> Literal["tools", "continue", "end"]:
    """Determine if the conversation should continue based on the last message"""
    message = state['messages']
    last_message = message[-1] 

    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    # If the conversation seems complete (checking for common end phrases)
    if isinstance(last_message, AIMessage) and (
        "thank you" in last_message.content.lower() or
        "goodbye" in last_message.content.lower() or
        "done" in last_message.content.lower() or
        "checkout?" in last_message.content.lower() or
        "complete your order" in last_message.content.lower() or
        "anything else" in last_message.content.lower()
    ):
        return "continue"
    return "continue"

def create_graph_with_checkpointing():
    "create a graph with checkpointing"
    graph_builder  = StateGraph(State)

    graph_builder.add_node("agent" , cartbot)
    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)

    # Set entry point
    graph_builder.set_entry_point("agent")

    # Add edges
    graph_builder.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "continue": "agent",
            "end": END
        }
    )
    graph_builder.add_edge("tools", "agent")
    # Compile with checkpointing
    saver = PostgresSaver.from_conn_string(os.getenv("SUPABASE_URL"))

    graph = graph_builder.compile(checkpointer=saver)

    try:
        graph_image = graph.get_graph().draw_mermaid_png()
        with open("graph.mermaid.png", "wb") as f:
           f.write(graph_image)
    except Exception as e:
        print("Could not generate PNG:", e)
        print(graph.get_graph().draw_mermaid())

    return graph, saver











