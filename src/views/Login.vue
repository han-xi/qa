<template>
  <a-form
    ref="formRef"
    layout="inline"
    

    :model="formState"
    :rules="rules"
    @finish="handleFinish"
    @finishFailed="handleFinishFailed"
  >
    <a-form-item has-feedback name="user">
      <a-input 
        v-model:value="formState.user"
        placeholder="Username"
        autocomplete="off"
        :allowClear="true"
      >
        <template #prefix
          ><UserOutlined style="color: rgba(0, 0, 0, 0.25)"
        /></template>
      </a-input>
    </a-form-item>
    <a-form-item has-feedback name="password">
      <a-input-password 
        v-model:value="formState.password"
      
        placeholder="Password"
       
      >
        <template #prefix
          ><LockOutlined style="color: rgba(0, 0, 0, 0.25)"
        /></template>
      </a-input-password>
    </a-form-item>
    <a-form-item  name="code">

      <a-row><a-col>
            <a-input 
        v-model:value="formState.code"
        placeholder="验证码"
        autocomplete="on"
        :allowClear="true"
        
      >
     
      </a-input></a-col>
    <a-col>   <img  :src="picurl" @click="getcode" style="cursor:pointer"></a-col></a-row>
     </a-form-item> 
    
    <a-form-item>
      <a-button
        type="primary"
        html-type="submit"
        :disabled="formState.user === '' || formState.password === ''"
      >
        Log in
      </a-button>
    </a-form-item>

  </a-form>
</template>
<script>
import auth from "../auth";
import md5 from "js-md5";
import user from "../apis/user";
import { UserOutlined, LockOutlined } from "@ant-design/icons-vue";
import { defineComponent, reactive, ref ,onBeforeMount} from "vue";
import { useRouter } from "vue-router";
import { message } from "ant-design-vue";
export default defineComponent({
  name: "UserLogin",
  setup() {
    const formRef = ref();
    let validatePass = async (rule, value) => {
      console.log(value);
      let pattern = /^\w\w{7,11}$/;
      if (value === "") {
        return Promise.reject("Please input the password");
      } else {
        if (!pattern.test(value)) {
          return Promise.reject("Please input correct password");
        } else {
          return Promise.resolve();
        }
      }
    };

    let validateUserName = async (rule, value) => {
      /* eslint-disable */
      console.log(value);
      let pattern = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
      console.log(value);
      if (value === "") {
        return Promise.reject("Please input the username");
      } else {
        if (!pattern.test(value)) {
          return Promise.reject(
            "Please input the correct format of the username "
          );
        }

        return Promise.resolve();
      }
    };
    const rules = {
      password: [
        {
          required: true,
          validator: validatePass,
          trigger: "change",
        },
      ],
      user: [
        {
          required: true,
          validator: validateUserName,
          trigger: "change",
        },
      ],
      code:[
        {
          required:true
        }
      ]
    };
    const router = useRouter();
    const formState = reactive({
      user: "",
      password: "",
      code:''
    });

    const handleFinish = (values) => {
      let check_code = localStorage.getItem('code')
      let postdata = {
        'username': formState.user,
        'password': md5(formState.password),
        'code':formState.code,
        'check_code':check_code
      }
      user
        .login(postdata)
        .then((res) => {
          localStorage.setItem("access_token", res.data["access_token"]);
          localStorage.setItem("refresh_token", res.data["refresh_token"]);
          localStorage.setItem("username",res.data['username'])
          localStorage.setItem("user_type",res.data["usertype"])
        //   localStorage.s
       
        auth.user.authenticated = true;
          router.go("/");
          
        })
        .catch(error => {message.error(error.data['message'])});
          
     
    };

    const handleFinishFailed = (errors) => {
      console.log(errors);
    };

    let picurl =ref("")

    onBeforeMount(()=>{
      getcode()
    })
   const getcode=()=>{
      user.getcode().then(res=>{
        if (res.data){
        localStorage.setItem('code',res.data['code'])
        picurl.value =  "data:;base64,"+res.data['image']
        }
      })
   }
    return {
      formRef,
      formState,
      handleFinish,
      handleFinishFailed,
      rules,
      picurl,
      getcode
    };
  },

  components: {
    UserOutlined,
    LockOutlined,
  },
});
</script>