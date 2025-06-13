<template>
  <div class="face-recording-container">
    <!-- 标题区域 -->
    <el-card class="header-card">
      <h2>人脸信息录入</h2>
      <p>请保持面部在摄像头中央并保持光线充足</p>
      <div v-if="currentUser" class="user-info">
        <span>当前用户: {{ currentUser.username }}</span>
      </div>
    </el-card>

    <!-- 视频捕获区域 -->
    <el-card class="video-card">
      <div class="video-container">
        <!-- 视频流显示 -->
        <video ref="videoEl" autoplay muted playsinline></video>
        <!-- 人脸检测结果显示画布 -->
        <canvas ref="canvasEl" class="canvas-overlay"></canvas>

        <!-- 检测状态指示器 -->
        <div class="detection-status" :class="{ 'detected': faceDetected }">
          <i :class="faceDetected ? 'el-icon-check' : 'el-icon-warning'"></i>
          <span>{{ faceDetected ? '已检测到人脸' : '未检测到人脸' }}</span>
        </div>
      </div>

      <!-- 操作按钮区域 -->
      <div class="action-buttons">
        <el-button type="primary" :loading="isInitializing" :disabled="!modelsLoaded || isCapturing"
          @click="startCamera">
          {{ cameraActive ? '重新开始' : '启动摄像头' }}
        </el-button>

        <el-button type="success" :disabled="!cameraActive || !faceDetected || isCapturing" @click="startCapturing">
          开始采集
        </el-button>

        <el-button type="primary" :loading="isSubmitting" :disabled="!captureComplete" @click="submitFaceFeatures">
          提交人脸信息
        </el-button>

        <el-button @click="resetAll">重置</el-button>
      </div>

      <!-- 采集进度 -->
      <div v-if="isCapturing" class="capture-progress">
        <el-progress :percentage="captureProgress" :status="captureComplete ? 'success' : ''">
        </el-progress>
        <p class="progress-text">{{ captureStatusText }}</p>
      </div>
    </el-card>

    <!-- 结果消息 -->
    <el-alert v-if="errorMessage" :title="errorMessage" type="error" :closable="true" show-icon>
    </el-alert>

    <el-alert v-if="successMessage" :title="successMessage" type="success" :closable="true" show-icon>
    </el-alert>
  </div>
</template>

