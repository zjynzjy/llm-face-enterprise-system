<template>
  <el-dropdown>
    <span class="el-dropdown-link">
      <el-avatar shape="square" :size="40" :src="squareUrl" />
      &nbsp;&nbsp;{{currentUser.username}}
      <el-icon class="el-icon--right">
        <arrow-down />
      </el-icon>
    </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item><router-link :to="{name:'个人中心'}">个人中心</router-link></el-dropdown-item>
        <el-dropdown-item @click="logout">安全退出</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup>
import { ArrowDown } from '@element-plus/icons-vue'
import requestUtil,{getServerUrl} from '@/util/request'
import router from '@/router'
import store from '@/store'
const currentUser=JSON.parse(sessionStorage.getItem("currentUser")) 


//获取头像图片路径
const squareUrl=getServerUrl()+'media/userAvatar/'+currentUser.avatar



// 点击事件
const logout=()=>{
  // 获取当前用户ID
  const userId = currentUser.id
  
  // 清理该用户的AI聊天记录
  if (userId) {
    localStorage.removeItem(`ai_chat_data_${userId}`)
  }
  
  window.sessionStorage.clear()
  store.commit("RESET_TAB")
  router.replace("/login")
}
</script>

<style lang="scss" scoped>
.el-dropdown-link {
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}
</style>
