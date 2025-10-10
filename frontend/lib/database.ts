export interface Product {
  id: string;
  item_name: string;
  sku: string;
  brand: string | null;
  quantity: number;
  unit: string | null;
  category: string | null;
  calories_per_100g: number | null;
  protein_g: number | null;
  fat_g: number | null;
  carbs_g: number | null;
  sugar_g: number | null;
  allergens: string | null;
  price: number;
  stock_quantity: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  image_url: string;
}
