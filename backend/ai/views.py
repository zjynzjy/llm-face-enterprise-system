# from django.http import JsonResponse
# from django.views import View
# import requests
# import json
#
#
# class ChatView(View):
#     def post(self, request):
#
#         # 解析 JSON 数据
#         data = json.loads(request.body)
#
#         # 打印整个请求数据
#         print("Full request data:", data)
#         # 打印 content 和 history
#         print("Content:", data.get("content"))
#         print("History:", data.get("history"))
#
#         print(request.POST.get("content"))
#         """Django 视图：封装 Dify 流式 API 并返回完整的 AI 回复"""
#         url = "https://api.dify.ai/v1/chat-messages"
#         api_key = "app-yJhD6gRaJixKw7aYvd8swMGx"
#
#         headers = {
#             "Authorization": f"Bearer {api_key}",
#             "Content-Type": "application/json"
#         }
#
#         data = {
#             "inputs": {},
#             "query": data.get("content"),
#             "response_mode": "streaming",
#             "conversation_id": "",  # 可以在这里处理对话ID
#             "user": "abc-123",
#             "history": data.get("history", [])  # 获取历史对话
#         }
#
#         response = requests.post(url, headers=headers, json=data, stream=True, timeout=50000)
#
#         answers = []
#         for line in response.iter_lines():
#             if line:
#                 try:
#                     parsed_data = json.loads(line.decode("utf-8").replace("data: ", ""))
#                     if parsed_data.get("event") == "agent_message":
#                         answers.append(parsed_data.get("answer", ""))
#                 except json.JSONDecodeError:
#                     continue
#
#         full_answer = "".join(answers)
#         print("full_answer:", full_answer)
#         return JsonResponse({"answer": full_answer})


# 安装依赖：pip install langchain langchain-community langchain-openai mysqlclient
# views.py

##
#
# 版本二


# from django.http import JsonResponse
# from django.views import View
# from langchain_community.utilities import SQLDatabase
# import json
# import requests
# import logging
#
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
#
# DIFY_API_KEY = "app-yJhD6gRaJixKw7aYvd8swMGx"
# DB_URI = "mysql://root:123456@localhost/db_admin2"
#
#
# class SecurityLogAnalyst:
#     def __init__(self):
#         self.db = SQLDatabase.from_uri(DB_URI)
#         self.execute_sql = self.db.run
#
#
# class ChatView(View):
#     def __init__(self):
#         super().__init__()
#         self.analyst = SecurityLogAnalyst()
#         self.face_verify_keywords = [
#             "人脸认证失败", "人脸异常", "打卡异常", "打卡失败",
#             "人脸验证", "人脸验证失败", "刷脸失败", "最近打卡",
#             "谁打卡失败", "打卡", "人脸", "认证", "验证"
#         ]
#
#     def _call_dify(self, query):
#         try:
#             url = "https://api.dify.ai/v1/chat-messages"
#             headers = {
#                 "Authorization": f"Bearer {DIFY_API_KEY}",
#                 "Content-Type": "application/json"
#             }
#             data = {
#                 "inputs": {},
#                 "query": query,
#                 "response_mode": "streaming",
#                 "conversation_id": "a",
#                 "user": "abc-123",
#                 "history": []
#             }
#             response = requests.post(url, headers=headers, json=data, stream=True, timeout=50000)
#             answers = []
#             for line in response.iter_lines():
#                 if line:
#                     try:
#                         parsed_data = json.loads(line.decode("utf-8").replace("data: ", ""))
#                         if parsed_data.get("event") == "agent_message":
#                             answers.append(parsed_data.get("answer", ""))
#                     except json.JSONDecodeError:
#                         continue
#             full_answer = "".join(answers)
#             return full_answer
#         except Exception as e:
#             logger.error(f"Dify调用失败: {str(e)}")
#             return f"政策查询服务暂不可用: {str(e)}"
#
#     def post(self, request):
#         try:
#             data = json.loads(request.body)
#             query = data.get("content", "").strip()
#
#             if not query:
#                 return JsonResponse({"answer": "问题内容不能为空"})
#
#             logger.info(f"原始查询: {query}")
#
#             # 检查是否是人脸验证相关查询
#             is_face_verify_query = False
#             for keyword in self.face_verify_keywords:
#                 if keyword in query:
#                     is_face_verify_query = True
#                     break
#
#             if "安全日志" in query and ("打卡" in query or "人脸" in query):
#                 is_face_verify_query = True
#
#             if is_face_verify_query:
#                 logger.info(f"人脸验证失败查询: {query}")
#
#                 # 简单直接的SQL查询
#                 sql = """
#                 SELECT DISTINCT u.username
#                 FROM sys_security_log s
#                 JOIN sys_user u ON s.user_id = u.id
#                 WHERE s.event_type = 'FACE_VERIFY_FAIL';
#                 """
#
#                 try:
#                     result = self.analyst.execute_sql(sql)
#                     logger.info(f"查询结果: {result}")
#
#                     # 直接提取用户名
#                     usernames = []
#                     for row in result:
#                         if row and row[0]:
#                             usernames.append(row[0])
#
#                     if not usernames:
#                         answer = "未找到人脸验证失败记录。"
#                     elif len(usernames) == 1:
#                         answer = f"最近有1位用户人脸验证失败，是{usernames[0]}。"
#                     else:
#                         users_str = "、".join(usernames)
#                         answer = f"用户人脸验证失败人员分别是{result}。"
#
#                 except Exception as e:
#                     logger.error(f"SQL查询失败: {str(e)}")
#                     answer = "查询失败，请稍后再试。"
#             else:
#                 logger.info(f"通用查询(Dify路径): {query}")
#                 answer = self._call_dify(query)
#
#             return JsonResponse({"answer": answer})
#
#         except json.JSONDecodeError:
#             return JsonResponse({"answer": "请求格式错误"}, status=400)
#         except Exception as e:
#             logger.error(f"处理异常: {str(e)}")
#             return JsonResponse({"answer": "系统繁忙，请稍后再试"}, status=500)

