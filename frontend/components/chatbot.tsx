"use client"
import type React from "react"
import { useState, useRef, useEffect } from "react"
import { Send, X, Bot, User, ShoppingCart, Wifi, WifiOff, Loader2 } from "lucide-react"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  timestamp: Date
}

interface ChatbotProps {
  isOpen: boolean
  onClose: () => void
}

export default function Chatbot({ isOpen, onClose }: ChatbotProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Welcome! What would you like to cook today? I'll help you find all the ingredients you need for your recipe.",
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
  const [reconnectAttempts, setReconnectAttempts] = useState(0)
  const [isReconnecting, setIsReconnecting] = useState(false)
  const scrollAreaRef = useRef<HTMLDivElement>(null)
  const wsRef = useRef<WebSocket | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  // WebSocket connection effect
  useEffect(() => {
    if (isOpen && !wsRef.current) {
      connectWebSocket()
    }
    return () => {
      if (wsRef.current) {
        wsRef.current.close()
        wsRef.current = null
      }
    }
  }, [isOpen])

  // Auto-scroll effect
  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight
    }
  }, [messages])

  // Focus input when connected
  useEffect(() => {
    if (isConnected && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isConnected])

  const connectWebSocket = () => {
    if (wsRef.current?.readyState === WebSocket.CONNECTING) {
      return // Already connecting
    }

    try {
      setIsReconnecting(true)
      // Update this URL to match your backend server
      const wsUrl = "ws://localhost:8000/ws"
      wsRef.current = new WebSocket(wsUrl)

      wsRef.current.onopen = () => {
        console.log("WebSocket connected")
        setIsConnected(true)
        setReconnectAttempts(0)
        setIsReconnecting(false)
      }

      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          if (data.response) {
            const assistantMessage: Message = {
              id: Date.now().toString(),
              role: "assistant",
              content: data.response,
              timestamp: new Date(),
            }
            setMessages((prev) => [...prev, assistantMessage])
          }
        } catch (error) {
          console.error("Error parsing WebSocket message:", error)
        }
        setIsLoading(false)
      }

      wsRef.current.onclose = (event) => {
        console.log("WebSocket disconnected", event.code, event.reason)
        setIsConnected(false)
        setIsReconnecting(false)
        wsRef.current = null
        
        // Auto-reconnect logic
        if (event.code !== 1000 && reconnectAttempts < 5) {
          setTimeout(() => {
            setReconnectAttempts(prev => prev + 1)
            connectWebSocket()
          }, Math.pow(2, reconnectAttempts) * 1000) // Exponential backoff
        }
      }

      wsRef.current.onerror = (error) => {
        console.error("WebSocket error:", error)
        setIsConnected(false)
        setIsLoading(false)
        setIsReconnecting(false)
        
        // Add error message to chat
        const errorMessage: Message = {
          id: Date.now().toString(),
          role: "assistant",
          content: "Sorry, I'm having trouble connecting. Please make sure the server is running and try again.",
          timestamp: new Date(),
        }
        setMessages((prev) => [...prev, errorMessage])
      }
    } catch (error) {
      console.error("Failed to connect WebSocket:", error)
      setIsConnected(false)
      setIsReconnecting(false)
    }
  }

  const handleSubmit = async (e?: React.FormEvent | React.MouseEvent) => {
    e?.preventDefault()
    if (!input.trim() || isLoading || !isConnected || !wsRef.current) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      // Send message via WebSocket
      wsRef.current.send(JSON.stringify({
        message: input
      }))
    } catch (error) {
      console.error("Error sending message:", error)
      setIsLoading(false)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Sorry, I encountered an error sending your message. Please try again.",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    }
  }

  const handleReconnect = () => {
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
    setReconnectAttempts(0)
    connectWebSocket()
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md h-[600px] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-t-lg">
          <div className="flex items-center gap-2">
            <ShoppingCart className="w-5 h-5" />
            <h3 className="font-semibold">Recipe Shopping Assistant</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-white hover:bg-opacity-20 rounded-full transition-colors"
            aria-label="Close chat"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Connection status indicator */}
        <div className="px-4 py-2 bg-gray-50 border-b">
          <div className="flex items-center gap-2 text-sm">
            {isConnected ? (
              <>
                <Wifi className="w-4 h-4 text-green-500" />
                <span className="text-green-600">Connected</span>
              </>
            ) : isReconnecting ? (
              <>
                <Loader2 className="w-4 h-4 text-yellow-500 animate-spin" />
                <span className="text-yellow-600">Reconnecting...</span>
              </>
            ) : (
              <>
                <WifiOff className="w-4 h-4 text-red-500" />
                <span className="text-red-600">Disconnected</span>
              </>
            )}
          </div>
        </div>

        {/* Chat messages */}
        <div 
          ref={scrollAreaRef}
          className="flex-1 overflow-y-auto p-4 space-y-4"
        >
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.role === "user"
                    ? "bg-blue-500 text-white"
                    : "bg-gray-100 text-gray-800"
                }`}
              >
                <div className="flex items-start gap-2">
                  {message.role === "assistant" && <Bot className="w-4 h-4 mt-1 flex-shrink-0" />}
                  {message.role === "user" && <User className="w-4 h-4 mt-1 flex-shrink-0" />}
                  <div className="flex-1">
                    <div className="whitespace-pre-wrap text-sm leading-relaxed">
                      {message.content}
                    </div>
                    <div className={`text-xs mt-1 ${
                      message.role === "user" ? "text-blue-100" : "text-gray-500"
                    }`}>
                      {message.timestamp.toLocaleTimeString([], { 
                        hour: '2-digit', 
                        minute: '2-digit' 
                      })}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="max-w-[80%] rounded-lg px-4 py-2 bg-gray-100 text-gray-800">
                <div className="flex items-start gap-2">
                  <Bot className="w-4 h-4 mt-1 flex-shrink-0" />
                  <div className="flex items-center gap-1">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span className="text-sm">Thinking...</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input area */}
        <div className="p-4 border-t bg-gray-50">
          {!isConnected && (
            <div className="mb-3 flex justify-center">
              <button
                onClick={handleReconnect}
                disabled={isReconnecting}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors text-sm flex items-center gap-2"
              >
                {isReconnecting ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Reconnecting...
                  </>
                ) : (
                  <>
                    <Wifi className="w-4 h-4" />
                    Reconnect to Server
                  </>
                )}
              </button>
            </div>
          )}

          <div className="flex gap-2">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={isConnected ? "Tell me what you'd like to cook..." : "Connecting..."}
              disabled={isLoading || !isConnected}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
              onKeyPress={handleKeyPress}
            />
            <button
              onClick={handleSubmit}
              disabled={isLoading || !isConnected || !input.trim()}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
            </button>
          </div>
          
          <div className="mt-2 text-xs text-gray-500 text-center">
            Press Enter to send • Shift+Enter for new line
          </div>
        </div>
      </div>
    </div>
  )
}