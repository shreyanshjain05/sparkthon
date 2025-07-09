"use client"

import { Card, CardContent } from "@/components/ui/card"
import type { Category } from "@/lib/database"

interface CategoriesSectionProps {
  categories: Category[]
  onCategoryClick: (category: string) => void
}

export default function CategoriesSection({ categories, onCategoryClick }: CategoriesSectionProps) {
  return (
    <section className="py-8">
      <h2 className="text-2xl font-bold mb-6">Shop by Category</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {categories.map((category) => (
          <Card
            key={category.id}
            className="cursor-pointer hover:shadow-lg transition-shadow"
            onClick={() => onCategoryClick(category.name)}
          >
            <CardContent className="p-4 text-center">
              <img
                src={category.image_url || "/placeholder.svg"}
                alt={category.name}
                className="w-16 h-16 mx-auto mb-2 rounded-full"
              />
              <h3 className="font-semibold text-sm">{category.name}</h3>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  )
}
