<template>
  <div>
    <el-row :gutter="20">
      <!-- Top Row with Three Charts -->
      <el-col :span="8">
        <div class="chart" style="height: 400px;"> <!-- Top Left Chart -->
          <pie-chart />
        </div>
      </el-col>
      <el-col :span="8">
        <div class="chart" style="height: 400px;"> <!-- Top Center Chart -->
          <map-chart />
        </div>
      </el-col>
      <el-col :span="8">
        <div class="chart" style="height: 400px;"> <!-- Top Right Chart -->
          <bar-chart />
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <!-- Bottom Row with Two Charts -->
      <el-col :span="12">
        <div class="chart" style="height: 300px;"> <!-- Bottom Left Chart -->
          <line-chart />
        </div>
      </el-col>
      <el-col :span="12">
        <div class="chart" style="height: 300px;"> <!-- Bottom Right Chart -->
          <line-chart2 />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import LineChart from "@/components/LineChart";
import BarChart from "@/components/BarChart";
import PieChart from "@/components/PieChart";
import MapChart from "@/components/MapChart";
import LineChart2 from "@/components/LineChart2";

export default {
  name: 'Dashboard',
  components: {
    LineChart,
    BarChart,
    PieChart,
    MapChart,
    LineChart2
  }
};
</script>

<style scoped>
.dashboard {
  background-image: url('../assets/wxb.png'); /* 替换为您的图片路径 */
  background-size: cover; /* 确保背景图充满容器 */
  background-position: center; /* 居中对齐 */
  min-height: 100vh; /* 让背景覆盖整个视口高度 */
  padding: 20px; /* 添加内边距以避免内容紧贴边缘 */
}
.chart {
  //display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  border-radius: 10px;
  transition: transform 0.3s; /* 添加动画效果 */
  //background-color: rgba(0, 0, 0, 0.5); /* 半透明背景色，以便更好地融合图片 */

}

.chart:hover {
  transform: translateY(-5px); /* 鼠标悬停时的效果 */
}

/* 确保在小屏幕上也具有良好的布局 */
@media (max-width: 768px) {
  .chart {
    height: 200px; /* 较小屏幕时设置高度 */
  }
}
</style>