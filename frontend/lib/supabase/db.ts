import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_SERVICE_KEY

if (!supabaseUrl || !supabaseKey) {
  throw new Error('Missing Supabase environment variables')
}

export const supabase = createClient(supabaseUrl, supabaseKey)

export interface Product {
  id: string
  item_name: string
  sku: string
  brand: string | null
  quantity: number
  unit: string | null
  category: string | null
  calories_per_100g: number | null
  protein_g: number | null
  fat_g: number | null
  carbs_g: number | null
  sugar_g: number | null
  allergens: string | null
  price: number
  stock_quantity: number
  is_active: boolean
  created_at: string
  updated_at: string
}