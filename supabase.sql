

CREATE TABLE public.cart_sessions (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  user_id text NOT NULL,
  session_id text NOT NULL UNIQUE,
  session_type text DEFAULT 'general'::text CHECK (session_type = ANY (ARRAY['general'::text, 'recipe_based'::text, 'bulk_order'::text])),
  active boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT now(),
  expires_at timestamp with time zone,
  metadata jsonb,
  CONSTRAINT cart_sessions_pkey PRIMARY KEY (id)
);
CREATE TABLE public.order_items (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  order_id uuid NOT NULL,
  sku text NOT NULL,
  product_name text,
  brand text,
  quantity integer NOT NULL CHECK (quantity > 0),
  unit_price numeric NOT NULL CHECK (unit_price >= 0::numeric),
  total_price numeric NOT NULL,
  CONSTRAINT order_items_pkey PRIMARY KEY (id),
  CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id),
  CONSTRAINT order_items_sku_fkey FOREIGN KEY (sku) REFERENCES public.products(sku)
);
CREATE TABLE public.orders (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  user_id text NOT NULL,
  order_number text NOT NULL UNIQUE,
  total_amount numeric NOT NULL CHECK (total_amount >= 0::numeric),
  order_status text DEFAULT 'pending'::text CHECK (order_status = ANY (ARRAY['pending'::text, 'confirmed'::text, 'processing'::text, 'shipped'::text, 'delivered'::text, 'cancelled'::text])),
  payment_method text,
  shipping_address text,
  delivery_date date,
  special_instructions text,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT orders_pkey PRIMARY KEY (id)
);
CREATE TABLE public.products (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  item_name text NOT NULL,
  sku text NOT NULL UNIQUE,
  brand text NOT NULL,
  quantity integer NOT NULL,
  unit text NOT NULL,
  category text NOT NULL,
  calories_per_100g integer,
  protein_g numeric,
  fat_g numeric,
  carbs_g numeric,
  sugar_g numeric,
  allergens text,
  price numeric NOT NULL,
  stock_quantity integer DEFAULT 100,
  is_active boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT products_pkey PRIMARY KEY (id)
);
CREATE TABLE public.shopping_carts (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  user_id text NOT NULL,
  sku text NOT NULL,
  product_name text,
  brand text,
  quantity integer NOT NULL CHECK (quantity > 0),
  unit_price numeric NOT NULL CHECK (unit_price >= 0::numeric),
  total_price numeric DEFAULT ((quantity)::numeric * unit_price),
  notes text,
  added_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  status text DEFAULT 'active'::text CHECK (status = ANY (ARRAY['active'::text, 'purchased'::text, 'removed'::text, 'pending'::text])),
  session_id text,
  order_id uuid,
  CONSTRAINT shopping_carts_pkey PRIMARY KEY (id),
  CONSTRAINT shopping_carts_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.cart_sessions(session_id),
  CONSTRAINT shopping_carts_sku_fkey FOREIGN KEY (sku) REFERENCES public.products(sku),
  CONSTRAINT shopping_carts_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id)
);