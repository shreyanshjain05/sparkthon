CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Products table
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_name TEXT NOT NULL,
    sku TEXT UNIQUE NOT NULL,
    brand TEXT,
    quantity INTEGER NOT NULL DEFAULT 0,
    unit TEXT,
    category TEXT,
    calories_per_100g INTEGER,
    protein_g NUMERIC(5,2),
    fat_g NUMERIC(5,2),
    carbs_g NUMERIC(5,2),
    sugar_g NUMERIC(5,2),
    allergens TEXT,
    price NUMERIC(10,2) NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Cart sessions table
CREATE TABLE cart_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT,
    session_id TEXT NOT NULL,
    session_type TEXT DEFAULT 'guest',
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ,
    metadata JSONB
);

-- Shopping carts table
CREATE TABLE shopping_carts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT,
    sku TEXT NOT NULL REFERENCES products(sku),
    product_name TEXT,
    brand TEXT,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price NUMERIC(10,2) NOT NULL,
    total_price NUMERIC(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    notes TEXT,
    added_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    status TEXT DEFAULT 'active',
    session_id TEXT NOT NULL,
    order_id UUID REFERENCES orders(id)
);

-- Orders table
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT NOT NULL,
    order_number TEXT UNIQUE NOT NULL,
    total_amount NUMERIC(10,2) NOT NULL,
    order_status TEXT DEFAULT 'pending',
    payment_method TEXT,
    shipping_address TEXT,
    delivery_date DATE,
    special_instructions TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Order items table
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    sku TEXT NOT NULL REFERENCES products(sku),
    product_name TEXT,
    brand TEXT,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL,
    total_price NUMERIC(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);

-- Create indexes for better performance
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_brand ON products(brand);
CREATE INDEX idx_products_is_active ON products(is_active);

CREATE INDEX idx_cart_sessions_user_id ON cart_sessions(user_id);
CREATE INDEX idx_cart_sessions_session_id ON cart_sessions(session_id);
CREATE INDEX idx_cart_sessions_active ON cart_sessions(active);

CREATE INDEX idx_shopping_carts_user_id ON shopping_carts(user_id);
CREATE INDEX idx_shopping_carts_session_id ON shopping_carts(session_id);
CREATE INDEX idx_shopping_carts_sku ON shopping_carts(sku);
CREATE INDEX idx_shopping_carts_status ON shopping_carts(status);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_order_number ON orders(order_number);
CREATE INDEX idx_orders_status ON orders(order_status);
CREATE INDEX idx_orders_created_at ON orders(created_at);

CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_sku ON order_items(sku);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers for updated_at columns
CREATE TRIGGER update_products_updated_at 
    BEFORE UPDATE ON products 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_shopping_carts_updated_at 
    BEFORE UPDATE ON shopping_carts 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_orders_updated_at 
    BEFORE UPDATE ON orders 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add foreign key constraints after all tables are created
ALTER TABLE shopping_carts 
ADD CONSTRAINT fk_shopping_carts_session_id 
FOREIGN KEY (session_id) REFERENCES cart_sessions(session_id);

-- Sample data (optional - remove if not needed)
-- Insert sample products
INSERT INTO products (item_name, sku, brand, quantity, unit, category, price, stock_quantity) VALUES
('Organic Bananas', 'BAN001', 'Fresh Farm', 6, 'pieces', 'Fruits', 3.99, 100),
('Whole Milk', 'MILK001', 'Dairy Best', 1, 'liter', 'Dairy', 2.49, 50),
('Brown Bread', 'BREAD001', 'Baker''s Choice', 1, 'loaf', 'Bakery', 1.99, 30);

-- Insert sample cart session
INSERT INTO cart_sessions (user_id, session_id, session_type) VALUES
('user123', 'sess_abc123', 'registered');

-- Insert sample shopping cart items
INSERT INTO shopping_carts (user_id, sku, product_name, brand, quantity, unit_price, session_id) VALUES
('user123', 'BAN001', 'Organic Bananas', 'Fresh Farm', 2, 3.99, 'sess_abc123'),
('user123', 'MILK001', 'Whole Milk', 'Dairy Best', 1, 2.49, 'sess_abc123');