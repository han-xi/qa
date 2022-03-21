<template>
  <div>
    <a-button type="primary" @click="showModal">注册</a-button>
    <a-modal
      v-model:visible="visible"
      title="用户注册"
      
      :footer="null"
    >
      <!-- <template #footer>
        <a-button key="back" @click="handleCancel">Return</a-button>
        <a-button key="submit" type="primary" :loading="loading" @click="handleOk">Submit</a-button>
      </template> -->
      <a-form
        name="custom-validation"
        ref="formRef"
        :model="formState"
        :rules="rules"
        v-bind="layout"
        @finish="handleFinish"
        @finishFailed="handleFinishFailed"
      >
        <a-form-item has-feedback label="用户邮箱" name="username">
          <a-input v-model:value="formState.username" autocomplete="off" />
        </a-form-item>
        <a-form-item has-feedback label="密码" name="password">
          <a-input-password
            v-model:value="formState.password"
           
          />
        </a-form-item>
        <a-form-item has-feedback label="确认密码" name="checkPass">
          <a-input
            v-model:value="formState.checkPass"
            type="password"
            autocomplete="off"
          />
        </a-form-item>
        <a-form-item has-feedback label="验证码" name="code">
          <a-input
            v-model:value="formState.code"
          />
          <img  :src="picurl" @click="getcode" style="cursor:pointer">
        </a-form-item>
        <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
          <a-button type="primary" :loading="loading" html-type="submit">登录</a-button>
          <a-button style="margin-left: 10px" @click="resetForm">重置</a-button>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>
<script>
import { defineComponent, ref, reactive,watch } from "vue";
import user from "../apis/user";
import md5 from "js-md5";
import {message} from 'ant-design-vue'
export default defineComponent({
  name: "UserRegister",
  setup() {
    //form
    const formRef = ref();
    const formState = reactive({
      password: "",
      checkPass: "",
      username: undefined,
      code:''
    });

    let validatePass = async (rule, value) => {
      // console.log(value)
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
      //   console.log(value)
      let pattern = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
      //   console.log(value);
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

    let validatePass2 = async (rule, value) => {
      if (value === "") {
        return Promise.reject("Please input the password again");
      } else if (value !== formState.password) {
        return Promise.reject("Two inputs don't match!");
      } else {
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
      checkPass: [
        {
          required: true,
          validator: validatePass2,
          trigger: "change",
        },
      ],
      username: [
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
    const layout = {
      labelCol: {
        span: 4,
      },
      wrapperCol: {
        span: 14,
      },
    };

    const handleFinish = (values) => {
        loading.value=true
          let check_code = localStorage.getItem('code_register')
      let postdata = {
        'username': formState.username,
        'password': md5(formState.password),
           'code':formState.code,
        'check_code':check_code
      };
 
      user
        .register(postdata)
        .then(res => {
            loading.value=false
message.success(res.data['message'])
visible.value = false;
        })
        .catch(error => {
            loading.value=false
            message.error(error.data['message'])
            getcode()
        });
      //   console.log(values, formState);
    };

    const handleFinishFailed = (errors) => {
      console.log(errors);
    };

    const resetForm = () => {
      formRef.value.resetFields();
    };
    //model
    const loading = ref(false);
    const visible = ref(false);

    const showModal = () => {
      visible.value = true;
    };
   let picurl =ref("")

watch(visible,(newval)=>{
  if(newval===true){
    getcode()
  }
})
   const getcode=()=>{
      user.getcode().then(res=>{
        if (res.data){
        localStorage.setItem('code_register',res.data['code'])
        picurl.value =  "data:;base64,"+res.data['image']
        }
      })
   }
    return {
      formState,
      formRef,
      rules,
      layout,
      handleFinishFailed,
      handleFinish,
      resetForm,
      loading,
      visible,
      showModal,
      getcode,
      picurl
      //   handleOk,
      //   handleCancel,
    };
  },
});
</script>