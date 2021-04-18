<template>
  <el-container style="border:1px solid #eee;" direction="vertical">
    <el-row>
      <el-col :span="24">
        <!-- 'price_dt', 'median_pb', 'median_pb_temperature', 'median_pe', 'median_pe_temperature', 'stock_count', 'IPO_count', 'st_count', 'index_point', 'date' -->
        <el-table v-loading="Aloading" element-loading-text="别着急，重要的数据可以多等等" :data="totalA" stripe border fit highlight-current-row style="width: 95%; font-size:12px;">
          <el-table-column align="center" label="序号"  width="65" type="index" />
          <el-table-column width="150px" align="center" label="日期" header-align="center" prop="date" />
          <el-table-column width="150px" align="center" label="PB中位数" sortable header-align="center" prop="median_pb" />
          <el-table-column width="180px" align="center" label="PB中位数温度" sortable header-align="center" prop="median_pb_temperature" />
          <el-table-column width="180px" align="center" label="PE中位数" sortable header-align="center" prop="median_pe" />
          <el-table-column width="180px" align="center" label="PE中位数温度" header-align="center" prop="median_pe_temperature" />
          <el-table-column width="180px" align="center" label="股票数量" sortable header-align="center" prop="stock_count" />
          <el-table-column width="100px" align="center" label="IPO数量" sortable header-align="center" prop="IPO_count" />
          <el-table-column width="100px" align="center" label="ST数量" sortable header-align="center" prop="st_count" />
          <el-table-column width="80px" align="center" label="指数" sortable header-align="center" prop="index_point" />
        </el-table>
      </el-col>
    </el-row>
    <br/>
    <el-row>
      <el-col :span="24">
        <el-table v-loading="loading" element-loading-text="别着急，重要的数据可以多等等" :data="industryValue" stripe border fit highlight-current-row style="width: 95%; font-size:12px;">
          <el-table-column align="center" label="序号" width="65" type="index" />
          <el-table-column width="150px" align="center" label="行业代码" header-align="center" prop="industry_id" />
          <el-table-column width="250px" align="center" label="行业名称" header-align="center" prop="industry_name" />
          <el-table-column width="80px" align="center" label="PE" sortable header-align="center" prop="pe" />
          <el-table-column width="180px" align="center" label="PE温度" sortable header-align="center" prop="pe_temperature" />
          <el-table-column width="100px" align="center" label="股票数" sortable header-align="center" prop="stock_num" />
          <el-table-column width="120px" align="center" label="亏损股票数" sortable header-align="center" prop="lost_num" />
          <el-table-column width="600px" align="center" label="股票(中证800)" header-align="center" prop="stocks" />
        </el-table>
      </el-col>
    </el-row>
  </el-container>
</template>

<script>
import axios from 'axios'
export default {
  name: 'ConvertBond',
  data () {
    return {
      totalA: [],
      industryValue: [],
      loading: false,
      Aloading: false
    }
  },
  mounted () {
    this.getTotalAValue()
    this.getDataList()
  },
  methods: {
    getTotalAValue () {
      this.Aloading = true
      var url = 'http://localhost:8089/JSLTemperature'
      axios.get(url)
        .then((res) => {
          this.totalA = res.data
          this.Aloading = false
        })
        .catch((error) => {
          console.error(error)
          this.Aloading = false
        })
    },
    getDataList () {
      this.loading = true
      var url = 'http://localhost:8089/IndustryPE'
      axios.get(url)
        .then((res) => {
          this.industryValue = res.data.result
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
