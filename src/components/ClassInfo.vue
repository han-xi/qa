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
        <a-descriptions title="班级信息" bordered>
          <a-descriptions-item label="班级名">          <a-typography-paragraph
              v-if="auth.user.authenticated && auth.user.usertype > 2"
              v-model:content="classname"
              :editable="{ onEnd: onEnd }"
            >
              <template v-slot:editableIcon><HighlightOutlined /></template>
              <template v-slot:editableTooltip>click to edit text</template>
            </a-typography-paragraph>
            <a-typography-paragraph v-else :content="classname"/>
            </a-descriptions-item>

          <a-descriptions-item label="注册时间">{{
            registertime
          }}</a-descriptions-item>
          <a-descriptions-item label="容纳数量"><a-typography-paragraph
              v-if="auth.user.authenticated && auth.user.usertype > 2"
              v-model:content="limitnum"
              :editable="{ onEnd: onEnd }"
            >
              <template v-slot:editableIcon><HighlightOutlined /></template>
              <template v-slot:editableTooltip>click to edit text</template>
            </a-typography-paragraph>
                        <a-typography-paragraph v-else :content="limitnum"/>

            
            </a-descriptions-item>
          <a-descriptions-item label="老师" v-if="teachers.length>0">
            <template v-for="(item, i) in teachers" :key="i"
              >
               <a @click="enterUserInfo(item.name)">{{ item.name }}</a>
             
              </template
            ></a-descriptions-item
          >
          <a-descriptions-item label="老师" v-else>
            <span>暂无</span>
          </a-descriptions-item>
          <a-descriptions-item label="学生数量" :span="2">{{
            student_num
          }}</a-descriptions-item>
          <a-descriptions-item label="开课状态" :span="3">
            <a-badge status="processing" v-if="status === '1'" text="开课中" />
            <a-badge status="error" v-else-if="status === '2'" text="已结束" />
            <a-badge status="success" v-else text="还未开始" />

          </a-descriptions-item>

          <a-descriptions-item label="公告">
            <a-typography-paragraph
              v-if="auth.user.authenticated && auth.user.usertype > 1"
              v-model:content="content"
              :editable="{ onEnd: onEnd }"
            >
              <template v-slot:editableIcon><HighlightOutlined /></template>
              <template v-slot:editableTooltip>click to edit text</template>
            </a-typography-paragraph>
            <a-typography-paragraph v-else content="欢迎欢迎">
            </a-typography-paragraph>
          </a-descriptions-item>
        </a-descriptions>
      </a-spin>
    </div>
  </div>
  <a-modal
    v-else
    v-model:visible="props.visible"
    :title="classname"
    :footer="null"
    @cancel="emitMes"
  >
    <div >
      <a-spin tip="Loading..." :spinning="loading">
        <a-descriptions title="班级信息" bordered>
          <a-descriptions-item label="班级名">  <a-typography-paragraph
              v-if="auth.user.authenticated && auth.user.usertype > 2"
              v-model:content="classname"
              :editable="{ onEnd: onEnd }"
            >
              <template v-slot:editableIcon><HighlightOutlined /></template>
              <template v-slot:editableTooltip>click to edit text</template>
            </a-typography-paragraph>
             <a-typography-paragraph v-else v-model:content="classname" />
            
            
            </a-descriptions-item>
          <a-descriptions-item label="注册时间">{{
            registertime
          }}</a-descriptions-item>
          <a-descriptions-item label="容纳数量">  <a-typography-paragraph
              v-if="auth.user.authenticated && auth.user.usertype > 2"
              v-model:content="limitnum"
              :editable="{ onEnd: onEnd }"
            >
              <template v-slot:editableIcon><HighlightOutlined /></template>
              <template v-slot:editableTooltip>click to edit text</template>
            </a-typography-paragraph>
            <a-typography-paragraph v-else v-model:content="limitnum" />
            
            
            
            </a-descriptions-item>
           
          <a-descriptions-item label="老师" v-if="teachers&&teachers.length>0">
            <template v-for="(item, i) in teachers" :key="i"
              >
              
             <a @click="enterUserInfo(item.name)">{{ item.name }}</a>
             
              
              
              
              </template
            ></a-descriptions-item
          >
          <a-descriptions-item label="老师" v-else>
            <span>暂无</span>
          </a-descriptions-item>
          <a-descriptions-item label="学生数量" :span="2">{{
            student_num
          }}</a-descriptions-item>
          <a-descriptions-item label="开课状态" :span="3">
             <a-badge status="processing" v-if="status === '1'" text="开课中" />
            <a-badge status="error" v-else-if="status === '2'" text="已结束" />
            <a-badge status="success" v-else text="还未开始" />

          </a-descriptions-item>

          <a-descriptions-item label="公告">
            <a-typography-paragraph
              v-if="auth.user.authenticated && auth.user.usertype > 1"
              v-model:content="content"
              :editable="{ onEnd: onEnd }"
            >
              <template v-slot:editableIcon><HighlightOutlined /></template>
              <template v-slot:editableTooltip>click to edit text</template>
            </a-typography-paragraph>
            <a-typography-paragraph v-else content="欢迎欢迎">
            </a-typography-paragraph>
          </a-descriptions-item>
        </a-descriptions>
      </a-spin>
    </div>
  </a-modal>
  <student-info  :ismodel="ismodel_user" :visible="modelvisible1" :isstudent='false'  :class_id="record_class_id" :user_id="record_username" @listen="listenuser" ></student-info>

