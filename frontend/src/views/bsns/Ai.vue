<template>
  <div class="ai-container">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="header">
        <h2 class="logo">DeepSeek</h2>
        <el-button type="primary" class="new-chat-btn" @click="startNewChat">
          <i class="el-icon-plus"></i>
          新建对话
        </el-button>
      </div>
      <div class="chat-history">
        <div
          v-for="(chat, index) in chatSessions"
          :key="index"
          class="chat-item"
          :class="{ active: activeChatIndex === index }"
          @click="switchChat(index)"
        >
          <i class="el-icon-chat-dot-round"></i>
          <span>{{ chat.title || `对话 ${index + 1}` }}</span>
          <i class="el-icon-delete" @click.stop="deleteChat(index)"></i>
        </div>
      </div>
    </aside>

    <!-- 主聊天区域 -->
    <main class="chat-main">
      <div class="message-container" ref="messageContainer">
        <div
          v-for="(message, index) in messages"
          :key="index"
          class="message-wrapper"
          :class="{
            'user-message': message.role === 'user',
            'ai-message': message.role === 'assistant'
          }"
        >
          <div class="message-bubble">
            <div class="avatar">
              <img
                v-if="message.role === 'user'"
                :src="squareUrl"
                alt="用户头像"
              />
              <div v-else class="ai-avatar">DS</div>
            </div>
            <div class="content">
              <!-- 恢复使用TypedDisplay组件，但传入渲染后的HTML -->
              <typed-display
                v-if="message.role === 'assistant'"
                :html="true"
                :text="message.content"
              />
              <template v-else>{{ message.content }}</template>
            </div>
          </div>
        </div>
        <div v-if="isLoading" class="loading-indicator">
          <div class="dot-flashing"></div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="input-container">
        <el-input
          type="textarea"
          :rows="3"
          v-model="inputMessage"
          @keydown.enter.exact.prevent="sendMessage"
          placeholder="输入消息...（Shift+Enter换行）"
          resize="none"
          class="message-input"
        />
        <el-button
          type="primary"
          @click="sendMessage"
          :disabled="isLoading"
          class="send-btn"
        >
          发送
        </el-button>
      </div>
    </main>

    <!-- 新建对话弹窗 -->
    <el-dialog v-model="showNewChatDialog" title="新建对话" width="30%">
      <span>是否要开始新对话？当前对话将保存到历史记录。</span>
      <template #footer>
        <el-button @click="showNewChatDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmNewChat">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import TypedDisplay from '@/components/TypedDisplay'
import requestUtil from '@/util/request'
// 引入markdown-it库
import MarkdownIt from 'markdown-it'

