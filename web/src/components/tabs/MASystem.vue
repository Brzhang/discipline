<template>
  <el-container style="border:1px solid #eee;">
    <el-popover
      placement="top-start"
      title="K 线图"
      v-model="kDialogVisible"
      center
      trigger="manual"
      height="100%"
      width="100%"
    >
      <el-button type="primary" size="mini" plain @click="kDialogVisible=false">X</el-button>
      <KChart ref="KChartDailog" style="height:900px; width:1500px" />
    </el-popover>
    <el-table v-loading="loading" element-loading-text="别着急，重要的数据可以多等等" :data="list" stripe border fit highlight-current-row style="width: 95%; font-size:12px;">
      <el-table-column
        align="center"
        label="序号"
        width="65"
        type="index"
      />
      <el-table-column width="50px" align="center" label="操作" header-align="center" prop="opt" />
      <el-table-column width="50px" align="center" label="仓位" header-align="center" prop="vol" />
      <el-table-column width="80px" align="center" label="代码" sortable header-align="center" prop="code" />
      <el-table-column width="100px" align="center" label="名称" header-align="center" prop="name" />
      <el-table-column width="80px" align="center" label="收盘价" header-align="center" prop="price" />
      <el-table-column width="180px" align="center" label="行业" sortable header-align="center" prop="HY" />
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
          <el-button
            size="mini"
            @click="handleView(scope.row.code)">看图</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-container>
</template>

<script>
import axios from 'axios'
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
      var url = 'http://localhost:8089/MASystem'
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
          this.$refs.KChartDailog.showChart(this.list[index].code + this.list[index].name, this.list[index].values)
          return
        }
      }
    }
  }
}
</script>
