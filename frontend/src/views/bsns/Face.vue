<template>
  <div class="face-check-container">
    <el-card class="video-card">
      <!-- 视频区域 -->
      <div class="video-wrapper">
        <video ref="videoEl" autoplay muted playsinline></video>
        <canvas ref="canvasEl" class="overlay-canvas"></canvas>
        
        <div class="status-indicator" :class="detectionStatus">
          <i :class="statusIcon"></i>
          {{ statusText }}
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button 
          type="primary" 
          :loading="isProcessing"
          @click="handleCheckIn">
          {{ isProcessing ? '正在验证...' : '人脸打卡' }}
        </el-button>
        
        <el-button @click="toggleCamera">
          {{ cameraActive ? '关闭摄像头' : '开启摄像头' }}
        </el-button>
      </div>

      <!-- 考勤结果 -->
      <div v-if="lastResult" class="result-panel">
        <el-alert 
          :title="resultTitle"
          :type="lastResult.success ? 'success' : 'error'"
          :closable="false"
          show-icon>
          <p>相似度：{{ (lastResult.similarity * 100).toFixed(1) }}%</p>
          <p>位置：{{ locationStatus }}</p>
          <p>时间：{{ new Date().toLocaleString() }}</p>
        </el-alert>
      </div>
    </el-card>
  </div>
</template>

<script>
import * as faceapi from 'face-api.js';
import requestUtil from '@/util/request';
import { ElMessage } from 'element-plus';  // 添加这行

