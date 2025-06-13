import json
import requests

url = "https://api.dify.ai/v1/chat-messages"
api_key = "app-yJhD6gRaJixKw7aYvd8swMGx"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "inputs": {},
    "query": "你好",
    "response_mode": "streaming",  # 流式返回
    "conversation_id": "",
    "user": "abc-123"
}

# 发送请求
response = requests.post(url, headers=headers, json=data, stream=True)

# 解析流式返回数据
answers = []
for line in response.iter_lines():
    if line:
        try:
            data = json.loads(line.decode("utf-8").replace("data: ", ""))  # 解析 JSON
            if data.get("event") == "agent_message":  # 只提取 AI 回复
                answers.append(data.get("answer", ""))
        except json.JSONDecodeError:
            continue

# 拼接完整的 AI 回答
full_answer = "".join(answers)

# **直接返回最终的回答**
print(full_answer)  # 这里可以改成 `return full_answer` 用于 API