# 版本三
# from django.http import JsonResponse
# from django.views import View
# from langchain_community.utilities import SQLDatabase
# import json
# import requests
# import logging
#
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
#
# DIFY_API_KEY = "app-yJhD6gRaJixKw7aYvd8swMGx"
# DB_URI = "mysql://root:123456@localhost/db_admin2"
#
#
# class SecurityLogAnalyst:
#     def __init__(self):
#         self.db = SQLDatabase.from_uri(DB_URI)
#         self.execute_sql = self.db.run
#
#     def get_security_logs(self):
#         """获取安全日志数据"""
#         try:
#             # 基础SQL查询，获取最近的安全日志
#             sql = """
#             SELECT *
#             FROM sys_security_log
#
#             """
#
#             # 执行SQL查询
#             result = self.execute_sql(sql)
#             print("sql_result:", result)
#             # 格式化结果
#             formatted_logs = []
#             for row in result:
#                 formatted_logs.append({
#                     "id": row[0],
#                     "event_type": row[1],
#                     "event_time": str(row[3]),
#                     "user_id": row[4]
#                 })
#
#             return formatted_logs
#             print("格式化后的：", formatted_logs)
#         except Exception as e:
#             logger.error(f"获取安全日志失败: {str(e)}")
#             return []
#
#
# class ChatView(View):
#     def __init__(self):
#         super().__init__()
#         self.analyst = SecurityLogAnalyst()
#         self.face_verify_keywords = [
#             "人脸认证失败", "人脸异常", "打卡异常", "打卡失败",
#             "人脸验证", "人脸验证失败", "刷脸失败", "最近打卡",
#             "谁打卡失败", "打卡", "人脸", "认证", "验证", "迟到", "位置"
#         ]
#
#     def _call_dify(self, query, conversation_id=None, history=None, context=None):
#         try:
#             url = "https://api.dify.ai/v1/chat-messages"
#             headers = {
#                 "Authorization": f"Bearer {DIFY_API_KEY}",
#                 "Content-Type": "application/json"
#             }
#
#             # 准备请求数据
#             data = {
#                 "inputs": {},
#                 "query": query,
#                 "response_mode": "streaming",
#                 "user": "abc-123"
#
#             }
#
#             # 如果有上下文信息，添加到inputs中
#             if context:
#                 data["inputs"] = {"context": context}
#
#             # 添加会话ID和历史记录
#             if conversation_id:
#                 data["conversation_id"] = conversation_id
#                 logger.info(f"使用会话ID: {conversation_id}")
#
#             if history and len(history) > 0:
#                 # 过滤掉包含错误信息的历史消息
#                 filtered_history = []
#                 for msg in history:
#                     if not ("服务器返回格式异常" in msg.get("content", "") or
#                             "AI服务连接失败" in msg.get("content", "")):
#                         filtered_history.append(msg)
#
#                 if filtered_history:
#                     data["history"] = filtered_history
#                     logger.info(f"发送历史消息数量: {len(filtered_history)}")
#
#             logger.info(f"Dify请求数据: {json.dumps(data, ensure_ascii=False)}")
#
#             # 发送请求
#             response = requests.post(url, headers=headers, json=data, stream=True, timeout=50000)
#
#             # 检查响应状态码
#             if response.status_code != 200:
#                 logger.error(f"Dify API返回错误状态码: {response.status_code}")
#                 logger.error(f"响应内容: {response.text}")
#
#                 # 如果是会话不存在错误，尝试创建新会话
#                 if response.status_code == 404 and "Conversation Not Exists" in response.text:
#                     logger.info("会话不存在，尝试创建新会话")
#                     # 移除会话ID，让Dify自动创建新会话
#                     if "conversation_id" in data:
#                         del data["conversation_id"]
#
#                     # 重新发送请求
#                     new_response = requests.post(url, headers=headers, json=data, stream=True, timeout=50000)
#                     if new_response.status_code == 200:
#                         logger.info("成功创建新会话")
#                         response = new_response
#                     else:
#                         return f"Dify API返回错误: HTTP {new_response.status_code}"
#                 else:
#                     return f"Dify API返回错误: HTTP {response.status_code}"
#
#             # 处理流式响应
#             answers = []
#             for line in response.iter_lines():
#                 if line:
#                     try:
#                         line_text = line.decode("utf-8")
#                         if line_text.startswith("data: "):
#                             line_text = line_text.replace("data: ", "")
#                             parsed_data = json.loads(line_text)
#                             if parsed_data.get("event") == "agent_message":
#                                 answer_part = parsed_data.get("answer", "")
#                                 answers.append(answer_part)
#                     except json.JSONDecodeError as e:
#                         logger.warning(f"JSON解析错误: {str(e)}, 行内容: {line}")
#                         continue
#                     except Exception as e:
#                         logger.warning(f"处理响应行时出错: {str(e)}")
#                         continue
#
#             full_answer = "".join(answers)
#             logger.info(f"完整回答长度: {len(full_answer)}")
#
#             if not full_answer:
#                 logger.warning("Dify返回了空回答")
#                 return "抱歉，AI未能生成回答。"
#
#             return full_answer
#         except Exception as e:
#             logger.error(f"Dify调用失败: {str(e)}")
#             return f"AI服务暂不可用: {str(e)}"
#
#     def post(self, request):
#         try:
#             data = json.loads(request.body)
#             query = data.get("content", "").strip()
#             history = data.get("history", [])
#             conversation_id = data.get("conversation_id", "")
#             print("data:", data)
#             print("query:", query)
#             print("history:", history)
#             print("conversation:", conversation_id)
#             if not query:
#                 return JsonResponse({"answer": "问题内容不能为空"})
#
#             logger.info(f"原始查询: {query}, 会话ID: {conversation_id}, 历史消息数: {len(history)}")
#
#             # 检查是否是人脸验证相关查询
#             is_face_verify_query = False
#             for keyword in self.face_verify_keywords:
#                 if keyword in query:
#                     is_face_verify_query = True
#                     break
#
#             if "安全日志" in query and ("打卡" in query or "人脸" in query):
#                 is_face_verify_query = True
#
#             if is_face_verify_query:
#                 logger.info(f"人脸验证相关查询: {query}")
#
#                 # 获取安全日志数据
#                 security_logs = self.analyst.get_security_logs()
#
#                 if not security_logs:
#                     logger.warning("未找到安全日志数据")
#                     return JsonResponse({"answer": "未找到相关的安全日志数据。"})
#
#                 # 将安全日志数据转换为上下文
#                 context = json.dumps(security_logs, ensure_ascii=False)
#
#                 # 构建增强查询
#                 enhanced_query = f"基于以下安全日志数据，请回答用户的问题: {query}"
#
#                 # 调用Dify API，传入上下文
#                 answer = self._call_dify(enhanced_query, conversation_id, history, context)
#             else:
#                 logger.info(f"通用查询(Dify路径): {query}")
#                 answer = self._call_dify(query, conversation_id, history)
#
#             return JsonResponse({"answer": answer})
#
#         except json.JSONDecodeError:
#             return JsonResponse({"answer": "请求格式错误"}, status=400)
#         except Exception as e:
#             logger.error(f"处理异常: {str(e)}")
#             return JsonResponse({"answer": "系统繁忙，请稍后再试"}, status=500)

