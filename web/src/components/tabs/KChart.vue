<template>
   <div :id='kChartID' style="margin:0 auto; width=1500px; height=900px"></div>
</template>

<script>
import echarts from 'echarts'
export default {
  name: 'KChart',
  props: {
    kChartID: {
      type: String,
      default: 'k-chart'
    }
  },
  data () {
    return {
      data: '',
      kChart: null,
      stockName: '',
      kChartDivVisble: false
    }
  },
  methods: {
    showChart (name, data) {
      this.kChartDivVisble = true
      this.stockName = name
      this.data = data
      this.kChart = echarts.init(document.getElementById(this.kChartID))
      var option = {
        title: {
          text: this.stockName,
          textStyle: {
            fontSize: 16
          },
          x: 'center',
          y: 'top',
          textAlign: 'left'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        legend: {
          right: '30',
          data: this.data.lineNames
        },
        dataZoom: [{
            startValue: this.data.x[0]
        }, {
            type: 'inside'
        }],
        tooltip: {
            trigger: 'axis'
        },
        xAxis: {
          data: this.data.x
        },
        yAxis: { name: '价格' },
        series: [
          {
            type: 'line',
            name: this.data.lineNames[0],
            data: this.data.Ys[0]
          },
          {
            type: 'line',
            name: this.data.lineNames[1],
            data: this.data.Ys[1]
          },
          {
            type: 'line',
            name: this.data.lineNames[2],
            data: this.data.Ys[2]
          },
          {
            type: 'line',
            name: this.data.lineNames[3],
            data: this.data.Ys[3]
          },
          {
            type: 'line',
            name: this.data.lineNames[4],
            data: this.data.Ys[4]
          }
        ]
      }
      this.kChart.setOption(option)
    }
  }
}
</script>
