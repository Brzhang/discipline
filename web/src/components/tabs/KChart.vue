<template>
   <div :id='kChartID' style="margin:0 0 0 0; width=100%; height=100%"></div>
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
    makeSeries (chartType) {
      let series = []
      for (let i = 0; i < this.data.lineNames.length; i++) {
        if (i === 0 && chartType === 'MA') {
          series.push({
            type: 'candlestick',
            name: this.data.lineNames[0],
            data: this.data.Ys[0],
            itemStyle: {
              color: '#FD1050',
              color0: '#0CF49B',
              borderColor: '#FD1050',
              borderColor0: '#0CF49B'
            },
            markLine: {
              symbol: 'none',
              label: {
                position: 'end'
              },
              lineStyle: {
                normal: {
                  type: 'dotted',
                  color: 'rgb(0, 0, 255)'
                }
              },
              data: [{xAxis: this.data.x[this.data.x.length - 5], name: '5日抵扣', label: {formatter: '5日抵扣'}},
                {xAxis: this.data.x[this.data.x.length - 10], name: '10日抵扣', label: {formatter: '10日抵扣'}},
                {xAxis: this.data.x[this.data.x.length - 20], name: '20日抵扣', label: {formatter: '20日抵扣'}},
                {xAxis: this.data.x[this.data.x.length - 60], name: '60日抵扣', label: {formatter: '60日抵扣'}},
                {xAxis: this.data.x[this.data.x.length - 120], name: '120日抵扣', label: {formatter: '120日抵扣'}}]
            }
          })
        } else {
          series.push({
            type: 'line',
            name: this.data.lineNames[i],
            data: this.data.Ys[i]
          })
        }
      }
      return series
    },
    showChart (name, data, chartType) {
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
          left: '0',
          right: '0',
          bottom: '0',
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        legend: {
          right: '30',
          inactiveColor: '#777',
          data: this.data.lineNames
        },
        color: this.data.colors,
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
        series: this.makeSeries(chartType)
      }
      this.kChart.setOption(option)
    }
  }
}
</script>
