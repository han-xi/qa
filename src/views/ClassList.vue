<template>
  <div style="height: 100%">
    <div :style="{ height: '64px', padding: '24px 0' }">
      <a-breadcrumb :routes="routes">
        <template #itemRender="{ route, routes, paths }">
          <span v-if="routes.indexOf(route) === routes.length - 1">
            {{ route.breadcrumbName }}
          </span>
          <router-link v-else :to="`${basePath}/${paths.join('/')}`">
            <home-outlined /> {{ route.breadcrumbName }}
          </router-link>
        </template>
      </a-breadcrumb>
    </div>
    <div
      :style="{
        padding: '24px',
        background: '#fff',
        height: 'calc(100% - 64px)',
      }"
    >
    <a-tabs v-model:activeKey="activeKey">
    <a-tab-pane key="1">
      <template #tab>
        <span>
          班级列表
        </span>
      </template>
      <table-search-class/>
    </a-tab-pane>
    <!-- <a-tab-pane key="2">
      <template #tab>
        <span>
          <android-outlined />
          查询学生
        </span>
      </template>
      Tab 2
    </a-tab-pane> -->
  </a-tabs>
    
    </div>
  </div>
</template>
<script>
import { ref,  defineComponent } from "vue";
import TableSearchClass from "../components/TableSearchClass.vue"

import {
    HomeOutlined
} from "@ant-design/icons-vue"
export default defineComponent({
    name:"ClassList",
    components:{
        HomeOutlined,
        TableSearchClass,
    },
    setup() {
        const activeKey = ref('1')
    const routes = ref([
      {
        path: "main",
        breadcrumbName: "home",
      },
      {
        path: "classlist",
        breadcrumbName: "classlist",
      },
    ]);
    return{
        routes,
        basePath:'',
        activeKey
    }
    },
})
</script>