"use client";

import { useEffect, useRef, useState } from "react";
import { useUser, useSessionContext } from "@supabase/auth-helpers-react";
import { useRouter } from "next/navigation";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { X } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface ChatbotProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function Chatbot({ isOpen, onClose }: ChatbotProps) {
  const user = useUser();
  const { session, isLoading: sessionLoading } = useSessionContext();
  const router = useRouter();
  const [inputText, setInputText] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (user && isOpen) {
      // Set up WebSocket connection
      wsRef.current = new WebSocket("ws://localhost:8000/ws");

      wsRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.response) {
          setMessages((prev) => [...prev, { role: "assistant", content: data.response }]);
          setIsLoading(false);
        }
      };

      wsRef.current.onerror = (error) => {
        console.error("WebSocket error:", error);
        setIsLoading(false);
      };

      wsRef.current.onclose = () => {
        console.log("WebSocket connection closed");
        setIsLoading(false);
      };

      // Cleanup on unmount
      return () => {
        if (wsRef.current) {
          wsRef.current.close();
        }
      };
    }
  }, [user, isOpen]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim() || !user || !wsRef.current) return;

    setIsLoading(true);
    setMessages((prev) => [...prev, { role: "user", content: inputText }]);
    
    wsRef.current.send(JSON.stringify({ message: inputText }));
    setInputText("");
  };

  if (!isOpen) return null;

  // Show loading state while session is being checked
  if (sessionLoading) {
    return (
      <div className="fixed bottom-4 right-4 z-50">
        <Card className="w-96 shadow-lg">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Loading...</CardTitle>
            <Button variant="ghost" size="icon" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </CardHeader>
          <CardContent>
            <p>Checking authentication...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Debug: Log the session and user state
  console.log("Session:", session);
  console.log("User:", user);

  if (!session && !user) {
    return (
      <div className="fixed bottom-4 right-4 z-50">
        <Card className="w-96 shadow-lg">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Sign in to start shopping</CardTitle>
            <Button variant="ghost" size="icon" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </CardHeader>
          <CardContent>
            <p className="mb-4">Please sign in to access the shopping assistant.</p>
            <Button onClick={() => router.push("/auth/login")}>Sign In</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <Card className="w-96 h-[600px] flex flex-col shadow-lg">
        <CardHeader className="flex flex-row items-center justify-between border-b">
          <CardTitle>Shopping Assistant</CardTitle>
          <Button variant="ghost" size="icon" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </CardHeader>
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-gray-500 mt-8">
              <p>Hello! How can I help you shop today?</p>
            </div>
          )}
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.role === "assistant" ? "justify-start" : "justify-end"
              }`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-3 ${
                  message.role === "assistant"
                    ? "bg-gray-200"
                    : "bg-blue-500 text-white"
                }`}
              >
                {message.content}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        <form onSubmit={handleSubmit} className="p-4 border-t">
          <div className="flex gap-2">
            <Input
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="What would you like to shop for?"
              disabled={isLoading}
              className="flex-1"
            />
            <Button type="submit" disabled={isLoading || !inputText.trim()}>
              {isLoading ? "Sending..." : "Send"}
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
}