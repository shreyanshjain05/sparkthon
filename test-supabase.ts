// Quick test to diagnose Supabase connection
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || ''
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''

console.log('Testing Supabase connection...')
console.log('URL:', supabaseUrl)
console.log('Key present:', !!supabaseKey)

if (!supabaseUrl || !supabaseKey) {
  console.error('❌ Missing Supabase credentials in .env')
  process.exit(1)
}

const supabase = createClient(supabaseUrl, supabaseKey)

async function test() {
  try {
    console.log('\nAttempting to fetch products...')
    const { data, error } = await supabase
      .from('products')
      .select('count')
    
    if (error) {
      console.error('❌ Database error:', error)
    } else {
      console.log('✅ Connection successful!')
      console.log('Products found:', data)
    }
  } catch (err) {
    console.error('❌ Connection failed:', err)
  }
}

test()