export default {
  name: 'AiChat',
  components: { TypedDisplay },
  data() {
    const currentUser = JSON.parse(sessionStorage.getItem('currentUser') || '{}')
    
    return {
      user_id:currentUser.id,
      inputMessage: '',
      messages: [],
      chatSessions: [
        {
          title: '初始对话',
          messages: []
        }
      ],
      activeChatIndex: 0,
      isLoading: false,
      showNewChatDialog: false,
      squareUrl: currentUser.avatar
        ? `http://localhost:8000/media/userAvatar/${currentUser.avatar}`
        : '',
      // Dify 会话 ID，首次为 null，后续更新
      conversation_id: null,
      // 添加 markdown-it 实例
      md: new MarkdownIt({
        html: true,
        linkify: true,
        typographer: true
      })
    }
  },
  created() {
    // 组件创建时从localStorage加载聊天数据
    this.loadChatData()
  },
  methods: {
    // 从localStorage加载聊天数据
    loadChatData() {
      const userId = this.user_id
      if (!userId) return
      
      const savedData = localStorage.getItem(`ai_chat_data_${userId}`)
      if (savedData) {
        try {
          const data = JSON.parse(savedData)
          this.chatSessions = data.chatSessions || this.chatSessions
          this.activeChatIndex = data.activeChatIndex || 0
          this.messages = data.messages || []
          this.conversation_id = data.conversation_id || null
        } catch (e) {
          console.error('加载聊天数据失败:', e)
        }
      }
    },
    
    // 保存聊天数据到localStorage
    saveChatData() {
      if (!this.user_id) return
      
      const dataToSave = {
        chatSessions: this.chatSessions,
        activeChatIndex: this.activeChatIndex,
        messages: this.messages,
        conversation_id: this.conversation_id
      }
      
      localStorage.setItem(`ai_chat_data_${this.user_id}`, JSON.stringify(dataToSave))
    },
    
    async sendMessage() {
      if (!this.inputMessage.trim() || this.isLoading) return

      // 推入用户消息
      this.messages.push({ role: 'user', content: this.inputMessage.trim() })
      const content = this.inputMessage.trim()
      this.inputMessage = ''
      this.isLoading = true

      try {
        const answer = await this.fetchAnswer(content, this.messages)
        this.messages.push({ role: 'assistant', content: answer })
        this.scrollToBottom()
        // 发送消息后保存数据
        this.saveChatData()
      } catch (err) {
        this.$message.error('请求失败: ' + err.message)
      } finally {
        this.isLoading = false
      }
    },

    async fetchAnswer(content, history) {
      const payload = {
        user_id:this.user_id,
        conversation_id: this.conversation_id,
        content,
        history: history.map(m => ({ role: m.role, content: m.content }))
      }
      const res = await requestUtil.post('ai/deepseek', payload)
      console.log('后端响应：', res)
      if (res && res.data) {
        // 更新会话 ID
        this.conversation_id = res.data.conversation_id
        return res.data.answer
      } else {
        console.warn('服务器返回格式有误', res)
        return '服务器返回格式异常'
      }
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const c = this.$refs.messageContainer
        c.scrollTop = c.scrollHeight
      })
    },

    startNewChat() {
      this.showNewChatDialog = true
    },
    
    confirmNewChat() {
      this.showNewChatDialog = false
      this.saveCurrentSession()
      this.createNewSession()
      // 重置会话 ID，让后端新建
      this.conversation_id = null
      // 保存数据
      this.saveChatData()
    },
    
    saveCurrentSession() {
      if (this.messages.length) {
        this.chatSessions.splice(this.activeChatIndex, 1, {
          ...this.chatSessions[this.activeChatIndex],
          messages: [...this.messages]
        })
        // 保存当前会话后保存数据
        this.saveChatData()
      }
    },
    
    createNewSession() {
      const idx = this.chatSessions.length
      this.chatSessions.push({ title: `对话 ${idx + 1}`, messages: [] })
      this.activeChatIndex = idx
      this.messages = []
    },
    
    switchChat(idx) {
      this.saveCurrentSession()
      this.activeChatIndex = idx
      this.messages = [...this.chatSessions[idx].messages]
      // 切换对话也需重置会话 ID，以防串会话
      this.conversation_id = null
      // 切换会话后保存数据
      this.saveChatData()
    },
    
    deleteChat(idx) {
      this.$confirm('删除此对话？', '提示', { type: 'warning' })
        .then(() => {
          this.chatSessions.splice(idx, 1)
          if (this.activeChatIndex === idx) {
            this.activeChatIndex = Math.max(0, idx - 1)
            this.messages = [...this.chatSessions[this.activeChatIndex].messages]
            this.conversation_id = null
          }
          // 删除会话后保存数据
          this.saveChatData()
        })
        .catch(() => {})
    },
    
    // 添加markdown渲染方法
    renderMarkdown(text) {
      return this.md.render(text);
    }
  }
}
</script>

