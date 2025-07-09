"use client"

import { useState, useEffect } from "react"
import Header from "@/components/header"
import ProductGrid from "@/components/product-grid"
import CategoriesSection from "@/components/categories-section"
import Chatbot from "@/components/chatbot"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import type { Product, Category } from "@/lib/database"

export default function HomePage() {
  const [products, setProducts] = useState<Product[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState("")
  const [isChatOpen, setIsChatOpen] = useState(false)

  // Mock categories data
  useEffect(() => {
    const mockCategories: Category[] = [
      { id: 1, name: "Electronics", slug: "electronics", image_url: "/placeholder.svg?height=64&width=64" },
      { id: 2, name: "Clothing", slug: "clothing", image_url: "/placeholder.svg?height=64&width=64" },
      { id: 3, name: "Home & Garden", slug: "home-garden", image_url: "/placeholder.svg?height=64&width=64" },
      { id: 4, name: "Sports & Outdoors", slug: "sports-outdoors", image_url: "/placeholder.svg?height=64&width=64" },
      { id: 5, name: "Health & Beauty", slug: "health-beauty", image_url: "/placeholder.svg?height=64&width=64" },
      { id: 6, name: "Grocery", slug: "grocery", image_url: "/placeholder.svg?height=64&width=64" },
    ]
    setCategories(mockCategories)
  }, [])

  const fetchProducts = async (query = "") => {
    setLoading(true)
    try {
      const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`)
      if (response.ok) {
        const data = await response.json()
        setProducts(data.products)
      } else {
        // Fallback to mock data if database is not available
        const mockProducts: Product[] = [
          {
            id: 1,
            name: "iPhone 15 Pro",
            description: "Latest Apple smartphone with advanced camera system",
            price: 999.99,
            image_url: "/placeholder.svg?height=300&width=300",
            category: "Electronics",
            brand: "Apple",
            rating: 4.8,
            reviews_count: 1250,
            in_stock: true,
          },
          {
            id: 2,
            name: 'Samsung 65" 4K Smart TV',
            description: "Ultra HD Smart TV with HDR and streaming apps",
            price: 799.99,
            image_url: "/placeholder.svg?height=300&width=300",
            category: "Electronics",
            brand: "Samsung",
            rating: 4.6,
            reviews_count: 890,
            in_stock: true,
          },
          {
            id: 3,
            name: "Nike Air Max 270",
            description: "Comfortable running shoes with air cushioning",
            price: 129.99,
            image_url: "/placeholder.svg?height=300&width=300",
            category: "Clothing",
            brand: "Nike",
            rating: 4.5,
            reviews_count: 2100,
            in_stock: true,
          },
          {
            id: 4,
            name: "Instant Pot Duo 7-in-1",
            description: "Multi-functional pressure cooker",
            price: 89.99,
            image_url: "/placeholder.svg?height=300&width=300",
            category: "Home & Garden",
            brand: "Instant Pot",
            rating: 4.7,
            reviews_count: 15600,
            in_stock: true,
          },
          {
            id: 5,
            name: "PlayStation 5",
            description: "Next-gen gaming console",
            price: 499.99,
            image_url: "/placeholder.svg?height=300&width=300",
            category: "Electronics",
            brand: "Sony",
            rating: 4.9,
            reviews_count: 8900,
            in_stock: false,
          },
          {
            id: 6,
            name: "MacBook Air M2",
            description: "Lightweight laptop with M2 chip",
            price: 1199.99,
            image_url: "/placeholder.svg?height=300&width=300",
            category: "Electronics",
            brand: "Apple",
            rating: 4.7,
            reviews_count: 950,
            in_stock: true,
          },
        ]

        if (query) {
          const filtered = mockProducts.filter(
            (product) =>
              product.name.toLowerCase().includes(query.toLowerCase()) ||
              product.description.toLowerCase().includes(query.toLowerCase()) ||
              product.category.toLowerCase().includes(query.toLowerCase()) ||
              product.brand.toLowerCase().includes(query.toLowerCase()),
          )
          setProducts(filtered)
        } else {
          setProducts(mockProducts)
        }
      }
    } catch (error) {
      console.error("Error fetching products:", error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchProducts()
  }, [])

  const handleSearch = (query: string) => {
    setSearchQuery(query)
    fetchProducts(query)
  }

  const handleCategoryClick = (category: string) => {
    setSearchQuery(category)
    fetchProducts(category)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header onSearch={handleSearch} onToggleChat={() => setIsChatOpen(!isChatOpen)} />

      <main className="container mx-auto px-4 py-8">
        {/* Hero Banner */}
        <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white rounded-lg p-8 mb-8">
          <div className="max-w-2xl">
            <h1 className="text-4xl font-bold mb-4">Save Money. Live Better.</h1>
            <p className="text-xl mb-6">
              Discover amazing deals on everything you need, from electronics to groceries.
            </p>
            <div className="flex space-x-4">
              <Button className="bg-yellow-400 hover:bg-yellow-500 text-black font-semibold">Shop Now</Button>
              <Button variant="outline" className="border-white text-white hover:bg-white hover:text-blue-600">
                Weekly Ad
              </Button>
            </div>
          </div>
        </section>

        {/* Categories */}
        <CategoriesSection categories={categories} onCategoryClick={handleCategoryClick} />

        {/* Search Results Header */}
        {searchQuery && (
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-4">
              <h2 className="text-2xl font-bold">
                {searchQuery ? `Results for "${searchQuery}"` : "Featured Products"}
              </h2>
              <Badge variant="secondary">{products.length} items</Badge>
            </div>
            {searchQuery && (
              <Button
                variant="outline"
                onClick={() => {
                  setSearchQuery("")
                  fetchProducts()
                }}
              >
                Clear Search
              </Button>
            )}
          </div>
        )}

        {/* Products Grid */}
        <ProductGrid products={products} loading={loading} />

        {/* Promotional Sections */}
        <section className="mt-12 grid md:grid-cols-2 gap-8">
          <div className="bg-green-100 rounded-lg p-6">
            <h3 className="text-2xl font-bold text-green-800 mb-2">Walmart+</h3>
            <p className="text-green-700 mb-4">Free delivery, member prices, and more benefits</p>
            <Button className="bg-green-600 hover:bg-green-700">Learn More</Button>
          </div>
          <div className="bg-yellow-100 rounded-lg p-6">
            <h3 className="text-2xl font-bold text-yellow-800 mb-2">Weekly Deals</h3>
            <p className="text-yellow-700 mb-4">Don't miss out on this week's hottest deals</p>
            <Button className="bg-yellow-600 hover:bg-yellow-700">View Deals</Button>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white mt-16">
        <div className="container mx-auto px-4 py-12">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h4 className="font-bold mb-4">Customer Service</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="#" className="hover:underline">
                    Help Center
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:underline">
                    Track Your Order
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:underline">
                    Returns & Exchanges
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:underline">
                    Contact Us
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Shop</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="#" className="hover:underline">
                    Weekly Ad
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:underline">
                    Clearance
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:underline">
                    Special Offers
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:underline">
                    Gift Cards
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Account</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="#" className="hover:underline">
                    Sign In
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:underline">
                    Create Account
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:underline">
                    Walmart+
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:underline">
                    Credit Card
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Company</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="#" className="hover:underline">
                    About Us
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:underline">
                    Careers
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:underline">
                    News
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:underline">
                    Investors
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-sm">
            <p>&copy; 2024 Walmart Clone. All rights reserved.</p>
          </div>
        </div>
      </footer>

      {/* Chatbot */}
      <Chatbot isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
    </div>
  )
}
