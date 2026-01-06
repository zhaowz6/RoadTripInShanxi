<template>
  <div>
    <v-chart :option="chartOptions" style="width: 100%; height: 350px;"></v-chart>
  </div>
</template>

<script>
export default {
  name: 'TouristSpotRating',
  data() {
    return {
      chartOptions: {
        title: {
          text: '评分Top旅游景点门票',
        },
        tooltip: {
          trigger: 'item',
        },
        xAxis: {
          type: 'category',
          data: [
            '关帝祖庙',
            '望仙大峡谷',
            '新绛县绛州景区',
            '闻喜幸福林场',
            '太行山',
            '云风石窟',

          ],
          axisLabel: {
            rotate: 45, // 旋转横坐标标签
            interval: 0, // 每个标签都显示
            fontSize: 12, // 字体大小
          },
        },
        yAxis: {
          type: 'value',
          max: 250, // 根据数据最大值调整Y轴
        },
        series: [
          {
            name: 'Price',
            type: 'bar', // 改为点图
            data: [
              { value: 238, name: '关帝祖庙' },
              { value: 128, name: '望仙大峡谷' },
              { value: 128, name: '新绛县绛州景区' },
              { value: 128, name: '闻喜幸福林场' },
              { value: 120, name: '太行山' },
              { value: 115, name: '云风石窟' },

            ],
            itemStyle: {
              color: '#A4C8E1',
            },
            symbolSize: function (value) { // 根据价格动态设置点的大小
              return value[0] / 10; // 调整比例使点大小合适
            },
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