<style scoped lang="scss">
.ai-container {
  display: flex;
  height: 100vh;
  background: #f5f7fb;
  .sidebar {
    width: 260px;
    background: #fff;
    border-right: 1px solid #e8e8e8;
    padding: 20px;
    display: flex;
    flex-direction: column;
    .header {
      padding-bottom: 20px;
      border-bottom: 1px solid #eee;
      .logo {
        color: #2d3a4b;
        font-size: 24px;
        margin: 0 0 20px;
      }
      .new-chat-btn {
        width: 100%;
      }
    }
    .chat-history {
      flex: 1;
      overflow-y: auto;
      margin-top: 20px;
      .chat-item {
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
        display: flex;
        align-items: center;
        cursor: pointer;
        transition: all 0.2s ease;  // 添加过渡效果
        
        &.active {
          background: #f0f4ff;
          font-weight: 500;
          border-left: 3px solid #4a90e2;  // 添加左侧边框标识活动项
        }
        
        i.el-icon-chat-dot-round {
          color: #4a90e2;
          margin-right: 8px;
        }
        
        span {
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          flex: 1;
        }
        
        .el-icon-delete {
          margin-left: auto;
          opacity: 0;
          transition: opacity 0.2s;
          color: #f56c6c;  // 删除图标使用红色
        }
        
        &:hover {
          background: #f5f7fb;
          .el-icon-delete {
            opacity: 0.7;
            &:hover {
              opacity: 1;
            }
          }
        }
      }
    }
  }
  .chat-main {
    flex: 1;
    display: flex;
    flex-direction: column;
    .message-container {
      flex: 1;
      overflow-y: auto;
      padding: 24px;
    }
    .message-wrapper {
      margin: 20px 0;
      &.user-message .message-bubble {
        flex-direction: row-reverse;
      }
      .message-bubble {
        display: flex;
        gap: 16px;
        max-width: 800px;
        margin: 0 auto;
        .avatar img,
        .ai-avatar {
          width: 40px;
          height: 40px;
          border-radius: 8px;
          background: #4a90e2;
          color: #fff;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: bold;  // 加粗AI头像中的文字
        }
        .content {
          padding: 16px;
          background: #f0f4ff;
          border-radius: 12px;
          line-height: 1.6;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);  // 添加轻微阴影
          
          // 添加代码高亮样式
          pre {
            background: #2d3748;
            color: #e2e8f0;
            padding: 12px;
            border-radius: 6px;
            overflow-x: auto;
            margin: 10px 0;
          }
          
          // 添加强调文本样式
          // 修改这里，使用:deep()选择器确保样式能穿透到v-html渲染的内容
          :deep(strong), :deep(b) {
            color: #3182ce;
            font-weight: 700; // 增加字重，使加粗更明显
          }
          
          :deep(em) {
            font-style: italic;
          }
          
          :deep(ul), :deep(ol) {
            padding-left: 20px;
            margin: 10px 0;
          }
          
          :deep(li) {
            margin-bottom: 5px;
          }
          
          // 添加链接样式
          a {
            color: #4a90e2;
            text-decoration: none;
            border-bottom: 1px dashed #4a90e2;
            &:hover {
              border-bottom: 1px solid #4a90e2;
            }
          }
        }
      }
      
      // 区分用户和AI消息的样式
      &.user-message .message-bubble .content {
        background: #e6f7ff;
        border: 1px solid #d6e8ff;
      }
      
      &.ai-message .message-bubble .content {
        background: #f8f9fa;
        border: 1px solid #eaecef;
      }
    }
    .input-container {
      padding: 20px;
      background: #fff;
      border-top: 1px solid #e8e8e8;
      display: flex;
      gap: 12px;
      box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.03);  // 添加顶部阴影
      
      .message-input ::v-deep .el-textarea__inner {
        border-radius: 12px;
        padding: 12px 16px;
        border: 1px solid #dcdfe6;
        transition: all 0.3s;
        
        &:focus {
          border-color: #4a90e2;
          box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
        }
      }
      
      .send-btn {
        align-self: flex-end;
        padding: 12px 24px;
        background: #4a90e2;
        color: #fff;
        border-radius: 8px;
        transition: all 0.3s;
        
        &:hover {
          background: #3a80d2;
          transform: translateY(-2px);
        }
        
        &:active {
          transform: translateY(0);
        }
        
        &:disabled {
          background: #a0cfff;
        }
      }
    }
  }
  .loading-indicator {
    display: flex;
    justify-content: center;
    margin: 20px 0;

    .dot-flashing {
      position: relative;
      width: 10px;
      height: 10px;
      border-radius: 5px;
      background-color: #4a90e2;
      animation: dotFlashing 1s infinite alternate;
      
      &::before,
      &::after {
        content: '';
        position: absolute;
        width: 10px;
        height: 10px;
        border-radius: 5px;
        background-color: #4a90e2;
        animation: dotFlashing 1s infinite alternate;
      }
      
      &::before {
        left: -15px;
        animation-delay: 0s;
      }
      
      &::after {
        left: 15px;
        animation-delay: 1s;
      }
    }
  }
  @keyframes dotFlashing {
    0% {
      opacity: 0.2;
    }
    50% {
      opacity: 0.5;
    }
    100% {
      opacity: 1;
    }
  }
}
</style>