<script>
// 导入人脸识别库
import * as faceapi from 'face-api.js';
import axios from 'axios';
import requestUtil from '@/util/request'; // 根据实际路径调整
export default {
  name: 'FaceRecording',
  data() {
    return {
      // 当前用户信息
      currentUser: null,
      token: null,

      // DOM元素引用
      videoEl: null,  // 视频元素
      canvasEl: null, // 画布元素
      stream: null,   // 媒体流

      // 状态标志
      modelsLoaded: false,   // 模型是否加载完成
      isInitializing: true,  // 初始化中
      cameraActive: false,   // 摄像头是否活跃
      faceDetected: false,   // 是否检测到人脸
      isCapturing: false,    // 是否正在采集特征
      captureComplete: false, // 采集是否完成
      isSubmitting: false,   // 是否正在提交数据

      // 采集相关
      captureCount: 0,      // 当前采集次数
      totalCaptures: 5,     // 总共需要采集次数
      captureTimer: null,   // 采集计时器
      detectionTimer: null, // 检测计时器
      faceFeatures: [],     // 采集的人脸特征数组

      // 消息提示
      errorMessage: '',   // 错误消息
      successMessage: '', // 成功消息
    };
  },

  computed: {
    // 计算采集进度百分比
    captureProgress() {
      return Math.floor((this.captureCount / this.totalCaptures) * 100);
    },

    // 采集状态文本
    captureStatusText() {
      if (this.captureComplete) {
        return '人脸特征采集完成，请提交';
      }
      return `正在采集人脸特征 (${this.captureCount}/${this.totalCaptures})`;
    }
  },

  created() {
    // 从会话存储中获取用户信息和令牌
    const userString = window.sessionStorage.getItem("currentUser");
    this.token = window.sessionStorage.getItem("token");

    if (userString) {
      try {
        this.currentUser = JSON.parse(userString);
      } catch (e) {
        console.error("解析用户信息失败:", e);
        this.$router.push('/login');
        return;
      }
    } else {
      // 用户未登录，跳转到登录页
      this.$router.push('/login');
      return;
    }
  },

  mounted() {
    // 获取DOM元素引用
    this.videoEl = this.$refs.videoEl;
    this.canvasEl = this.$refs.canvasEl;

    // 加载人脸识别模型
    this.loadFaceApiModels();
  },

  beforeDestroy() {
    // 清理资源
    this.stopCamera();
    this.clearTimers();
  },

  methods: {
    /**
     * 加载face-api.js模型
     */
    async loadFaceApiModels() {
      try {
        this.isInitializing = true;

        // 使用CDN加载模型
        const modelPath = 'https://justadudewhohacks.github.io/face-api.js/models';

        // 加载人脸检测、特征点和特征向量提取模型
        await Promise.all([
          faceapi.nets.ssdMobilenetv1.loadFromUri(modelPath),
          faceapi.nets.faceLandmark68Net.loadFromUri(modelPath),
          faceapi.nets.faceRecognitionNet.loadFromUri(modelPath)
        ]);

        this.modelsLoaded = true;
        console.log('人脸识别模型加载完成');
      } catch (error) {
        console.error('模型加载失败:', error);
        this.errorMessage = '人脸识别模型加载失败，请刷新页面重试';
      } finally {
        this.isInitializing = false;
      }
    },

    /**
     * 启动摄像头
     */
    async startCamera() {
      // 如果摄像头已启动，先停止它
      if (this.cameraActive) {
        this.stopCamera();
        return;
      }

      try {
        // 请求摄像头访问权限
        this.stream = await navigator.mediaDevices.getUserMedia({
          video: {
            width: 640,
            height: 480,
            facingMode: 'user' // 使用前置摄像头
          }
        });

        // 将视频流设置到video元素
        this.videoEl.srcObject = this.stream;
        this.cameraActive = true;

        // 开始人脸检测
        this.startFaceDetection();
      } catch (error) {
        console.error('摄像头访问失败:', error);
        this.errorMessage = '无法访问摄像头，请确保已授予摄像头权限';
      }
    },

    /**
     * 停止摄像头
     */
    stopCamera() {
      if (this.stream) {
        // 停止所有视频轨道
        this.stream.getTracks().forEach(track => track.stop());
        this.stream = null;
      }

      if (this.videoEl) {
        this.videoEl.srcObject = null;
      }

      this.cameraActive = false;
      this.faceDetected = false;

      // 清除检测计时器
      if (this.detectionTimer) {
        clearInterval(this.detectionTimer);
        this.detectionTimer = null;
      }
    },

    /**
     * 开始人脸检测
     */
    startFaceDetection() {
      // 确保摄像头已启动
      if (!this.cameraActive) return;

      // 设置画布尺寸
      this.canvasEl.width = this.videoEl.videoWidth || 640;
      this.canvasEl.height = this.videoEl.videoHeight || 480;

      // 创建画布上下文
      const ctx = this.canvasEl.getContext('2d');

      // 清除之前的计时器
      if (this.detectionTimer) {
        clearInterval(this.detectionTimer);
      }

      // 设置检测计时器，每100ms检测一次
      this.detectionTimer = setInterval(async () => {
        if (!this.cameraActive) return;

        try {
          // 使用SSD MobileNet进行人脸检测
          const detections = await faceapi.detectAllFaces(this.videoEl)
            .withFaceLandmarks()  // 获取人脸特征点
            .withFaceDescriptors(); // 获取人脸特征向量

          // 清除画布
          ctx.clearRect(0, 0, this.canvasEl.width, this.canvasEl.height);

          // 绘制视频帧
          ctx.drawImage(this.videoEl, 0, 0, this.canvasEl.width, this.canvasEl.height);

          // 更新人脸检测状态
          this.faceDetected = detections.length > 0;

          // 如果检测到人脸，绘制人脸框和特征点
          if (this.faceDetected) {
            // 调整检测结果尺寸以匹配画布
            const resizedDetections = faceapi.resizeResults(detections, {
              width: this.canvasEl.width,
              height: this.canvasEl.height
            });

            // 绘制人脸框
            faceapi.draw.drawDetections(this.canvasEl, resizedDetections);

            // 绘制人脸特征点
            faceapi.draw.drawFaceLandmarks(this.canvasEl, resizedDetections);
          }
        } catch (error) {
          console.error('人脸检测错误:', error);
        }
      }, 100);
    },

    /**
     * 开始采集人脸特征
     */
    startCapturing() {
      // 确保摄像头已启动且检测到人脸
      if (!this.cameraActive || !this.faceDetected) return;

      this.isCapturing = true;
      this.captureCount = 0;
      this.faceFeatures = [];

      // 清除之前的计时器
      if (this.captureTimer) {
        clearInterval(this.captureTimer);
      }

      // 设置采集计时器，每1秒采集一次
      this.captureTimer = setInterval(async () => {
        if (this.captureCount >= this.totalCaptures) {
          // 采集完成
          clearInterval(this.captureTimer);
          this.captureComplete = true;
          return;
        }

        try {
          // 检测到人脸才进行采集
          if (this.faceDetected) {
            // 使用SSD MobileNet进行人脸检测并提取特征
            const detections = await faceapi.detectAllFaces(this.videoEl)
              .withFaceLandmarks()
              .withFaceDescriptors();

            if (detections.length > 0) {
              // 取第一个检测到的人脸特征
              const descriptor = Array.from(detections[0].descriptor);
              this.faceFeatures.push(descriptor);
              this.captureCount++;

              // 播放采集音效或提示
              this.$message({
                message: `已采集第 ${this.captureCount} 组人脸特征`,
                type: 'success'
              });
            }
          }
        } catch (error) {
          console.error('特征采集错误:', error);
        }
      }, 1000);
    },

    /**
     * 提交人脸特征到后端
     */
    async submitFaceFeatures() {
      if (!this.captureComplete || this.isSubmitting) {
        return;
      }
      
      this.isSubmitting = true;
      this.errorMessage = '';
      this.successMessage = '';

      try {
        // 计算平均特征向量
        const averageFeature = this.calculateAverageFeature(this.faceFeatures);
        
        // 确保数据格式正确
        const processedFeature = Array.from(averageFeature).map(val => 
          typeof val === 'number' ? val : parseFloat(val));
        
        // 日志输出请求数据
        console.log('发送特征数据:');
        console.log('- 特征向量类型:', typeof processedFeature);
        console.log('- 特征向量是否数组:', Array.isArray(processedFeature));
        console.log('- 特征向量长度:', processedFeature.length);
        console.log('- 前5个元素:', processedFeature.slice(0, 5));
        // const token = window.sessionStorage.getItem("token");
        // 发送请求
        // const BACKEND_URL = 'http://localhost:8000'; // 确认此地址正确
        // const response = await axios.post(`${BACKEND_URL}/face/register`, {
        //   feature: processedFeature
        // }, {
        //   headers: {
        //     'Authorization': `Bearer ${this.token}`,
        //     'Content-Type': 'application/json'
        //   }
        // });
        const user = {
          user:this.currentUser.id,
          name:this.currentUser.username,
        }
        // 发送请求
        const response = await requestUtil.post('face/register', {
            feature: processedFeature,
            user:user
        });
        
        // 打印完整响应以进行调试
        console.log('服务器响应状态:', response.status);
        console.log('服务器响应数据:', response.data);
        
        // 处理响应 - 增加容错处理
        if (response.status >= 200 && response.status < 300) {
          // 成功响应
          if (response.data && response.data.code === 400) {
            // 服务器返回了业务逻辑错误
            this.errorMessage = response.data.message || '操作失败';
          } else {
            // 真正成功的情况
            this.successMessage = response.data.message || '人脸信息录入成功';
            this.resetCapturing();
          }
        } else {
          // 非成功HTTP状态
          this.errorMessage = '请求失败: ' + response.statusText;
        }
      } catch (error) {
        console.error('提交人脸特征时出错:', error);
        
        // 详细错误处理
        if (error.response) {
          // 服务器返回了错误状态码
          console.log('错误状态码:', error.response.status);
          console.log('错误响应数据:', error.response.data);
          
          let errorMsg = '服务器返回错误';
          if (error.response.data && error.response.data.message) {
            errorMsg += ': ' + error.response.data.message;
          } else {
            errorMsg += ` (${error.response.status})`;
          }
          this.errorMessage = errorMsg;
        } else if (error.request) {
          // 请求已发送但没有收到响应
          this.errorMessage = '服务器未响应，请检查网络连接';
        } else {
          // 发送请求时出错
          this.errorMessage = '请求错误: ' + error.message;
        }
      } finally {
        this.isSubmitting = false;
      }
    },

    /**
     * 计算多个特征向量的平均值
     * @param {Array} features 特征向量数组
     * @returns {Array} 平均特征向量
     */
    calculateAverageFeature(features) {
      if (features.length === 0) return [];

      // 假设所有特征向量长度相同
      const vectorLength = features[0].length;
      const result = new Array(vectorLength).fill(0);

      // 对所有特征向量求和
      for (const feature of features) {
        for (let i = 0; i < vectorLength; i++) {
          result[i] += feature[i];
        }
      }

      // 计算平均值
      for (let i = 0; i < vectorLength; i++) {
        result[i] /= features.length;
      }

      return result;
    },

    /**
     * 重置采集状态
     */
    resetCapturing() {
      this.isCapturing = false;
      this.captureComplete = false;
      this.captureCount = 0;
      this.faceFeatures = [];

      if (this.captureTimer) {
        clearInterval(this.captureTimer);
      }
    },

    /**
     * 清除所有计时器
     */
    clearTimers() {
      if (this.captureTimer) {
        clearInterval(this.captureTimer);
      }

      if (this.detectionTimer) {
        clearInterval(this.detectionTimer);
      }
    },

    /**
     * 完全重置组件状态
     */
    resetAll() {
      this.resetCapturing();
      this.errorMessage = '';
      this.successMessage = '';
    }
  }
}
</script>

<style scoped>
.face-recording-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.header-card {
  margin-bottom: 20px;
  text-align: center;
}

.header-card h2 {
  margin-top: 0;
  color: #409EFF;
}

.user-info {
  margin-top: 10px;
  font-weight: bold;
  color: #67C23A;
}

.video-card {
  margin-bottom: 20px;
}

.video-container {
  position: relative;
  width: 100%;
  height: 480px;
  background-color: #000;
  border-radius: 4px;
  overflow: hidden;
}

video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.canvas-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.detection-status {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: rgba(255, 73, 73, 0.8);
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.3s;
}

.detection-status.detected {
  background-color: rgba(103, 194, 58, 0.8);
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
}

.capture-progress {
  margin-top: 20px;
}

.progress-text {
  text-align: center;
  color: #409EFF;
  margin-top: 8px;
}

.el-alert {
  margin-top: 20px;
}
</style>