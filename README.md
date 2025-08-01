# 🛒 AI Recipe Shopping Assistant - Walmart Clone

An intelligent shopping assistant that helps users shop for recipe ingredients through natural conversation. Built with LangGraph for orchestrated AI workflows, this project combines a Walmart-inspired frontend with a powerful agentic backend.


### 📝 Medium Article

Complete documentation of the code and implementation can be found here:  
**_👉 [LangGraph + Supabase + Groq: Production-Grade Agentic Workflow](https://medium.com/gitconnected/langgraph-supabase-groq-api-production-grade-agentic-workflow-e3b706278b6a)_**


### Langgraph Flow


![Recipe Shopping Assistant Banner](https://github.com/shreyanshjain05/sparkthon/blob/main/backend/graph.png)

## 🎥 Demo Video


https://github.com/user-attachments/assets/d687eb69-0f4f-422e-88ad-3f24474def68


*Click the image above to watch our demo video showcasing the AI Recipe Shopping Assistant in action!*

## 🌟 Features

- **Conversational Shopping**: Chat naturally about recipes and get ingredient suggestions
- **Smart Cart Management**: AI automatically adds ingredients to your cart
- **Product Comparison**: Compare prices, nutrition, and alternatives
- **Real-time Inventory**: Check product availability instantly
- **Session Management**: Maintains shopping context throughout the conversation

## 🏗️ Architecture

### System Overview
```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│                 │     │                  │     │                 │
│  Next.js        │────▶│  FastAPI         │────▶│  Supabase      │
│  Frontend       │     │  + LangGraph     │     │  Database      │
│                 │     │                  │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```


*The agent orchestrates multiple tools to handle recipe parsing, ingredient searching, cart management, and checkout processes.*
---

## 👥 Team Credits

This project was built collaboratively by:

* **Frontend (Walmart Clone)**: [Shreya Rahul Jain](https://github.com/ShreyaRahulJain)

  * Next.js implementation
  * UI/UX design
  * Component architecture

* **Backend & Integration**: [Shreya Rahul Jain](https://github.com/ShreyaRahulJain)

  * FastAPI server setup
  * WebSocket implementation
  * Database integration

* **Agentic Model**: [Shreyansh Jain](https://github.com/shreyanshjain05) & [Chirag Vinid](https://github.com/chirag-vinid)

  * LangGraph agent design
  * Tool implementation
  * Conversation flow logic

---


## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Supabase account

### Backend Setup

1. **Clone the repository**
```bash
git clone [https://github.com/shreyanshjain05/sparkthon/](https://github.com/shreyanshjain05/sparkthon)
cd spakthon/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy .env.example to .env and fill in your credentials
cp .env.example .env
```

5. **Set up Supabase**
```bash
# Run the SQL script to create necessary tables
# Execute supabase.sql in your Supabase SQL editor
```

6. **Start the backend**
```bash
python3 agent.py
```

The backend will start on `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd ../frontend
```

2. **Install dependencies**
```bash
npm install --legacy-peer-deps
```

3. **Start the development server**
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📁 Project Structure

```
spakthon/
├── backend/
│   ├── agent.py           # Main LangGraph agent and FastAPI server
│   ├── main.py           # Additional backend utilities
│   ├── requirements.txt   # Python dependencies
│   ├── supabase.sql      # Database schema
│   ├── graph.png         # LangGraph visualization
│   └── .env.example      # Environment variables template
│
└── frontend/
    ├── app/              # Next.js app directory
    ├── components/       # React components
    ├── hooks/           # Custom React hooks
    ├── lib/             # Utility functions
    ├── public/          # Static assets
    └── styles/          # CSS styles
```

## 🔧 Environment Variables

Create a `.env` file in the backend directory with:

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key

# Groq API (for LLM)
GROQ_API_KEY=your_groq_api_key

# Optional: Other LLM providers
OPENAI_API_KEY=your_openai_key
```

## 🤖 Agent Tools

The AI assistant leverages these specialized tools:

- **`extract_recipe_ingredients`**: Parses recipes to identify required ingredients
- **`check_ingredient_availability`**: Searches product inventory
- **`add_to_cart`**: Manages shopping cart operations
- **`get_product_details_for_comparison`**: Compares product options
- **`checkout_cart`**: Processes order completion
- **`get_nutrition_comparison`**: Analyzes nutritional information

## 💬 Usage Example

```
User: "I want to make spaghetti carbonara"

Bot: "Great, let's shop for spaghetti carbonara! The ingredients are: 
spaghetti, eggs, bacon, parmesan cheese, black pepper, and garlic. 
I'll start by finding options for 'spaghetti'. Is that okay?"

User: "Yes please"

Bot: "I found a few options for pasta:
1. Barilla Spaghetti ($2.99)
2. De Cecco Spaghetti ($3.49)
3. Store Brand Spaghetti ($1.99)
Which one would you like?"

User: "Let's go with Barilla"

Bot: "Okay, I've added Barilla Spaghetti to your cart. 
Shall we look for 'eggs' next?"
```

## 🛠️ Technology Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **WebSocket** - Real-time chat communication

### Backend
- **FastAPI** - Modern Python web framework
- **LangGraph** - AI agent orchestration
- **LangChain** - LLM integration
- **Groq LLM** - Language model provider
- **Supabase** - PostgreSQL database

## 📊 Database Schema

The application uses the following main tables:
- `products` - Product inventory
- `shopping_carts` - Active cart items
- `orders` - Completed orders
- `order_items` - Order line items
- `cart_sessions` - Shopping session tracking


## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---
