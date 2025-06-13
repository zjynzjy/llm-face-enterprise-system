<template>
  <div class="login">
   <!-- ref="loginRef"：注册表单引用，用于后续的表单验证
:model="loginForm"：绑定表单数据对象
:rules="loginRules"：绑定表单验证规则 -->
    <el-form ref="loginRef" :model="loginForm" :rules="loginRules" class="login-form">
      <h3 class="title">公司后台管理系统</h3>

      <el-form-item prop="username">

        <el-input
            v-model="loginForm.username"
            type="text"
            size="large"
            auto-complete="off"
            placeholder="账号"
        >
          <template #prefix><svg-icon icon="user" /></template>
        </el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input
            v-model="loginForm.password"
            type="password"
            size="large"
            auto-complete="off"
            placeholder="密码"
        >
          <template #prefix><svg-icon icon="password" /></template>
        </el-input>
      </el-form-item>


      <el-checkbox v-model="loginForm.rememberMe" style="margin:0px 0px 25px 0px;">记住密码</el-checkbox>
      <el-form-item style="width:100%;">
        <el-button
            size="large"
            type="primary"
            style="width:100%;"
            @click.prevent="handleLogin"
        >
          <span>登 录</span>

        </el-button>

      </el-form-item>
    </el-form>

  </div>
</template>

<script setup>
  import {ref} from 'vue'
  import requestUtil from '@/util/request'
  import qs from 'qs'
  import {ElMessage} from 'element-plus'
  import Cookies from "js-cookie";
  import { encrypt, decrypt } from "@/util/jsencrypt";
  
  import router from '@/router'


  const loginForm=ref({
    username:'',
    password:'',
    rememberMe:false
  })

  const loginRef=ref(null)

  const loginRules = {
    username: [{required: true, trigger: "blur", message: "请输入您的账号"}],
    password: [{required: true, trigger: "blur", message: "请输入您的密码"}]
  };

  const handleLogin=()=>{
    // 触发验证
    loginRef.value.validate(async (valid)=>{
      if(valid){
        // 表单验证通过
        let result=await requestUtil.post("user/login?"+qs.stringify(loginForm.value))//给后端传入user与password
        console.log(result)

        let data=result.data
        if(data.code==200){
        //用户名在数据库中匹配
          //成功登录弹框
          ElMessage.success(data.info)//显示成功消息ElMessage：这是 Element UI 提供的一个消息提示组件，用于在页面上弹出一个短暂显示的消息框，向用户展示一些提示信息。
          // 将令牌存储到会话存储中
          window.sessionStorage.setItem("token",data.token)
  
          const currentUser = data.user
          currentUser.roles = data.roles
          window.sessionStorage.setItem("currentUser", JSON.stringify(currentUser))  


          window.sessionStorage.setItem("menuList",JSON.stringify(data.menuList))
          // 勾选了需要记住密码设置在 cookie 中设置记住用户名和密码
          if (loginForm.value.rememberMe) {
            Cookies.set("username", loginForm.value.username, { expires: 30 });
            Cookies.set("password", encrypt(loginForm.value.password), { expires: 30 });
            Cookies.set("rememberMe", loginForm.value.rememberMe, { expires: 30 });

          } else {
          // 否则移除
            Cookies.remove("username");
            Cookies.remove("password");
            Cookies.remove("rememberMe");
          }

          router.replace("/")//登录成功跳转到主页面

        }else{
        //用户数据库中没有
          ElMessage.error(data.info)

        }
      }else{
        //表单输入不合法验证失败
        console.log("验证失败")
      }
    })
  }
  function getCookie() {
  const username = Cookies.get("username");//从cookies中获取因为该值双向绑定的表单，故表单输入框中被填充
  const password = Cookies.get("password");
  const rememberMe = Cookies.get("rememberMe");
  loginForm.value ={
  username: username === undefined ? loginForm.value.username : username,
  password: password === undefined ? loginForm.value.password :
decrypt(password),
  rememberMe: rememberMe === undefined ? false : Boolean(rememberMe)
  };
}
  getCookie();//js调用方法

</script>

<style lang="scss" scoped>
a {
  color: white
}

.login {
  // 增添
  background-position: center;      // 确保图片居中显示
  background-repeat: no-repeat;     // 防止重复平铺
  background-attachment: fixed;     // 固定背景产生视差效果
  background-color: #b8c4ce;        // 添加备用背景色（与图片主色调协调）
  &::before {                       // 添加遮罩层
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.3); // 深色透明遮罩
    z-index: 0;
  }
  // 
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background-image: url("../assets/images/login-background.jpg");
  background-size: cover;
}

.title {
  margin: 0px auto 30px auto;
  text-align: center;
  // color: #707070;
  // 
  color: #409EFF;                   // 使用Element主题色
  font-size: 24px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); // 文字阴影
  // 
}

.login-form {
  // 
  animation: formEntrance 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
  @keyframes formEntrance {
  0% {
    opacity: 0;
    transform: translateY(50px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
// 
  border-radius: 6px;
  background: #ffffff;
  width: 400px;
  padding: 25px 25px 5px 25px;
  // 
  position: relative;               // 确保在遮罩层上方
  z-index: 1;
  box-shadow: 0 2px 30px rgba(0, 0, 0, 0.2); // 增加立体感
  background: rgba(255, 255, 255, 0.95);     // 半透明白色背景
  border-radius: 10px;              // 增大圆角
  backdrop-filter: blur(2px);       // 毛玻璃效果（可选）
  // 
  .el-input {
    height: 40px;
    input {
      display: inline-block;
      height: 40px;
    }
  }
  
  .input-icon {
    height: 39px;
    width: 14px;
    margin-left: 0px;
  }
}

.login-tip {
  font-size: 13px;
  text-align: center;
  color: #bfbfbf;
}

.login-code {
  width: 33%;
  height: 40px;
  float: right;
  img {
    cursor: pointer;
    vertical-align: middle;
  }
}

.el-login-footer {
  height: 40px;
  line-height: 40px;
  position: fixed;
  bottom: 0;
  width: 100%;
  text-align: center;
  color: #fff;
  font-family: Arial;
  font-size: 12px;
  letter-spacing: 1px;
}

.login-code-img {
  height: 40px;
  padding-left: 12px;
}
.el-button--primary {
  background: linear-gradient(45deg, #409EFF, #3375b9); // 渐变色
  border: none;
  transition: all 0.3s;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(64, 158, 255, 0.4);
  }
}
@media (max-width: 768px) {
  .login-form {
    width: 90%;
    padding: 20px 15px;
  }
  
  .title {
    font-size: 20px;
    margin-bottom: 20px;
  }
}
</style>