<template>
  <div style="height: 100%">
    <div :style="{ height: '64px', padding: '24px 0' }">
      <a-breadcrumb :routes="routes">
        <template #itemRender="{ route, routes, paths }">
          <span v-if="routes.indexOf(route) === routes.length - 1">
            {{ route.breadcrumbName }}
          </span>
          <router-link
            v-else-if="routes.indexOf(route) === 0"
            :to="`${basePath}/${paths.join('/')}`"
          >
            <home-outlined /> {{ route.breadcrumbName }}
          </router-link>
          <router-link v-else :to="`${basePath}/${paths[1]}`">
            {{ route.breadcrumbName }}
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
            <span> {{ cname }}学生信息 </span>
          </template>
          <table-search-student />
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
import { ref, defineComponent } from "vue";
import TableSearchStudent from "../components/TableSearchStudent.vue";

import { HomeOutlined } from "@ant-design/icons-vue";
import { useRoute } from "vue-router";
export default defineComponent({
  name: "ClassStudent",
  components: {
    HomeOutlined,
    TableSearchStudent,
  },
  setup() {
    const activeKey = ref("1");
    const routes = ref([
      {
        path: "main",
        breadcrumbName: "home",
      },
      {
        path: "classlist",
        breadcrumbName: "classlist",
      },
      {
        path: "class",
        breadcrumbName: "class",
      },
    ]);

    const route = useRoute();
    const cid = route.params.cid;
    const cname = route.params.cname
    return {
      cid,
      routes,
      basePath: "",
      activeKey,
      cname
    };
  },
});
</script>