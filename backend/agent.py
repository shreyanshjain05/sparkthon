from typing import List, Dict, TypedDict, Optional, Literal, Any
from langchain.tools import tool
from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import uuid
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.runnables import Runnable
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.prebuilt import ToolNode
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
import uvicorn

# Load environment variables
load_dotenv(dotenv_path="../.env")

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# use llm to get ingredients
llm_ing = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
)

# State definition
class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    session_id: str


@tool
def extract_recipe_ingredients(recipe_request: str) -> str:
    """Extract required ingredients from a recipe request using an LLM. Returns a JSON string."""

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a helpful assistant that extracts ingredients from the recipe mentioned by the user. "
            "Return a JSON object in the following format ONLY:\n"
            '{"recipe": "<name_of_recipe>", "ingredients": ["ingredient1", "ingredient2", "..."]}'
        ),
        ("human", "{recipe_request}"),
    ])

    chain: Runnable = prompt | llm_ing
    result = chain.invoke({"recipe_request": recipe_request})

    try:
        json_obj = json.loads(result)
        return json.dumps(json_obj)
    except json.JSONDecodeError:
        return json.dumps({
            "recipe": "unknown",
            "ingredients": []
        })


@tool
def check_ingredient_availability(ingredient_name: str, category: Optional[str] = None) -> str:
    """Check if an ingredient exists in the products table and fetch available options. Returns a JSON string."""
    try:
        query = supabase.table('products').select('*').eq('is_active', True)
        query = query.ilike('item_name', f'%{ingredient_name}%')
        if category:
            query = query.eq('category', category)
        
        response = query.execute()
        
        if response.data:
            result = {
                "available": True,
                "options": response.data,
                "count": len(response.data)
            }
            return json.dumps(result)
        else:
            result = {
                "available": False,
                "options": [],
                "count": 0
            }
            return json.dumps(result)
    except Exception as e:
        result = {
            "available": False,
            "error": str(e),
            "options": []
        }
        return json.dumps(result)

@tool
def create_cart_session(user_id: str, session_type: str = "recipe_based") -> str:
    """Create a new cart session for the user. Returns a JSON string."""
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
        result = {
            "success": True,
            "session_id": response.data[0]["session_id"],
            "data": response.data[0]
        }
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool
def get_product_details_for_comparison(skus: List[str]) -> str:
    """Fetch detailed product information for comparison. Returns a JSON string."""
    try:
        response = supabase.table('products').select('*').in_('sku', skus).eq('is_active', True).execute()
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
                "price_per_unit": f"₹{float(item.get('price', 0))}/{item.get('quantity')}{item.get('unit')}",
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
        products.sort(key=lambda x: x["price"])
        return json.dumps(products)
    except Exception as e:
        print(f"Error fetching product details: {e}")
        return json.dumps([])

