<template>
  <el-icon>
    <HomeFilled/>
  </el-icon>
  <el-breadcrumb separator="/">
    <el-breadcrumb-item v-for="(item,index) in breadcrumbList"><span>{{ item.name }}</span></el-breadcrumb-item>

  </el-breadcrumb>
</template>


<script setup>
import {HomeFilled} from '@element-plus/icons-vue'
import {ref, watch} from 'vue'
import {useRoute} from 'vue-router'
import store from "@/store";
const route=useRoute()// 获取当前路由信息对象

const breadcrumbList=ref([])// 创建响应式面包屑数组
// ref是vue3的响应式API，创建响应式对象，值变化时自动更新视图。通过.value访问实际值。

const initBreadcrumbList=()=>{
  breadcrumbList.value=route.matched;// 获取路由匹配记录
}
//监听路由有变化，重新调用initBreadcrumbList()方法
watch(route,()=>{
  initBreadcrumbList()
},{deep:true,immediate:true})
console.log(breadcrumbList);



</script>

<style lang="scss" scoped>

</style>
