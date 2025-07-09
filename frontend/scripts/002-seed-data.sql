-- Insert categories
INSERT INTO categories (name, slug, image_url) VALUES
('Electronics', 'electronics', '/placeholder.svg?height=200&width=200'),
('Clothing', 'clothing', '/placeholder.svg?height=200&width=200'),
('Home & Garden', 'home-garden', '/placeholder.svg?height=200&width=200'),
('Sports & Outdoors', 'sports-outdoors', '/placeholder.svg?height=200&width=200'),
('Health & Beauty', 'health-beauty', '/placeholder.svg?height=200&width=200'),
('Grocery', 'grocery', '/placeholder.svg?height=200&width=200');

-- Insert sample products
INSERT INTO products (name, description, price, image_url, category, brand, rating, reviews_count, in_stock) VALUES
('iPhone 15 Pro', 'Latest Apple smartphone with advanced camera system', 999.99, '/placeholder.svg?height=300&width=300', 'Electronics', 'Apple', 4.8, 1250, true),
('Samsung 65" 4K Smart TV', 'Ultra HD Smart TV with HDR and streaming apps', 799.99, '/placeholder.svg?height=300&width=300', 'Electronics', 'Samsung', 4.6, 890, true),
('Nike Air Max 270', 'Comfortable running shoes with air cushioning', 129.99, '/placeholder.svg?height=300&width=300', 'Clothing', 'Nike', 4.5, 2100, true),
('Instant Pot Duo 7-in-1', 'Multi-functional pressure cooker', 89.99, '/placeholder.svg?height=300&width=300', 'Home & Garden', 'Instant Pot', 4.7, 15600, true),
('Fitbit Charge 5', 'Advanced fitness tracker with GPS', 179.99, '/placeholder.svg?height=300&width=300', 'Electronics', 'Fitbit', 4.4, 3200, true),
('Levi''s 501 Original Jeans', 'Classic straight-leg denim jeans', 59.99, '/placeholder.svg?height=300&width=300', 'Clothing', 'Levi''s', 4.3, 5400, true),
('Dyson V15 Detect', 'Cordless vacuum with laser dust detection', 749.99, '/placeholder.svg?height=300&width=300', 'Home & Garden', 'Dyson', 4.6, 1800, true),
('PlayStation 5', 'Next-gen gaming console', 499.99, '/placeholder.svg?height=300&width=300', 'Electronics', 'Sony', 4.9, 8900, false),
('Adidas Ultraboost 22', 'Premium running shoes with boost technology', 189.99, '/placeholder.svg?height=300&width=300', 'Sports & Outdoors', 'Adidas', 4.5, 1200, true),
('KitchenAid Stand Mixer', 'Professional 5-quart stand mixer', 379.99, '/placeholder.svg?height=300&width=300', 'Home & Garden', 'KitchenAid', 4.8, 2800, true),
('MacBook Air M2', 'Lightweight laptop with M2 chip', 1199.99, '/placeholder.svg?height=300&width=300', 'Electronics', 'Apple', 4.7, 950, true),
('The North Face Jacket', 'Waterproof outdoor jacket', 199.99, '/placeholder.svg?height=300&width=300', 'Clothing', 'The North Face', 4.4, 680, true);
