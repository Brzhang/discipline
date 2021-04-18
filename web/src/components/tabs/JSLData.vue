<template>
  <el-container style="border:1px solid #eee;">
    <el-table v-loading="loading" element-loading-text="别着急，重要的数据可以多等等" :data="list" stripe border fit highlight-current-row style="width: 95%; font-size:12px;">
      <el-table-column
        align="center"
        label="序号"
        width="65"
        type="index"
      />
    <!--代码，名称，价格，涨幅，成交额(万)，市值，PE TTM，PE温度，pb，pb温度，5年均股息率，股息率，静态股息率，
    最新年报ROE，5年均ROE，5年营收增长，5年利润增长，5年现金流增长，5年分红率增长，净利同比增长，有息负债率，行业名称
    'stock_id', 'stock_nm', 'price', 'increase_rt', 'volume', 'total_value','pe', 'pe_temperature', 'pb', 'pb_temperature','aft_dividend', 'dividend_rate', 'dividend_rate2',
    'roe', 'roe_average', 'revenue_average', 'profit_average','cashflow_average', 'dividend_rate_average', 'eps_growth_ttm', 'int_debt_rate','industry_nm'
    !-->
      <el-table-column width="50px" align="center" label="代码" header-align="center" prop="stock_id" />
      <el-table-column width="50px" align="center" label="名称" header-align="center" prop="stock_nm" />
      <el-table-column width="80px" align="center" label="价格" sortable header-align="center" prop="price" />
      <el-table-column width="100px" align="center" label="涨幅" sortable header-align="center" prop="increase_rt" />
      <el-table-column width="80px" align="center" label="成交额W" sortable header-align="center" prop="volume" />
      <el-table-column width="180px" align="center" label="市值" sortable header-align="center" prop="total_value" />
      <el-table-column width="100px" align="center" label="PE TTM" sortable header-align="center" prop="pe" />
      <el-table-column width="80px" align="center" label="PE温度" sortable header-align="center" prop="pe_temperature" />
      <el-table-column width="80px" align="center" label="PB" sortable header-align="center" prop="pb" />
      <el-table-column width="80px" align="center" label="PB温度" sortable header-align="center" prop="pb_temperature" />
      <el-table-column width="80px" align="center" label="5年均股息率" sortable header-align="center" prop="aft_dividend" />
      <el-table-column width="80px" align="center" label="股息率" sortable header-align="center" prop="dividend_rate" />
      <el-table-column width="80px" align="center" label="静态股息率" sortable header-align="center" prop="dividend_rate2" />
      <el-table-column width="100px" align="center" label="最新年报ROE" sortable header-align="center" prop="roe" />
      <el-table-column width="100px" align="center" label="5年均ROE" sortable header-align="center" prop="roe_average" />
      <el-table-column width="100px" align="center" label="5年营收增长" sortable header-align="center" prop="revenue_average" />
      <el-table-column width="100px" align="center" label="5年利润增长" sortable header-align="center" prop="profit_average" />
      <el-table-column width="100px" align="center" label="5年现金流增长" sortable header-align="center" prop="cashflow_average" />
      <el-table-column width="100px" align="center" label="5年分红率增长" sortable header-align="center" prop="dividend_rate_average" />
      <el-table-column width="100px" align="center" label="净利同比增长" sortable header-align="center" prop="eps_growth_ttm" />
      <el-table-column width="100px" align="center" label="有息负债" sortable header-align="center" prop="int_debt_rate" />
      <el-table-column width="100px" align="center" label="行业名称" sortable header-align="center" prop="industry_nm" />
    </el-table>
  </el-container>
</template>

<script>
import axios from 'axios'
export default {
  name: 'JSLData',
  data () {
    return {
      list: [],
      loading: false
    }
  },
  mounted () {
    this.getDataList()
  },
  methods: {
    getDataList () {
      this.loading = true
      var url = 'http://localhost:8089/JSLData'
      axios.get(url)
        .then((res) => {
          this.list = res.data
          this.loading = false
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.loading = false
        })
    }
  }
}
</script>