</template>
<script>
import { ref, defineComponent, watch, onBeforeMount } from "vue";
import { useRoute } from "vue-router";
import { HomeOutlined, HighlightOutlined } from "@ant-design/icons-vue";
import classes from "../apis/classes";
import auth from "../auth";
import { message } from "ant-design-vue";
import StudentInfo from "../components/StudentInfo.vue"
export default defineComponent({
  name: "ClassInfo",
  components: {
    HomeOutlined,
    HighlightOutlined,
    StudentInfo
  },
  props: {
    ismodel: {
      type: Number,
      default: 0,
    },
    class_id: String,
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
        path: "classinfo",
        breadcrumbName: "classinfo",
      },
    ]);

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
    let classname = ref("");
    let status = ref("1");
    let teachers = ref([]);
     let content = ref("欢迎欢迎");
    let student_num = ref(0);
    let limitnum = ref(50);
    let record_class_id =ref("")
    let getclassinfo = () => {
      let class_id = "";
      if (props.ismodel !== 0) {
        class_id = props.class_id;
      } else {
        class_id = route.params.cid;
      }
      let postdata = {
        class_id: class_id,
      };
      classes
        .getclassinfo(postdata)
        .then((res) => {
          classname.value = res.data["name"];
          record_class_id.value = res.data["key"]
          registertime.value = res.data["registertime"];
          status.value = res.data["status"];
          teachers.value = eval(res.data["teacher"]);
          content.value = res.data['content']
          student_num.value = res.data["student_num"];
          limitnum.value = res.data["limitnum"];
          loading.value = false;
        })
        .catch((error) => {
          console.log(error);
          loading.value = false;
        });
    };
   
   
  
    let onEnd = () => {
      let postdata = {
        class_id: route.params.cid,
        content: content.value,
        class_name:classname.value,
        limitnum:limitnum.value

      };
      classes
        .postclassinfo(postdata)
        .then((res) => {
          message.success(res.data["message"]);
        })
        .catch((error) => {
           message.error(error.data["message"]);
        });
    };
    
let modelvisible1 =ref(false)

let record_username =ref("")
let ismodel_user = ref(1)
let enterUserInfo =(record)=>{
  record_username.value=record
   ismodel_user.value=2
  modelvisible1.value = true
 
}
    let listenuser =(val)=>{
  if (val!==''){
     ismodel_user.value=1
    modelvisible1.value = false
   
  }
}
    return {
      routes,
      basePath: "",
      id,
      classname,
      registertime,
      loading,
      status,
      teachers,
      student_num,
      limitnum,
      onEnd,
      content,
      auth,
      props,
      emitMes,
      enterUserInfo,
      listenuser,
      modelvisible1,
      record_class_id,
      record_username,
     ismodel_user

    };
  },
});
</script>