# 最终版一

#
#
# from django.http import JsonResponse
# from django.views import View
# from langchain_community.utilities import SQLDatabase
# import json
# import requests
# import logging
# import os
#
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
#
# # 配置项：请替换为你的真实值
# DIFY_API_KEY = "app-yJhD6gRaJixKw7aYvd8swMGx"
# DEEPSEEK_API_KEY = "sk-1a92e8b805d645c1bb0a1362b5803109"
# DB_URI = "mysql://root:123456@localhost/db_admin2"
#
# # DeepSeek API 配置
# DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
#
# # HR 流程关键字
# HR_KEYWORDS = ["请假", "报销", "审批", "休假", "假期", "考勤"]
#
# # 简易内存存储，生产推荐换 Redis
# USER_CONVERSATIONS = {}
#
#
# class SecurityLogAnalyst:
#     def __init__(self):
#         self.db = SQLDatabase.from_uri(DB_URI)
#         self.execute_sql = self.db.run
#
#     def get_security_logs(self):
#         try:
#             rows = self.execute_sql("SELECT * FROM sys_security_log")
#             return [
#                 {"id": r[0], "event_type": r[1], "event_time": str(r[3]), "user_id": r[4]}
#                 for r in rows
#             ]
#         except Exception as e:
#             logger.error(f"获取安全日志失败：{e}")
#             return []
#
#
# def call_deepseek_api(messages, user_id="anonymous"):
#     """调用 DeepSeek API 进行对话"""
#     try:
#         headers = {
#             "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
#             "Content-Type": "application/json"
#         }
#
#         payload = {
#             "model": "deepseek-chat",
#             "messages": messages,
#             "temperature": 0.7,
#             "max_tokens": 2000
#         }
#
#         response = requests.post(
#             DEEPSEEK_API_URL,
#             headers=headers,
#             json=payload,
#             timeout=60
#         )
#
#         if response.status_code == 200:
#             result = response.json()
#             return result["choices"][0]["message"]["content"]
#         else:
#             logger.error(f"DeepSeek API 错误: {response.status_code} - {response.text}")
#             return "抱歉，AI 服务暂时不可用，请稍后再试。"
#
#     except Exception as e:
#         logger.error(f"调用 DeepSeek API 失败: {str(e)}")
#         return "抱歉，发生了一个错误，请稍后再试。"
#
#
# class ChatView(View):
#     """
#     路由逻辑：
#       - HR 相关问题（请假/报销等）走 Dify Agent + 安全日志；
#       - 其它对话走 DeepSeek API 多轮管理；
#     接口仍为 POST /ai/deepseek
#     """
#
#     def _call_dify(self, query, conversation_id=None, history=None, context=None):
#         url = "https://api.dify.ai/v1/chat-messages"
#         headers = {
#             "Authorization": f"Bearer {DIFY_API_KEY}",
#             "Content-Type": "application/json"
#         }
#         data = {
#             "inputs": {"context": context} if context else {},
#             "query": query,
#             "response_mode": "streaming",
#             "user": "abc-123"
#         }
#         if conversation_id:
#             data["conversation_id"] = conversation_id
#         if history:
#             # 过滤掉"错误"提示
#             data["history"] = [
#                 m for m in history
#                 if "错误" not in m.get("content", "")
#             ]
#
#         try:
#             resp = requests.post(url, json=data, headers=headers, stream=True, timeout=60)
#             if resp.status_code != 200:
#                 # 尝试移除 ID 重试
#                 data.pop("conversation_id", None)
#                 resp = requests.post(url, json=data, headers=headers, stream=True, timeout=60)
#
#             new_conv = conversation_id
#             parts = []
#             for line in resp.iter_lines():
#                 if not line: continue
#                 txt = line.decode("utf-8").lstrip("data:").strip()
#                 try:
#                     p = json.loads(txt)
#                 except:
#                     continue
#                 if p.get("event") == "session_state" and p.get("conversation_id"):
#                     new_conv = p["conversation_id"]
#                 if p.get("event") == "agent_message":
#                     parts.append(p.get("answer", ""))
#             return "".join(parts), new_conv
#         except Exception as e:
#             logger.error(f"调用 Dify API 失败: {str(e)}")
#             return "抱歉，HR 服务暂时不可用，请稍后再试。", conversation_id
#
#     def post(self, request):
#         try:
#             payload = json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse({"answer": "请求格式错误"}, status=400)
#
#         user_id = payload.get("user_id", "anonymous")
#         query = payload.get("content", "").strip()
#         history = payload.get("history", [])
#         conv_id = payload.get("conversation_id")
#
#         if not query:
#             return JsonResponse({"answer": "问题内容不能为空"}, status=400)
#
#         # 判断 HR 意图
#         if any(kw in query for kw in HR_KEYWORDS):
#             # 增强上下文
#             logs = SecurityLogAnalyst().get_security_logs()
#             ctx = json.dumps(logs, ensure_ascii=False)
#             enhanced = f"基于以下安全日志数据，请回答用户的问题：{query}"
#             answer, new_conv = self._call_dify(enhanced, conv_id, history, ctx)
#             return JsonResponse({"answer": answer, "conversation_id": new_conv})
#
#         # 否则走 DeepSeek API 多轮对话
#         # 获取或创建会话
#         if conv_id and conv_id in USER_CONVERSATIONS:
#             messages = USER_CONVERSATIONS[conv_id]
#         else:
#             # 创建新会话
#             messages = [{"role": "system", "content": "你是一个有用的AI助手，请提供准确、有帮助的回答。"}]
#             conv_id = f"conv_{user_id}_{len(USER_CONVERSATIONS) + 1}"
#
#         # 添加用户消息
#         messages.append({"role": "user", "content": query})
#
#         # 调用 DeepSeek API
#         reply = call_deepseek_api(messages, user_id)
#
#         # 添加助手回复到历史
#         messages.append({"role": "assistant", "content": reply})
#
#         # 保存会话历史
#         USER_CONVERSATIONS[conv_id] = messages
#
#         # 如果历史消息过长，裁剪以避免超出上下文限制
#         if len(messages) > 20:
#             # 保留系统消息和最近的对话
#             USER_CONVERSATIONS[conv_id] = [messages[0]] + messages[-19:]
#
#         return JsonResponse({"answer": reply, "conversation_id": conv_id})

