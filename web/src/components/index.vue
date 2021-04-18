<template>
  <div class="tab-container">
    <el-tabs v-model="activeName" type="border-card" style="margin-top:0px;" @tab-click="handleClick">
      <el-tab-pane label="行业估值" :name="tabNames[0]">
        <industryValue :ref="tabNames[0]" />
      </el-tab-pane>
      <el-tab-pane label="集思录数据" :name="tabNames[1]">
        <JSLData :ref="tabNames[1]" />
      </el-tab-pane>
      <el-tab-pane label="可转债数据" :name="tabNames[2]">
        <convertBond :ref="tabNames[2]" />
      </el-tab-pane>
      <el-tab-pane label="MASystem" :name="tabNames[3]">
        <MASystem :ref="tabNames[3]" />
      </el-tab-pane>
      <el-tab-pane label="模拟持仓" :name="tabNames[4]">
        <virtualAccount :ref="tabNames[4]" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { industryValue, JSLData, convertBond, MASystem, virtualAccount } from './tabs'
import { mapGetters } from 'vuex'
export default {
  name: 'Discipline',
  components: {
    industryValue,
    JSLData,
    convertBond,
    MASystem,
    virtualAccount
  },
  data () {
    return {
      tabNames: ['industryValue', 'JSLData', 'convertBond', 'MASystem', 'virtualAccount'],
      tabsHandler: [],
      activeName: 'industryValue'
    }
  },
  computed: {
    ...mapGetters([
      'name'
    ])
  },
  mounted () {
    this.tabsHandler[this.tabNames[0]] = this.$refs.industryValue
    this.tabsHandler[this.tabNames[1]] = this.$refs.JSLData
    this.tabsHandler[this.tabNames[2]] = this.$refs.convertBond
    this.tabsHandler[this.tabNames[3]] = this.$refs.MASystem
    this.tabsHandler[this.tabNames[4]] = this.$refs.virtualAccount
  },
  methods: {
    handleClick (tab) {
      // this.tabsHandler[tab.name].handleShow()
    }
  }
}
</script>

<style scoped>
  .tab-container {
    margin: 0px;
  }
</style>
