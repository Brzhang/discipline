<template>
  <el-row :gutter="40">
    <el-col :span="12" style="font-size:12px; width:50%" > 当前持仓
      <el-table height="900px" v-loading="loading" element-loading-text="别着急，重要的数据可以多等等" :data="positionlist" stripe border fit highlight-current-row style="width: 100%; font-size:12px;">
        <el-table-column align="center" label="序号" width="65px" type="index" />
        <el-table-column width="100px" align="center" label="代码" sortable header-align="center" prop="code" />
        <el-table-column width="100px" align="center" label="名称" header-align="center" prop="name" />
        <el-table-column width="150px" align="center" label="数量" header-align="center" prop="vol" />
        <el-table-column width="100px" align="center" label="买入价" header-align="center" prop="buyprice" />
        <el-table-column width="100px" align="center" label="现价" sortable header-align="center" prop="price" />
        <el-table-column width="100px" align="center" label="利润" sortable header-align="center" prop="profit" />
      </el-table>
    </el-col>
    <el-col :span="12" style="font-size:12px; width:50%" > 交易记录
      <el-table height="900px" v-loading="loading" element-loading-text="别着急，重要的数据可以多等等" :data="tradelist" stripe border fit highlight-current-row style="width: 100%; font-size:12px;">
        <el-table-column align="center" label="序号" width="65px" type="index" />
        <el-table-column width="100px" align="center" label="代码" sortable header-align="center" prop="code" />
        <el-table-column width="100px" align="center" label="名称" header-align="center" prop="name" />
        <el-table-column width="150px" align="center" label="数量" header-align="center" prop="vol" />
        <el-table-column width="100px" align="center" label="买入价" header-align="center" prop="buyprice" />
        <el-table-column width="100px" align="center" label="现价" sortable header-align="center" prop="price" />
        <el-table-column width="150px" align="center" label="交易时间" sortable header-align="center" prop="date" />
        <el-table-column width="100px" align="center" label="操作" header-align="center" prop="opt" />
        <!-- <el-table-column width="100px" align="center" label="单次利润" sortable header-align="center" prop="profit" /> -->
      </el-table>
    </el-col>
  </el-row>
</template>

<script>
import axios from 'axios'
import { baseUrl } from './'
export default {
  name: 'virtualAccount',
  data () {
    return {
      positionlist: [],
      tradelist: [],
      loading: false,
      kDialogVisible: false
    }
  },
  mounted () {
    this.getPositionList()
    this.getTradeList()
  },
  methods: {
    getPositionList () {
      this.loading = true
      var url = baseUrl + 'PositionList'
      axios.get(url)
        .then((res) => {
          this.positionlist = res.data
          this.loading = false
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.loading = false
        })
    },
    getTradeList () {
      this.loading = true
      var url = baseUrl + 'TradeList'
      axios.get(url)
        .then((res) => {
          this.tradelist = res.data
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