@tool
def add_to_cart(user_id: str, sku: str, quantity: int = 1, notes: str = "", session_id: str = None) -> str:
    """Add a selected product to the shopping cart with session tracking. Returns a JSON string."""
    try:
        # Verify product exists
        product_response = supabase.table('products').select('*').eq('sku', sku).single().execute()
        product = product_response.data
        if not product:
            return json.dumps({"success": False, "error": "Product not found"})
        
        if product.get('stock_quantity', 0) < quantity:
            return json.dumps({"success": False, "error": f"Insufficient stock. Only {product.get('stock_quantity')} available"})
        
        # Verify or create session_id
        if not session_id:
            return json.dumps({"success": False, "error": "session_id is required (foreign key constraint)"})
        
        # Check if session exists
        session_check = supabase.table('cart_sessions').select('session_id').eq('session_id', session_id).execute()
        if not session_check.data:
            return json.dumps({"success": False, "error": f"Session {session_id} does not exist. Please create a cart session first."})
        
        existing = supabase.table('shopping_carts').select('*').match({'user_id': user_id, 'sku': sku, 'status': 'active', 'session_id': session_id}).execute()
        unit_price = float(product.get('price', 0))
        
        if existing.data:
            new_quantity = existing.data[0]['quantity'] + quantity
            response = supabase.table('shopping_carts').update({
                'quantity': new_quantity,
                'updated_at': datetime.now().isoformat()
            }).eq('id', existing.data[0]['id']).execute()
            action = "updated"
        else:
            cart_item = {
                'user_id': user_id,
                'sku': sku,
                'product_name': product.get('item_name'),
                'brand': product.get('brand'),
                'quantity': quantity,
                'unit_price': unit_price,
                'notes': notes or '',
                'status': 'active',
                'session_id': session_id
            }
            response = supabase.table('shopping_carts').insert(cart_item).execute()
            action = "added"
        
        result = {"success": True, "message": f"Item {action} to cart", "data": response.data[0]}
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool
def get_user_cart(user_id: str, status: str = "active") -> str:
    """Retrieve the current cart contents for a user. Returns a JSON string."""
    try:
        response = supabase.table('shopping_carts').select('*').match({'user_id': user_id, 'status': status}).execute()
        cart_items = response.data
        total_price = sum(float(item.get('unit_price', 0)) * item.get('quantity', 0) for item in cart_items)
        total_items = sum(item.get('quantity', 0) for item in cart_items)
        
        brands = {}
        for item in cart_items:
            brand = item.get('brand', 'Unknown')
            if brand not in brands:
                brands[brand] = 0
            brands[brand] += 1
        
        result = {
            "user_id": user_id, "items": cart_items, "item_count": len(cart_items), "total_items": total_items,
            "total_price": round(total_price, 2), "brands_summary": brands, "status": status
        }
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e), "items": [], "total_price": 0})

@tool
def remove_from_cart(user_id: str, sku: str) -> str:
    """Remove an item from the user's cart by marking it as removed. Returns a JSON string."""
    try:
        response = supabase.table('shopping_carts').update({'status': 'removed', 'updated_at': datetime.now().isoformat()}).match({'user_id': user_id, 'sku': sku, 'status': 'active'}).execute()
        if response.data:
            return json.dumps({"success": True, "message": "Item removed from cart"})
        else:
            return json.dumps({"success": False, "message": "Item not found in cart"})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool
def update_cart_quantity(user_id: str, sku: str, new_quantity: int) -> str:
    """Update the quantity of an item in the cart. Returns a JSON string."""
    try:
        if new_quantity <= 0:
            return remove_from_cart(user_id, sku)
        
        cart_item = supabase.table('shopping_carts').select('*').match({'user_id': user_id, 'sku': sku, 'status': 'active'}).single().execute()
        if not cart_item.data:
            return json.dumps({"success": False, "error": "Item not found in cart"})
        
        product = supabase.table('products').select('stock_quantity').eq('sku', sku).single().execute()
        if product.data.get('stock_quantity', 0) < new_quantity:
            return json.dumps({"success": False, "error": f"Insufficient stock. Only {product.data.get('stock_quantity')} available"})
        
        response = supabase.table('shopping_carts').update({'quantity': new_quantity, 'updated_at': datetime.now().isoformat()}).eq('id', cart_item.data['id']).execute()
        return json.dumps({"success": True, "message": "Quantity updated", "data": response.data[0]})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool
def search_alternatives(ingredient_name: str, exclude_skus: List[str] = [], category: str = None) -> str:
    """Search for alternative products. Returns a JSON string."""
    try:
        query = supabase.table('products').select('*').eq('is_active', True)
        if category:
            query = query.or_(f'item_name.ilike.%{ingredient_name}%,category.eq.{category}')
        else:
            query = query.ilike('item_name', f'%{ingredient_name}%')
        if exclude_skus:
            query = query.not_.in_('sku', exclude_skus)
        query = query.gt('stock_quantity', 0)
        response = query.limit(5).execute()
        
        alternatives = []
        for product in response.data:
            alternatives.append({
                "sku": product.get("sku"), "item_name": product.get("item_name"), "brand": product.get("brand"),
                "price": float(product.get("price", 0)), "quantity": f"{product.get('quantity')} {product.get('unit')}",
                "category": product.get("category"), "in_stock": product.get("stock_quantity", 0) > 0
            })
        return json.dumps(alternatives)
    except Exception as e:
        print(f"Error finding alternatives: {e}")
        return json.dumps([])

