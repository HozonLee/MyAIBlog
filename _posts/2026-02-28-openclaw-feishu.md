---
title: "OpenClaw对接飞书：打造智能AI助手"
date: 2026-02-28
tags: [OpenClaw, 飞书, 集成, AI助手]
---

# OpenClaw对接飞书：打造智能AI助手

## 引言

在前一篇文章中，我们介绍了如何在MacBook Pro上本地部署OpenClaw和DeepSeek。今天，我们将进一步探索如何将OpenClaw与飞书（Feishu/Lark）集成，打造一个智能的AI助手，让团队成员可以通过飞书机器人与本地部署的大模型进行交互。

## 为什么要对接飞书？

### 1. 团队协作
飞书作为企业级协作平台，拥有完善的即时通讯、文档协作和日程管理功能。将AI助手集成到飞书中，可以让团队成员在日常工作中无缝使用AI能力。

### 2. 权限管理
飞书提供了完善的权限管理系统，可以控制谁可以访问AI助手，以及使用哪些功能。

### 3. 消息通知
通过飞书机器人，AI可以将重要信息主动推送给相关人员，实现智能化的工作流。

## 前置条件

### 1. 已部署的OpenClaw服务
确保你已经按照上一篇文章的步骤，在本地或服务器上成功部署了OpenClaw，并且可以通过API访问。

