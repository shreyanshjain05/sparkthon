import { streamText } from "ai"
import { openai } from "@ai-sdk/openai"

export async function POST(req: Request) {
  try {
    const { messages } = await req.json()

    const result = streamText({
      model: openai("gpt-4o"),
      system: `You are a helpful Walmart shopping assistant. You help customers find products, answer questions about pricing, availability, and provide shopping recommendations. 

Key guidelines:
- Be friendly and helpful
- Focus on Walmart products and services
- Provide specific product recommendations when possible
- Help with price comparisons and deals
- Assist with store policies and services
- If asked about products not available at Walmart, politely redirect to Walmart alternatives
- Keep responses concise but informative`,
      messages,
    })

    return result.toDataStreamResponse()
  } catch (error) {
    console.error("Chat API error:", error)
    return new Response("Error processing chat request", { status: 500 })
  }
}
