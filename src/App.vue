<template>
  <a-layout style="min-height: 100vh">
    <a-layout-sider v-model:collapsed="collapsed" :trigger="null" collapsible>
      <div class="logo" @click="goMain"><span>答题网</span></div>
      <a-menu
        v-model:selectedKeys="selectedKeys"
        @click="clickMenu"
        theme="dark"
        mode="inline"
      >
        <a-sub-menu key="1" v-if="authenticated">
          <template #icon>
            <UserOutlined />
          </template>
          <template #title>用户信息</template>
          <a-menu-item-group key="g1">
            <template #icon>
              <CalendarOutlined />
            </template>
            <template #title>注册时间</template>
            <a-menu-item key="100" :disabled="true">{{
              register_time
            }}</a-menu-item>
          </a-menu-item-group>
          <a-menu-item-group key="g2">
            <template #icon>
              <UserOutlined />
            </template>
            <template #title>邮箱</template>
            <a-menu-item key="101" :disabled="true">{{ user_mail }}</a-menu-item>
          </a-menu-item-group>
          <a-menu-item-group key="g3">
            <template #icon>
              <UserOutlined />
            </template>
            <template #title>等级</template>
            <a-menu-item key="102" :disabled="true">{{ user_type }}</a-menu-item>
          </a-menu-item-group>
                    <a-menu-item-group key="g4"  v-if="authenticated &&usertype<3">
            <template #icon>
              <UserOutlined />
            </template>
             <a-menu-item key="103"  @click="UpgradePermission" >升级权限</a-menu-item>
             
          </a-menu-item-group>
          <a-menu-item-group key="g4">


           <a-menu-item key="104" >
           <forget-password
             :username="user_mail"
            ></forget-password>
            </a-menu-item>
          </a-menu-item-group>
        </a-sub-menu>
        <a-menu-item key="2">
          <video-camera-outlined />
          <span>首页</span>
        </a-menu-item>
        <a-menu-item key="3" v-if="authenticated">
          <video-camera-outlined />
          <span>错题库</span>
        </a-menu-item>
        <a-menu-item key="7" v-if="authenticated">
          <video-camera-outlined />
          <span>收藏库</span>
        </a-menu-item>
        <a-menu-item key="4" v-if="authenticated">
          <video-camera-outlined />
          <span>班级列表</span>
        </a-menu-item>
        <a-menu-item key="5" v-if="authenticated &&usertype>1">
          <video-camera-outlined />
          <span>申请信息</span>
        </a-menu-item>
        <a-menu-item key="6" v-if="authenticated &&usertype>1">
          <video-camera-outlined />
          <span>信息录入</span>
        </a-menu-item>
        <a-menu-item key="10" v-if="authenticated">
          <upload-outlined />
          <span>退出登录</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header style="background: #fff; padding: 0; background: #3c8dbc"
        ><a-row type="flex" justify="space-around" align="middle">
          <a-col flex="100px">
            <menu-unfold-outlined
              v-if="collapsed"
              class="trigger"
              @click="() => (collapsed = !collapsed)" />
            <menu-fold-outlined
              v-else
              class="trigger"
              @click="() => (collapsed = !collapsed)"
          /></a-col>
          <a-col flex="auto">
            <user-login v-if="!authenticated"></user-login>
            
            
            </a-col
          ><a-col flex="auto"
            ><user-register
              flex="100px"
              v-if="!authenticated"
            ></user-register>
            
            </a-col
          >
          <a-col flex="auto"
            ><forget-password
              flex="100px"
              v-if="!authenticated"
            ></forget-password>
            
            </a-col
          >
          
          <a-col v-if="authenticated" flex="right" :pull="1">
            <a-badge :count="count">
              <notification-outlined
                style="font-size: 30px"
                @click="getMessage"
              /> </a-badge></a-col
        ></a-row>
       <a-modal
          v-if="authenticated"
          v-model:visible="messagemodel"
          title="消息"
          :footer="null"
        >
          <a-spin :spinning="messageloading">
            <a-list item-layout="horizontal" :data-source="messagedata">
              <template #renderItem="{ item }">
                <a-list-item>
                  <a-list-item-meta :description="`${item.time}`">
                    <template #title>
                      
                      {{ item.message }}
                    </template>
                  </a-list-item-meta>
                </a-list-item>
              </template>
            </a-list>
          </a-spin>
        </a-modal>
      </a-layout-header>
      <a-layout-content
        :style="{
          margin: '0 16px',
          //<!-- height:'100%', -->
          //padding: '24px',
          // background: '#fff',
          // minHeight: '280px',
        }"
      >
        <router-view />
         
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script>
import auth from "./auth";
import {
  UserOutlined,
  VideoCameraOutlined,
  UploadOutlined,
  MenuUnfoldOutlined,
  MenuFoldOutlined,
  CalendarOutlined,
  NotificationOutlined,
} from "@ant-design/icons-vue";
import UserLogin from "./views/Login.vue";
import UserRegister from "./views/Register.vue";
import ForgetPassword from "./views/ForgetPassword.vue"
import { ref, reactive, toRefs, defineComponent, watch, onBeforeMount } from "vue";
import { useRoute, useRouter } from "vue-router";
import user from "./apis/user";
import classes from "./apis/classes";
import { message } from "ant-design-vue";
// import { message } from "ant-design-vue";