@tool
def checkout_cart(user_id: str, shipping_address: str = "Default Address", delivery_date: str = None, special_instructions: str = "") -> str:
    """Convert active cart items to an order. Returns a JSON string."""
    try:
        # Validate inputs
        if not user_id:
            return json.dumps({"success": False, "error": "User ID is required"})
        
        if not shipping_address or shipping_address.strip() == "":
            shipping_address = "Default Delivery Address"
        
        # Fetch cart items
        cart_response = supabase.table('shopping_carts').select('*').match({'user_id': user_id, 'status': 'active'}).execute()
        
        if not cart_response.data:
            return json.dumps({"success": False, "error": "Cart is empty"})
        
        # Calculate totals
        total_amount = sum(float(item.get('unit_price', 0)) * item.get('quantity', 0) for item in cart_response.data)
        order_number = f"ORD-{user_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Parse delivery_date properly (schema expects 'date' type)
        parsed_delivery_date = None
        if delivery_date:
            try:
                parsed_delivery_date = datetime.fromisoformat(delivery_date).date().isoformat()
            except:
                parsed_delivery_date = datetime.now().date().isoformat()
        else:
            parsed_delivery_date = datetime.now().date().isoformat()
        
        # Create order (no created_at field in schema, will use default)
        order_data = {
            'user_id': user_id,
            'order_number': order_number,
            'total_amount': round(total_amount, 2),
            'order_status': 'pending',
            'shipping_address': shipping_address,
            'delivery_date': parsed_delivery_date,
            'special_instructions': special_instructions or ''
        }
        
        order_response = supabase.table('orders').insert(order_data).execute()
        
        if not order_response.data:
            return json.dumps({"success": False, "error": "Failed to create order"})
        
        order_id = order_response.data[0]['id']
        
        # Create order items (DO NOT include total_price as it's a generated column)
        order_items = [
            {
                'order_id': order_id,
                'sku': item.get('sku'),
                'product_name': item.get('product_name'),
                'brand': item.get('brand'),
                'quantity': item.get('quantity'),
                'unit_price': float(item.get('unit_price'))
            }
            for item in cart_response.data
        ]
        
        supabase.table('order_items').insert(order_items).execute()
        
        # Update cart status (add order_id as per schema foreign key)
        cart_ids = [item['id'] for item in cart_response.data]
        supabase.table('shopping_carts').update({
            'status': 'purchased',
            'order_id': order_id,
            'updated_at': datetime.now().isoformat()
        }).in_('id', cart_ids).execute()
        
        # Update product stock
        for item in cart_response.data:
            try:
                product_response = supabase.table('products').select('stock_quantity').eq('sku', item['sku']).single().execute()
                new_stock = product_response.data['stock_quantity'] - item['quantity']
                supabase.table('products').update({
                    'stock_quantity': max(0, new_stock),
                    'updated_at': datetime.now().isoformat()
                }).eq('sku', item['sku']).execute()
            except Exception as stock_error:
                print(f"Warning: Could not update stock for SKU {item['sku']}: {stock_error}")
        
        result = {
            "success": True,
            "order_id": order_id,
            "order_number": order_number,
            "total_amount": round(total_amount, 2),
            "item_count": len(order_items),
            "message": f"Order placed successfully! Order number: {order_number}"
        }
        return json.dumps(result)
    
    except Exception as e:
        print(f"Checkout error: {str(e)}")
        return json.dumps({"success": False, "error": f"Checkout failed: {str(e)}"})

