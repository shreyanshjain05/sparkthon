import type { Metadata } from 'next'
import './globals.css'

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
      <body>{children}</body>
    </html>
  )
}
