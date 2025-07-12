"""
Simple testing dashboard endpoint
Add this to your API routes
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

testing_router = APIRouter()

@testing_router.get("/dashboard", response_class=HTMLResponse)
async def testing_dashboard():
    """Simple testing dashboard"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Agent Testing Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
            .chat-box { border: 1px solid #ddd; height: 400px; overflow-y: scroll; padding: 10px; margin: 10px 0; background: #fafafa; }
            .input-section { margin: 10px 0; }
            input, select, button { padding: 10px; margin: 5px; font-size: 14px; }
            input[type="text"] { width: 60%; }
            button { background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .message { margin: 10px 0; padding: 8px; border-radius: 5px; }
            .user-message { background: #e3f2fd; text-align: right; }
            .agent-message { background: #f1f8e9; }
            .status { background: #fff3cd; padding: 10px; margin: 10px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 AI Agent Testing Dashboard</h1>
            
            <div class="status" id="status">
                <strong>System Status:</strong> <span id="status-text">Checking...</span>
            </div>
            
            <div class="input-section">
                <h3>💬 Chat with Agent</h3>
                <input type="text" id="message-input" placeholder="Type your message here..." />
                <button onclick="sendMessage()">Send</button>
                <button onclick="clearChat()">Clear</button>
            </div>
            
            <div class="chat-box" id="chat-box">
                <div class="message agent-message">
                    <strong>Agent:</strong> Hello! I'm your AI assistant. How can I help you today?
                </div>
            </div>
            
            <div class="input-section">
                <h3>🎯 Delegate to Specialist</h3>
                <select id="agent-type">
                    <option value="sales">Sales Agent</option>
                    <option value="operations">Operations Agent</option>
                    <option value="quote">Quote Agent</option>
                    <option value="scheduler">Scheduler Agent</option>
                </select>
                <input type="text" id="task-input" placeholder="Describe the task..." />
                <button onclick="delegateTask()">Delegate</button>
            </div>
            
            <div class="input-section">
                <h3>🧪 Quick Tests</h3>
                <button onclick="testEndpoint('/agent/status')">Check Status</button>
                <button onclick="testWebChat()">Test Web Chat</button>
                <button onclick="testWhatsApp()">Test WhatsApp</button>
            </div>
        </div>

        <script>
            let messageCount = 0;
            
            // Check system status on load
            window.onload = function() {
                checkStatus();
            };
            
            async function checkStatus() {
                try {
                    const response = await fetch('/agent/status');
                    const status = await response.json();
                    document.getElementById('status-text').innerHTML = 
                        `Mode: ${status.mode} | API: ${status.api_configured ? '✅' : '❌'} | Users: ${status.conversation_users}`;
                } catch (error) {
                    document.getElementById('status-text').innerHTML = '❌ Error checking status';
                }
            }
            
            async function sendMessage() {
                const input = document.getElementById('message-input');
                const message = input.value.trim();
                if (!message) return;
                
                addMessage(message, 'user');
                input.value = '';
                
                try {
                    const response = await fetch('/agent/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            message: message,
                            user_id: 'dashboard_user',
                            context: {source: 'dashboard'}
                        })
                    });
                    
                    const result = await response.json();
                    addMessage(result.response, 'agent');
                    
                    if (result.actions_taken && result.actions_taken.length > 0) {
                        addMessage(`Actions: ${result.actions_taken.join(', ')}`, 'agent', true);
                    }
                } catch (error) {
                    addMessage('Error: ' + error.message, 'agent');
                }
            }
            
            async function delegateTask() {
                const agentType = document.getElementById('agent-type').value;
                const task = document.getElementById('task-input').value.trim();
                if (!task) return;
                
                addMessage(`Delegating to ${agentType}: ${task}`, 'user');
                document.getElementById('task-input').value = '';
                
                try {
                    const response = await fetch('/agent/delegate', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            agent_type: agentType,
                            task: task,
                            context: {source: 'dashboard'}
                        })
                    });
                    
                    const result = await response.json();
                    addMessage(`${agentType.toUpperCase()}: ${result.response}`, 'agent');
                } catch (error) {
                    addMessage('Error: ' + error.message, 'agent');
                }
            }
            
            function addMessage(text, sender, isAction = false) {
                const chatBox = document.getElementById('chat-box');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}-message`;
                
                if (isAction) {
                    messageDiv.innerHTML = `<em>${text}</em>`;
                } else {
                    messageDiv.innerHTML = `<strong>${sender === 'user' ? 'You' : 'Agent'}:</strong> ${text}`;
                }
                
                chatBox.appendChild(messageDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            }
            
            function clearChat() {
                const chatBox = document.getElementById('chat-box');
                chatBox.innerHTML = '<div class="message agent-message"><strong>Agent:</strong> Chat cleared. How can I help you?</div>';
            }
            
            async function testEndpoint(endpoint) {
                try {
                    const response = await fetch(endpoint);
                    const result = await response.json();
                    addMessage(`${endpoint}: ${JSON.stringify(result, null, 2)}`, 'agent');
                } catch (error) {
                    addMessage(`Error testing ${endpoint}: ${error.message}`, 'agent');
                }
            }
            
            async function testWebChat() {
                try {
                    const response = await fetch('/webchat/message', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            session_id: 'dashboard_test',
                            message: 'Test web chat message',
                            user_info: {name: 'Dashboard User'}
                        })
                    });
                    const result = await response.json();
                    addMessage(`Web Chat Test: ${result.message}`, 'agent');
                } catch (error) {
                    addMessage(`Web Chat Error: ${error.message}`, 'agent');
                }
            }
            
            async function testWhatsApp() {
                addMessage('WhatsApp test: Webhook endpoint ready at /whatsapp/webhook', 'agent');
            }
            
            // Allow Enter key to send message
            document.getElementById('message-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
            
            document.getElementById('task-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    delegateTask();
                }
            });
        </script>
    </body>
    </html>
    """
    return html_content
