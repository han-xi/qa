<template>
  <a-form
    ref="formRef"
    v-bind="formItemLayoutWithOutLabel"
    :model="dynamicValidateForm"
  >
    <a-form-item
      has-feedback
      label="班级名称"
      name="name"
      v-bind="formItemLayout"
      :rules="{
        required: true,
        message: '问题不能为空',
        trigger: 'change',
      }"
    >
      <a-input v-model:value="dynamicValidateForm.name" />
    </a-form-item>
        <a-form-item
      has-feedback
      label="班级容量"
      name="limitnum"
      v-bind="formItemLayout"
    >
      <a-input v-model:value="dynamicValidateForm.limitnum" />
    </a-form-item>
    <a-form-item
      has-feedback
      label="公告"
      name="content"
      v-bind="formItemLayout"
      :rules="{
        required: true,
        message: '公告不能为空',
        trigger: 'change',
      }"
    >
      <a-input v-model:value="dynamicValidateForm.content" />
    </a-form-item>
    <a-form-item
      has-feedback
      label="开课时间"
      name="date"
      v-bind="formItemLayout"
      :autoLink="false"
      ref="name"
      :rules="{
        required: true,
        message: '时间不能为空',
      }"
    >
      <a-range-picker
        :format="dateFormat"
        :locale="locale"
        v-model:value="dynamicValidateForm.date"
        @change="
          () => {
            $refs.name.onFieldChange();
          }
        "
      />
    </a-form-item>
    <a-form-item v-bind="formItemLayoutWithOutLabel">
      <a-button
        type="primary"
        html-type="submit"
        @click="submitForm"
        :loading="loading"
        >提交</a-button
      >
      <a-button style="margin-left: 10px" @click="resetForm">重置</a-button>
    </a-form-item>
  </a-form>
</template>
<script>
import { defineComponent, reactive, ref } from "vue";
import locale from "ant-design-vue/es/date-picker/locale/zh_CN";
import classes from "../apis/classes";
import { message } from "ant-design-vue";
export default defineComponent({
  name: "ClassForm",
  setup() {
    const formRef = ref();
    const dateFormat = "YYYY/MM/DD";
    const formItemLayout = {
      labelCol: {
        xs: {
          span: 24,
        },
        sm: {
          span: 4,
        },
      },
      wrapperCol: {
        xs: {
          span: 24,
        },
        sm: {
          span: 20,
        },
      },
    };
    const formItemLayoutWithOutLabel = {
      wrapperCol: {
        xs: {
          span: 24,
          offset: 0,
        },
        sm: {
          span: 20,
          offset: 4,
        },
      },
    };
    const dynamicValidateForm = reactive({
      name: "",
      limitnum: 50,
      content: "欢迎欢迎",
      date: [],
    
    });
    let loading = ref(false);
    const submitForm = () => {
      formRef.value
        .validate()
        .then(() => {
          loading.value = true;
          let date = new Array();
          dynamicValidateForm.date.forEach((Element)=>{
            date.push(Element.unix())
          })
          let postdata = {
            class_name: dynamicValidateForm.name,
            content: dynamicValidateForm.content,
            date: date.toString(),
            limitnum: dynamicValidateForm.limitnum,
          };
          classes
            .addclass(postdata)
            .then((res) => {
              message.success(res.data["message"]);
              loading.value = false;
            })
            .catch((error) => {
              message.error(error.data["message"]);
              loading.value = false;
            });
        })
        .catch((error) => {
          console.log("error", error);
        });
    };

    const resetForm = () => {
      formRef.value.resetFields();
    };

    return {
      formRef,
      formItemLayout,
      formItemLayoutWithOutLabel,
      dynamicValidateForm,
      submitForm,
      resetForm,
      dateFormat,
      locale,
      loading,
    };
  },
});
</script>
<style>
.dynamic-delete-button {
  cursor: pointer;
  position: relative;
  top: 4px;
  font-size: 24px;
  color: #999;
  transition: all 0.3s;
}
.dynamic-delete-button:hover {
  color: #777;
}
.dynamic-delete-button[disabled] {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>