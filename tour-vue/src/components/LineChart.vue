<template>
  <div>
    <v-chart :option="chartOptions" style="width: 100%; height: 300px;"></v-chart>
  </div>
</template>

<script>
export default {
  name: 'TouristSpotRanking',
  data() {
    return {
      chartOptions: {
        title: {
          text: '各地营业额排名',
        },
        tooltip: {
          trigger: 'axis',
        },
        legend: {
          data: ['营业额'],
        },
        xAxis: {
          type: 'category',
          data: ['临汾', '吕梁', '大同', '太原', '忻州', '晋中', '晋城', '朔州', '运城', '长治', '阳泉'],
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            name: '营业额',
            type: 'line',
            data: [141094, 7720, 80000, 241220, 106190, 211290, 185482, 44000, 206575, 69250, 9552],
          },
        ],
      },
    };
  },
};
</script>

<style scoped>
/* 添加一些样式使图表看起来更好 */
</style>