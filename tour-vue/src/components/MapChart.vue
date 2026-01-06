<template>
  <div ref="chartContainer" class="map-chart" style="width: 100%; height: 100%;"></div>
</template>

<script>
import * as echarts from 'echarts/core';
import { MapChart } from 'echarts/charts';
import { TitleComponent, TooltipComponent, VisualMapComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
import 'echarts-gl';

import ShanxiMap from "@/map/山西省.json"; // 确保路径正确

echarts.use([
  TitleComponent,
  TooltipComponent,
  VisualMapComponent,
  MapChart,
  CanvasRenderer
]);

export default {
  name: 'MapChart',
  data() {
    return {
      myChart: null,
    };
  },
  mounted() {
    this.initChart();
  },
  beforeDestroy() {
    if (this.myChart) {
      this.myChart.dispose(); // 销毁实例以释放资源
    }
  },
  methods: {
    initChart() {
      // 初始化 ECharts 实例
      this.myChart = echarts.init(this.$refs.chartContainer);

      // 注册山西地图
      echarts.registerMap('ShanxiMap', ShanxiMap);

      const option = {
        tooltip: {
          trigger: 'item',
        },
        visualMap: {
          min: 0,
          max: 20,
          left: 'right',
          top: 'bottom',
          text: ['高', '低'], // 文本
          calculable: true,
          inRange: {
            color: ['#2196F3', '#FFEB3B'] // 蓝色到米色
          }
        },
        series: [
          {
            type: 'map3D', // 使用 3D 地图
            map: 'ShanxiMap',
            data: [
              { name: '太原市', value: 13 },
              { name: '运城市', value: 12 },
              { name: '晋中市', value: 6 },
              { name: '大同市', value: 6 },
              { name: '忻州市', value: 5 },
              { name: '临汾市', value: 4 },
              { name: '长治市', value: 4 },
              { name: '晋城市', value: 3 },
              { name: '阳泉市', value: 3 },
              { name: '朔州市', value: 1 },
              { name: '吕梁市', value: 0 }
            ],
            itemStyle: {
              areaColor: '#1F75B8',
              borderColor: '#93eaf8',
            },
            label: {
              show: true, // 始终显示城市名称
              formatter: '{b}', // 使用城市名称
              textStyle: {
                color: '#FFFFFF', // 设置字体颜色
                fontSize: 12, // 设置字体大小
              },
            },
          }
        ]
      };

      // 设置图表选项
      this.myChart.setOption(option);

      // 添加点击事件
      this.myChart.on('click', function (params) {
        console.log(params); // 打印点击的信息
      });
    },
  }
};
</script>

<style scoped>
.map-chart {
  border-radius: 10px;
}
</style>