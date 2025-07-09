import { Star, Heart } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import type { Product } from "@/lib/database"

interface ProductGridProps {
  products: Product[]
  loading?: boolean
}

export default function ProductGrid({ products, loading }: ProductGridProps) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {Array.from({ length: 8 }).map((_, i) => (
          <Card key={i} className="animate-pulse">
            <CardContent className="p-4">
              <div className="bg-gray-200 h-48 rounded mb-4"></div>
              <div className="bg-gray-200 h-4 rounded mb-2"></div>
              <div className="bg-gray-200 h-4 rounded w-3/4 mb-2"></div>
              <div className="bg-gray-200 h-6 rounded w-1/2"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  if (products.length === 0) {
    return (
      <div className="text-center py-12">
        <h3 className="text-xl font-semibold mb-2">No products found</h3>
        <p className="text-gray-600">Try adjusting your search terms</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {products.map((product) => (
        <Card key={product.id} className="group hover:shadow-lg transition-shadow">
          <CardContent className="p-4">
            <div className="relative mb-4">
              <img
                src={product.image_url || "/placeholder.svg"}
                alt={product.name}
                className="w-full h-48 object-cover rounded"
              />
              <Button
                size="sm"
                variant="ghost"
                className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity bg-white hover:bg-gray-100"
              >
                <Heart className="h-4 w-4" />
              </Button>
              {!product.in_stock && (
                <Badge variant="destructive" className="absolute top-2 left-2">
                  Out of Stock
                </Badge>
              )}
            </div>

            <div className="space-y-2">
              <h3 className="font-semibold text-sm line-clamp-2 group-hover:text-blue-600">{product.name}</h3>

              <div className="flex items-center space-x-1">
                <div className="flex items-center">
                  {Array.from({ length: 5 }).map((_, i) => (
                    <Star
                      key={i}
                      className={`h-3 w-3 ${
                        i < Math.floor(product.rating) ? "fill-yellow-400 text-yellow-400" : "text-gray-300"
                      }`}
                    />
                  ))}
                </div>
                <span className="text-xs text-gray-600">({product.reviews_count})</span>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <span className="text-lg font-bold text-green-600">${product.price}</span>
                  <p className="text-xs text-gray-600">{product.brand}</p>
                </div>
              </div>

              <Button className="w-full bg-blue-600 hover:bg-blue-700" disabled={!product.in_stock}>
                {product.in_stock ? "Add to Cart" : "Out of Stock"}
              </Button>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