# 最终版本二
'''
版本功能：1、可以询问员工手册内容走dify路线
        2、可以根据数据库打卡记录信息，结合deepseek API 回答用户问题，根据用户权限，如果用户权限不是超级管理员无权访问
        3、其他问题走Deepseek APi路线
        4、多轮对哈靠全局字典
'''
from role.models import SysUserRole

# from django.http import JsonResponse
# from django.views import View
# from langchain_community.utilities import SQLDatabase
# import json
# import requests
# import logging
# import traceback
# from role.models import SysUserRole, SysRole
#
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
#
# # 配置项：请替换为你的真实值
# DIFY_API_KEY = "app-yJhD6gRaJixKw7aYvd8swMGx"
# DEEPSEEK_API_KEY = "sk-1a92e8b805d645c1bb0a1362b5803109"
# DB_URI = "mysql://root:123456@localhost/db_admin2"
#
# # DeepSeek API 配置
# DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
#
# # HR 流程关键字 - 仅保留请假相关
# HR_KEYWORDS = ["请假", "休假", "假期"]
#
# # 安全日志关键字
# SECURITY_LOG_KEYWORDS = ["安全日志", "日志", "记录", "打卡失败", "位置"]
#
# # 简易内存存储，生产推荐换 Redis
# ##模块级变量
# # 存储用户会话历史，键为会话 ID，值为对话历史列表
# USER_CONVERSATIONS = {}
#
#
# class DatabaseAnalyst:
#     def __init__(self):
#         self.db = SQLDatabase.from_uri(DB_URI)
#         self.execute_sql = self.db.run
#
#     def get_security_logs(self, limit=20, event_type=None):
#         """获取安全日志数据，限制返回数量"""
#         try:
#             # 直接使用原生SQL查询，避免LangChain SQLDatabase解析问题
#             import pymysql
#
#             # 从DB_URI解析连接信息
#             # 格式: mysql://user:password@host/dbname
#             db_info = DB_URI.replace('mysql://', '').split('@')
#             user_pass = db_info[0].split(':')
#             host_db = db_info[1].split('/')
#
#             conn = pymysql.connect(
#                 host=host_db[0],
#                 user=user_pass[0],
#                 password=user_pass[1],
#                 database=host_db[1],
#                 charset='utf8mb4'
#             )
#
#             try:
#                 with conn.cursor() as cursor:
#                     # 构建查询条件
#                     where_clause = ""
#                     if event_type:
#                         where_clause = f"WHERE sl.event_type = '{event_type}'"
#
#                     # 联合查询安全日志和用户信息，限制返回数量
#                     query = f"""
#                     SELECT
#                         sl.id, sl.event_type, sl.timestamp,
#                         sl.user_id, u.username
#                     FROM
#                         sys_security_log sl
#                     LEFT JOIN
#                         sys_user u ON sl.user_id = u.id
#                     {where_clause}
#                     ORDER BY
#                         sl.timestamp DESC
#                     LIMIT {limit}
#                     """
#
#                     cursor.execute(query)
#                     rows = cursor.fetchall()
#
#                     # 格式化结果
#                     results = []
#                     for r in rows:
#                         results.append({
#                             "id": r[0],
#                             "type": r[1],
#                             "time": str(r[2]) if r[2] else None,
#                             "user": r[4] or f"用户ID:{r[3]}"
#                         })
#
#                     logger.info(f"成功获取 {len(results)} 条安全日志记录")
#                     return results
#             finally:
#                 conn.close()
#         except Exception as e:
#             logger.error(f"获取安全日志失败：{str(e)}")
#             logger.error(traceback.format_exc())
#             return []
#
#
# def call_deepseek_api(messages, user_id="anonymous"):
#     """调用 DeepSeek API 进行对话"""
#     try:
#         headers = {
#             "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
#             "Content-Type": "application/json"
#         }
#
#         payload = {
#             "model": "deepseek-chat",
#             "messages": messages,
#             "temperature": 0.7,
#             "max_tokens": 2000
#         }
#
#         response = requests.post(
#             DEEPSEEK_API_URL,
#             headers=headers,
#             json=payload,
#             timeout=60
#         )
#
#         if response.status_code == 200:
#             result = response.json()
#             return result["choices"][0]["message"]["content"]
#         else:
#             logger.error(f"DeepSeek API 错误: {response.status_code} - {response.text}")
#             return "抱歉，AI 服务暂时不可用，请稍后再试。"
#
#     except Exception as e:
#         logger.error(f"调用 DeepSeek API 失败: {str(e)}")
#         logger.error(traceback.format_exc())
#         return "抱歉，发生了一个错误，请稍后再试。"
#
#
# class ChatView(View):
#     """
#     路由逻辑：
#       - 请假相关问题走 Dify Agent；
#       - 安全日志查询走 DeepSeek + 数据库增强；
#       - 其它对话走 DeepSeek API 多轮管理；
#     """
#
#     def _call_dify(self, query, conversation_id=None, history=None, context=None):
#         url = "https://api.dify.ai/v1/chat-messages"
#         headers = {
#             "Authorization": f"Bearer {DIFY_API_KEY}",
#             "Content-Type": "application/json"
#         }
#         data = {
#             "inputs": {"context": context} if context else {},
#             "query": query,
#             "response_mode": "streaming",
#             "user": "abc-123"
#         }
#         if conversation_id:
#             data["conversation_id"] = conversation_id
#         if history:
#             # 过滤掉"错误"提示
#             data["history"] = [
#                 m for m in history
#                 if "错误" not in m.get("content", "")
#             ]
#
#         try:
#             resp = requests.post(url, json=data, headers=headers, stream=True, timeout=60)
#             if resp.status_code != 200:
#                 # 尝试移除 ID 重试
#                 data.pop("conversation_id", None)
#                 resp = requests.post(url, json=data, headers=headers, stream=True, timeout=60)
#
#             new_conv = conversation_id
#             parts = []
#             for line in resp.iter_lines():
#                 if not line: continue
#                 txt = line.decode("utf-8").lstrip("data:").strip()
#                 try:
#                     p = json.loads(txt)
#                 except:
#                     continue
#                 if p.get("event") == "session_state" and p.get("conversation_id"):
#                     new_conv = p["conversation_id"]
#                 if p.get("event") == "agent_message":
#                     parts.append(p.get("answer", ""))
#             return "".join(parts), new_conv
#         except Exception as e:
#             logger.error(f"调用 Dify API 失败: {str(e)}")
#             logger.error(traceback.format_exc())
#             return "抱歉，HR 服务暂时不可用，请稍后再试。", conversation_id
#
#     def post(self, request):
#         try:
#             payload = json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse({"answer": "请求格式错误"}, status=400)
#
#         user_id = payload.get("user_id", "anonymous")
#         query = payload.get("content", "").strip()
#         history = payload.get("history", [])
#         conv_id = payload.get("conversation_id")
#
#         # print("user_id:", user_id)
#
#         if not query:
#             return JsonResponse({"answer": "问题内容不能为空"}, status=400)
#
#         # 判断是否是请假相关问题 - 走 Dify
#         if any(kw in query for kw in HR_KEYWORDS):
#             answer, new_conv = self._call_dify(query, conv_id, history)
#             return JsonResponse({"answer": answer, "conversation_id": new_conv})
#
#         # 判断是否是安全日志查询 - 走 DeepSeek + 数据库增强
#         if any(kw in query for kw in SECURITY_LOG_KEYWORDS):
#
#             qunxian = False
#             # 使用 filter 代替 get 获取所有关联记录
#             user_roles = SysUserRole.objects.filter(user_id=user_id)
#
#             # 提取所有 role_id 到列表
#             role_ids = [ur.role_id for ur in user_roles]
#             for i in role_ids:
#                 if i == 1:
#                     qunxian = True
#
#             print("qunxian:", qunxian)
#
#             # 获取或创建会话
#             if conv_id and conv_id in USER_CONVERSATIONS:
#                 messages = USER_CONVERSATIONS[conv_id]
#             else:
#                 # 创建新会话
#                 messages = [{"role": "system", "content": "你是一个有用的AI助手，请根据提供的数据库信息回答用户的问题。"}]
#                 conv_id = f"conv_{user_id}_{len(USER_CONVERSATIONS) + 1}"
#
#             if qunxian:
#                 # 分析查询意图，确定要获取的日志类型
#                 event_type = None
#                 if "人脸验证" in query or "FACE_VERIFY" in query:
#                     event_type = "FACE_VERIFY_FAIL"
#                 elif "位置" in query or "LOCATION" in query:
#                     event_type = "LOCATION_MISMATCH"
#
#                 # 获取安全日志和用户数据，限制为最近20条
#                 logs = DatabaseAnalyst().get_security_logs(limit=20, event_type=event_type)
#
#                 # 构建增强提示，简化数据表示
#                 enhanced_prompt = f"""
#                 请根据以下安全日志数据，回答用户的问题："{query}"
#
#                 安全日志数据（最近20条{event_type or ''}记录）：
#                 {json.dumps(logs, ensure_ascii=False)}
#
#                 请分析这些数据，并给出简洁的回答。如果数据中没有相关信息，请明确告知用户。
#                 """
#
#                 # 添加用户消息
#                 messages.append({"role": "user", "content": enhanced_prompt})
#
#                 # 调用 DeepSeek API
#                 reply = call_deepseek_api(messages, user_id)
#
#                 # 添加助手回复到历史，但使用原始问题而非增强提示
#                 messages.pop()  # 移除增强提示
#                 messages.append({"role": "user", "content": query})  # 添加原始问题
#                 messages.append({"role": "assistant", "content": reply})  # 添加回复
#
#                 # 保存会话历史
#                 USER_CONVERSATIONS[conv_id] = messages
#
#                 # 如果历史消息过长，裁剪以避免超出上下文限制
#                 if len(messages) > 10:
#                     # 保留系统消息和最近的对话
#                     USER_CONVERSATIONS[conv_id] = [messages[0]] + messages[-9:]
#
#                 return JsonResponse({"answer": reply, "conversation_id": conv_id})
#             else:
#                 return JsonResponse({"answer": "抱歉，您无权访问此功能。", "conversation_id": conv_id})
#
#         # 其他问题走 DeepSeek API 多轮对话
#         # 获取或创建会话
#         if conv_id and conv_id in USER_CONVERSATIONS:
#             messages = USER_CONVERSATIONS[conv_id]
#         else:
#             # 创建新会话
#             messages = [{"role": "system", "content": "你是一个有用的AI助手，请提供准确、有帮助的回答。"}]
#             conv_id = f"conv_{user_id}_{len(USER_CONVERSATIONS) + 1}"
#
#         # 添加用户消息
#         messages.append({"role": "user", "content": query})
#
#         # 调用 DeepSeek API
#         reply = call_deepseek_api(messages, user_id)
#
#         # 添加助手回复到历史
#         messages.append({"role": "assistant", "content": reply})
#
#         # 保存会话历史
#         USER_CONVERSATIONS[conv_id] = messages
#
#         # 如果历史消息过长，裁剪以避免超出上下文限制
#         if len(messages) > 10:
#             # 保留系统消息和最近的对话
#             USER_CONVERSATIONS[conv_id] = [messages[0]] + messages[-9:]
#
#         return JsonResponse({"answer": reply, "conversation_id": conv_id})


