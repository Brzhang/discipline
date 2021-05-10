<template>
  <el-container style="border:0px solid #eee;">
    <el-table height="920px" v-loading="loading" element-loading-text="别着急，重要的数据可以多等等" :data="list" stripe border fit highlight-current-row style="width: 100%; font-size:12px;">
      <el-table-column align="center" label="序号" width="65px" type="index" />
      <el-table-column width="80px" align="center" label="代码" sortable header-align="center" prop="code" />
      <el-table-column width="100px" align="center" label="名称" header-align="center" prop="name" />
      <el-table-column width="50px" align="center" label="数量" header-align="center" prop="vol" />
      <el-table-column width="80px" align="center" label="买入价" header-align="center" prop="buyprice" />
      <el-table-column width="180px" align="center" label="现价" sortable header-align="center" prop="price" />
      <el-table-column width="100px" align="center" label="利润" sortable header-align="center" prop="profit" />
    </el-table>
  </el-container>
</template>

<script>
import axios from 'axios'
export default {
  name: 'virtualAccount',
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
      var url = ''
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
    }
  }
}
</script>