@tool
def get_nutrition_comparison(skus: List[str]) -> str:
    """Compare nutritional information for multiple products. Returns a JSON string."""
    try:
        response = supabase.table('products').select('sku, item_name, brand, calories_per_100g, protein_g, fat_g, carbs_g, sugar_g, allergens').in_('sku', skus).execute()
        comparisons = []
        for product in response.data:
            comparisons.append({
                "sku": product.get("sku"), "name": f"{product.get('brand')} {product.get('item_name')}",
                "nutrition_per_100g": {"calories": product.get("calories_per_100g", 0), "protein": f"{product.get('protein_g', 0)}g", "fat": f"{product.get('fat_g', 0)}g", "carbs": f"{product.get('carbs_g', 0)}g", "sugar": f"{product.get('sugar_g', 0)}g"},
                "allergens": product.get("allergens", "None").split(",") if product.get("allergens") else ["None"]
            })
        return json.dumps(comparisons)
    except Exception as e:
        print(f"Error comparing nutrition: {e}")
        return json.dumps([])

@tool
def clear_expired_sessions() -> str:
    """Clean up expired cart sessions. Returns a JSON string."""
    try:
        response = supabase.table('cart_sessions').update({'active': False}).lt('expires_at', datetime.now().isoformat()).eq('active', True).execute()
        return json.dumps({"success": True, "sessions_expired": len(response.data)})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


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
    timeout=30,
    max_retries=2,
)

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = """You are a helpful and highly conversational shopping assistant. Your primary goal is to guide a user through adding ingredients for a recipe to their cart, one step at a time. You MUST be conversational.

When displaying prices, always use the Indian Rupee symbol (₹) instead of dollar signs.

**Core Conversation Flow:**

**Rule 1: Initial Recipe Request**
- When the user mentions a recipe, your first job is to use two tools in parallel: `extract_recipe_ingredients` and `create_cart_session`.
- **CRITICAL:** After these tools run and you get the ingredient list and session_id, you MUST stop and talk to the user. DO NOT call any other tools yet.
- Your response should confirm the recipe and list the ingredients. Example: "Great, let's shop for pasta! The ingredients are: pasta, tomato sauce, garlic, olive oil, cheese, and basil. I'll start by finding options for 'pasta'. Is that okay?"

**Rule 2: Finding Ingredient Options**
- When the user confirms, proceed with the first ingredient. Use the `check_ingredient_availability` tool for that ONE ingredient.
- **CRITICAL:** After the tool returns the available products, you MUST stop and present these options to the user. DO NOT move on to the next ingredient.
- Your response should be a clear, numbered list of choices with prices in ₹. Ask the user to pick one.

**Rule 3: Adding to Cart**
- When the user makes a choice, use the `add_to_cart` tool with the correct SKU and session_id.
- **CRITICAL:** After adding the item, you MUST confirm it to the user and then propose the next step.

**Rule 4: Checkout**
- When the user requests checkout, ONLY call the `checkout_cart` tool. DO NOT call get_user_cart afterwards.
- After checkout_cart returns, parse the JSON response to check if "success" is true.
- If success is true, display a success message with:
  * Order number from the response
<<<<<<< HEAD
  * Total amount in ₹ from the response
=======
>>>>>>> 5ccee3e (auth and stuff all done)
  * Item count from the response
  * Thank the user and confirm their order is being processed
- If success is false, explain the error from the response.
- NEVER call get_user_cart after checkout - the cart will be empty because items are marked as purchased.
"""

def cartbot(state: State):
    """Main chatbot that handles the conversation"""
    messages = state["messages"]

    # Add system message if not already present
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    # Add user_id and session_id to the context
    context_info = []
    if state.get("user_id"):
        context_info.append(f"user_id={state['user_id']}")
    if state.get("session_id"):
        context_info.append(f"session_id={state['session_id']}")

    if context_info:
        context = f"\n\nCurrent context: {', '.join(context_info)}"
        messages.append(SystemMessage(content=context))

    # Invoke the LLM with tools
    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}

