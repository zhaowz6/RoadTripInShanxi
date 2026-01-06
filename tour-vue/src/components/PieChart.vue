<template>
  <div>
    <v-chart :option="chartOptions" style="width: 100%; height: 400px;"></v-chart>
  </div>
</template>

<script>
export default {
  name: 'PieChart',
  data() {
    return {
      chartOptions: {
        title: {
          text: '地区数量分布',
          left: 'center', // 标题居中
          textStyle: {
            fontSize: 20,
            fontWeight: 'bold',
            color: '#333', // 标题颜色
          },
        },
        tooltip: {
          trigger: 'item',
        },
        series: [{
          type: 'pie',
          radius: ['40%', '70%'], // 内外半径，形成环形饼图
          data: [
            { name: '太原', value: 13 },
            { name: '运城', value: 12 },
            { name: '晋中', value: 6 },
            { name: '大同', value: 6 },
            { name: '忻州', value: 5 },
            { name: '临汾', value: 4 },
            { name: '长治', value: 4 },
            { name: '晋城', value: 3 },
            { name: '阳泉', value: 3 },
            { name: '朔州', value: 3 },
            { name: '吕梁', value: 0 }
          ],
          itemStyle: {
            borderColor: '#fff', // 边框颜色
            borderWidth: 2, // 边框宽度
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)', // 高亮时的阴影效果
            },
          },
          color: [
            '#B2C3D3', '#A4C8E1', '#E1B2C3', '#C8D3E1', '#D3E1B2',
            '#C4B3D3', '#D3C4B3', '#B3D3C4', '#D3C8B3', '#B3C4D3',
            '#C4D3B3', '#E1D3B2'
          ],
        }],
      },
    };
  },
};
</script>

<style scoped>
/* 添加一些样式使图表看起来更好 */
</style>