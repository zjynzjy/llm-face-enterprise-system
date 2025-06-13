// 在退出登录方法中添加
const logout = () => {
  // 获取当前用户ID
  const currentUser = JSON.parse(sessionStorage.getItem('currentUser') || '{}')
  const userId = currentUser.id
  
  // 清理该用户的AI聊天记录
  if (userId) {
    localStorage.removeItem(`ai_chat_data_${userId}`)
  }
  
  // 原有的退出登录逻辑
  sessionStorage.removeItem('currentUser')
  sessionStorage.removeItem('token')
  // 其他清理操作...
  
  // 跳转到登录页
  router.push('/login')
}