<template>
  <el-container style="border:1px solid #eee;" direction="vertical">
    <el-dialog
      :visible.sync="kDialogVisible"
      center
      trigger="manual"
      top=0
      height="100%"
      width="100%"
    >
      <KChart ref="KChartDailog" style="height:900px; width:1600px" />
    </el-dialog>
    <el-row>
      <el-col :span="24">
        <!-- 'price_dt', 'median_pb', 'median_pb_temperature', 'median_pe', 'median_pe_temperature', 'stock_count', 'IPO_count', 'st_count', 'index_point', 'date' -->
        <el-table v-loading="Aloading" element-loading-text="别着急，重要的数据可以多等等" :data="totalA" stripe border fit highlight-current-row style="width: 100%; font-size:12px;">
          <el-table-column align="center" label="序号"  width="45" type="index" />
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
        <el-table height="920" :row-class-name="tableRowClassName" :cell-style="cellStyleBG" v-loading="loading" element-loading-text="别着急，重要的数据可以多等等"
        ref="PETable" @sort-change="dataSorted" :data="industryValue" border fit highlight-current-row style="width: 100%; font-size:12px;">
          <el-table-column align="center" label="序号" width="45" type="index" />
          <el-table-column width="130px" align="center" label="行业代码" header-align="center" prop="industry_id" />
          <el-table-column width="240px" align="center" label="行业名称" header-align="center" prop="industry_name" />
          <el-table-column width="80px" align="center" label="PE" sortable header-align="center" prop="pe" />
          <el-table-column width="120px" align="center" label="PE温度" sortable header-align="center" prop="pe_temperature" />
          <el-table-column width="90px" align="center" label="股票数" sortable header-align="center" prop="stock_num" />
          <el-table-column width="110px" align="center" label="亏损股票数" sortable header-align="center" prop="lost_num" />
          <el-table-column width="900px" align="center" label="股票(中证800)" header-align="center" prop="stocks" />
          <el-table-column label="">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleView(scope.row.industry_id)">看图</el-button>
          </template>
        </el-table-column>
        </el-table>
      </el-col>
    </el-row>
  </el-container>
</template>

<script>
import axios from 'axios'
import { baseUrl } from './'
import KChart from './KChart'
export default {
  name: 'ConvertBond',
  components: {KChart},
  data () {
    return {
      totalA: [],
      industryValue: [],
      sortedIndustryValue: [],
      loading: false,
      Aloading: false,
      kDialogVisible: false
    }
  },
  mounted () {
    this.getTotalAValue()
    this.getDataList()
  },
  methods: {
    getTotalAValue () {
      this.Aloading = true
      var url = baseUrl + 'JSLTemperature'
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
      var url = baseUrl + 'IndustryPE'
      axios.get(url)
        .then((res) => {
          this.industryValue = res.data.result
          this.sortedIndustryValue = this.industryValue
          this.loading = false
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.loading = false
        })
    },
    drawPELines (hycode, name) {
      this.loading = true
      var url = baseUrl + 'IndustryPELinesData'
      axios.get(url, {
        params: {
          code: hycode
        }
      })
        .then((res) => {
          this.loading = false
          this.$refs.KChartDailog.showChart(hycode + '_' + name, res.data.values)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.loading = false
        })
    },
    handleView (code) {
      // show echart dialog
      for (let index = 0; index < this.industryValue.length; index++) {
        if (this.industryValue[index].industry_id === code) {
          this.kDialogVisible = true
          this.drawPELines(code, code + this.industryValue[index].industry_name)
          return
        }
      }
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
    tableRowClassName ({row, rowIndex}) {
      if (this.sortedIndustryValue[rowIndex].pe_temperature < 10) {
        // return 'info-row'
      }
      return ''
    },
    cellStyleBG ({row, column, rowIndex, columnIndex}) {
      if (columnIndex === 4 && this.sortedIndustryValue[rowIndex].pe !== 0) {
        return this.setTemperatureGBColor(this.sortedIndustryValue[rowIndex].pe_temperature)
      }
    },
    dataSorted ({column, prop, order}) {
      this.sortedIndustryValue = this.$refs.PETable.tableData
    }
  }
}
</script>
<style>
.el-table .info-row {
  background-color: green;
}
</style>