### 2. 飞书开发者账号
你需要有一个飞书开发者账号，可以在[飞书开放平台](https://open.feishu.cn/)注册。

### 3. Python环境
用于编写飞书机器人的中间服务。

## 对接步骤

### 第一步：创建飞书机器人

1. 登录[飞书开放平台](https://open.feishu.cn/)
2. 点击"创建企业自建应用"
3. 填写应用名称（如"AI助手"）和应用描述
4. 在"凭证与基础信息"中获取 **App ID** 和 **App Secret**

### 第二步：配置机器人权限

在"权限管理"中，添加以下权限：
- `im:chat:readonly` - 读取群组信息
- `im:message.group_msg` - 发送群组消息
- `im:message:send` - 发送消息
- `im:message.p2p_msg` - 发送单聊消息

### 第三步：启用机器人功能

在"机器人"功能模块中：
1. 启用机器人
2. 设置机器人名称和头像
3. 配置消息卡片（可选）

### 第四步：编写中间服务

创建一个Python脚本来连接飞书和OpenClaw：

```python
# feishu_openclaw_bot.py
import requests
import json
from flask import Flask, request

app = Flask(__name__)

# 配置
FEISHU_APP_ID = 'your_app_id'
FEISHU_APP_SECRET = 'your_app_secret'
OPENCLAW_URL = 'http://localhost:8000/api/generate'

# 获取飞书tenant_access_token
def get_tenant_access_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    headers = {'Content-Type': 'application/json'}
    data = {
        'app_id': FEISHU_APP_ID,
        'app_secret': FEISHU_APP_SECRET
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json().get('tenant_access_token')

# 发送消息到飞书
def send_feishu_message(chat_id, message):
    token = get_tenant_access_token()
    url = 'https://open.feishu.cn/open-apis/message/v4/send'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        'chat_id': chat_id,
        'msg_type': 'text',
        'content': {
            'text': message
        }
    }
    requests.post(url, headers=headers, json=data)

# 调用OpenClaw生成回复
def generate_openclaw_response(prompt):
    headers = {'Content-Type': 'application/json'}
    data = {
        'prompt': prompt,
        'max_tokens': 500,
        'temperature': 0.7
    }
    try:
        response = requests.post(OPENCLAW_URL, headers=headers, json=data)
        result = response.json()
        return result.get('text', '抱歉，我无法生成回复。')
    except Exception as e:
        return f'调用OpenClaw时出错：{str(e)}'

# 飞书消息回调接口
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    # 处理URL验证
    if data.get('type') == 'url_verification':
        return {'challenge': data.get('challenge')}
    
    # 处理消息事件
    if 'event' in data:
        event = data['event']
        if event.get('type') == 'message':
            message = event.get('text', '')
            chat_id = event.get('open_chat_id')
            
            # 调用OpenClaw生成回复
            response = generate_openclaw_response(message)
            
            # 发送回复到飞书
            send_feishu_message(chat_id, response)
    
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 第五步：配置飞书事件订阅

1. 在飞书开放平台的"事件订阅"中，启用事件订阅
2. 设置请求地址为你的服务器地址（如：`http://your-server:5000/webhook`）
3. 订阅以下事件：
   - `im.message.receive_v1` - 接收消息

### 第六步：部署和测试

1. 在你的服务器上运行中间服务：
```bash
python feishu_openclaw_bot.py
```

2. 确保服务器可以被飞书访问（需要公网IP或使用内网穿透工具如ngrok）

3. 在飞书中添加机器人到群组或发送私聊消息进行测试

## 高级功能

### 1. 上下文管理
为了让AI助手能够进行多轮对话，我们需要维护对话上下文：

```python
# 简单的上下文管理
conversation_history = {}

def generate_with_context(chat_id, message):
    if chat_id not in conversation_history:
        conversation_history[chat_id] = []
    
    # 添加用户消息到历史
    conversation_history[chat_id].append(f"用户：{message}")
    
    # 构建完整的对话上下文
    context = "\n".join(conversation_history[chat_id][-5:])  # 保留最近5轮对话
    
    # 调用OpenClaw
    response = generate_openclaw_response(context)
    
    # 添加AI回复到历史
    conversation_history[chat_id].append(f"AI：{response}")
    
    return response
```

### 2. 命令系统
可以添加特定的命令来执行不同的操作：

```python
def handle_command(message, chat_id):
    if message.startswith('/clear'):
        # 清空对话历史
        conversation_history.pop(chat_id, None)
        return "对话历史已清空"
    
    elif message.startswith('/help'):
        return """可用命令：
/clear - 清空对话历史
/help - 显示帮助信息
/status - 查看系统状态"""
    
    elif message.startswith('/status'):
        return "OpenClaw服务运行正常"
    
    return None
```

### 3. 消息格式化
使用飞书的富文本消息格式，让回复更加美观：

```python
def send_rich_message(chat_id, title, content):
    token = get_tenant_access_token()
    url = 'https://open.feishu.cn/open-apis/message/v4/send'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # 构建卡片消息
    card_data = {
        'chat_id': chat_id,
        'msg_type': 'interactive',
        'card': {
            'config': {'wide_screen_mode': True},
            'header': {
                'title': {
                    'tag': 'plain_text',
                    'content': title
                }
            },
            'elements': [
                {
                    'tag': 'div',
                    'text': {
                        'tag': 'lark_md',
                        'content': content
                    }
                }
            ]
        }
    }
    
    requests.post(url, headers=headers, json=card_data)
```

## 安全考虑

### 1. 请求验证
验证飞书的请求签名，防止伪造请求：

```python
import hmac
import hashlib

def verify_signature(timestamp, nonce, signature, body):
    # 使用App Secret验证签名
    key = FEISHU_APP_SECRET.encode('utf-8')
    message = f"{timestamp}{nonce}{body}".encode('utf-8')
    expected_signature = hmac.new(key, message, hashlib.sha256).hexdigest()
    return signature == expected_signature
```

### 2. 访问控制
限制只有特定的用户或群组可以访问AI助手：

```python
ALLOWED_USERS = ['user_id_1', 'user_id_2']
ALLOWED_CHATS = ['chat_id_1']

def check_permission(user_id, chat_id):
    return user_id in ALLOWED_USERS or chat_id in ALLOWED_CHATS
```

## 常见问题

### 1. 飞书无法访问本地服务
**解决方案**：使用内网穿透工具，如ngrok：
```bash
ngrok http 5000
```

### 2. OpenClaw响应慢
**解决方案**：
- 优化OpenClaw配置，使用更小的模型
- 添加异步处理，先发送"正在思考..."的提示
- 使用缓存机制，缓存常见问题的回复

### 3. 消息长度限制
飞书对消息长度有限制，需要对长回复进行分段：

```python
def split_long_message(text, max_length=2000):
    chunks = []
    while len(text) > max_length:
        chunks.append(text[:max_length])
        text = text[max_length:]
    chunks.append(text)
    return chunks
```

## 总结

通过将OpenClaw与飞书对接，我们成功打造了一个智能的AI助手，让团队成员可以在日常工作中方便地使用AI能力。这种集成不仅提高了工作效率，还确保了数据的安全性和隐私性。

未来，你可以进一步扩展这个系统，添加更多的功能，如：
- 文档自动总结
- 会议纪要生成
- 智能问答系统
- 工作流自动化

希望这篇文章对你有所帮助！

## 参考资源

- [飞书开放平台文档](https://open.feishu.cn/document/ukTMukTMukTM/uITNz4iM1MjLyUzM)
- [OpenClaw GitHub仓库](https://github.com/openclaw/openclaw)
- [Flask官方文档](https://flask.palletsprojects.com/)