export default defineComponent({
  name: "App",
  setup() {
    const Person = {
      1: "学生",
      2: "教师",
      3: "管理员",
    };
    let authenticated = ref()
    authenticated.value = auth.user.authenticated
    let usertype = ref(auth.user.usertype)

    let user_mail = ref("");
    let register_time = ref("");
    let user_type = ref("");
    let count = ref(0);
    onBeforeMount(async()=>{
    if (authenticated.value) {
       await user
        .home()
        .then((res) => {
          user_mail.value = res.data["username"];
          register_time.value = res.data["registertime"];
          user_type.value = Person[res.data["usertype"]];
          auth.user.usertype = Number(res.data["usertype"]);
          usertype.value = Number(res.data["usertype"]);
          // console.log(res.data)
        })
        .catch((error) => {
          console.log(error);
        });
      classes.getmessagecount().then((res) => {
        count.value = Number(res.data["count"]);
      });
    }
    })

    const state = reactive({
      selectedKeys: [],
      openKeys: [],
    });
    // const selectedKeys =reactive([])
    const route = useRoute();
    const router = useRouter();
    watch(
      () => route.path,
      () => {
        if (route.path === "/main") {
          state.selectedKeys = ["2"];
        } else if (route.path === "/wrongquestion") {
          state.selectedKeys = ["3"];
        } else if (route.path === "/classlist") {
          state.selectedKeys = ["4"];
        } else if (route.path === "/apply") {
          state.selectedKeys = ["5"];
        }else if (route.path === "/addinfo") {
          state.selectedKeys = ["6"];
        }else if (route.path === "/collectquestion") {
          state.selectedKeys = ["7"];
        }
      }
    );
    const UpgradePermission=()=>{
      user.upgradepermission().then(res=>{
        message.success(res.data['message'])
      }).catch(err=>{
        console.log(err)
      })
    }
    const clickMenu = (e) => {
      console.log(e)
      if (e.key === "2") {
         console.log(route.path)
        if (route.path === "/main") {
          if(auth.user.authenticated){
            router.replace('/refresh')
          }else{
          router.go("/refresh");
          }
        } else {
          router.push("/main");
        }
      } else if (e.key === "3") {
        router.push("/wrongquestion");
      } else if (e.key === "4") {
        router.push("/classlist");
      } else if (e.key === "5") {
        router.push("/apply");
      }
      else if (e.key === "6") {
        router.push("/addinfo");
      }
          else if (e.key === "7") {
        router.push("/collectquestion");
      }
      else if (e.key === "10") {
        auth.user.authenticated = false;
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        router.go("/");
      }
    };
    const goMain = () => {
      if (route.path === "/main") {
        router.replace("/refresh");
      } else {
        router.push("/main");
      }
      state.selectedKeys.pop();
    };
    let messagemodel = ref(false);
    let messageloading = ref(false);
    let messagedata = ref([]);
    const getMessage = () => {
      messagemodel.value = true;
      messageloading.value = true;
      classes
        .getmessageinfo()
        .then((res) => {
          messagedata.value = res.data["result"];
          messageloading.value = false;
        })
        .catch((err) => {
          console.log(err);
          messageloading.value = false;
        });
        console.log(messagemodel.value)
    };
    return {
      user_mail,
      register_time,
      authenticated,
      usertype,
      ...toRefs(state),
      clickMenu,
      goMain,
      getMessage,
      count,
      messagemodel,
      user_type,
      messageloading,
      messagedata,
      UpgradePermission
    };
  },
  data() {
    return {
      collapsed: false,
      // register_time: "2021/03/09",
      // user_mail: "1179865214@qq.com",
      selectName: "",
    };
  },
  components: {
    UserRegister,
    UserOutlined,
    VideoCameraOutlined,
    UploadOutlined,
    MenuUnfoldOutlined,
    MenuFoldOutlined,
    CalendarOutlined,
    UserLogin,
    NotificationOutlined,
    ForgetPassword,
  },
});
</script>

<style>
.trigger {
  font-size: 18px;
  line-height: 64px;
  padding: 0 24px;
  cursor: pointer;
  transition: color 0.3s;
}

.trigger:hover {
  color: #1890ff;
}

.logo {
  height: 64px;
  background: #367fa9;
  /* margin: 16px; */
  cursor: pointer;
  color: #fff;
  font-size: 20px;
  line-height: 60px;
  text-align: center;
  font-weight: 300;
}

.site-layout .site-layout-background {
  background: #fff;
}
</style>