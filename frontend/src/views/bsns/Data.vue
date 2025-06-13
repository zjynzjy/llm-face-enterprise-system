<template>
  <div class="data-dashboard">
    <div v-if="loading" class="loading-overlay">
      <el-icon class="loading-icon"><Loading /></el-icon>
      数据加载中...
    </div>
    
    <div v-if="error" class="error-message">
      {{ error }}
      <el-button @click="fetchData">重试</el-button>
    </div>

    <div class="header">
      <div class="logo">{{ companyName }} 考勤系统</div>
      <div class="real-time">
        <span>当前时间: {{ new Date().toLocaleString() }}</span>
        <div class="stats">
          <div class="stat-item">
            <div class="label">在岗率</div>
            <div class="value">{{ attendanceRate }}%</div>
          </div>
          <div class="stat-item warning">
            <div class="label">异常考勤</div>
            <div class="value">{{ abnormalCount }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="main-content">
      <div class="left-panel">
        <div class="chart-container">
          <v-chart class="chart" :option="departmentOption" autoresize />
        </div>
      </div>

      <div class="right-panel">
        <div class="chart-container">
          <v-chart class="chart" :option="trendOption" autoresize />
        </div>
      </div>
    </div>

    <div class="footer">
      <div class="alert-list">
        <div class="alert-title">实时异常预警</div>
        <div class="alert-items">
          <div v-for="(alert, index) in alerts" :key="index" class="alert-item">
            [{{ alert.time }}] {{ alert.department }}: {{ alert.message }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import requestUtil from '@/util/request'

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
])

export default {
  components: { VChart },
  data() {
    return {
      loading: true,
      error: null,
      companyName: '公司',
      attendanceRate: 0,
      abnormalCount: 0,
      alerts: [],
      departmentOption: {
        title: { 
          text: '部门出勤率对比', 
          left: 'center',
          textStyle: { color: '#fff' }
        },
        tooltip: { trigger: 'axis' },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: { color: '#fff' }
        },
        yAxis: { 
          type: 'value', 
          max: 100,
          axisLabel: { color: '#fff' }
        },
        series: [{
          data: [],
          type: 'bar',
          itemStyle: { color: '#00F7F7' }
        }]
      },
      trendOption: {
        title: { 
          text: '出勤趋势分析', 
          left: 'center',
          textStyle: { color: '#fff' }
        },
        tooltip: { trigger: 'axis' },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: { color: '#fff' }
        },
        yAxis: {
          type: 'value',
          max: 100,
          axisLabel: { color: '#fff' }
        },
        series: [{
          data: [],
          type: 'line',
          smooth: true,
          itemStyle: { color: '#FF6347' }
        }]
      }
    }
  },
  mounted() {
    this.fetchData()
    this.timer = setInterval(this.fetchData, 60000)
  },
  beforeUnmount() {
    clearInterval(this.timer)
  },
  methods: {
    async fetchData() {
      try {
        const { data } = await requestUtil.get('datascreen/Attendance')
        
        this.attendanceRate = data.attendance_rate
        this.abnormalCount = data.abnormal_count
        this.alerts = data.alerts
        
        this.departmentOption = {
          ...this.departmentOption,
          xAxis: { ...this.departmentOption.xAxis, data: data.departments.map(d => d.name) },
          series: [{ ...this.departmentOption.series[0], data: data.departments.map(d => d.rate) }]
        }
        
        this.trendOption = {
          ...this.trendOption,
          xAxis: { ...this.trendOption.xAxis, data: data.trend_data.map(t => t.date) },
          series: [{ ...this.trendOption.series[0], data: data.trend_data.map(t => t.rate) }]
        }
        
        this.error = null
      } catch (error) {
        console.error('数据获取失败:', error)
        this.error = '数据加载失败，请稍后重试'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.loading-icon {
  font-size: 40px;
  margin-right: 10px;
  animation: rotate 2s linear infinite;
}

.error-message {
  padding: 20px;
  background: #ff000030;
  border-radius: 8px;
  margin: 20px;
  text-align: center;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.data-dashboard {
  background: #0A1A35;
  color: #fff;
  min-height: 100vh;
  height: 100%;
  overflow: hidden;  /* 修改为hidden避免出现双滚动条 */
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.main-content {
  margin-bottom: 20px;
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  min-height: 400px;  /* 新增最小高度保证内容区高度 */
}

.alert-items {
  height: calc(100vh - 650px);  /* 动态高度计算 */
  min-height: 150px;
  overflow-y: auto;
  padding-right: 10px;
}

/* 移除重复的.alert-list和.footer定义 */
.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #00F7F7;
}

.real-time {
  display: flex;
  align-items: center;
  gap: 30px;
}

.stats {
  display: flex;
  gap: 20px;
}

.stat-item {
  background: rgba(255,255,255,0.1);
  padding: 10px 20px;
  border-radius: 8px;
  text-align: center;
}

.stat-item.warning {
  background: rgba(255, 99, 71, 0.3);
}

.main-content {
  margin-bottom: 20px;
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.chart-container {
  background: rgba(255,255,255,0.05);
  border-radius: 12px;
  padding: 15px;
  height: 400px;
}

.footer {
  margin-top: 20px;
  margin-bottom: 20px
}

.alert-list {
  background: rgba(255,255,255,0.05);
  border-radius: 8px;
  padding: 15px;
  min-height: 150px
}

.alert-title {
  color: #FF6347;
  margin-bottom: 10px;
}

.alert-items {
  height: 280px;  /* 增加高度 */
  overflow-y: auto;
  padding-right: 10px;
  scrollbar-width: thin;  /* 添加自定义滚动条样式 */
  scrollbar-color: #FF6347 rgba(255,255,255,0.1);
}

.alert-items::-webkit-scrollbar {
  width: 6px;
}

.alert-items::-webkit-scrollbar-track {
  background: rgba(255,255,255,0.1);
  border-radius: 3px;
}

.alert-items::-webkit-scrollbar-thumb {
  background: #FF6347;
  border-radius: 3px;
}

.alert-item {
  padding: 12px 0;
  line-height: 1.4;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.alert-list {
  background: rgba(255,255,255,0.05);
  border-radius: 8px;
  padding: 20px;
  height: auto;
  min-height: 250px;
}

.footer {
  margin-top: 20px;
  margin-bottom: 20px;
  height: auto;
}
</style>