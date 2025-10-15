from flask import Flask, request, render_template_string, Response
import requests
import json
import time

app = Flask(__name__)

# DeepSeek API 配置
API_KEY = "sk-5702c61a17fa4f888c1871a4dcf1625c"
API_URL = "https://api.deepseek.com/v1/chat/completions"

def call_deepseek_api(user_input):
    """直接調用DeepSeek API"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": user_input}],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"API錯誤 (狀態碼: {response.status_code})"
    except Exception as e:
        return f"請求失敗: {str(e)}"

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>WingAI 智能系統</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); margin: 0; padding: 20px; min-height: 100vh; }
            .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 15px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
            h1 { text-align: center; color: #333; }
            .chat-box { border: 2px solid #ddd; border-radius: 10px; padding: 15px; margin: 20px 0; min-height: 300px; background: #f9f9f9; }
            .input-area { display: flex; gap: 10px; }
            input { flex: 1; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; }
            button { padding: 12px 24px; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; }
            button:hover { background: #5a6fd8; }
            .message { margin: 10px 0; padding: 10px; border-radius: 8px; }
            .user { background: #e3f2fd; text-align: right; }
            .ai { background: #f5f5f5; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 WingAI 智能系統</h1>
            <div>深度思考 • 繁體中文支援</div>
            
            <div class="chat-box" id="chatBox">
                <div class="message ai">💫 歡迎使用 WingAI！請輸入問題開始對話...</div>
            </div>
            
            <div class="input-area">
                <input type="text" id="userInput" placeholder="請輸入您的問題..." onkeypress="if(event.key=='Enter') sendMessage()">
                <button onclick="sendMessage()">🚀 發送問題</button>
            </div>
            
            <div style="text-align: center; margin-top: 20px; color: #666;">
                <div id="currentTime">載入中...</div>
                <div>© 2025 WingAI 系統 - 簡化版本</div>
            </div>
        </div>

        <script>
            function updateTime() {
                const now = new Date();
                document.getElementById('currentTime').textContent = 
                    now.toLocaleDateString('zh-TW') + ' ' + now.toLocaleTimeString('zh-TW');
            }
            setInterval(updateTime, 1000);
            updateTime();

            async function sendMessage() {
                const userInput = document.getElementById('userInput').value.trim();
                if (!userInput) return;

                const chatBox = document.getElementById('chatBox');
                
                // 顯示用戶消息
                const userMsg = document.createElement('div');
                userMsg.className = 'message user';
                userMsg.textContent = '👤 ' + userInput;
                chatBox.appendChild(userMsg);

                // 顯示思考中
                const thinkingMsg = document.createElement('div');
                thinkingMsg.className = 'message ai';
                thinkingMsg.textContent = '🤔 思考中...';
                chatBox.appendChild(thinkingMsg);

                document.getElementById('userInput').value = '';
                document.querySelector('button').disabled = true;

                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                        body: 'user_input=' + encodeURIComponent(userInput)
                    });
                    
                    const data = await response.json();
                    
                    // 移除思考中消息，顯示AI回應
                    chatBox.removeChild(thinkingMsg);
                    const aiMsg = document.createElement('div');
                    aiMsg.className = 'message ai';
                    aiMsg.textContent = '🤖 ' + data.response;
                    chatBox.appendChild(aiMsg);

                } catch (error) {
                    chatBox.removeChild(thinkingMsg);
                    const errorMsg = document.createElement('div');
                    errorMsg.className = 'message ai';
                    errorMsg.textContent = '❌ 請求失敗，請稍後再試';
                    chatBox.appendChild(errorMsg);
                }

                document.querySelector('button').disabled = false;
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        </script>
    </body>
    </html>
    '''

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('user_input', '').strip()
    
    if not user_input:
        return json.dumps({'response': '請輸入有效問題'})
    
    # 直接調用API
    response = call_deepseek_api(user_input)
    
    return json.dumps({'response': response})

if __name__ == '__main__':
    print("🚀 WingAI 智能系統啟動完成！")
    print("🌐 服務器運行在: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)