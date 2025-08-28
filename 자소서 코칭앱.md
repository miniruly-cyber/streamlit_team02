import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { MessageSquare, Send } from "lucide-react";
import { motion } from "framer-motion";

export default function ResumeCoachUI() {
  const [messages, setMessages] = useState([
    { from: "bot", text: "안녕하세요! AI 자기소개서 코치입니다. 어떤 항목을 도와드릴까요?" },
  ]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (!input.trim()) return;
    setMessages([...messages, { from: "user", text: input }]);
    setInput("");
    // 가짜 응답 추가 (실제 AI 연동 시 교체)
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { from: "bot", text: "좋은 답변이에요! 좀 더 구체적인 경험을 추가해 보시면 어떨까요?" },
      ]);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <Card className="w-full max-w-2xl shadow-xl rounded-2xl">
        <CardContent className="p-6 space-y-4">
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <MessageSquare className="w-6 h-6 text-blue-500" /> AI 자기소개서 코치
          </h1>
          <div className="h-96 overflow-y-auto bg-white rounded-xl p-4 border space-y-3">
            {messages.map((msg, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className={`p-3 rounded-xl max-w-[75%] ${
                  msg.from === "bot"
                    ? "bg-blue-100 text-gray-800 self-start"
                    : "bg-green-100 text-gray-900 self-end ml-auto"
                }`}
              >
                {msg.text}
              </motion.div>
            ))}
          </div>
          <div className="flex gap-2">
            <Input
              placeholder="메시지를 입력하세요..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            />
            <Button onClick={sendMessage}>
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