'''终极版本
版本功能：1、可以询问员工手册内容走dify路线
        2、可以根据数据库打卡记录信息，结合deepseek API 回答用户问题，根据用户权限，如果用户权限不是超级管理员无权访问
        3、其他问题走Deepseek APi路线
        4、多轮对话靠langchain
'''
from django.http import JsonResponse
from django.views import View
from langchain_community.utilities import SQLDatabase
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import json
import requests
import logging
import traceback
import pymysql
import uuid

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 配置项：请替换为你的真实值
DIFY_API_KEY = "app-yJhD6aJix"
DEEPSEEK_API_KEY = "sk-1a92e8b8051"
DB_URI = "mysql://root:123456@localhost/db_admin2"

# DeepSeek API 配置
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# HR 流程关键字 - 仅保留请假相关
HR_KEYWORDS = ["请假", "休假", "假期"]

# 安全日志关键字
SECURITY_LOG_KEYWORDS = ["安全日志", "日志", "记录", "打卡失败", "人脸验证", "位置", "打卡"]

# 使用Redis或其他持久化存储来替代内存字典
# 这里为了简单，仍使用字典，但通过LangChain管理对话
CONVERSATION_CHAINS = {}


class DatabaseAnalyst:
    def __init__(self):
        self.db = SQLDatabase.from_uri(DB_URI)

    def get_security_logs(self, limit=20, event_type=None):
        """获取安全日志数据，限制返回数量"""
        try:
            # 直接使用原生SQL查询
            db_info = DB_URI.replace('mysql://', '').split('@')
            user_pass = db_info[0].split(':')
            host_db = db_info[1].split('/')

            conn = pymysql.connect(
                host=host_db[0],
                user=user_pass[0],
                password=user_pass[1],
                database=host_db[1],
                charset='utf8mb4'
            )

            try:
                with conn.cursor() as cursor:
                    # 构建查询条件
                    where_clause = ""
                    if event_type:
                        where_clause = f"WHERE sl.event_type = '{event_type}'"

                    # 联合查询安全日志和用户信息
                    query = f"""
                    SELECT 
                        sl.id, sl.event_type, sl.timestamp, 
                        sl.user_id, u.username
                    FROM 
                        sys_security_log sl
                    LEFT JOIN 
                        sys_user u ON sl.user_id = u.id
                    {where_clause}
                    ORDER BY 
                        sl.timestamp DESC
                    LIMIT {limit}
                    """

                    cursor.execute(query)
                    rows = cursor.fetchall()

                    # 格式化结果
                    results = []
                    for r in rows:
                        results.append({
                            "id": r[0],
                            "type": r[1],
                            "time": str(r[2]) if r[2] else None,
                            "user": r[4] or f"用户ID:{r[3]}"
                        })

                    logger.info(f"成功获取 {len(results)} 条安全日志记录")
                    return results
            finally:
                conn.close()
        except Exception as e:
            logger.error(f"获取安全日志失败：{str(e)}")
            logger.error(traceback.format_exc())
            return []


