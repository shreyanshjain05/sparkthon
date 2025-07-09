"use client"

import type React from "react"

import { useState } from "react"
import { Search, ShoppingCart, Menu, User, Heart } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"

interface HeaderProps {
  onSearch: (query: string) => void
  onToggleChat: () => void
}

export default function Header({ onSearch, onToggleChat }: HeaderProps) {
  const [searchQuery, setSearchQuery] = useState("")

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    onSearch(searchQuery)
  }

  return (
    <header className="bg-blue-600 text-white sticky top-0 z-50">
      <div className="container mx-auto px-4">
        {/* Top bar */}
        <div className="flex items-center justify-between py-2 text-sm">
          <div className="flex items-center space-x-4">
            <span>Free shipping on orders $35+</span>
          </div>
          <div className="flex items-center space-x-4">
            <button className="hover:underline">Sign In</button>
            <button className="hover:underline">Create Account</button>
          </div>
        </div>

        {/* Main header */}
        <div className="flex items-center justify-between py-4">
          <div className="flex items-center space-x-8">
            <h1 className="text-2xl font-bold">Walmart</h1>

            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="text-white hover:bg-blue-700">
                  <Menu className="h-5 w-5 mr-2" />
                  Departments
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56">
                <DropdownMenuItem>Electronics</DropdownMenuItem>
                <DropdownMenuItem>Clothing</DropdownMenuItem>
                <DropdownMenuItem>Home & Garden</DropdownMenuItem>
                <DropdownMenuItem>Sports & Outdoors</DropdownMenuItem>
                <DropdownMenuItem>Health & Beauty</DropdownMenuItem>
                <DropdownMenuItem>Grocery</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>

          {/* Search bar */}
          <form onSubmit={handleSearch} className="flex-1 max-w-2xl mx-8">
            <div className="relative">
              <Input
                type="text"
                placeholder="Search everything at Walmart online and in store"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-4 pr-12 py-3 text-black rounded-full"
              />
              <Button
                type="submit"
                size="sm"
                className="absolute right-1 top-1 bottom-1 bg-yellow-400 hover:bg-yellow-500 text-black rounded-full px-4"
              >
                <Search className="h-4 w-4" />
              </Button>
            </div>
          </form>

          {/* Right side icons */}
          <div className="flex items-center space-x-4">
            <Button variant="ghost" className="text-white hover:bg-blue-700" onClick={onToggleChat}>
              💬 Chat
            </Button>
            <Button variant="ghost" className="text-white hover:bg-blue-700">
              <Heart className="h-5 w-5" />
            </Button>
            <Button variant="ghost" className="text-white hover:bg-blue-700">
              <User className="h-5 w-5" />
            </Button>
            <Button variant="ghost" className="text-white hover:bg-blue-700 relative">
              <ShoppingCart className="h-5 w-5" />
              <span className="absolute -top-1 -right-1 bg-yellow-400 text-black text-xs rounded-full h-5 w-5 flex items-center justify-center">
                0
              </span>
            </Button>
          </div>
        </div>
      </div>
    </header>
  )
}