# routing function
def should_continue(state: State) -> Literal["tools", "end"]:
    """Determine if the conversation should continue based on the last message"""
    messages = state['messages']
    last_message = messages[-1] if messages else None

    # If the last message has tool calls, go to tools
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    
    # Otherwise, end the conversation cycle (but continue chatting)
    return "end"

# Helper function to build the graph
def build_graph():
    """Build the LangGraph structure with tools and conditional routing"""
    graph_builder = StateGraph(State)

    # Add nodes
    graph_builder.add_node("agent", cartbot)
    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)

    # Set entry point
    graph_builder.set_entry_point("agent")

    # Simplified routing - no self-loops
    graph_builder.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )

    # Tools always return to the agent
    graph_builder.add_edge("tools", "agent")

    return graph_builder

def chat_with_recipe_bot(user_id: str, thread_id: str = None):
    """Run an interactive chat session by manually managing message history."""
    print("What's on the menu today?")
    print("Type 'quit' to exit\n")

    if thread_id is None:
        thread_id = str(uuid.uuid4())

    # Compile the graph
    graph = build_graph().compile()
    
    config = {"recursion_limit": 50}

    messages = []

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            break

        if user_input.lower() in ["quit", "exit", "bye"]:
            print("\nThank you for shopping with us! 👋")
            break

        if not user_input:
            continue
            
        messages.append(HumanMessage(content=user_input))
        input_data = {"messages": messages}

        try:
            print("Processing...")
            result = graph.invoke(input_data, config=config)
            messages = result['messages']
            
            latest_ai_message = messages[-1]
            if isinstance(latest_ai_message, AIMessage) and latest_ai_message.content:
                print(f"\nAssistant: {latest_ai_message.content}")
            
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Let's try that again.")
            messages.pop()
    
    return thread_id

graph = build_graph()
graph = graph.compile()

app = FastAPI(title="Simple Recipe Chatbot API")

conversation_history = []

@app.get("/api/search")
async def search_products(q: str = ""):
    """Search for products in the database"""
    if not q.strip():
        return {"products": [], "count": 0}
    
    try:
        response = supabase.table('products').select('*').eq('is_active', True).ilike('item_name', f'%{q}%').limit(10).execute()
        
        products = []
        for item in response.data:
            products.append({
                "id": item.get("id"),
                "sku": item.get("sku"),
                "name": item.get("item_name"),
                "brand": item.get("brand"),
                "price": float(item.get("price", 0)),
                "category": item.get("category"),
                "in_stock": item.get("stock_quantity", 0) > 0,
                "stock_quantity": item.get("stock_quantity", 0)
            })
        
        return {"products": products, "count": len(products)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Recipe Chatbot API is running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """A single endpoint for the chatbot."""
    await websocket.accept()
    global conversation_history
    conversation_history = []

    try:
        while True:
            data = await websocket.receive_text()
            user_input = json.loads(data).get("message")

            if not user_input:
                continue

            conversation_history.append(HumanMessage(content=user_input))

            graph_input = {
                "messages": conversation_history,
                "user_id": 'user123'
            }

            final_state = graph.invoke(graph_input)
            ai_response = final_state["messages"][-1].content
            conversation_history = final_state["messages"]

            await websocket.send_json({"response": ai_response})

    except WebSocketDisconnect:
        print("Client disconnected. Chat history has been reset.")
    except Exception as e:
        print(f"An error occurred: {e}")
<<<<<<< HEAD
        await websocket.send_json({"response": "Sorry, an error occurred. Please try again."})
=======
        await websocket.send_json({"response": "Sorry, an error occurred. Please try again."})
>>>>>>> 5ccee3e (auth and stuff all done)