# ... existing code ...

def get_or_create_conversation_chain(conv_id, system_message=None):
    """获取或创建对话链"""
    if conv_id in CONVERSATION_CHAINS:
        return CONVERSATION_CHAINS[conv_id]

    # 创建默认系统消息
    if system_message is None:
        system_message = "你是一个有用的AI助手，请提供准确、有帮助的回答。"

    # 使用LangChain的ChatOpenAI类，但自定义API调用
    from langchain_core.language_models.chat_models import BaseChatModel
    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
    from langchain_core.outputs import ChatGeneration, ChatResult
    from typing import Any, Dict, List, Optional

    class DeepSeekChat(BaseChatModel):
        """自定义DeepSeek聊天模型，兼容LangChain接口"""

        api_key: str

        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            formatted_messages = []
            for message in messages:
                if isinstance(message, SystemMessage):
                    formatted_messages.append({"role": "system", "content": message.content})
                elif isinstance(message, HumanMessage):
                    formatted_messages.append({"role": "user", "content": message.content})
                elif isinstance(message, AIMessage):
                    formatted_messages.append({"role": "assistant", "content": message.content})

            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "model": "deepseek-chat",
                    "messages": formatted_messages,
                    "temperature": 0.7,
                    "max_tokens": 2000
                }

                response = requests.post(
                    DEEPSEEK_API_URL,
                    headers=headers,
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]

                    message = AIMessage(content=content)
                    generation = ChatGeneration(message=message)
                    return ChatResult(generations=[generation])
                else:
                    logger.error(f"DeepSeek API 错误: {response.status_code} - {response.text}")
                    message = AIMessage(content="抱歉，AI 服务暂时不可用，请稍后再试。")
                    generation = ChatGeneration(message=message)
                    return ChatResult(generations=[generation])

            except Exception as e:
                logger.error(f"调用 DeepSeek API 失败: {str(e)}")
                logger.error(traceback.format_exc())
                message = AIMessage(content="抱歉，发生了一个错误，请稍后再试。")
                generation = ChatGeneration(message=message)
                return ChatResult(generations=[generation])

        @property
        def _llm_type(self) -> str:
            return "deepseek-chat"

    # 创建记忆组件
    memory = ConversationBufferMemory(return_messages=True)

    # 创建提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    # 创建对话链
    chain = ConversationChain(
        memory=memory,
        prompt=prompt,
        llm=DeepSeekChat(api_key=DEEPSEEK_API_KEY)
    )

    # 存储对话链
    CONVERSATION_CHAINS[conv_id] = chain
    return chain


