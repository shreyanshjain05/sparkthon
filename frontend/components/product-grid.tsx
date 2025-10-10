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
              {/* <img
                src="/placeholder.svg"
                alt={product.item_name}
                className="w-full h-48 object-cover rounded"
              /> */}
              {product.stock_quantity === 0 && (
                <Badge variant="destructive" className="absolute top-2 left-2">
                  Out of Stock
                </Badge>
              )}
            </div>

            <div className="space-y-3">
              <h3 className="font-semibold text-sm line-clamp-2 group-hover:text-blue-600">
                {product.item_name}
              </h3>
            

              <div className="flex items-center justify-between">
                <div>
                  <span className="text-lg font-bold text-green-600">
                    ₹{product.price.toFixed(2)}
                  </span>
                  {product.brand && (
                    <p className="text-xs text-gray-600">{product.brand}</p>
                  )}
                </div>
                {product.category && (
                  <Badge variant="secondary" className="text-xs">
                    {product.category}
                  </Badge>
                )}
              </div>

              {/* <Button 
                className="w-full bg-blue-600 hover:bg-blue-700" 
                disabled={product.stock_quantity === 0 || !product.is_active}
              >
                {product.stock_quantity > 0 ? 
                  `Add to Cart ` : 
                  "Out of Stock"}
              </Button> */}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
