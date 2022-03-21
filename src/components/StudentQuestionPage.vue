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
               <router-link
            v-else-if="route.breadcrumbName === 'class'"
            :to="`${basePath}/${paths[1]}/${paths[2]}/${params_cid}/${params_cname}`"
          >
            {{ route.breadcrumbName }}
          </router-link>
               <router-link
            v-else-if="route.breadcrumbName === 'studentwrongquestion'"
            :to="`${basePath}/${paths[1]}/${paths[2]}/${params_cid}/${params_cname}/studentwrongquestion/${params_sid}`"
          >
            {{ route.breadcrumbName }}
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
        <a-card style="width: 100%; height: 100%">
             <template #title>
        <a-tooltip>
    <template #title>
      {{Title}}
    </template>
        <a-typography-title  :ellipsis='true' :level="3"
        :content="Title"
          ></a-typography-title
        >
        
        </a-tooltip></template
      >
       
          <a-radio-group v-model:value="Wrong">
            <a-radio
              :style="radioStyle"
              v-for="(item, i) in Options"
              :value="i + 1"
              :key="i"
              :disabled="true"
              ><a-typography-title
                :level="3"
                type="success"
                v-if="Wrong !== '' && i + 1 === Answer"
                >{{ OP[i + 1] }}.{{ item }}</a-typography-title
              ><a-typography-title
                type="danger"
                :level="5"
                v-else-if="Wrong == i + 1 && i + 1 != Answer"
                >{{ OP[i + 1] }}.{{ item }}</a-typography-title
              ><a-typography-title :level="5" v-else
                >{{ OP[i + 1] }}.{{ item }}</a-typography-title
              ></a-radio
            >
          </a-radio-group>
        </a-card>
      </a-spin>
    </div>
  </div>
</template>
<script>
import { ref, reactive, onMounted } from "vue";
import { useRoute} from "vue-router";
import question from "../apis/question";
import auth from "../auth";
import { message } from "ant-design-vue";
//import { query_list } from "../apis/query";
export default {
  name: "StudentQuestionPage",
  setup() {
    const route = useRoute();
      const params_cid = ref("");
       const params_sid = ref("");
    const params_cname = ref("");
    params_cid.value = route.params.cid;
    params_cname.value = route.params.cname;
    params_sid.value = route.params.sid;
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
        {
        path: "studentwrongquestion",
        breadcrumbName: "studentwrongquestion",
      },      {
        path: "question",
        breadcrumbName: "question",
      },    
    ]);
    let pid = ref("");
    let IsCollected = ref(false);
    let collectflag = ref(false)
    pid.value = route.params.pid;
    let Title = ref("");
    let Options = ref([]);
    let Answer = ref();
    let Wrong = ref();
    // let IsCollected = ref(false)
    let loading = ref(false);
    onMounted(() => {
      getwronginfo();
    });
    const getwronginfo = () => {
      let postdata = {
        problem_id: pid.value,
        user_id:route.params.sid,
         class_id:route.params.cid
      };
      loading.value = true;
      question
        .getwronginfo(postdata)
        .then((res) => {
          Title.value = res.data["Title"];
          Options.value = eval(res.data["Options"]);
          Wrong.value = Number(res.data["Wrong"]);
          Answer.value = Number(res.data["Answer"]);
          IsCollected.value = res.data['IsCollected']

          loading.value = false;
        })
        .catch((err) => {
          message.error(err.data['message'])
          loading.value = false;
        });
    };

    const OP = reactive({
      1: "A",
      2: "B",
      3: "C",
      4: "D",
    });

    const radioStyle = reactive({
      display: "block",
      // height: "80px",
      lineHeight: "20px",
    });

   
    return {
      radioStyle,
      OP,
      routes,
      Title,
      auth,
      Options,
      Answer,
      Wrong,
     
      loading,
      basePath: "",
      IsCollected,
      collectflag,
      params_cid,
      params_sid,
      params_cname
    };
  },
};
</script>
<style scoped>
.btn {
  animation: scaleDrew 2.5s ease-in-out infinite;
}

@keyframes scaleDrew {
  /* 定义关键帧、scaleDrew是需要绑定到选择器的关键帧名称 */
  0% {
    transform: scale(1);
  }

  25% {
    transform: scale(1.1);
  }

  50% {
    transform: scale(1);
  }

  75% {
    transform: scale(1.1);
  }
}
</style>
