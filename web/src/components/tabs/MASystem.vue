<template>
  <el-container style="border:0px solid #eee;" direction="vertical">
    <el-dialog :visible.sync="kDialogVisible" center trigger="manual" top=0 height="100%" width="100%">
      <KChart ref="KChartDailog" style="height:900px; width:1600px" />
    </el-dialog>
    <el-row>
      <div style="font-size:11px">策略：收盘价高于20日均线，20、60多头排列，5、10多头排列预上穿20日均线。行业估值低于25历史百分位</div>
    </el-row>
    <el-row>
      <el-table height="920px" v-loading="loading" element-loading-text="别着急，重要的数据可以多等等" :data="list" stripe border fit highlight-current-row style="width: 100%; font-size:12px;">
        <el-table-column align="center" label="序号" width="65" type="index" />
        <el-table-column width="50px" align="center" label="操作" header-align="center" prop="opt" />
        <el-table-column width="50px" align="center" label="仓位" header-align="center" prop="vol" />
        <el-table-column width="80px" align="center" label="代码" sortable header-align="center" prop="code" />
        <el-table-column width="100px" align="center" label="名称" header-align="center" prop="name" />
        <el-table-column width="80px" align="center" label="收盘价" header-align="center" prop="price" />
        <el-table-column width="180px" align="center" label="行业" sortable header-align="center" prop="HY" />
        <el-table-column width="100px" align="center" label="行业PE" sortable header-align="center" prop="HYPE" />
        <el-table-column width="100px" align="center" label="行业温度" sortable header-align="center" prop="HYPETemperature" />
        <el-table-column width="100px" align="center" label="动态PE" sortable header-align="center" prop="dynamicPE" />
        <el-table-column width="80px" align="center" label="PE" sortable header-align="center" prop="PE" />
        <el-table-column width="80px" align="center" label="PB" sortable header-align="center" prop="PB" />
        <el-table-column width="80px" align="center" label="MA5抵扣" header-align="center" prop="5Cost" />
        <el-table-column width="80px" align="center" label="MA10抵扣" header-align="center" prop="10Cost" />
        <el-table-column width="80px" align="center" label="MA20抵扣" header-align="center" prop="20Cost" />
        <el-table-column width="80px" align="center" label="MA60抵扣" header-align="center" prop="60Cost" />
        <el-table-column width="100px" align="center" label="MA120抵扣" header-align="center" prop="120Cost" />
        <el-table-column label="">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleView(scope.row.code)">看图</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-row>
  </el-container>
</template>

<script>
import axios from 'axios'
import { baseUrl } from './'
import KChart from './KChart'
export default {
  name: 'MASystem',
  components: {KChart},
  data () {
    return {
      list: [],
      loading: false,
      kDialogVisible: false
    }
  },
  mounted () {
    this.getDataList()
  },
  methods: {
    getDataList () {
      this.loading = true
      var url = baseUrl + 'MASystem'
      axios.get(url)
        .then((res) => {
          this.list = res.data.result
          this.loading = false
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.loading = false
        })
    },
    handleView (code) {
      // show echart dialog
      for (let index = 0; index < this.list.length; index++) {
        if (this.list[index].code === code) {
          this.kDialogVisible = true
          this.$refs.KChartDailog.showChart(this.list[index].code + ' - ' + this.list[index].name, this.list[index].values, 'MA')
          return
        }
      }
    }
  }
}
</script>
