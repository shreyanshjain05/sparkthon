CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    image_url TEXT,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create a trigger to automatically update the updated_at column
CREATE TRIGGER update_categories_updated_at
    BEFORE UPDATE ON categories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert some initial categories
INSERT INTO categories (name, slug, image_url) VALUES
    ('Grocery', 'grocery', '/categories/grocery.svg'),
    ('Fresh Produce', 'fresh-produce', '/categories/produce.svg'),
    ('Dairy & Eggs', 'dairy-eggs', '/categories/dairy.svg'),
    ('Meat & Seafood', 'meat-seafood', '/categories/meat.svg'),
    ('Bakery', 'bakery', '/categories/bakery.svg'),
    ('Beverages', 'beverages', '/categories/beverages.svg'),
    ('Snacks', 'snacks', '/categories/snacks.svg'),
    ('Frozen Foods', 'frozen-foods', '/categories/frozen.svg'),
    ('Pantry', 'pantry', '/categories/pantry.svg'),
    ('Household', 'household', '/categories/household.svg')
ON CONFLICT (slug) DO NOTHING;