# ... rest of the code remains the same ...


def call_deepseek_api(messages, user_id="anonymous"):
    """直接调用 DeepSeek API 进行对话"""
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }

        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            logger.error(f"DeepSeek API 错误: {response.status_code} - {response.text}")
            return "抱歉，AI 服务暂时不可用，请稍后再试。"

    except Exception as e:
        logger.error(f"调用 DeepSeek API 失败: {str(e)}")
        logger.error(traceback.format_exc())
        return "抱歉，发生了一个错误，请稍后再试。"


class ChatView(View):
    """
    路由逻辑：
      - 请假相关问题走 Dify Agent；
      - 安全日志查询走 DeepSeek + 数据库增强；
      - 其它对话走 DeepSeek API 多轮管理；
    """

    def _call_dify(self, query, conversation_id=None, history=None, context=None):
        url = "https://api.dify.ai/v1/chat-messages"
        headers = {
            "Authorization": f"Bearer {DIFY_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "inputs": {"context": context} if context else {},
            "query": query,
            "response_mode": "streaming",
            "user": "abc-123"
        }
        if conversation_id:
            data["conversation_id"] = conversation_id
        if history:
            # 过滤掉"错误"提示
            data["history"] = [
                m for m in history
                if "错误" not in m.get("content", "")
            ]

        try:
            resp = requests.post(url, json=data, headers=headers, stream=True, timeout=60)
            if resp.status_code != 200:
                # 尝试移除 ID 重试
                data.pop("conversation_id", None)
                resp = requests.post(url, json=data, headers=headers, stream=True, timeout=60)

            new_conv = conversation_id
            parts = []
            for line in resp.iter_lines():
                if not line: continue
                txt = line.decode("utf-8").lstrip("data:").strip()
                try:
                    p = json.loads(txt)
                except:
                    continue
                if p.get("event") == "session_state" and p.get("conversation_id"):
                    new_conv = p["conversation_id"]
                if p.get("event") == "agent_message":
                    parts.append(p.get("answer", ""))
            return "".join(parts), new_conv
        except Exception as e:
            logger.error(f"调用 Dify API 失败: {str(e)}")
            logger.error(traceback.format_exc())
            return "抱歉，HR 服务暂时不可用，请稍后再试。", conversation_id

    def post(self, request):
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"answer": "请求格式错误"}, status=400)

        user_id = payload.get("user_id", "anonymous")
        query = payload.get("content", "").strip()
        history = payload.get("history", [])
        conv_id = payload.get("conversation_id")

        if not query:
            return JsonResponse({"answer": "问题内容不能为空"}, status=400)

        # 判断是否是请假相关问题 - 走 Dify
        if any(kw in query for kw in HR_KEYWORDS):
            answer, new_conv = self._call_dify(query, conv_id, history)
            return JsonResponse({"answer": answer, "conversation_id": new_conv})

        # 判断是否是安全日志查询 - 走 DeepSeek + 数据库增强
        if any(kw in query for kw in SECURITY_LOG_KEYWORDS):

            # 确保有会话ID
            if not conv_id:
                conv_id = f"log_query_{uuid.uuid4()}"

            # 判断用户是否有权限
            qunxian = False
            # 使用 filter 代替 get 获取所有关联记录
            user_roles = SysUserRole.objects.filter(user_id=user_id)

            # 提取所有 role_id 到列表
            role_ids = [ur.role_id for ur in user_roles]
            for i in role_ids:
                if i == 1:
                    qunxian = True

            # print("qunxian:", qunxian)

            if qunxian == True:

                # 分析查询意图，确定要获取的日志类型
                event_type = None
                if "人脸验证" in query or "FACE_VERIFY" in query:
                    event_type = "FACE_VERIFY_FAIL"
                elif "位置" in query or "LOCATION" in query:
                    event_type = "LOCATION_MISMATCH"

                # 获取安全日志和用户数据，限制为最近20条
                logs = DatabaseAnalyst().get_security_logs(limit=20, event_type=event_type)

                # 构建增强提示，简化数据表示
                enhanced_prompt = f"""
                请根据以下安全日志数据，回答用户的问题："{query}"
    
                安全日志数据（最近20条{event_type or ''}记录）：
                {json.dumps(logs, ensure_ascii=False)}
    
                请分析这些数据，并给出简洁的回答。如果数据中没有相关信息，请明确告知用户。
                """

                # 使用一次性调用，不保存增强提示到对话历史
                messages = [
                    {"role": "system", "content": "你是一个有用的AI助手，请根据提供的数据库信息回答用户的问题。"},
                    {"role": "user", "content": enhanced_prompt}
                ]

                # 调用 DeepSeek API
                reply = call_deepseek_api(messages, user_id)

                # 获取或创建对话链，保存原始问题和回答
                chain = get_or_create_conversation_chain(
                    conv_id,
                    "你是一个有用的AI助手，专门回答关于安全日志的问题。"
                )

                # 将原始问题和回答添加到对话历史
                chain.memory.chat_memory.add_user_message(query)
                chain.memory.chat_memory.add_ai_message(reply)

                return JsonResponse({"answer": reply, "conversation_id": conv_id})
            else:
                return JsonResponse({"answer": "抱歉，您没有权限执行此操作。", "conversation_id": conv_id})

        # 其他问题走 LangChain 管理的 DeepSeek 对话
        # 确保有会话ID
        if not conv_id:
            conv_id = f"chat_{uuid.uuid4()}"

        # 获取或创建对话链
        chain = get_or_create_conversation_chain(conv_id)

        # 使用对话链处理查询
        reply = chain.predict(input=query)

        return JsonResponse({"answer": reply, "conversation_id": conv_id})