export default {
  
  data() {
    const currentUser=JSON.parse(sessionStorage.getItem("currentUser"))
    return {
      // 用户信息
      currentUser: currentUser, // 添加到返回对象中
      // 视频控制
      videoEl: null,
      canvasEl: null,
      stream: null,
      cameraActive: false,
      
      // 识别状态
      isProcessing: false,
      lastResult: null,
      faceDescriptor: null,
      
      // 定位信息
      geoLocation: null,
      locationError: null,
      
      // 设备信息
      deviceInfo: {
        userAgent: navigator.userAgent,
        platform: navigator.platform
      }
    };
  },

  computed: {
    detectionStatus() {
      if (!this.cameraActive) return 'disabled';
      return this.faceDescriptor ? 'detected' : 'searching';
    },
    statusIcon() {
      return {
        'disabled': 'el-icon-video-camera-solid',
        'searching': 'el-icon-loading',
        'detected': 'el-icon-user-solid'
      }[this.detectionStatus];
    },
    statusText() {
      return {
        'disabled': '摄像头未启动',
        'searching': '正在检测人脸...',
        'detected': '人脸识别就绪'
      }[this.detectionStatus];
    },
    resultTitle() {
      return this.lastResult && this.lastResult.success ? '打卡成功' : '打卡失败';
    },
    locationStatus() {
      if (this.geoLocation) {
        return `纬度: ${this.geoLocation.lat.toFixed(4)}, 经度: ${this.geoLocation.lng.toFixed(4)}`;
      } else if (this.locationError) {
        return `定位错误: ${this.locationError}`;
      } else {
        return '定位中...';
      }
    }
  },

  mounted() {
    this.initialize();
  },

  methods: {
    async initialize() {
      await this.loadModels();
      this.setupElements();
      this.getLocation();
    },

    async loadModels() {
      try {
        const MODEL_URL = 'https://cdn.jsdelivr.net/npm/@vladmandic/face-api/model';
        console.log('开始加载模型...');
        
        const loadingMessage = ElMessage({
          message: '正在加载人脸识别模型...',
          duration: 0,
          type: 'info'
        });

        await Promise.all([
          faceapi.nets.ssdMobilenetv1.loadFromUri(MODEL_URL),//SSD MobileNet V1是一种用于对象检测的深度学习模型，在这里用于检测视频流中的人脸。
          faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),//这是加载面部标志点检测模型的Promise。
          faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL)//这是加载面部识别模型的Promise,该模型用于生成面部特征描述符，以便进行面部识别和匹配。
        ]);

        loadingMessage.close();
        ElMessage.success('模型加载成功');
        console.log('模型加载成功');
      } catch (error) {
        console.error('模型加载失败:', error);
        ElMessage.error({
          message: '人脸识别模型加载失败，请检查网络连接后刷新页面重试',
          duration: 5000
        });
      }
    },
    setupElements() {
      // 获取 video 与 canvas 元素
      this.videoEl = this.$refs.videoEl;
      this.canvasEl = this.$refs.canvasEl;
    },

    async toggleCamera() {
      if (this.cameraActive) {
        this.stopCamera();
      } else {
        await this.startCamera();
        this.startDetection();
      }
    },

    async startCamera() {
      try {
        this.stream = await navigator.mediaDevices.getUserMedia({
          video: { width: 640, height: 480 }
        });
        this.videoEl.srcObject = this.stream;
        
        // 等待视频加载完成
        await new Promise(resolve => {
          this.videoEl.onloadedmetadata = () => {
            resolve();
          };
        });
        
        this.cameraActive = true;
        ElMessage.success('摄像头启动成功');
      } catch (error) {
        console.error('开启摄像头失败:', error);
        ElMessage.error('摄像头启动失败，请检查摄像头权限');
      }
    },

    stopCamera() {
      if (this.stream) {
        this.stream.getTracks().forEach(track => track.stop());
      }
      this.cameraActive = false;
      this.faceDescriptor = null;
    },

    async startDetection() {
      const detectFrame = async () => {
        if (!this.cameraActive) return;
        
        try {  // 添加错误处理
          const detection = await faceapi
            .detectSingleFace(this.videoEl)
            .withFaceLandmarks()
            .withFaceDescriptor();
    
          // 将检测结果存储到 faceDescriptor 中
          this.faceDescriptor = detection ? detection.descriptor : null;
          
          // 只有在摄像头激活时继续检测
          if (this.cameraActive) {
            requestAnimationFrame(detectFrame);
          }
        } catch (error) {
          console.error('人脸检测错误:', error);
          ElMessage.warning('人脸检测出现问题，请刷新页面重试');
          this.stopCamera();
        }
      };
      detectFrame();
    },

    formatLocation() {
      // 根据获取的地理位置信息格式化为 "纬度,经度" 字符串，
      // 如果后端需要 "经度,纬度"，请调整此处的顺序
      if (this.geoLocation) {
        return `${this.geoLocation.lat},${this.geoLocation.lng}`;
      }
      return '';
    },

    async handleCheckIn() {
      if (!this.faceDescriptor) {
        ElMessage.warning('请等待人脸检测完成');
        return;
      }

      if (!this.geoLocation) {
        ElMessage.warning('正在获取位置信息，请稍候');
        return;
      }
      
      this.isProcessing = true;
      
      try {
        const payload = {
          feature: Array.from(this.faceDescriptor),
          location: this.formatLocation(),
          accuracy: this.geoLocation?.accuracy || 0,//accuracy 为 10 表示定位精度在 10 米范围内
          device_info: this.deviceInfo,
          user:this.currentUser.id,
        };
    
        console.log('发送打卡数据:', payload); // 添加日志
        const response = await requestUtil.post('face/verify', payload);
        console.log('服务器响应:', response); // 添加日志
        
        if (response.data.code === 200) {
          this.lastResult = {
            success: true,
            similarity: response.data.similarity || 0,
            message: response.data.message || '打卡成功'
          };
          ElMessage.success('打卡成功');
        } else {
          this.lastResult = {
            success: false,
            similarity: response.data.similarity || 0,
            message: response.data.message || '打卡失败'
          };
          ElMessage.error(response.data.message || '打卡失败');
        }
        
        this.$emit('check-complete', this.lastResult);
      } catch (error) {
        console.error('打卡失败:', error);
        this.lastResult = {
          success: false,
          similarity: 0,
          message: '打卡失败，请稍后重试'
        };
        ElMessage.error('打卡失败，请稍后重试');
      } finally {
        this.isProcessing = false;
      }
    },

    getLocation() {
      const options = {
        enableHighAccuracy: true,  // 改为true以获取更精确的位置
        timeout: 15000,           // 增加超时时间
        maximumAge: 0            // 不使用缓存
      };

      // 使用默认位置作为最终备用方案
      const useDefaultLocation = () => {
        this.geoLocation = {
          lat: 39.9042,  // 北京市中心坐标
          lng: 116.4074,
          accuracy: 10000
        };
        this.locationError = '使用默认位置';
        console.log('使用默认位置:', this.geoLocation);
        ElMessage.warning('无法获取精确位置，使用默认位置');
      };

      // 尝试IP定位
      const tryIpLocation = async () => {
        try {
          ElMessage.info('正在通过IP获取位置...');
          const response = await fetch('https://ipinfo.io/json?token=ce3a89ea32cb79');
          const data = await response.json();
          if (data && data.loc) {
            const [lat, lng] = data.loc.split(',').map(parseFloat);
            this.geoLocation = { lat, lng, accuracy: 5000 };
            console.log('IP定位成功:', this.geoLocation);
            ElMessage.success('位置获取成功');
          } else {
            throw new Error('IP定位返回数据无效');
          }
        } catch (error) {
          console.error('IP定位失败:', error);
          useDefaultLocation();
        }
      };

      // 尝试浏览器定位
      navigator.geolocation.getCurrentPosition(
        position => {
          this.geoLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
            accuracy: position.coords.accuracy
          };
          console.log('浏览器定位成功:', this.geoLocation);
          ElMessage.success('位置获取成功');
        },
        error => {
          console.error('浏览器定位错误:', error);
          ElMessage.warning('浏览器定位失败，尝试备用方案');
          tryIpLocation();
        },
        options
      );
    }
  }
};
</script>

<style scoped>
.face-check-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.video-card {
  padding: 20px;
}

.video-wrapper {
  position: relative;
  width: 640px;
  height: 480px;
  margin: 0 auto;
  background: #000;
}

video {
  width: 100%;
  height: 100%;
}

.overlay-canvas {
  position: absolute;
  top: 0;
  left: 0;
}

.status-indicator {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 5px 10px;
  color: #fff;
  background-color: rgba(0, 0, 0, 0.6);
  border-radius: 4px;
}

.action-buttons {
  margin-top: 15px;
  display: flex;
  justify-content: space-around;
}

.result-panel {
  margin-top: 20px;
}
</style>
