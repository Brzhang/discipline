<template>
  <el-container style="border:0px solid #eee;">
    <el-table height="920px" ref="JSLDataTable" @sort-change="dataSorted" :cell-style="cellStyleBG" v-loading="loading" element-loading-text="别着急，重要的数据可以多等等"
    :data="list" stripe border fit highlight-current-row style="width: 100%; font-size:12px;">
      <el-table-column align="center" label="序号" width="45" type="index" />
    <!--代码，名称，价格，涨幅，成交额(万)，市值，PE TTM，PE温度，pb，pb温度，5年均股息率，股息率，静态股息率，
    最新年报ROE，5年均ROE，5年营收增长，5年利润增长，5年现金流增长，5年分红率增长，净利同比增长，有息负债率，行业名称
    'stock_id', 'stock_nm', 'price', 'increase_rt', 'volume', 'total_value','pe', 'pe_temperature', 'pb', 'pb_temperature','aft_dividend', 'dividend_rate', 'dividend_rate2',
    'roe', 'roe_average', 'revenue_average', 'profit_average','cashflow_average', 'dividend_rate_average', 'eps_growth_ttm', 'int_debt_rate','industry_nm'
    !-->
      <el-table-column width="65px" align="center" label="代码" header-align="center" prop="stock_id" />
      <el-table-column width="90px" align="center" label="名称" header-align="center" prop="stock_nm" />
      <el-table-column width="70px" align="center" label="价格" sortable header-align="center" prop="price" />
      <el-table-column width="70px" align="center" label="涨幅" sortable header-align="center" prop="increase_rt" />
      <el-table-column width="80px" align="center" label="成交额W" sortable header-align="center" prop="volume" />
      <el-table-column width="80px" align="center" label="市值" sortable header-align="center" prop="total_value" />
      <el-table-column width="80px" align="center" label="PE TTM" sortable header-align="center" prop="pe" />
      <el-table-column width="80px" align="center" label="PE温度" sortable header-align="center" prop="pe_temperature" />
      <el-table-column width="80px" align="center" label="PB" sortable header-align="center" prop="pb" />
      <el-table-column width="80px" align="center" label="PB温度" sortable header-align="center" prop="pb_temperature" />
      <el-table-column width="80px" align="center" label="5年均股息率" sortable header-align="center" prop="aft_dividend" />
      <el-table-column width="80px" align="center" label="股息率" sortable header-align="center" prop="dividend_rate" />
      <el-table-column width="80px" align="center" label="静态股息率" sortable header-align="center" prop="dividend_rate2" />
      <el-table-column width="80px" align="center" label="最新年报ROE" sortable header-align="center" prop="roe" />
      <el-table-column width="80px" align="center" label="5年均ROE" sortable header-align="center" prop="roe_average" />
      <el-table-column width="80px" align="center" label="5年营收增长" sortable header-align="center" prop="revenue_average" />
      <el-table-column width="80px" align="center" label="5年利润增长" sortable header-align="center" prop="profit_average" />
      <el-table-column width="80px" align="center" label="5年现金流增长" sortable header-align="center" prop="cashflow_average" />
      <el-table-column width="80px" align="center" label="5年分红率增长" sortable header-align="center" prop="dividend_rate_average" />
      <el-table-column width="80px" align="center" label="净利同比增长" sortable header-align="center" prop="eps_growth_ttm" />
      <el-table-column width="80px" align="center" label="有息负债" sortable header-align="center" prop="int_debt_rate" />
      <el-table-column width="110px" align="center" label="行业名称" sortable header-align="center" prop="industry_nm" />
    </el-table>
  </el-container>
</template>

<script>
import axios from 'axios'
import { baseUrl } from './'
export default {
  name: 'JSLData',
  data () {
    return {
      list: [],
      sortedList: [],
      loading: false
    }
  },
  mounted () {
    this.getDataList()
  },
  methods: {
    getDataList () {
      this.loading = true
      var url = baseUrl + 'JSLData'
      axios.get(url)
        .then((res) => {
          this.list = res.data
          this.sortedList = this.list
          this.loading = false
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.loading = false
        })
    },
    setTemperatureGBColor (data) {
      if (data < 10) {
        return 'background-color: rgb(51,255,0)'
      } else if (data < 20) {
        return 'background-color: rgb(102, 255, 0)'
      } else if (data < 30) {
        return 'background-color: rgb(153, 255, 0)'
      } else if (data < 40) {
        return 'background-color: rgb(204, 255, 0)'
      } else if (data < 50) {
        return 'background-color: rgb(255, 255, 0)'
      } else if (data < 60) {
        return 'background-color: rgb(255, 204, 0)'
      } else if (data < 70) {
        return 'background-color: rgb(255, 154, 0)'
      } else if (data < 80) {
        return 'background-color: rgb(255, 103, 0)'
      } else if (data < 90) {
        return 'background-color: rgb(255, 51, 0)'
      } else {
        return 'background-color: rgb(255, 0, 0)'
      }
    },
    cellStyleBG ({row, column, rowIndex, columnIndex}) {
      if (columnIndex === 8) {
        return this.setTemperatureGBColor(this.sortedList[rowIndex].pe_temperature)
      }
      if (columnIndex === 10) {
        return this.setTemperatureGBColor(this.sortedList[rowIndex].pb_temperature)
      }
    },
    dataSorted ({column, prop, order}) {
      this.sortedList = this.$refs.JSLDataTable.tableData
    }
  }
}
</script>
