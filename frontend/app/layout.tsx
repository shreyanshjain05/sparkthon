import type { Metadata } from 'next'
import './globals.css'
import { SupabaseProvider } from '@/components/providers/supabase-provider'

export const metadata: Metadata = {
  title: 'sparkthon',
  description: 'Created for sparkthon',
  generator: 'sparkthon.dev',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>
        <SupabaseProvider>
          {children}
        </SupabaseProvider>
      </body>
    </html>
  )
}