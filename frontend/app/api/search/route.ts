import { type NextRequest, NextResponse } from "next/server"
import { searchProducts } from "@/lib/database"

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const query = searchParams.get("q") || ""

    const products = await searchProducts(query)

    return NextResponse.json({ products })
  } catch (error) {
    console.error("Search error:", error)
    return NextResponse.json({ error: "Failed to search products" }, { status: 500 })
  }
}
