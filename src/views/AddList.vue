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
            <span> 问题录入 </span>
          </template>
          <problem-form />
        </a-tab-pane>

        <a-tab-pane
          key="2"
          v-if="auth.user.authenticated && auth.user.usertype > 2"
        >
          <template #tab>
            <span> 问题修改 </span>
          </template>
        </a-tab-pane>
        <a-tab-pane
          key="3"
          v-if="auth.user.authenticated && auth.user.usertype > 2"
        >
          <template #tab>
            <span> 班级录入 </span>
          </template>
          <class-form />
        </a-tab-pane>
      </a-tabs>
    </div>
  </div>
</template>
<script>
import { ref, defineComponent } from "vue";
import ProblemForm from "../components/ProblemForm.vue";
import auth from "../auth";
import { HomeOutlined } from "@ant-design/icons-vue";
import ClassForm from "@/components/ClassForm.vue";
export default defineComponent({
  name: "AddList",
  components: {
    HomeOutlined,
    ProblemForm,
    ClassForm,
  },
  setup() {
    const activeKey = ref("1");
    const routes = ref([
      {
        path: "main",
        breadcrumbName: "home",
      },
      {
        path: "addinfo",
        breadcrumbName: "addinfo",
      },
    ]);
    return {
      routes,
      basePath: "",
      activeKey,
      auth,
    };
  },
});
</script>