import Vue from 'vue'
import Router from 'vue-router'
import TradeSystem from '@/components/index'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'TradeSystem',
      component: TradeSystem
    }
  ]
})
