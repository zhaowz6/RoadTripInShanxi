<template>
  <div>
    <v-chart :option="chartOptions" style="width: 100%; height: 300px;"></v-chart>
  </div>
</template>

<script>
export default {
  name: 'LineChart2',
  data() {
    return {
      chartOptions: {
        title: {
          text: '各地区门票价格',
        },
        tooltip: {
          trigger: 'axis',
        },
        legend: {
          data: ['门票价格'],
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
            name: '门票价格',
            type: 'line',
            data: [327.4, 64.7, 178, 558.8, 216.6, 436, 394.3, 87.9, 727.2, 145, 19.9],
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