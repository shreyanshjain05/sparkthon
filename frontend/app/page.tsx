"use client"

import { useState, useEffect } from "react"
import Header from "@/components/header"
import ProductGrid from "@/components/product-grid"
// import CategoriesSection from "@/components/categories-section"
import Chatbot from "@/components/chatbot"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import type { Category } from "@/lib/database"
import type { Product } from "@/lib/supabase/db"
import { AuthButton } from "@/components/auth-button"

export default function HomePage() {
  const [products, setProducts] = useState<Product[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState("")
  const [isChatOpen, setIsChatOpen] = useState(false)

  // Fetch categories from the API
  const fetchCategories = async () => {
    try {
      const response = await fetch('/api/categories')
      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch categories')
      }
      
      setCategories(data.categories)
    } catch (error) {
      console.error("Error fetching categories:", error)
      setCategories([])
    }
  }

  useEffect(() => {
    fetchCategories()
  }, [])

  const fetchProducts = async (query = "") => {
    setLoading(true)
    try {
      const response = await fetch(`/api/products?q=${encodeURIComponent(query)}`)
      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch products')
      }
      
      setProducts(data.products)
    } catch (error) {
      console.error("Error fetching products:", error)
      // Initialize with empty products on error
      setProducts([])
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
              <Button 
                onClick={() => window.location.href = '/auth/login'} 
                className="bg-yellow-400 hover:bg-yellow-500 text-black font-semibold"
              >
                Shop Now
              </Button>
              <Button variant="outline" className="border-white text-white hover:bg-white hover:text-blue-600">
                Weekly Ad
              </Button>
            </div>
          </div>
        </section>

        {/* Categories */}
        {/* <CategoriesSection categories={categories} onCategoryClick={handleCategoryClick} /> */}

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
                  <AuthButton />
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

