import { neon } from "@neondatabase/serverless"

const sql = neon(process.env.DATABASE_URL!)

export interface Product {
  id: number
  name: string
  description: string
  price: number
  image_url: string
  category: string
  brand: string
  rating: number
  reviews_count: number
  in_stock: boolean
}

export interface Category {
  id: number
  name: string
  slug: string
  image_url: string
}

export async function searchProducts(query: string): Promise<Product[]> {
  if (!query.trim()) {
    return await sql`SELECT * FROM products ORDER BY rating DESC LIMIT 12`
  }

  return await sql`
    SELECT * FROM products 
    WHERE name ILIKE ${"%" + query + "%"} 
       OR description ILIKE ${"%" + query + "%"}
       OR category ILIKE ${"%" + query + "%"}
       OR brand ILIKE ${"%" + query + "%"}
    ORDER BY rating DESC
    LIMIT 20
  `
}

export async function getCategories(): Promise<Category[]> {
  return await sql`SELECT * FROM categories ORDER BY name`
}

export async function getProductsByCategory(category: string): Promise<Product[]> {
  return await sql`
    SELECT * FROM products 
    WHERE category ILIKE ${category}
    ORDER BY rating DESC
    LIMIT 12
  `
}
