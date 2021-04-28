<template>
  <el-container style="border:1px solid #eee;">
    <!--转债代码，转债名称，现价，涨跌幅，正股名，正股价， 正股涨跌，pb，转股价，转股价值，溢价率，评级，强赎触发价
    'bond_id', 'bond_nm', 'price', 'increase_rt', 'stock_nm', 'sprice','sincrease_rt', 'pb', 'convert_price', 'convert_value', 'premium_rt','rating_cd', 'force_redeem_price'-->
    <el-table height="920" v-loading="loading" element-loading-text="别着急，重要的数据可以多等等" :data="list" stripe border fit highlight-current-row style="width: 95%; font-size:12px;">
      <el-table-column
        align="center"
        label="序号"
        width="65"
        type="index"
      />
      <el-table-column width="50px" align="center" label="转债代码" header-align="center" prop="bond_id" />
      <el-table-column width="50px" align="center" label="转债名称" header-align="center" prop="bond_nm" />
      <el-table-column width="80px" align="center" label="现价" sortable header-align="center" prop="price" />
      <el-table-column width="100px" align="center" label="涨跌幅" sortable header-align="center" prop="increase_rt" />
      <el-table-column width="80px" align="center" label="正股名" header-align="center" prop="stock_nm" />
      <el-table-column width="180px" align="center" label="正股价" sortable header-align="center" prop="sprice" />
      <el-table-column width="100px" align="center" label="正股涨跌" sortable header-align="center" prop="sincrease_rt" />
      <el-table-column width="80px" align="center" label="PB" sortable header-align="center" prop="pb" />
      <el-table-column width="80px" align="center" label="转股价" sortable header-align="center" prop="convert_price" />
      <el-table-column width="80px" align="center" label="转股价值" sortable header-align="center" prop="convert_value" />
      <el-table-column width="80px" align="center" label="溢价率" sortable header-align="center" prop="premium_rt" />
      <el-table-column width="80px" align="center" label="评级" sortable header-align="center" prop="rating_cd" />
      <el-table-column width="80px" align="center" label="强赎触发价" sortable header-align="center" prop="force_redeem_price" />
    </el-table>
  </el-container>
</template>

<script>
import axios from 'axios'
export default {
  name: 'ConvertBond',
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
      var url = 'http://localhost:8089/ConvertBond'
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
