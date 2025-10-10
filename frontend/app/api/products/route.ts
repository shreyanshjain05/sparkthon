import { NextResponse } from 'next/server'
import { supabase } from '@/lib/supabase/db'

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url)
    const query = searchParams.get('q') || ''
    const category = searchParams.get('category') || ''

    let dbQuery = supabase
      .from('products')
      .select('*')
      .eq('is_active', true)

    // Apply search filter if query exists
    if (query) {
      dbQuery = dbQuery.or(`item_name.ilike.%${query}%,brand.ilike.%${query}%,category.ilike.%${query}%`)
    }

    // Apply category filter if category exists
    if (category) {
      dbQuery = dbQuery.eq('category', category)
    }

    const { data: products, error } = await dbQuery

    if (error) {
      console.error('Database error:', error)
      return NextResponse.json({ error: 'Failed to fetch products' }, { status: 500 })
    }

    // Return the raw database data
    const transformedProducts = products.map(product => ({
      id: product.id,
      item_name: product.item_name,
      sku: product.sku,
      brand: product.brand,
      quantity: product.quantity,
      unit: product.unit,
      category: product.category,
      calories_per_100g: product.calories_per_100g,
      protein_g: product.protein_g,
      fat_g: product.fat_g,
      carbs_g: product.carbs_g,
      sugar_g: product.sugar_g,
      allergens: product.allergens,
      price: product.price,
      stock_quantity: product.stock_quantity,
      is_active: product.is_active,
      created_at: product.created_at,
      updated_at: product.updated_at
    }))

    return NextResponse.json({ products: transformedProducts })
  } catch (error) {
    console.error('API error:', error)
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
  }
}