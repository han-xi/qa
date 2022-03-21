<template>
  <div style="height: 100%" v-if="props.ismodel === 0">
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
      <a-spin tip="Loading..." :spinning="loading">
        <a-descriptions title="学生信息" bordered>
          <a-descriptions-item label="学生名">{{
            studentname
          }}</a-descriptions-item>
          <a-descriptions-item label="注册时间">{{
            registertime
          }}</a-descriptions-item>
          <a-descriptions-item label="Automatic Renewal"
            >YES</a-descriptions-item
          >

          <a-descriptions-item label="状态" :span="3">
            <a-badge status="processing" v-if="status" text="在线" />
            <a-badge status="Default" v-else text="离线" />
          </a-descriptions-item>
        </a-descriptions>
      </a-spin>
    </div>
  </div>
  <a-modal
    v-else
    v-model:visible="props.visible"
    :title="studentname"
    :footer="null"
    @cancel="emitMes"
  >
    <div

    >
      <a-spin tip="Loading..." :spinning="loading">
        <a-descriptions title="学生信息" bordered>
          <a-descriptions-item label="学生名">{{
            studentname
          }}</a-descriptions-item>
          <a-descriptions-item label="注册时间">{{
            registertime
          }}</a-descriptions-item>
          <a-descriptions-item label="Automatic Renewal"
            >YES</a-descriptions-item
          >

          <a-descriptions-item label="状态" :span="3">
            <a-badge status="processing" v-if="status" text="在线" />
            <a-badge status="Default" v-else text="离线" />
          </a-descriptions-item>
        </a-descriptions>
      </a-spin>
    </div>
  </a-modal>
</template>
<script>
import { ref, defineComponent, onBeforeMount, watch } from "vue";
import { useRoute } from "vue-router";
import { HomeOutlined } from "@ant-design/icons-vue";
import classes from "../apis/classes";
export default defineComponent({
  name: "StudentInfo",
  components: {
    HomeOutlined,
  },
  props: {
    ismodel: {
      type: Number,
      default: 0,
    },
    class_id: String,
    user_id: String,
    isstudent: Boolean,
    visible: {
      type: Boolean,
      default: true,
    },
  },
  setup(props, context) {
    const route = useRoute();

    const emitMes = () => {
      context.emit("listen", true);
    };
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
        path: "studentinfo",
        breadcrumbName: "studentinfo",
      },
    ]);
    // watch(props, () => {
    //   getclassinfo();
    // });
    let loading = ref(true);
    if (props.ismodel === 0) {
      loading.value = true;
    } else {
      loading.value = false;
    }

    const id = ref("");
    id.value = route.params.id;
    onBeforeMount(() => {
      if (props.ismodel === 0) {
        getclassinfo();
      }
    });
    watch(props, () => {
      if (props.ismodel === 0 || props.ismodel === 2) {
        loading.value = true;

        getclassinfo();
      }
    });
    let registertime = ref("");
    let studentname = ref("");
    let status = ref(false);

    let getclassinfo = () => {
      let class_id = "";
      let user_id = "";
      if (props.ismodel !== 0) {
        class_id = props.class_id;
        user_id = props.user_id;
      } else {
        class_id = route.params.cid;
        user_id = route.params.sid;
      }
      let postdata = {
        class_id: class_id,
        user_id: user_id,
      };

      if (props.ismodel == 2 && props.isstudent) {
        console.log(props.isstudent)
        classes
          .getstudentinfo(postdata)
          .then((res) => {
            studentname.value = res.data["name"];
            registertime.value = res.data["registertime"];
            status.value = res.data["status"];
            loading.value = false;
          })
          .catch((error) => {
            console.log(error);
            loading.value = false;
          });
      } else if (props.ismodel == 2 && !props.isstudent) {
        classes
          .getteacherinfo(postdata)
          .then((res) => {
            studentname.value = res.data["name"];
            registertime.value = res.data["registertime"];
            status.value = res.data["status"];
            loading.value = false;
          })
          .catch((error) => {
            console.log(error);
            loading.value = false;
          });
      } else {
        classes
          .getstudentinfo(postdata)
          .then((res) => {
            studentname.value = res.data["name"];
            registertime.value = res.data["registertime"];
            status.value = res.data["status"];
            loading.value = false;
          })
          .catch((error) => {
            console.log(error);
            loading.value = false;
          });
      }
    };
    return {
      routes,
      basePath: "",
      id,
      studentname,
      registertime,
      loading,

      props,
      emitMes,
    };
  },
});
</script>
